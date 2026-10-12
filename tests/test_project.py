"""Dependency-free regression checks for public ZV project information."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MINT = "7dWLzsJkWNYnLShY7QqqPqeWSapzv2nYBjknEjz1pump"


class ProjectIntegrityTests(unittest.TestCase):
    def test_expected_public_documents_exist(self):
        for relative in (
            "README.md",
            "docs/TOKEN-INFO.md",
            "docs/ROADMAP.md",
            "SECURITY.md",
            "CONTRIBUTING.md",
            "docs/FAQ.md",
            "CODE_OF_CONDUCT.md",
            "assets/logo.svg",
            ".github/workflows/quality.yml",
        ):
            with self.subTest(path=relative):
                self.assertTrue((ROOT / relative).is_file(), relative)

    def test_mint_address_is_consistent(self):
        for relative in ("README.md", "docs/TOKEN-INFO.md"):
            content = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn(MINT, content)

    def test_readme_points_to_committed_logo(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("assets/logo.svg", readme)
        self.assertTrue((ROOT / "assets/logo.svg").is_file())

    def test_readme_has_risk_disclosure(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("not a promise of profit", readme)
        self.assertIn("meme token", readme)

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
