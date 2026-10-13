# Security Policy

## Scope

This repository contains documentation, read-only on-chain verification scripts, and an early read-only Zorathvael (ZV) web dashboard. The dashboard reads public chain data and, after explicit user action, requests a wallet's public address to read its token balance. It must not request seed phrases/private keys or sign/send transactions. Neither source verification nor these read-only features constitute a smart-contract or product security audit.

## Reporting a vulnerability

Please do not publish exploitable details, private information, credentials, or wallet secrets in a public issue. Use GitHub's private vulnerability reporting feature if it is enabled for this repository. If it is unavailable, contact the repository owner through a verified channel and share only the minimum details required for triage.

Do not send seed phrases or private keys to anyone, including maintainers. Maintainers will never need them.

## User safety

- Never enter a seed phrase or private key into a website reached from a DM, advertisement, QR code, or unsolicited message.
- Verify the full token mint/contract address and network before interacting.
- Beware of fake ZV tokens, fake support accounts, malicious wallet approvals, phishing links, and promises of guaranteed returns.
- Review transaction details and revoke suspicious wallet approvals using reputable tools.
- Do not assume that a repository, token listing, verified source, or logo proves a token is safe or liquid.

## Repository security

- Keep secrets out of commits, issues, screenshots, logs, and workflow output.
- Use least-privilege permissions for GitHub Actions and integrations.
- Pin third-party GitHub Actions to reviewed full commit SHAs before using them in sensitive workflows.
- Review dependency changes and workflow permission changes.
- Require review and independent security assessment for code that can move funds, sign transactions, bridge assets, or access credentials.
- Publish security claims only when supported by evidence.

## Supported versions

Security reports concerning repository files, the dashboard, and future code are welcome.
