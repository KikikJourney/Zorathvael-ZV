# Preliminary BNB token control review

**Status: preliminary source/ABI review, not a security audit.** This note records what is observable from the verified TokenV3 implementation interface associated with implementation address `0x88881b6f03090462a969eC7f48385744Eeb63333`. Before relying on any conclusion, confirm the proxy's live implementation slot and the full verified source against the exact ZV proxy address.

## Verified project identifiers
- Proxy/token: `0x2c6b35f3e70500b1189e331547b493904c598888`
- Reported implementation: `0x88881b6f03090462a969eC7f48385744Eeb63333`
- Recorded owner/getOwner: `0xe2ce6ab80874fa9fa2aae65d277dd6b8e65c9de0`
- Explorer: https://bscscan.com/token/0x2c6b35f3e70500b1189e331547b493904c598888

## High-priority review points

The verified implementation ABI exposes privileged or operationally sensitive functions including:
- `openSwapGate()` — appears to change swap-gate state.
- `startMigration()` and `finalizeMigration()` — migration lifecycle controls.
- `transferOwnership(address)` and `renounceOwnership()` — ownership administration.
- `initialize(...)` — initialization surface; confirm proxy initialization is complete and cannot be replayed.
- Read surfaces `owner()`, `isSwapGateOpen()`, `poolState()`, `mainPool()`, `pools(address)`, `taxProcessor()`, `dividendContract()`, and `flapV4Hook()` expose important state that should be recorded.

This function inventory does not establish who can call each function, the exact state transition, whether a swap can currently occur, or whether a vulnerability exists. Those conclusions require tracing the exact source code, modifiers, proxy storage, initialization transaction, pool configuration, hook and external contracts, and on-chain events.

## Required checks before transaction features
1. Confirm the proxy address and implementation slot from live BNB RPC; compare exact bytecode and verified source.
2. Read the current owner, swap-gate state, pool state, main pool, registered pools, hook, tax processor, dividend contract, and migration state where available.
3. Trace all owner-only and hook-only paths, including whether token transfers can be blocked, taxes changed, pools migrated, or balances diverted.
4. Inspect external hook/tax/dividend contracts and their admin controls; verify no untrusted arbitrary-call path.
5. Review initializer protection and the proxy's initialization history.
6. Test expected and adversarial paths on a fork/testnet; get an independent audit before enabling token-moving app functionality.

## Market evidence
A deployed token and verified source are not proof of active liquidity. No claim is made here that a liquid pool, safe swap route, or recent buy/sell activity has been confirmed. Verify pool addresses and reserves from on-chain factory/pair contracts and corroborate recent swap events before publishing market claims.

## Decision
Until the checks above are completed, keep the ZV dashboard read-only. Do not add swap, staking, bridge, reward, or other transaction-signing features to the dashboard. No change to the deployed token contract is made by this review.
