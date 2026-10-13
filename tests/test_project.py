"""Dependency-free regression checks for public ZV project information."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MINT = "7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump"


class ProjectIntegrityTests(unittest.TestCase):
    def test_expected_public_documents_exist(self):
        for relative in (
            "README.md",
            "LICENSE.md",
            "docs/TOKEN-INFO.md",
            "docs/ROADMAP.md",
            "SECURITY.md",
            "CONTRIBUTING.md",
            "docs/FAQ.md",
            "CODE_OF_CONDUCT.md",
            "assets/1791818551418.png",
            "scripts/verify_onchain.py",
            "scripts/verify_bnb_contract.py",
            "scripts/verify_bnb_etherscan.py",
            ".github/workflows/bnb-verification.yml",
            "chains/solana.md",
            "chains/bnb-smart-chain.md",
            ".github/workflows/quality.yml",
            ".github/workflows/onchain-verification.yml",
            "docs/VERIFICATION.md",
            "docs/ECOSYSTEM-ARCHITECTURE.md",
            "docs/BNB-PRELIMINARY-SECURITY-REVIEW.md",
            "app/index.html",
        ):
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_dashboard_is_read_only_and_covers_both_networks(self):
        app = (ROOT / "app/index.html").read_text(encoding="utf-8")
        for marker in ("getTokenSupply", "getTokenAccountsByOwner", "eth_call", "eth_requestAccounts", "eth_requestAccounts", "0x70a08231", "7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEj1pump", "0x2c6b35f3e70500b1189e331547b493904c598888"):
            with self.subTest(marker=marker):
                self.assertIn(marker, app)
        self.assertNotIn("eth_sendTransaction", app)
        self.assertNotIn("sendTransaction(", app)
        self.assertIn("docs/ECOSYSTEM-ARCHITECTURE.md", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_mint_address_is_consistent(self):
        for relative in ("README.md", "docs/TOKEN-INFO.md"):
            content = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn(MINT, content)

    def test_readme_points_to_committed_logo(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("assets/1791818551418.png", readme)
        self.assertTrue((ROOT / "assets/1791818551418.png").is_file())

    def test_readme_has_risk_disclosure(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("promise of profit", readme)
        self.assertIn("meme token", readme)

    def test_bnb_expected_supply_and_docs_are_consistent(self):
        verifier = (ROOT / "scripts/verify_bnb_contract.py").read_text(encoding="utf-8")
        self.assertRegex(verifier, r'EXPECTED_SUPPLY\s*=\s*Decimal\("1000000000"\)')
        for relative in ("README.md", "docs/TOKEN-INFO.md",
                         "docs/VERIFICATION.md", "chains/bnb-smart-chain.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn("1,000,000,000 ZV", text)
                self.assertNotRegex(text, r"(?<![0-9,])1,000,000 ZV(?![0-9,])")

    def test_etherscan_v2_check_uses_secret_and_bnb_chain(self):
        script = (ROOT / "scripts/verify_bnb_etherscan.py").read_text(encoding="utf-8")
        workflow = (ROOT / ".github/workflows/bnb-verification.yml").read_text(encoding="utf-8")
        self.assertIn('CHAIN_ID = "56"', script)
        self.assertIn("https://api.etherscan.io/v2/api", script)
        self.assertIn('os.environ.get("ETHERSCAN_API_KEY"', script)
        self.assertIn("secrets.ETHERSCAN_API_KEY", workflow)
        self.assertNotIn("eth_sendRawTransaction", script)
        self.assertIn("not an independent security audit", script)

    def test_markdown_relative_links_resolve(self):
        markdown_files = [ROOT / "README.md", ROOT / "SECURITY.md",
                          ROOT / "CONTRIBUTING.md", *((ROOT / "docs").glob("*.md"))]
        pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for file in markdown_files:
            content = file.read_text(encoding="utf-8")
            for target in pattern.findall(content):
                if target.startswith(("https://", "http://", "mailto:", "#")):
                    continue
                path = target.split("#", 1)[0]
                if not path:
                    continue
                with self.subTest(file=str(file.relative_to(ROOT)), target=target):
                    self.assertTrue((file.parent / path).resolve().exists(), target)


if __name__ == "__main__":
    unittest.main()
