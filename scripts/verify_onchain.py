#!/usr/bin/env python3
"""Read-only verification of the published ZV mint using Solana's public JSON-RPC."""
from __future__ import annotations

import base64
import json
import os
import struct
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
MINT_BASE_SIZE = 82
ACCOUNT_TYPE_OFFSET = 165
TLV_START = 166
TOKEN_2022_MINT_ACCOUNT_TYPE = 1
METADATA_POINTER_EXTENSION = 18
TOKEN_METADATA_EXTENSION = 19


def rpc(method: str, params: list) -> dict:
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    request = urllib.request.Request(
        RPC_URL,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Zorathvael-ZV-verifier/1.1"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"Solana RPC request failed: {exc}") from exc
    if body.get("error"):
        raise RuntimeError(f"Solana RPC error: {body['error']}")
    return body.get("result") or {}


def _read_borsh_string(data: bytes, offset: int) -> tuple[str, int]:
    if offset + 4 > len(data):
        raise ValueError("truncated Borsh string length")
    length = struct.unpack_from("<I", data, offset)[0]
    offset += 4
    if offset + length > len(data):
        raise ValueError("truncated Borsh string data")
    return data[offset:offset + length].decode("utf-8"), offset + length


def parse_token_2022_extensions(encoded_account_data: str) -> dict:
    """Decode the Token-2022 mint TLV extensions without external dependencies."""
    raw = base64.b64decode(encoded_account_data, validate=True)
    result = {
        "metadata_pointer_present": False,
        "metadata_present": False,
        "name": None,
        "symbol": None,
        "uri": None,
        "metadata_update_authority": None,
        "additional_metadata": {},
        "metadata_status": "no Token-2022 extensions detected",
    }
    if len(raw) <= MINT_BASE_SIZE:
        return result
    if len(raw) <= ACCOUNT_TYPE_OFFSET or raw[ACCOUNT_TYPE_OFFSET] != TOKEN_2022_MINT_ACCOUNT_TYPE:
        raise ValueError("account has extension-sized data but no valid Token-2022 mint account-type marker")

    offset = TLV_START
    while offset + 4 <= len(raw):
        extension_type, length = struct.unpack_from("<HH", raw, offset)
        offset += 4
        if extension_type == 0 and length == 0:
            break
        end = offset + length
        if end > len(raw):
            raise ValueError(f"extension {extension_type} length exceeds account data")
        value = raw[offset:end]
        offset = end
        if extension_type == METADATA_POINTER_EXTENSION:
            result["metadata_pointer_present"] = True
            if len(value) >= 64:
                result["metadata_pointer_authority"] = _pubkey_or_none(value[:32])
                result["metadata_pointer_address"] = _pubkey_or_none(value[32:64])
        elif extension_type == TOKEN_METADATA_EXTENSION:
            result["metadata_present"] = True
            if len(value) < 64:
                raise ValueError("TokenMetadata extension is shorter than its authority and mint fields")
            result["metadata_update_authority"] = _pubkey_or_none(value[:32])
            metadata_mint = _pubkey_or_none(value[32:64])
            cursor = 64
            name, cursor = _read_borsh_string(value, cursor)
            symbol, cursor = _read_borsh_string(value, cursor)
            uri, cursor = _read_borsh_string(value, cursor)
            if cursor + 4 > len(value):
                raise ValueError("TokenMetadata extension is missing additional-metadata count")
            count = struct.unpack_from("<I", value, cursor)[0]
            cursor += 4
            additional = {}
            for _ in range(count):
                key, cursor = _read_borsh_string(value, cursor)
                val, cursor = _read_borsh_string(value, cursor)
                additional[key] = val
            result.update({
                "name": name,
                "symbol": symbol,
                "uri": uri,
                "metadata_mint": metadata_mint,
                "additional_metadata": additional,
                "metadata_status": "TokenMetadata extension decoded",
            })
    if not result["metadata_present"]:
        result["metadata_status"] = (
            "MetadataPointer extension exists but TokenMetadata extension was not found"
            if result["metadata_pointer_present"]
            else "No TokenMetadata extension found in mint account"
        )
    return result


def _pubkey_or_none(raw: bytes) -> str | None:
    if len(raw) != 32 or raw == bytes(32):
        return None
    # Base58 encoding, implemented locally to keep this verifier dependency-free.
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    number = int.from_bytes(raw, "big")
    encoded = ""
    while number:
        number, remainder = divmod(number, 58)
        encoded = alphabet[remainder] + encoded
    leading_zeroes = len(raw) - len(raw.lstrip(b"\\0"))
    return "1" * leading_zeroes + (encoded or ("" if leading_zeroes else "1"))


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

    metadata = {
        "metadata_status": "Skipped: account is not owned by Token-2022",
        "metadata_pointer_present": None,
        "metadata_present": None,
        "name": None,
        "symbol": None,
        "uri": None,
        "metadata_update_authority": None,
        "additional_metadata": {},
    }
    if program_id == "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb":
        raw_result = rpc("getAccountInfo", [MINT, {"encoding": "base64", "commitment": "confirmed"}])
        raw_account = raw_result.get("value") or {}
        raw_data = raw_account.get("data")
        if not isinstance(raw_data, list) or not raw_data:
            raise RuntimeError("Solana RPC returned no base64 mint-account data for metadata inspection.")
        try:
            metadata = parse_token_2022_extensions(raw_data[0])
        except (ValueError, UnicodeDecodeError, struct.error) as exc:
            metadata = {
                "metadata_status": f"Could not decode Token-2022 metadata safely: {exc}",
                "metadata_pointer_present": None,
                "metadata_present": None,
                "name": None,
                "symbol": None,
                "uri": None,
                "metadata_update_authority": None,
                "additional_metadata": {},
            }

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
        "metadata_source": "Token-2022 mint account via Solana RPC; no Solscan API key required",
        **metadata,
        "interpretation": (
            "Read-only snapshot. Metadata fields are reported only when decoded from the mint account; "
            "the URI content and logo are not fetched or authenticated by this check. "
            "Not a security audit or investment recommendation."
        ),
    }


if __name__ == "__main__":
    try:
        print(json.dumps(verify(), indent=2, sort_keys=True))
    except Exception as exc:  # print a clear failure for CI logs
        print(f"VERIFICATION FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
