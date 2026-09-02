from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "skills" / "prodloop" / "scripts"


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def initialize(project: Path, state_dir: str | None = None) -> subprocess.CompletedProcess[str]:
    args = [
        "--project-root", str(project),
        "--name", "Test Product",
        "--mode", "feature",
        "--quality", "Q1",
        "--objective", "Verify portable delivery state",
    ]
    if state_dir:
        args.extend(["--state-dir", state_dir])
    return run_script("init_delivery_state.py", *args)


class ProdloopScriptTests(unittest.TestCase):
    def test_new_project_uses_neutral_state_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            result = initialize(project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / ".prodloop" / "STATE.json").is_file())
            self.assertFalse((project / ".codex" / "delivery").exists())

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            payload = json.loads(validation.stdout)
            self.assertEqual(Path(payload["state_dir"]), (project / ".prodloop").resolve())

    def test_legacy_state_is_auto_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            initialized = initialize(project, ".codex/delivery")
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            payload = json.loads(validation.stdout)
            self.assertEqual(Path(payload["state_dir"]), (project / ".codex" / "delivery").resolve())

    def test_conflicting_standard_state_directories_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project).returncode, 0)
            (project / ".codex" / "delivery").mkdir(parents=True)

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertNotEqual(validation.returncode, 0)
            payload = json.loads(validation.stdout)
            self.assertIn("Multiple delivery state directories", payload["errors"][0])

            traceability = run_script("check_traceability.py", "--project-root", str(project))
            self.assertNotEqual(traceability.returncode, 0)
            payload = json.loads(traceability.stdout)
            self.assertIn("Multiple delivery state directories", payload["errors"][0])

    def test_init_refuses_existing_legacy_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project, ".codex/delivery").returncode, 0)
            second = initialize(project)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("Delivery state already exists", second.stderr)

    def test_state_directory_cannot_escape_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "project"
            project.mkdir()
            result = initialize(project, "../outside")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must be inside project root", result.stderr)


if __name__ == "__main__":
    unittest.main()
