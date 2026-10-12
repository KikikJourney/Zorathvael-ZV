#!/usr/bin/env python3
"""Read-only verification of the published ZV mint using Solana's public JSON-RPC."""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

MINT = "7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEjz1pump"
RPC_URL = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
TOKEN_PROGRAMS = {
    "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA": "SPL Token",
    "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb": "Token-2022",
}


def rpc(method: str, params: list) -> dict:
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    request = urllib.request.Request(
        RPC_URL,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Zorathvael-ZV-verifier/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Solana RPC request failed: {exc}") from exc
    if body.get("error"):
        raise RuntimeError(f"Solana RPC error: {body['error']}")
    return body.get("result") or {}


def verify() -> dict:
    account_result = rpc("getAccountInfo", [MINT, {"encoding": "jsonParsed", "commitment": "confirmed"}])
    account = account_result.get("value")
    if not account:
        raise RuntimeError("The configured mint account was not found on Solana mainnet.")
    program_id = account.get("owner")
    if program_id not in TOKEN_PROGRAMS:
        raise RuntimeError(f"Mint account owner is not a recognized SPL token program: {program_id!r}")
    parsed = account.get("data", {}).get("parsed", {})
    if parsed.get("type") != "mint":
        raise RuntimeError("The supplied address does not parse as an SPL token mint.")
    mint_info = parsed.get("info", {})
    supply_result = rpc("getTokenSupply", [MINT, {"commitment": "confirmed"}]).get("value")
    if not supply_result:
        raise RuntimeError("Solana RPC returned no token-supply data.")
    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "network": "Solana mainnet-beta",
        "mint": MINT,
        "token_program": TOKEN_PROGRAMS[program_id],
        "owner_program_id": program_id,
        "decimals": supply_result.get("decimals"),
        "supply_raw": supply_result.get("amount"),
        "supply_ui": supply_result.get("uiAmountString"),
        "mint_authority": mint_info.get("mintAuthority"),
        "freeze_authority": mint_info.get("freezeAuthority"),
        "rpc_commitment": "confirmed",
        "interpretation": "Snapshot only; not a security audit or investment recommendation.",
    }


if __name__ == "__main__":
    try:
        print(json.dumps(verify(), indent=2, sort_keys=True))
    except Exception as exc:  # print a clear failure for CI logs
        print(f"VERIFICATION FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
