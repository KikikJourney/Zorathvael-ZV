#!/usr/bin/env python3
"""Read-only Etherscan V2 source/ABI check for the ZV BNB Chain proxy.

The API key is read only from ETHERSCAN_API_KEY and is never printed.
This checks explorer publication metadata; it is not a security audit.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

CHAIN_ID = "56"
CONTRACT = "0x2c6b35f3e70500b1189e331547b493904c598888"
API_URL = "https://api.etherscan.io/v2/api"


def fetch_source(api_key: str) -> dict:
    query = urllib.parse.urlencode({
        "chainid": CHAIN_ID,
        "module": "contract",
        "action": "getsourcecode",
        "address": CONTRACT,
        "apikey": api_key,
    })
    request = urllib.request.Request(
        f"{API_URL}?{query}",
        headers={"Accept": "application/json", "User-Agent": "Zorathvael-ZV-readonly-verifier/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Etherscan V2 request failed ({type(exc).__name__}); key value withheld") from exc
    if payload.get("status") != "1" or not isinstance(payload.get("result"), list):
        message = str(payload.get("result") or payload.get("message") or "unexpected API response")
        # Never print the URL or request, as it contains the API key.
        raise RuntimeError(f"Etherscan V2 rejected the request: {message[:240]}")
    if not payload["result"]:
        raise RuntimeError("Etherscan V2 returned no contract metadata for the target address.")
    return payload["result"][0]


def verify() -> dict:
    key = os.environ.get("ETHERSCAN_API_KEY", "").strip()
    if not key:
        raise RuntimeError("ETHERSCAN_API_KEY secret is missing or empty.")
    item = fetch_source(key)
    source = item.get("SourceCode") or ""
    abi_raw = item.get("ABI") or ""
    verified = bool(source.strip()) and abi_raw not in ("", "Contract source code not verified")
    try:
        abi = json.loads(abi_raw) if abi_raw.startswith("[") else []
    except json.JSONDecodeError:
        abi = []
    functions = sorted({
        entry.get("name", "")
        for entry in abi
        if isinstance(entry, dict) and entry.get("type") == "function" and entry.get("name")
    })
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "network": "BNB Smart Chain",
        "chain_id": int(CHAIN_ID),
        "contract": CONTRACT,
        "explorer_source_verified": verified,
        "contract_name": item.get("ContractName") or None,
        "compiler_version": item.get("CompilerVersion") or None,
        "optimization_used": item.get("OptimizationUsed") or None,
        "proxy_flag": item.get("Proxy") or None,
        "implementation_address": item.get("Implementation") or None,
        "abi_function_names": functions,
        "privileged_function_review_flags": [
            name for name in functions
            if any(term in name.lower() for term in (
                "owner", "admin", "initialize", "upgrade", "migration",
                "swapgate", "tax", "pause", "blacklist", "whitelist",
                "mint", "burn", "role", "rescue", "withdraw"
            ))
        ],
        "source_code_returned": bool(source.strip()),
        "limitations": [
            "Explorer source publication is not an independent security audit.",
            "Proxy implementation and privileged controls must be reviewed against live on-chain state.",
            "This check does not prove liquidity, market activity, or token safety.",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    if not verified:
        raise RuntimeError("Explorer did not return verified source and ABI for this contract.")
    return result


if __name__ == "__main__":
    try:
        verify()
    except Exception as exc:
        print(f"ETHERSCAN SOURCE CHECK FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
