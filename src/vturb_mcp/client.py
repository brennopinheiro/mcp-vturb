"""VTurb Analytics async HTTP client.

Auth: 2 headers — X-Api-Token + X-Api-Version. POST endpoints use JSON body,
GET endpoints use query params.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any, Optional

import httpx

API_VERSION = "v1"
BASE_URL = "https://analytics.vturb.net"
ENV_VAR_TOKEN = "VTURB_API_TOKEN"


class VturbError(Exception):
    """Error from the VTurb Analytics API."""

    def __init__(self, message: str, status_code: int = 0, details: Optional[dict] = None):
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class RateLimitError(VturbError):
    """Quota exhausted — see `details.resets_at` for retry window."""


class VturbClient:
    """Async client for analytics.vturb.net."""

    def __init__(self, token: Optional[str] = None):
        self._token = token or os.environ.get(ENV_VAR_TOKEN, "")
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=BASE_URL,
                timeout=httpx.Timeout(30.0, read=60.0),
                limits=httpx.Limits(max_connections=20),
                headers={
                    "X-Api-Token": self._token,
                    "X-Api-Version": API_VERSION,
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "User-Agent": "vturb-mcp/0.1.0",
                },
            )
        return self._client

    async def request(
        self,
        method: str,
        path: str,
        params: Optional[dict[str, Any]] = None,
        json_body: Optional[dict[str, Any]] = None,
    ) -> Any:
        """Make an authenticated request. Retries on 429 with backoff."""
        if not self._token:
            raise VturbError(
                f"Missing {ENV_VAR_TOKEN} env var. Get a token at "
                "https://app.vturb.com/settings/analytics-api",
                status_code=401,
            )

        client = await self._get_client()
        url = path if path.startswith("http") else f"/{path.lstrip('/')}"

        # Strip None values from params/body so we don't send literal "None"
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}
        clean_body = {k: v for k, v in (json_body or {}).items() if v is not None}

        last_resp: Optional[httpx.Response] = None
        for attempt in range(3):
            resp = await client.request(
                method,
                url,
                params=clean_params or None,
                json=clean_body if clean_body else None,
            )
            last_resp = resp

            if 200 <= resp.status_code < 300:
                if not resp.content:
                    return None
                try:
                    return resp.json()
                except Exception:
                    return {"raw": resp.text}

            if resp.status_code == 429:
                # VTurb sends { error, code, details: { resets_at, ... } }
                payload = self._safe_json(resp)
                details = payload.get("details", {}) if isinstance(payload, dict) else {}
                if attempt < 2:
                    await asyncio.sleep(2 ** (attempt + 1))
                    continue
                raise RateLimitError(
                    payload.get("error", "Rate limited") if isinstance(payload, dict) else "Rate limited",
                    status_code=429,
                    details=details,
                )

            # Non-retryable error
            payload = self._safe_json(resp)
            msg = payload.get("error") or payload.get("message") or resp.text[:500] if isinstance(payload, dict) else resp.text[:500]
            raise VturbError(msg, status_code=resp.status_code, details=payload if isinstance(payload, dict) else {})

        raise VturbError(
            f"Max retries exceeded ({last_resp.status_code if last_resp else 'no response'})",
            status_code=last_resp.status_code if last_resp else 0,
        )

    @staticmethod
    def _safe_json(resp: httpx.Response) -> Any:
        try:
            return resp.json()
        except Exception:
            return {"error": resp.text[:500]}

    async def get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(self, path: str, json_body: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("POST", path, json_body=json_body)

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
