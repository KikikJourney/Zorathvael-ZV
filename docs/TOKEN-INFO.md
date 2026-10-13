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
- **Reported supply:** 1,000,000 tokens — **user-provided, not yet independently verified**
- **Name / symbol / decimals:** not yet independently verified
- **Contract source verification and owner/admin privileges:** not yet independently verified

Do not present the reported supply as confirmed until it is checked against current on-chain data and the contract's decimals. A token's displayed supply and its raw integer `totalSupply()` are not the same value when decimals are applied.

### BNB verification checklist

- [ ] Open the BscScan page and compare the full contract address.
- [ ] Confirm the contract is deployed on BNB Smart Chain.
- [ ] Read the contract's name, symbol, decimals, and `totalSupply()`.
- [ ] Check whether the source code is verified and inspect owner/admin functions.
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
