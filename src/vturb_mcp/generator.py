"""Generate FastMCP tool modules from the consolidated VTurb OpenAPI spec.

Reads `specs/vturb-openapi.json`, groups operations by first path segment
(category), and emits one Python module per category under `src/vturb_mcp/tools/`.

Function naming: `{category}_{rest_of_path}` (always globally unique).
Idempotent: re-running produces identical output if the spec is unchanged.
"""

from __future__ import annotations

import json
import keyword
import re
import textwrap
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
SPEC_PATH = ROOT / "specs" / "vturb-openapi.json"
TOOLS_DIR = Path(__file__).resolve().parent / "tools"

PYTHON_RESERVED = set(keyword.kwlist) | {
    "id", "type", "filter", "list", "set", "dict", "map",
    "input", "format", "hash", "object", "zip", "bytes",
}

TYPE_MAP = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "list",
    "object": "dict",
}


def _snake(s: str) -> str:
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    return s.lower().replace("-", "_").replace(" ", "_")


def _safe_param(name: str) -> str:
    return f"{name}_" if name in PYTHON_RESERVED else name


def _py_type(schema: dict) -> str:
    """Map an OpenAPI schema to a Python type annotation (always Optional-wrappable)."""
    t = schema.get("type", "string")
    if t == "array":
        items = schema.get("items", {}) or {}
        inner = _py_type(items) if items else "str"
        return f"list[{inner}]"
    return TYPE_MAP.get(t, "str")


def _func_name(path: str) -> str:
    """Derive the tool function name from the URL path.

    `/sessions/stats_by_field_by_day` → `sessions_stats_by_field_by_day`
    `/quota/usage` → `quota_usage`
    """
    parts = [p for p in path.strip("/").split("/") if p and not p.startswith("{")]
    return _snake("_".join(parts))


def _category(path: str) -> str:
    """First non-empty path segment → module name."""
    parts = [p for p in path.strip("/").split("/") if p]
    return _snake(parts[0]) if parts else "misc"


def _collect_params_from_request_body(op: dict) -> list[dict]:
    """Pull body params from POST operations (application/json schema)."""
    body = op.get("requestBody", {}) or {}
    content = body.get("content", {}) or {}
    schema = (content.get("application/json", {}) or {}).get("schema", {}) or {}
    if schema.get("type") != "object":
        return []
    required = set(schema.get("required", []) or [])
    props = schema.get("properties", {}) or {}
    out: list[dict] = []
    for name, prop in props.items():
        out.append({
            "name": name,
            "in": "body",
            "required": name in required,
            "schema": prop,
            "description": prop.get("description", "").strip(),
        })
    return out


def _collect_params_from_parameters(op: dict) -> list[dict]:
    """Pull query/path params from GET operations."""
    out: list[dict] = []
    for p in op.get("parameters", []) or []:
        out.append({
            "name": p.get("name", ""),
            "in": p.get("in", "query"),
            "required": p.get("required", False),
            "schema": p.get("schema", {}) or {},
            "description": p.get("description", "").strip(),
        })
    return out


def _format_docstring(summary: str, description: str, method: str, path: str, params: list[dict]) -> str:
    """Multi-line docstring with summary, endpoint, args, and enum hints."""
    lines: list[str] = []
    if summary:
        lines.append(summary.strip())
    lines.append("")
    lines.append(f"{method} {path}")
    if description and description.strip() != summary.strip():
        lines.append("")
        for ln in description.strip().splitlines():
            lines.append(ln.rstrip())
    if params:
        lines.append("")
        lines.append("Args:")
        for p in params:
            schema = p["schema"] or {}
            arg_desc = p["description"] or ""
            arg_desc = " ".join(arg_desc.split())
            extras: list[str] = []
            if "enum" in schema:
                vals = ", ".join(str(v) for v in schema["enum"])
                extras.append(f"Values: {vals}")
            if schema.get("format"):
                extras.append(f"Format: {schema['format']}")
            if "default" in schema:
                extras.append(f"Default: {schema['default']}")
            if "minimum" in schema or "maximum" in schema:
                rng = f"{schema.get('minimum', '-inf')}..{schema.get('maximum', 'inf')}"
                extras.append(f"Range: {rng}")
            if "example" in schema:
                extras.append(f"Example: {schema['example']}")
            joined = " ".join(extras)
            req = "required" if p["required"] else "optional"
            arg_line = f"    {p['name']} ({req}): {arg_desc}"
            if joined:
                arg_line += f" [{joined}]"
            lines.append(arg_line)
    return "\n".join(lines)


