import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from mkdocs.commands.build import build
from mkdocs.config import load_config


class _HomepageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_home_actions = False
        self.home_action_links = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if tag == "div" and "home-actions" in classes:
            self.in_home_actions = True
        elif tag == "a" and self.in_home_actions and "md-button" in classes:
            self.home_action_links += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self.in_home_actions:
            self.in_home_actions = False


class HomepageLayoutTest(unittest.TestCase):
    def test_primary_actions_share_the_home_actions_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config = load_config(
                config_file="mkdocs.yml",
                site_dir=str(Path(tmp) / "site"),
            )
            build(config)
            homepage = (Path(tmp) / "site" / "index.html").read_text(
                encoding="utf-8"
            )

        parser = _HomepageParser()
        parser.feed(homepage)

        self.assertEqual(parser.home_action_links, 2)
        self.assertIn("stylesheets/extra.css", homepage)


if __name__ == "__main__":
    unittest.main()
