# Zorathvael (ZV) — Combined Token Information

This document tracks the project identifiers reported for two separate networks. They are not interchangeable assets. Listing them in one repository does not combine supply, liquidity, holders, ownership, or transferability.

## Solana

- **Project name:** Zorathvael
- **Ticker:** ZV (project label)
- **Network:** Solana
- **Mint:** `7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump`
- **Token page:** https://pump.fun/coin/7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump
- **Explorer:** https://solscan.io/token/7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump

### Recorded Solana snapshot — 2026-10-12 18:32:32 UTC

Source: read-only Solana mainnet-beta JSON-RPC snapshot, as recorded by the repository's on-chain verification workflow. This is not a security audit or proof of ownership, legitimacy, safety, or value.

| Field | Observed value |
|---|---|
| Mint account | Found; parsed as a token mint |
| Token program | Token-2022 (`TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb`) |
| Decimals | `6` |
| Total supply reported by RPC | `1,000,000,000` tokens (`1000000000000000` base units) |
| Mint authority | `null` |
| Freeze authority | `null` |

This is a point-in-time snapshot. Re-run the workflow for current values. It does not verify liquidity, holders, market conditions, or display metadata.

## BNB Smart Chain

- **Network:** BNB Smart Chain (BSC) — reported by project owner
- **Contract address supplied by project owner:** `0x2c6b35f3e70500b1189e331547b493904c598888`
- **Explorer:** https://bscscan.com/token/0x2c6b35f3e70500b1189e331547b493904c598888
- **On-chain name():** `Zorathvael` (read-only RPC, 2026-10-13)
- **On-chain symbol():** `ZV` (read-only RPC, 2026-10-13)
- **Decimals:** `18` (read-only RPC, 2026-10-13)
- **Raw totalSupply():** `1000000000000000000000000000`
- **Human-readable total supply:** `1,000,000,000 ZV` (read-only RPC, 2026-10-13)
- **Owner / getOwner result:** `0xe2ce6ab80874fa9fa2aae65d277dd6b8e65c9de0`
- **Contract bytecode:** present
- **Source-code verification on BscScan:** not confirmed by RPC; manual explorer review remains required

**Supply discrepancy:** the project owner previously reported 1,000,000 ZV, while the on-chain `totalSupply()` read returned 1,000,000,000 ZV. The verifier correctly flags this mismatch. Resolve the discrepancy before using the earlier one-million figure in public materials.

Do not present the reported supply as confirmed until it is checked against current on-chain data and the contract's decimals. A token's displayed supply and its raw integer `totalSupply()` are not the same value when decimals are applied.

### BNB verification checklist

- [ ] Open the BscScan page and compare the full contract address.
- [x] Confirm deployed bytecode and read name, symbol, decimals, and `totalSupply()` from public BNB RPC.
- [ ] Manually confirm BscScan source-code verification and review source/ABI.
- [x] BscScan source code is marked verified; contract is a TokenV3 minimal proxy.
- [ ] Review implementation source/ABI and privileged/admin controls; source verification is not a security audit.
- [ ] Check whether minting, pausing, blacklist, fees, upgradeability, or other privileged controls exist.
- [ ] Record the observation time (UTC) and sources in a follow-up commit.
- [ ] Have a second reviewer review high-impact claims.

## Cross-network caution

The Solana mint and BNB contract are separate token instances. This repository does not assert that one is a wrapped representation of the other, that their supplies are backed one-to-one, or that a bridge exists. Do not add supply figures together as if they were one fungible pool. Verify each address on its own network.

## General verification rules

1. Always compare the full address character-for-character.
2. Record the source and timestamp for every on-chain snapshot.
3. Do not claim audits, locked liquidity, burns, ownership, partnerships, exchange listings, or utility without independent evidence.
4. Never commit seed phrases, private keys, or confidential account data.
