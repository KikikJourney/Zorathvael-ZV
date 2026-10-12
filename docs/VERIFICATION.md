# On-chain verification

The repository includes a read-only verifier at `scripts/verify_onchain.py`. It queries Solana mainnet-beta JSON-RPC for the published mint and reports the token program, decimals, raw/UI supply, mint authority, and freeze authority.

## Run it

Requires Python 3.10+ and network access to a Solana JSON-RPC endpoint. No wallet, private key, API key, or transaction signing is required.

```bash
python scripts/verify_onchain.py
```

To use a different RPC endpoint, set `SOLANA_RPC_URL` in the environment. Never put credentials or secrets into committed files.

The GitHub Actions workflow `On-chain mint verification` runs weekly and can also be triggered manually. Its output is a point-in-time snapshot; inspect the workflow logs and timestamp before relying on it.

## What this does not prove

- It does not audit token code, holders, liquidity, trading venues, or market manipulation.
- A revoked mint authority does not make a token safe or guarantee liquidity.
- A present mint/freeze authority is a control risk that users should understand.
- It does not independently validate social accounts, project ownership, or the authenticity of logos and websites.
- RPC availability and responses can vary; a failed query means verification did not complete, not that the mint is invalid.

Always compare the full mint address: `7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEjz1pump`.
