# On-chain verification

## Solana mint

The repository includes a read-only verifier at `scripts/verify_onchain.py`. It queries Solana mainnet-beta JSON-RPC for the published mint and reports token program, decimals, raw/UI supply, mint authority, and freeze authority.

```bash
python scripts/verify_onchain.py
```

The workflow [On-chain mint verification](../.github/workflows/onchain-verification.yml) runs on pushes to `main`, can be manually dispatched, and runs weekly.

## BNB Smart Chain contract

The repository includes `scripts/verify_bnb_contract.py` for contract `0x2c6b35f3e70500b1189e331547b493904c598888`. It queries a public BNB Smart Chain JSON-RPC endpoint for deployed bytecode and standard token read methods (`name()`, `symbol()`, `decimals()`, `totalSupply()`), then compares the decoded human-readable supply with the expected **1,000,000,000 ZV tokens**. It also checks common `owner()` / `getOwner()` methods when available.

```bash
python scripts/verify_bnb_contract.py
```

Optional RPC override: set `BSC_RPC_URL`. No wallet, private key, API key, transaction signing, or write call is required. The [BNB contract verification](../.github/workflows/bnb-verification.yml) workflow runs weekly, on pushes to `main`, and on manual dispatch.

A mismatch or undecodable supply makes the verifier exit with a warning/failure so the discrepancy is visible in CI. RPC cannot establish whether BscScan source code is verified, and this verifier is not a security audit. Review the BscScan Contract tab and source/ABI for proxy patterns, mint controls, ownership/roles, pausing, fees, blacklist, and upgradeability.

## How to run and review

1. Open the repository's [Actions page](https://github.com/KikikJourney/Zorathvael-ZV/actions).
2. Select **On-chain mint verification** or **BNB contract verification**.
3. Run the workflow manually if needed; the workflow files support `workflow_dispatch`.
4. Open the latest run and inspect the job logs and timestamp. A successful workflow only confirms that its programmed checks passed; it is not a security audit or market validation.

## Limitations

- A token metadata call succeeding does not prove the token is safe or legitimate.
- Detecting an owner address is a basic signal; absence of `owner()` or `getOwner()` does not prove control has been renounced.
- The verifier does not assess liquidity, holder concentration, trading activity, market manipulation, or legal status.
- RPC responses are point-in-time; record the timestamp and re-run for current state.
- Never commit seed phrases, private keys, or confidential account data.
