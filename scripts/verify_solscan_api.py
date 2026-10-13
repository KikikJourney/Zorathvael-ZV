#!/usr/bin/env python3
"""Read-only Solscan Pro API metadata check for the published ZV mint."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

MINT = "7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump"
API_URL = "https://pro-api.solscan.io/v2.0/token/meta"
EXPECTED_DECIMALS = 6


def fetch_metadata() -> dict:
    api_key = os.environ.get("SOLSCAN_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("SOLSCAN_API_KEY is not configured in the environment.")
    query = urllib.parse.urlencode({"address": MINT})
    request = urllib.request.Request(
        f"{API_URL}?{query}",
        headers={
            "accept": "application/json",
            "token": api_key,
            "User-Agent": "Zorathvael-ZV-verifier/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        # Do not print request headers or credentials.
        raise RuntimeError(f"Solscan API returned HTTP {exc.code}. Check key access, plan, and rate limits.") from exc
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"Solscan API request failed: {type(exc).__name__}: {exc}") from exc
    if not isinstance(body, dict) or body.get("success") is not True:
        errors = body.get("errors") if isinstance(body, dict) else None
        raise RuntimeError(f"Solscan API did not return success=true (errors={errors!r}).")
    data = body.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("Solscan API response is missing the token metadata object.")
    return data


def verify() -> dict:
    data = fetch_metadata()
    if data.get("address") != MINT:
        raise RuntimeError("Solscan returned metadata for an unexpected token address.")
    decimals = data.get("decimals")
    if decimals != EXPECTED_DECIMALS:
        raise RuntimeError(f"Solscan decimals mismatch: expected {EXPECTED_DECIMALS}, received {decimals!r}.")
    supply_raw = data.get("supply")
    if supply_raw is not None:
        try:
            supply_raw = str(int(supply_raw))
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f"Solscan returned a non-integer raw supply: {supply_raw!r}.") from exc
    # Market fields are informational snapshots, not evidence of executable liquidity.
    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "provider": "Solscan Pro API v2.0",
        "mint": MINT,
        "address_match": True,
        "name": data.get("name"),
        "symbol": data.get("symbol"),
        "decimals": decimals,
        "supply_raw": supply_raw,
        "holder_count": data.get("holder"),
        "price_usd": data.get("price"),
        "market_cap_usd": data.get("market_cap"),
        "total_dex_volume_24h_usd": data.get("total_dex_vol_24h"),
        "mint_authority": data.get("mint_authority"),
        "freeze_authority": data.get("freeze_authority"),
        "metadata_uri": data.get("metadata_uri"),
        "interpretation": (
            "Solscan indexed-data snapshot only. Price/volume/holder fields may be missing or stale; "
            "this does not prove executable liquidity, verified buys, token safety, or investment merit."
        ),
    }


if __name__ == "__main__":
    try:
        print(json.dumps(verify(), indent=2, sort_keys=True))
    except Exception as exc:
        print(f"VERIFICATION FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
