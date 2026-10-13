#!/usr/bin/env python3
"""Read-only BNB Smart Chain token verification using public JSON-RPC."""
import json, os, sys, urllib.error, urllib.request
from datetime import datetime, timezone
from decimal import Decimal

CONTRACT = "0x2c6b35f3e70500b1189e331547b493904c598888"
RPC_URL = os.environ.get("BSC_RPC_URL", "https://bsc-dataseed.binance.org/")
EXPECTED_SUPPLY = Decimal("1000000")

def rpc(method, params):
    payload = json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    request = urllib.request.Request(RPC_URL, data=payload, headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"BNB RPC request failed: {exc}") from exc
    if body.get("error"):
        raise RuntimeError(f"BNB RPC error: {body['error']}")
    return body.get("result")

def call(selector):
    try:
        value = rpc("eth_call", [{"to":CONTRACT,"data":selector},"latest"])
        return value if isinstance(value,str) and value.startswith("0x") and len(value)>2 else None
    except RuntimeError:
        return None

def uint(value):
    try: return int(value,16) if value else None
    except ValueError: return None

def string(value):
    if not value: return None
    try:
        raw=bytes.fromhex(value[2:])
        if len(raw)==32: return raw.rstrip(b"\x00").decode("utf-8") or None
        if len(raw)>=64:
            offset=int.from_bytes(raw[:32],"big")
            length=int.from_bytes(raw[offset:offset+32],"big")
            return raw[offset+32:offset+32+length].decode("utf-8")
    except (ValueError,UnicodeDecodeError,IndexError): return None
    return None

def address(value):
    try:
        raw=bytes.fromhex(value[2:]) if value else b""
        result=raw[-20:].hex()
        return "0x"+result if len(raw)>=32 and int(result,16) else None
    except ValueError: return None

def verify():
    code=rpc("eth_getCode",[CONTRACT,"latest"])
    if not isinstance(code,str) or code in ("0x","0x0"):
        raise RuntimeError("No deployed contract bytecode found at this address on the configured BNB RPC.")
    name=string(call("0x06fdde03"))
    symbol=string(call("0x95d89b41"))
    decimals=uint(call("0x313ce567"))
    raw_supply=uint(call("0x18160ddd"))
    if not any((name,symbol,decimals is not None,raw_supply is not None)):
        raise RuntimeError("Bytecode exists, but standard token read methods returned no usable data.")
    supply=Decimal(raw_supply)/(Decimal(10)**decimals) if raw_supply is not None and decimals is not None else None
    owner=address(call("0x8da5cb5b")) or address(call("0x893d20e8"))
    matches=supply==EXPECTED_SUPPLY if supply is not None else False
    return {
      "checked_at_utc":datetime.now(timezone.utc).isoformat(),
      "network":"BNB Smart Chain mainnet (chain ID 56 expected)",
      "rpc_url":RPC_URL,"contract":CONTRACT,"contract_bytecode_present":True,
      "name":name,"symbol":symbol,"decimals":decimals,
      "total_supply_raw":str(raw_supply) if raw_supply is not None else None,
      "total_supply_tokens":str(supply) if supply is not None else None,
      "owner_or_getOwner":owner,"reported_supply_tokens":str(EXPECTED_SUPPLY),
      "reported_supply_matches_onchain":matches,
      "source_code_verified_on_explorer":"Not checked by RPC; inspect BscScan Contract tab",
      "limitations":["Read-only snapshot, not a security audit.",
        "Owner detection checks only owner() and getOwner(); absence does not prove renounced ownership.",
        "Review source/ABI for proxy patterns and privileged controls."]
    }

if __name__=="__main__":
    try:
        result=verify()
        print(json.dumps(result,indent=2,sort_keys=True))
        if not result["reported_supply_matches_onchain"]:
            print("WARNING: on-chain supply differs from or could not confirm the reported 1,000,000 tokens.",file=sys.stderr)
            sys.exit(2)
    except Exception as exc:
        print(f"VERIFICATION FAILED: {exc}",file=sys.stderr)
        sys.exit(1)
