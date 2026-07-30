import importlib
import os
import unittest
from pathlib import Path


class RepoPathConfigurationTest(unittest.TestCase):
    def tearDown(self) -> None:
        os.environ.pop("SIM_REPOS_ROOT", None)

    def test_environment_root_places_every_repo_under_shared_parent(self) -> None:
        os.environ["SIM_REPOS_ROOT"] = "repos"

        import sync_docs

        module = importlib.reload(sync_docs)

        self.assertEqual(
            {name: repo for name, (repo, _) in module.REPOS.items()},
            {name: Path("repos") / name for name in module.REPOS},
        )

    def test_missing_environment_root_preserves_local_absolute_paths(self) -> None:
        os.environ.pop("SIM_REPOS_ROOT", None)

        import sync_docs

        module = importlib.reload(sync_docs)

        self.assertEqual(module.REPOS["MiniKafka"][0], Path("~/MiniKafka"))
        self.assertEqual(
            module.REPOS["MiniRedis"][0],
            Path("~/MiniRedis-workspace/MiniRedis"),
        )


if __name__ == "__main__":
    unittest.main()