def _generate_function(path: str, method: str, op: dict) -> str:
    """Generate the Python source for one tool function."""
    fname = _func_name(path)
    summary = (op.get("summary") or "").strip()
    description = (op.get("description") or "").strip()

    if method == "POST":
        params = _collect_params_from_request_body(op)
    else:
        params = _collect_params_from_parameters(op)

    # Order: required first, then optional
    params_sorted = sorted(params, key=lambda p: (not p["required"], p["name"]))

    sig_parts: list[str] = []
    body_lines: list[str] = []
    body_container = "json_body" if method == "POST" else "params"
    body_lines.append(f"    {body_container}: dict = {{}}")

    for p in params_sorted:
        py_name = _safe_param(p["name"])
        py_type = _py_type(p["schema"])
        if p["required"]:
            sig_parts.append(f"{py_name}: {py_type}")
        else:
            sig_parts.append(f"{py_name}: Optional[{py_type}] = None")
        # Send under the ORIGINAL key (preserve API name even when py_name has trailing _)
        body_lines.append(f"    if {py_name} is not None:")
        body_lines.append(f"        {body_container}[{p['name']!r}] = {py_name}")

    signature = f"async def {fname}(" + ", ".join(sig_parts) + ") -> Any:"

    doc = _format_docstring(summary, description, method, path, params_sorted)
    doc_block = '    """' + doc.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    if "\n" in doc:
        doc_block += '\n    """'
    else:
        doc_block += '"""'
    doc_block = doc_block.replace("\n", "\n    ").rstrip() + "\n"

    if method == "POST":
        call = f"    return await _client.post({path!r}, json_body={body_container} or None)"
    else:
        call = f"    return await _client.get({path!r}, params={body_container} or None)"

    return "\n".join([signature, doc_block, *body_lines, call]) + "\n"


def _module_header(category: str) -> str:
    return textwrap.dedent(f'''\
        """Auto-generated VTurb Analytics tools — {category}.

        Do not edit by hand. Regenerate via:
            python -m vturb_mcp.generator
        """

        from __future__ import annotations

        from typing import Any, Optional

        from vturb_mcp.client import VturbClient

        _client = VturbClient()

    ''')


def generate() -> dict[str, int]:
    spec = json.loads(SPEC_PATH.read_text())
    paths = spec.get("paths", {})

    by_category: dict[str, list[str]] = {}
    for path, methods in sorted(paths.items()):
        for method, op in methods.items():
            method = method.upper()
            if method not in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                continue
            cat = _category(path)
            func_src = _generate_function(path, method, op)
            by_category.setdefault(cat, []).append(func_src)

    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    # Wipe old generated files (but keep __init__.py and any manual modules)
    for f in TOOLS_DIR.glob("*.py"):
        if f.name in ("__init__.py",):
            continue
        f.unlink()

    counts: dict[str, int] = {}
    all_func_names: list[str] = []
    for cat, funcs in sorted(by_category.items()):
        out = TOOLS_DIR / f"{cat}.py"
        body = _module_header(cat) + "\n\n".join(funcs)
        out.write_text(body)
        counts[cat] = len(funcs)
        for f in funcs:
            m = re.match(r"async def (\w+)\(", f)
            if m:
                all_func_names.append(m.group(1))

    # Write a minimal __init__.py so the tools package is importable
    init = TOOLS_DIR / "__init__.py"
    init.write_text('"""Auto-generated VTurb tool modules."""\n')

    return counts


if __name__ == "__main__":
    counts = generate()
    total = sum(counts.values())
    print(f"Generated {total} tools across {len(counts)} modules:")
    for cat, n in sorted(counts.items()):
        print(f"  {cat}: {n}")
