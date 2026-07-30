import json
import tempfile
import unittest
from pathlib import Path


class RepoPathConfigurationTest(unittest.TestCase):
    def test_environment_root_places_every_repo_under_shared_parent(self) -> None:
        import sync_docs

        repos = sync_docs._resolve_repos(
            environ={"SIM_REPOS_ROOT": "repos"},
            config_path=Path("does-not-need-to-exist.json"),
        )

        self.assertEqual(
            {name: repo for name, (repo, _) in repos.items()},
            {name: Path("repos") / name for name in repos},
        )

    def test_local_config_supplies_explicit_repo_paths(self) -> None:
        import sync_docs

        configured_paths = {
            name: f"/srv/system-in-miniature/{name}"
            for name in sync_docs.PROJECT_EXTRAS
        }
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "repos.local.json"
            config_path.write_text(json.dumps(configured_paths), encoding="utf-8")
            repos = sync_docs._resolve_repos(environ={}, config_path=config_path)

        self.assertEqual(
            {name: repo for name, (repo, _) in repos.items()},
            {name: Path(path) for name, path in configured_paths.items()},
        )

    def test_missing_environment_and_local_config_reports_both_options(self) -> None:
        import sync_docs

        with tempfile.TemporaryDirectory() as tmp:
            missing_config = Path(tmp) / "repos.local.json"
            with self.assertRaisesRegex(
                RuntimeError,
                "SIM_REPOS_ROOT.*repos\\.local\\.json",
            ):
                sync_docs._resolve_repos(environ={}, config_path=missing_config)

    def test_local_config_requires_every_project(self) -> None:
        import sync_docs

        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "repos.local.json"
            config_path.write_text(
                json.dumps({"MiniKafka": "/srv/MiniKafka"}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(RuntimeError, "missing project paths"):
                sync_docs._resolve_repos(environ={}, config_path=config_path)


if __name__ == "__main__":
    unittest.main()
