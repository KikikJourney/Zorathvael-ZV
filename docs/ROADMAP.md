# Zorathvael (ZV) — Roadmap

This roadmap distinguishes shipped code from future work. It is not a promise of price performance, token utility, listings, or financial returns.

## Phase 0 — Identity and repository
- [x] Establish public repository, risk disclosures, license, and contribution/security guidance.
- [x] Document the Solana mint and BNB Smart Chain contract as separate token instances.
- [x] Commit the supplied logo and automated read-only verification workflows.
- [x] Add a read-only ecosystem dashboard that reads both networks and can read wallet balances after an explicit connect click.

## Phase 1 — Trust, publishing, and verification
- [ ] Publish the dashboard on HTTPS and verify desktop/mobile layout plus compatible wallet browsers.
- [ ] Independently review the BNB minimal-proxy implementation and all owner/admin privileges.
- [ ] Independently verify actual pools, reserves, swap routes, and recent trade events on each network.
- [ ] Publish dated findings with evidence; do not equate token transfers with buys or claim liquidity without proof.
- [ ] Verify official community channels and enable repository security/branch protections where available.

## Phase 2 — Define a real utility
- [ ] Select one user problem and validate demand before building transactions.
- [ ] Specify user journey, token role, fees/costs, abuse controls, support owner, success metrics, and failure/recovery path.
- [ ] Prefer a first utility that can read existing balances without changing immutable Solana mint settings.
- [ ] Implement tests, threat model, and testnet validation; obtain independent security review before mainnet transaction features.

## Phase 3 — Transactions and ecosystem operations
- [ ] Only after Phase 2 review: implement the selected utility with explicit wallet signing, transparent fees, and user confirmation.
- [ ] Add monitoring, incident response, versioned releases, and reproducible deployment instructions.
- [ ] Keep private keys and seed phrases out of the repository, app, and support workflow.

## Cross-chain policy
The Solana mint and BNB contract are separate assets today. The dashboard unifies discovery and visibility only. A bridge or canonical cross-chain asset is **not implemented**. Any such feature requires a separate design choice, explicit backing/trust assumptions, threat model, recovery plan, independent audit, and operational budget before deployment. Never imply 1:1 backing or unified supply beforehand.

## Change control
A checkbox may be marked complete only when the implementation exists and has been verified. Dashboard data does not prove active liquidity, safety, market value, or that the project has a production utility.
