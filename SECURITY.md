# Security Policy

## Scope

This repository currently contains public documentation for the Zorathvael (ZV) Solana meme-token project. It is not evidence that the token or any third-party service has undergone a security audit.

## Reporting a vulnerability

Please do not publish exploitable details, private information, credentials, or wallet secrets in a public issue. Use GitHub's private vulnerability reporting feature if it is enabled for this repository. If it is unavailable, contact the repository owner through a verified channel and share only the minimum details required for triage.

Do not send seed phrases or private keys to anyone, including maintainers. Maintainers will never need them.

## User safety

- Never enter a seed phrase or private key into a website reached from a DM, advertisement, QR code, or unsolicited message.
- Verify the full token mint address before swapping.
- Beware of fake ZV tokens, fake support accounts, malicious wallet approvals, phishing links, and promises of guaranteed returns.
- Review transaction details and revoke suspicious wallet approvals using reputable tools.
- Do not assume that a GitHub repository, token listing, or logo proves a token is safe.

## Repository security

- Keep secrets out of commits, issues, screenshots, logs, and workflow output.
- Use least-privilege permissions for GitHub Actions and integrations.
- Pin third-party GitHub Actions to reviewed full commit SHAs before using them in sensitive workflows.
- Review dependency changes and workflow permission changes.
- Require review for code that can move funds, sign transactions, or access credentials.
- Publish security claims only when supported by evidence.

## Supported versions

The repository is documentation-first. Security reports concerning this repository's files and any future code are welcome.