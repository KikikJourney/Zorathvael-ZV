# Zorathvael (ZV) — BNB Smart Chain

## Contract identity — read-only RPC checked 2026-10-13

- **Network:** BNB Smart Chain mainnet (public RPC response)
- **Contract:** `0x2c6b35f3e70500b1189e331547b493904c598888`
- **Explorer:** https://bscscan.com/token/0x2c6b35f3e70500b1189e331547b493904c598888
- **On-chain name():** `Zorathvael`
- **On-chain symbol():** `ZV`
- **On-chain decimals():** `18`
- **On-chain totalSupply():** `1000000000000000000000000000` base units
- **Human-readable total supply:** **1,000,000,000 ZV**
- **owner() / getOwner():** `0xe2ce6ab80874fa9fa2aae65d277dd6b8e65c9de0` (contract reports an owner address; this is not proof of who controls that wallet)
- **Deployed bytecode:** present
- **BscScan source code:** verified
- **Contract type:** TokenV3 minimal proxy
- **Implementation:** `0x88881b6f03090462a969eC7f48385744Eeb63333`
- **Compiler reported by BscScan:** `v0.8.26+commit.8a97fa7a`

**Important discrepancy:** the project owner previously reported a supply of **1,000,000 ZV**, but the current RPC read reports **1,000,000,000 ZV** (one billion), with 18 decimals. Treat the on-chain read as the observed contract state and resolve the project documentation/communications discrepancy before publishing a supply claim. Do not assume the on-chain figure is a circulating supply figure.

## Verification evidence and limitations

The values above were returned by the repository's read-only verifier, `scripts/verify_bnb_contract.py`, against `https://bsc-dataseed.binance.org/` on 2026-10-13. The exact timestamp and raw response are available in the GitHub Actions run logs.

- [Run BNB contract verification](https://github.com/KikikJourney/Zorathvael-ZV/actions/workflows/bnb-verification.yml)
- [BscScan contract page](https://bscscan.com/token/0x2c6b35f3e70500b1189e331547b493904c598888)

BscScan marks the proxy contract source as verified and identifies it as a TokenV3 minimal proxy with the implementation address above. See [proxy source](https://bscscan.com/address/0x2c6b35f3e70500b1189e331547b493904c598888#code) and [implementation page](https://bscscan.com/address/0x88881b6f03090462a969eC7f48385744Eeb63333). This is source verification, not an independent security audit. The RPC `owner()`/`getOwner()` read returned `0xe2ce6ab80874fa9fa2aae65d277dd6b8e65c9de0`, although BscScan displays no public owner label; the address-to-person identity is not established. Proxy behavior and implementation-level admin controls still require a careful source/ABI review.

## Cross-network distinction

This is a separate contract from the Solana mint documented in [solana.md](solana.md). A shared project name, ticker, or logo does not establish a bridge, one-to-one backing, or combined supply.
