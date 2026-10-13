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

**Important discrepancy:** the project owner previously reported a supply of **1,000,000 ZV**, but the current RPC read reports **1,000,000,000 ZV** (one billion), with 18 decimals. Treat the on-chain read as the observed contract state and resolve the project documentation/communications discrepancy before publishing a supply claim. Do not assume the on-chain figure is a circulating supply figure.

## Verification evidence and limitations

The values above were returned by the repository's read-only verifier, `scripts/verify_bnb_contract.py`, against `https://bsc-dataseed.binance.org/` on 2026-10-13. The exact timestamp and raw response are available in the GitHub Actions run logs.

- [Run BNB contract verification](https://github.com/KikikJourney/Zorathvael-ZV/actions/workflows/bnb-verification.yml)
- [BscScan contract page](https://bscscan.com/token/0x2c6b35f3e70500b1189e331547b493904c598888)

The RPC check **does not establish whether BscScan has verified the source code**. It also does not audit the contract. Review the BscScan Contract tab/source and ABI for owner privileges, minting, proxy/upgradeability, pause, fees, blacklist, and other privileged controls. An `owner()` result only means the contract returns an address for that method; it does not establish the controller's identity.

## Cross-network distinction

This is a separate contract from the Solana mint documented in [solana.md](solana.md). A shared project name, ticker, or logo does not establish a bridge, one-to-one backing, or combined supply.
