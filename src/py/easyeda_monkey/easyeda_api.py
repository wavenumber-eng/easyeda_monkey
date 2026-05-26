"""
LCSC / EasyEDA component API client.

Fetches symbol, footprint, and 3D model data by LCSC part number.
Uses ``requests`` for HTTP — this is the only module with an external dependency.
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Any

from .easyeda_footprint import EasyEdaFootprint
from .easyeda_symbol import EasyEdaSymbol

log = logging.getLogger(__name__)

_API_BASE = "https://easyeda.com/api/products"
_API_VERSION = "6.4.19.5"
_USER_AGENT = "wn_pcb_tools/1.0"
_DEFAULT_TIMEOUT = 15


class EasyEdaApiClient:
    """
    Client for the LCSC / EasyEDA component API.

    Fetches component data by LCSC part number (e.g. ``C21190``).
    Supports optional disk caching for offline use and test fixture generation.
    """

    def __init__(
        self,
        cache_dir: str | Path | None = None,
        timeout: int = _DEFAULT_TIMEOUT,
        rate_limit_seconds: float = 0.5,
    ) -> None:
        self._cache_dir = Path(cache_dir) if cache_dir else None
        self._timeout = timeout
        self._rate_limit = rate_limit_seconds
        self._last_request_time: float = 0.0

        if self._cache_dir:
            self._cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch_component(self, lcsc_id: str) -> dict[str, Any]:
        """
        Fetch raw API response for an LCSC component.

        Returns the full JSON response dict. Caches to disk if cache_dir set.
        """
        lcsc_id = lcsc_id.strip().upper()
        if not lcsc_id.startswith("C"):
            lcsc_id = f"C{lcsc_id}"

        # Check cache first
        if self._cache_dir:
            cache_path = self._cache_dir / f"{lcsc_id}.json"
            if cache_path.exists():
                log.debug("Cache hit for %s", lcsc_id)
                return json.loads(cache_path.read_text(encoding="utf-8"))

        # Rate limiting
        now = time.monotonic()
        elapsed = now - self._last_request_time
        if elapsed < self._rate_limit:
            time.sleep(self._rate_limit - elapsed)

        import requests

        url = f"{_API_BASE}/{lcsc_id}/components?version={_API_VERSION}"
        headers = {
            "User-Agent": _USER_AGENT,
            "Accept": "application/json",
        }

        log.info("Fetching %s from LCSC API", lcsc_id)
        response = requests.get(url, headers=headers, timeout=self._timeout)
        self._last_request_time = time.monotonic()
        response.raise_for_status()

        data = response.json()

        if not data.get("success") or not data.get("result"):
            log.warning("API returned empty/failed result for %s", lcsc_id)
            return {}

        # Cache to disk
        if self._cache_dir:
            cache_path = self._cache_dir / f"{lcsc_id}.json"
            cache_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            log.debug("Cached %s (%d bytes)", lcsc_id, cache_path.stat().st_size)

        return data

    def fetch_symbol(self, lcsc_id: str) -> EasyEdaSymbol:
        """Fetch and parse a schematic symbol by LCSC part number."""
        data = self.fetch_component(lcsc_id)
        if not data:
            raise ValueError(f"No component data for {lcsc_id}")
        return EasyEdaSymbol.from_json(data)

    def fetch_footprint(self, lcsc_id: str) -> EasyEdaFootprint:
        """Fetch and parse a PCB footprint by LCSC part number."""
        data = self.fetch_component(lcsc_id)
        if not data:
            raise ValueError(f"No component data for {lcsc_id}")
        return EasyEdaFootprint.from_json(data)

    def fetch_both(self, lcsc_id: str) -> tuple[EasyEdaSymbol, EasyEdaFootprint]:
        """Fetch and parse both symbol and footprint in a single API call."""
        data = self.fetch_component(lcsc_id)
        if not data:
            raise ValueError(f"No component data for {lcsc_id}")
        return EasyEdaSymbol.from_json(data), EasyEdaFootprint.from_json(data)
