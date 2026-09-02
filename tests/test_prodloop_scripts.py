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


def initialize(
    project: Path,
    state_dir: str | None = None,
    mode: str = "feature",
    context: str | None = None,
    interface_scope: str | None = None,
) -> subprocess.CompletedProcess[str]:
    args = [
        "--project-root", str(project),
        "--name", "Test Product",
        "--mode", mode,
        "--quality", "Q1",
        "--objective", "Verify portable delivery state",
    ]
    if state_dir:
        args.extend(["--state-dir", state_dir])
    if context:
        args.extend(["--context", context])
    if interface_scope:
        args.extend(["--interface-scope", interface_scope])
    return run_script("init_delivery_state.py", *args)


class ProdloopScriptTests(unittest.TestCase):
    def test_new_project_uses_neutral_state_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            result = initialize(project)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / ".prodloop" / "STATE.json").is_file())
            self.assertFalse((project / ".codex" / "delivery").exists())
            state = json.loads((project / ".prodloop" / "STATE.json").read_text())
            self.assertEqual(state["schema_version"], 3)
            self.assertEqual(state["project_context"], "brownfield")
            self.assertEqual(state["interface_scope"], "undetermined")
            self.assertTrue((project / ".prodloop" / "UI_CONTRACT.md").is_file())
            self.assertTrue((project / ".prodloop" / "UI_VERIFICATION.md").is_file())

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)
            payload = json.loads(validation.stdout)
            self.assertEqual(Path(payload["state_dir"]), (project / ".prodloop").resolve())

    def test_greenfield_context_does_not_create_takeover_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            result = initialize(project, mode="greenfield")
            self.assertEqual(result.returncode, 0, result.stderr)
            state = json.loads((project / ".prodloop" / "STATE.json").read_text())
            self.assertEqual(state["project_context"], "greenfield")
            self.assertFalse((project / ".prodloop" / "SYSTEM_MAP.md").exists())

    def test_brownfield_g1_requires_completed_takeover_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project).returncode, 0)
            delivery = project / ".prodloop"
            state_path = delivery / "STATE.json"
            state = json.loads(state_path.read_text())
            state["current_stage"] = "S2_PRODUCT_DEFINITION"
            state["gate_status"]["G0"] = "passed"
            state["gate_status"]["G1"] = "passed"
            state["interface_scope"] = "out-of-scope"
            state["next_action"] = "Define the product delta"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            incomplete = run_script("validate_state.py", "--project-root", str(project))
            self.assertNotEqual(incomplete.returncode, 0)
            payload = json.loads(incomplete.stdout)
            self.assertTrue(any("brownfield artifact is incomplete" in item for item in payload["errors"]))

            for artifact in delivery.glob("*.md"):
                content = artifact.read_text(encoding="utf-8")
                if "Status: pending" in content:
                    artifact.write_text(content.replace("Status: pending", "Status: complete"), encoding="utf-8")

            complete = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(complete.returncode, 0, complete.stdout + complete.stderr)

    def test_v1_state_remains_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project).returncode, 0)
            state_path = project / ".prodloop" / "STATE.json"
            state = json.loads(state_path.read_text())
            state["schema_version"] = 1
            state.pop("project_context")
            state_path.write_text(json.dumps(state), encoding="utf-8")

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_v2_state_remains_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project).returncode, 0)
            state_path = project / ".prodloop" / "STATE.json"
            state = json.loads(state_path.read_text())
            state["schema_version"] = 2
            state.pop("interface_scope")
            state_path.write_text(json.dumps(state), encoding="utf-8")

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_g0_requires_explicit_interface_scope_for_v3(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project, mode="greenfield").returncode, 0)
            state_path = project / ".prodloop" / "STATE.json"
            state = json.loads(state_path.read_text())
            state["current_stage"] = "S1_DISCOVERY"
            state["gate_status"]["G0"] = "passed"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("interface_scope is undetermined", validation.stdout)

            state["interface_scope"] = "out-of-scope"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_interface_gates_require_ui_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(
                initialize(project, mode="greenfield", interface_scope="in-scope").returncode,
                0,
            )
            delivery = project / ".prodloop"
            state_path = delivery / "STATE.json"
            state = json.loads(state_path.read_text())
            state["current_stage"] = "S4_DELIVERY_PLANNING"
            for index in range(4):
                state["gate_status"][f"G{index}"] = "passed"
            state_path.write_text(json.dumps(state), encoding="utf-8")

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("UI_CONTRACT.md is incomplete", validation.stdout)

            contract = delivery / "UI_CONTRACT.md"
            contract.write_text(contract.read_text().replace("Status: pending", "Status: complete"))
            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

            state["current_stage"] = "S7_RELEASE_READINESS"
            for index in range(7):
                state["gate_status"][f"G{index}"] = "passed"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("UI_VERIFICATION.md is incomplete", validation.stdout)

            report = delivery / "UI_VERIFICATION.md"
            report.write_text(report.read_text().replace("Status: pending", "Status: complete"))
            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

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
