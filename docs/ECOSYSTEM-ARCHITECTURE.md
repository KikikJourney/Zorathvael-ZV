# Zorathvael ecosystem architecture

## Goal
Make the repository the source of truth for a usable ZV ecosystem, not merely a token listing. The first deliverable is a read-only dashboard at `app/index.html` that connects public on-chain data to the documented token instances.

## Current implementation
- Static, dependency-free web dashboard; intended for GitHub Pages or any static HTTPS host.
- Reads Solana mainnet token supply through `getTokenSupply`.
- Reads BNB Smart Chain BEP-20 supply/decimals through public JSON-RPC `eth_call`.
- Optional wallet connect is explicitly user-initiated. It reads the public wallet address and the ZV balance only.
- No signing, token transfers, approvals, private-key handling, analytics trackers, or third-party JavaScript packages.
- If a public RPC is unavailable or rate-limited, the UI reports the error rather than inventing data.

## Asset identity and cross-chain constraint
The Solana mint `7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump` and BNB contract `0x2c6b35f3e70500b1189e331547b493904c598888` are separate token instances. This dashboard aggregates visibility, not token supply or liquidity. It does not bridge, burn, lock, mint, wrap, or claim one-to-one backing. Cross-chain fungibility requires a separately specified bridge or canonical-asset design, threat model, independent audit, and a funded operational model; it must not be improvised as a UI feature.

## Roadmap gates
1. **Read-only foundation (implemented):** public dashboard and wallet balance reads.
2. **Publishing and QA:** host on HTTPS, test desktop/mobile and supported wallets, and check RPC failure paths.
3. **Market evidence:** identify official pools per chain; independently verify pool addresses, reserves/liquidity, swap routes, and actual trade events before claiming an active market.
4. **BNB contract review:** trace the proxy to implementation source, identify owner/admin privileges and upgradeability, review privileged functions and external dependencies, and commission independent review before any transaction feature.
5. **Utility specification:** select one real user problem and define the workflow, value, abuse controls, costs, and success metrics. Prefer a utility that can initially use existing token balances without modifying immutable Solana mint settings.
6. **Transactions only after review:** if necessary, define contracts/programs, tests, threat model, testnet trial, independent review, and explicit user consent. Never ask for seed phrases or private keys.
7. **Cross-chain only as a separate project:** choose lock/mint, burn/mint, or non-fungible independent token model transparently. Document trust assumptions and failure/recovery modes; no claim of unified token until this is deployed and independently reviewed.

## Known limitations
- Dashboard is read-only and not a swap, staking, rewards, governance, bridge, or token-gated product.
- Public RPC availability and CORS vary; UI failures must remain visible.
- Wallet providers differ by browser and extension. Wallet connection may not work when the static page is opened outside a compatible wallet-enabled browser.
- Token metadata and total supply do not establish liquidity, price, trading activity, holder distribution, safety, or value.
- No deployment or external security audit is claimed by this file.
