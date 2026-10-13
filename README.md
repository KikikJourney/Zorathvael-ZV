<p align="center">
  <img src="assets/1791818551418.png" alt="Zorathvael (ZV) official logo" width="240">
</p>

<h1 align="center">Zorathvael (ZV)</h1>

<p align="center"><em>From Fragility to Resilience.</em></p>
<p align="center">Audience → Holders → Community → Ecosystem.</p>

<p align="center">
  <a href="https://pump.fun/coin/7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump">Solana / pump.fun</a> ·
  <a href="https://solscan.io/token/7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump">Solscan</a> ·
  <a href="https://bscscan.com/token/0x2c6b35f3e70500b1189e331547b493904c598888">BNB Chain / BscScan</a> ·
  <a href="https://github.com/KikikJourney/Zorathvael-ZV/issues">Issues</a>
</p>

> **Risk notice:** ZV is a crypto/meme token and may be highly volatile, illiquid, or lose all of its value. This repository is informational, not financial, investment, legal, or tax advice. Never share seed phrases or private keys.

## Project and network overview

Zorathvael (ZV) is documented here across two separate networks. **The Solana mint and BNB Smart Chain contract are separate on-chain token instances.** A shared name, ticker, logo, or repository does not make them the same asset, automatically bridge them, or combine their supplies, liquidity, holders, or ownership.

| Field | Solana | BNB Smart Chain |
|---|---|---|
| Project name | Zorathvael | Zorathvael |
| Ticker | ZV | ZV |
| Network | Solana mainnet | BNB Smart Chain (BSC) |
| Mint / contract | `7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump` | `0x2c6b35f3e70500b1189e331547b493904c598888` |
| Decimals | 6 (recorded Solana RPC snapshot) | 18 (read-only RPC check, 2026-10-13) |
| Total supply | **1,000,000,000 ZV** (recorded RPC snapshot, 2026-10-12) | **1,000,000,000 ZV** (read-only RPC check, 2026-10-13) |
| Explorer | [Solscan](https://solscan.io/token/7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump) | [BscScan](https://bscscan.com/token/0x2c6b35f3e70500b1189e331547b493904c598888) |

The supply figure for **each network is one billion ZV**. The values above are network-specific on-chain observations with the timestamps noted; re-check the explorers or run the verification workflows for current state. Supply is not the same as circulating supply, liquidity, holder count, or trading volume.

## Ecosystem dashboard

The first functional ecosystem interface is [`app/index.html`](app/index.html); a GitHub Pages deployment workflow is configured in [pages.yml](.github/workflows/pages.yml). It reads live supply/decimals from public RPC endpoints for both networks and, after a user clicks Connect, can read the connected wallet's public ZV balance. It is intentionally read-only: no signing, approvals, transfers, staking, rewards, swap, or bridge. Open it from a static HTTPS host or a wallet-compatible browser; local/file previews may block RPC requests or wallet providers. Architecture and remaining security gates: [Ecosystem architecture](docs/ECOSYSTEM-ARCHITECTURE.md) and [preliminary BNB security review](docs/BNB-PRELIMINARY-SECURITY-REVIEW.md).

## Market status

A token page or deployed contract does **not** by itself prove that a usable buy/sell market exists. Pool liquidity, swap routing, actual trades, holder distribution, and current market status must be checked independently on each network. Do not interpret transfers alone as proof of purchases, and do not claim buyers, liquidity, or trading activity without evidence.

## Verification status

- **Dashboard publishing:** the GitHub Pages build artifact succeeded, but deployment returned HTTP 404 because GitHub Pages is not enabled for this repository. The workflow is ready; enable Pages in repository Settings → Pages, then rerun [Deploy Zorathvael dashboard](https://github.com/KikikJourney/Zorathvael-ZV/actions/workflows/pages.yml). Public hosting is not claimed until a deployment succeeds.

- **Solana:** a read-only mainnet RPC snapshot dated 2026-10-12 recorded 6 decimals, total supply of 1,000,000,000 ZV, and null mint/freeze authorities. This is a point-in-time check, not a security audit or market-status check.
- **BNB Smart Chain:** a read-only RPC check dated 2026-10-13 returned name `Zorathvael`, symbol `ZV`, 18 decimals, total supply of 1,000,000,000 ZV, and owner/getOwner result `0xe2ce6ab80874fa9fa2aae65d277dd6b8e65c9de0`. BscScan marks the TokenV3 minimal-proxy contract source as verified and identifies implementation `0x88881b6f03090462a969eC7f48385744Eeb63333`. The owner address does not identify a real-world person, and source verification is not a security audit. Implementation-level privileged controls still require review.
- **Market and holders:** current holder counts, active liquidity pools, and verified buy trades are not asserted by this README; these require a separate current on-chain market audit.

A blockchain explorer is a starting point for verification, not proof of legitimacy, safety, ownership, liquidity, or value. Always compare the complete address before interacting with a token.

## Purpose and limitations

This repository is the public development and documentation home for Zorathvael (ZV). The first read-only ecosystem dashboard is implemented, but the project does not claim its own blockchain, validator network, audited smart contract, bridge, staking/rewards, swap, or production token utility. No cross-chain bridge or one-to-one backing is implied by documenting both networks together.

## Security principles

1. Never request, store, commit, or share anyone's seed phrase, private key, wallet export, or access token.
2. Verify each network's complete address independently; names, tickers, and logos do not uniquely identify a token.
3. Never publish unverified claims about supply, authorities, liquidity locks, audits, partnerships, or utility.
4. Treat unsolicited DMs, fake support accounts, airdrops, and links as potentially malicious.
5. Document changes through reviewable commits. Do not fake activity, holders, endorsements, or audit status.

## Repository map

- `chains/solana.md` — Solana mint details and recorded RPC snapshot
- `chains/bnb-smart-chain.md` — BNB contract details and verification evidence
- `scripts/verify_bnb_contract.py` — read-only BNB contract verifier
- `.github/workflows/bnb-verification.yml` — automated BNB verification workflow
- `scripts/verify_onchain.py` — read-only Solana mint verifier
- `.github/workflows/onchain-verification.yml` — automated Solana verification workflow
- `app/index.html` — read-only ecosystem dashboard for both token instances
- `docs/ECOSYSTEM-ARCHITECTURE.md` — architecture, security gates, and remaining work
- `docs/TOKEN-INFO.md` — combined network comparison
- `docs/VERIFICATION.md` — verification procedure
- `assets/1791818551418.png` — official logo image supplied by the project owner and used in this README
- `SECURITY.md` — security policy
- `CONTRIBUTING.md` — contribution guide
- `CODE_OF_CONDUCT.md` — community code of conduct

## Disclaimer

Cryptocurrency assets are risky, speculative, and may be illiquid. Nothing in this repository is a promise of profit, price performance, liquidity, exchange listing, or future development. On-chain and market information can change; independently verify current facts before acting.
