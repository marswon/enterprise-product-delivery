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
    visualization_scope: str | None = None,
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
    if visualization_scope:
        args.extend(["--visualization-scope", visualization_scope])
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
            self.assertEqual(state["schema_version"], 5)
            self.assertEqual(state["project_context"], "brownfield")
            self.assertEqual(state["interface_scope"], "undetermined")
            self.assertEqual(state["visualization_scope"], "undetermined")
            self.assertTrue((project / ".prodloop" / "UI_CONTRACT.md").is_file())
            self.assertTrue((project / ".prodloop" / "UI_VERIFICATION.md").is_file())
            self.assertTrue((project / ".prodloop" / "DATA_VIS_CONTRACT.md").is_file())
            self.assertTrue((project / ".prodloop" / "DATA_VIS_VERIFICATION.md").is_file())
            self.assertEqual(state["context_checkpoint_count"], 0)
            self.assertIsNone(state["last_context_checkpoint_at"])
            self.assertEqual(state["material_actions_since_checkpoint"], 0)
            self.assertFalse(state["context_checkpoint_due"])
            self.assertEqual(state["context_checkpoint_reasons"], [])
            self.assertTrue((project / ".prodloop" / "CONTEXT.md").is_file())
            self.assertTrue((project / ".prodloop" / "CONTEXT_HISTORY.md").is_file())
            self.assertTrue((project / ".prodloop" / "MEMORY_CANDIDATES.md").is_file())
            self.assertIn("soft_limit_k: 120", (project / ".prodloop" / "DELIVERY_MANIFEST.yaml").read_text())

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
            state["visualization_scope"] = "out-of-scope"
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
            state.pop("interface_scope")
            state.pop("visualization_scope")
            state.pop("context_checkpoint_count")
            state.pop("last_context_checkpoint_at")
            state.pop("material_actions_since_checkpoint")
            state.pop("context_checkpoint_due")
            state.pop("context_checkpoint_reasons")
            state_path.write_text(json.dumps(state), encoding="utf-8")
            for filename in [
                "UI_CONTRACT.md",
                "UI_VERIFICATION.md",
                "DATA_VIS_CONTRACT.md",
                "DATA_VIS_VERIFICATION.md",
                "CONTEXT.md",
                "CONTEXT_HISTORY.md",
                "MEMORY_CANDIDATES.md",
            ]:
                (project / ".prodloop" / filename).unlink()

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
            state.pop("visualization_scope")
            state.pop("context_checkpoint_count")
            state.pop("last_context_checkpoint_at")
            state.pop("material_actions_since_checkpoint")
            state.pop("context_checkpoint_due")
            state.pop("context_checkpoint_reasons")
            state_path.write_text(json.dumps(state), encoding="utf-8")
            for filename in [
                "UI_CONTRACT.md",
                "UI_VERIFICATION.md",
                "DATA_VIS_CONTRACT.md",
                "DATA_VIS_VERIFICATION.md",
                "CONTEXT.md",
                "CONTEXT_HISTORY.md",
                "MEMORY_CANDIDATES.md",
            ]:
                (project / ".prodloop" / filename).unlink()

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_v3_state_without_visualization_fields_remains_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project).returncode, 0)
            delivery = project / ".prodloop"
            state_path = delivery / "STATE.json"
            state = json.loads(state_path.read_text())
            state["schema_version"] = 3
            state.pop("visualization_scope")
            state.pop("context_checkpoint_count")
            state.pop("last_context_checkpoint_at")
            state.pop("material_actions_since_checkpoint")
            state.pop("context_checkpoint_due")
            state.pop("context_checkpoint_reasons")
            state_path.write_text(json.dumps(state), encoding="utf-8")
            (delivery / "DATA_VIS_CONTRACT.md").unlink()
            (delivery / "DATA_VIS_VERIFICATION.md").unlink()
            (delivery / "CONTEXT.md").unlink()
            (delivery / "CONTEXT_HISTORY.md").unlink()
            (delivery / "MEMORY_CANDIDATES.md").unlink()

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_v4_state_without_context_management_remains_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project).returncode, 0)
            delivery = project / ".prodloop"
            state_path = delivery / "STATE.json"
            state = json.loads(state_path.read_text())
            state["schema_version"] = 4
            state.pop("context_checkpoint_count")
            state.pop("last_context_checkpoint_at")
            state.pop("material_actions_since_checkpoint")
            state.pop("context_checkpoint_due")
            state.pop("context_checkpoint_reasons")
            state_path.write_text(json.dumps(state), encoding="utf-8")
            (delivery / "CONTEXT.md").unlink()
            (delivery / "CONTEXT_HISTORY.md").unlink()
            (delivery / "MEMORY_CANDIDATES.md").unlink()

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_legacy_state_can_enable_ui_gates_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project).returncode, 0)
            delivery = project / ".prodloop"
            state_path = delivery / "STATE.json"
            state = json.loads(state_path.read_text())
            state["schema_version"] = 2
            state.pop("interface_scope")
            state_path.write_text(json.dumps(state), encoding="utf-8")
            (delivery / "UI_CONTRACT.md").unlink()
            (delivery / "UI_VERIFICATION.md").unlink()
            manifest_path = delivery / "DELIVERY_MANIFEST.yaml"
            manifest = manifest_path.read_text()
            before_experience, after_experience = manifest.split("experience:\n", 1)
            _, after_autonomy = after_experience.split("autonomy:\n", 1)
            manifest_path.write_text(before_experience + "autonomy:\n" + after_autonomy)

            enabled = run_script(
                "enable_ui_delivery.py",
                "--project-root", str(project),
                "--interface-scope", "in-scope",
            )
            self.assertEqual(enabled.returncode, 0, enabled.stdout + enabled.stderr)
            upgraded = json.loads(state_path.read_text())
            self.assertEqual(upgraded["schema_version"], 2)
            self.assertEqual(upgraded["interface_scope"], "in-scope")
            self.assertTrue((delivery / "STATE.before-ui-enable.json").is_file())
            self.assertTrue((delivery / "DELIVERY_MANIFEST.before-ui-enable.yaml").is_file())
            self.assertIn('interface_scope: "in-scope"', manifest_path.read_text())
            contract = delivery / "UI_CONTRACT.md"
            self.assertIn("## Information Architecture", contract.read_text())

            contract.write_text(contract.read_text() + "\nPreserve this content.\n")
            enabled_again = run_script(
                "enable_ui_delivery.py",
                "--project-root", str(project),
                "--interface-scope", "in-scope",
            )
            self.assertEqual(enabled_again.returncode, 0, enabled_again.stdout + enabled_again.stderr)
            self.assertIn("Preserve this content.", contract.read_text())

    def test_g0_requires_explicit_interface_and_visualization_scope_for_v5(self) -> None:
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
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("visualization_scope is undetermined", validation.stdout)

            state["visualization_scope"] = "out-of-scope"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_interface_gates_require_ui_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(
                initialize(
                    project,
                    mode="greenfield",
                    interface_scope="in-scope",
                    visualization_scope="out-of-scope",
                ).returncode,
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

    def test_visualization_gates_require_contract_and_verification(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(
                initialize(
                    project,
                    mode="greenfield",
                    interface_scope="in-scope",
                    visualization_scope="in-scope",
                ).returncode,
                0,
            )
            delivery = project / ".prodloop"
            state_path = delivery / "STATE.json"
            state = json.loads(state_path.read_text())
            state["current_stage"] = "S4_DELIVERY_PLANNING"
            for index in range(4):
                state["gate_status"][f"G{index}"] = "passed"
            (delivery / "UI_CONTRACT.md").write_text(
                (delivery / "UI_CONTRACT.md").read_text().replace("Status: pending", "Status: complete")
            )
            state_path.write_text(json.dumps(state), encoding="utf-8")

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("DATA_VIS_CONTRACT.md is incomplete", validation.stdout)

            contract = delivery / "DATA_VIS_CONTRACT.md"
            contract.write_text(contract.read_text().replace("Status: pending", "Status: complete"))
            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

            state["current_stage"] = "S7_RELEASE_READINESS"
            for index in range(7):
                state["gate_status"][f"G{index}"] = "passed"
            state_path.write_text(json.dumps(state), encoding="utf-8")
            (delivery / "UI_VERIFICATION.md").write_text(
                (delivery / "UI_VERIFICATION.md").read_text().replace("Status: pending", "Status: complete")
            )
            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("DATA_VIS_VERIFICATION.md is incomplete", validation.stdout)

            report = delivery / "DATA_VIS_VERIFICATION.md"
            report.write_text(report.read_text().replace("Status: pending", "Status: complete"))
            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertEqual(validation.returncode, 0, validation.stdout + validation.stderr)

    def test_legacy_state_can_enable_visualization_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(
                initialize(
                    project,
                    mode="greenfield",
                    interface_scope="out-of-scope",
                    visualization_scope="out-of-scope",
                ).returncode,
                0,
            )
            delivery = project / ".prodloop"
            state_path = delivery / "STATE.json"
            state = json.loads(state_path.read_text())
            state["schema_version"] = 3
            state.pop("visualization_scope")
            state_path.write_text(json.dumps(state), encoding="utf-8")
            (delivery / "DATA_VIS_CONTRACT.md").unlink()
            (delivery / "DATA_VIS_VERIFICATION.md").unlink()

            enabled = run_script(
                "enable_data_visualization.py",
                "--project-root", str(project),
                "--visualization-scope", "in-scope",
            )
            self.assertEqual(enabled.returncode, 0, enabled.stdout + enabled.stderr)
            upgraded = json.loads(state_path.read_text())
            self.assertEqual(upgraded["schema_version"], 3)
            self.assertEqual(upgraded["visualization_scope"], "in-scope")
            self.assertTrue((delivery / "STATE.before-data-vis-enable.json").is_file())
            self.assertTrue((delivery / "DELIVERY_MANIFEST.before-data-vis-enable.yaml").is_file())
            self.assertIn('visualization_scope: "in-scope"', (delivery / "DELIVERY_MANIFEST.yaml").read_text())

            contract = delivery / "DATA_VIS_CONTRACT.md"
            contract.write_text(contract.read_text() + "\nPreserve this content.\n")
            enabled_again = run_script(
                "enable_data_visualization.py",
                "--project-root", str(project),
                "--visualization-scope", "in-scope",
            )
            self.assertEqual(enabled_again.returncode, 0, enabled_again.stdout + enabled_again.stderr)
            self.assertIn("Preserve this content.", contract.read_text())

    def test_legacy_state_can_enable_context_management_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project, mode="greenfield").returncode, 0)
            delivery = project / ".prodloop"
            state_path = delivery / "STATE.json"
            state = json.loads(state_path.read_text())
            state["schema_version"] = 4
            state.pop("context_checkpoint_count")
            state.pop("last_context_checkpoint_at")
            state.pop("material_actions_since_checkpoint")
            state.pop("context_checkpoint_due")
            state.pop("context_checkpoint_reasons")
            state_path.write_text(json.dumps(state), encoding="utf-8")
            for filename in ["CONTEXT.md", "CONTEXT_HISTORY.md", "MEMORY_CANDIDATES.md"]:
                (delivery / filename).unlink()
            manifest_path = delivery / "DELIVERY_MANIFEST.yaml"
            before, after = manifest_path.read_text().split("context_management:\n", 1)
            _, suffix = after.split("required_gates:", 1)
            manifest_path.write_text(before + "required_gates:" + suffix)

            enabled = run_script("enable_context_management.py", "--project-root", str(project))
            self.assertEqual(enabled.returncode, 0, enabled.stdout + enabled.stderr)
            upgraded = json.loads(state_path.read_text())
            self.assertEqual(upgraded["schema_version"], 4)
            self.assertEqual(upgraded["context_checkpoint_count"], 0)
            self.assertEqual(upgraded["material_actions_since_checkpoint"], 0)
            self.assertFalse(upgraded["context_checkpoint_due"])
            self.assertTrue((delivery / "STATE.before-context-enable.json").is_file())
            self.assertTrue((delivery / "DELIVERY_MANIFEST.before-context-enable.yaml").is_file())
            self.assertIn("context_management:", manifest_path.read_text())
            premature = run_script(
                "checkpoint_context.py",
                "--project-root", str(project),
                "--reason", "manual",
            )
            self.assertNotEqual(premature.returncode, 0)
            self.assertIn("empty or unresolved", premature.stderr)
            context_file = delivery / "CONTEXT.md"
            context_file.write_text(context_file.read_text() + "\nPreserve this content.\n")

            enabled_again = run_script("enable_context_management.py", "--project-root", str(project))
            self.assertEqual(enabled_again.returncode, 0, enabled_again.stdout + enabled_again.stderr)
            self.assertIn("Preserve this content.", context_file.read_text())

    def test_context_checkpoint_records_bounded_resume_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project, mode="greenfield").returncode, 0)
            delivery = project / ".prodloop"

            checkpoint = run_script(
                "checkpoint_context.py",
                "--project-root", str(project),
                "--reason", "manual",
                "--revision", "abc1234",
            )
            self.assertEqual(checkpoint.returncode, 0, checkpoint.stdout + checkpoint.stderr)
            payload = json.loads(checkpoint.stdout)
            self.assertEqual(payload["checkpoint"], "CP-0001")
            state = json.loads((delivery / "STATE.json").read_text())
            self.assertEqual(state["context_checkpoint_count"], 1)
            self.assertIsNotNone(state["last_context_checkpoint_at"])
            self.assertIn("abc1234", (delivery / "CONTEXT_HISTORY.md").read_text())

            context_file = delivery / "CONTEXT.md"
            context_file.write_text(context_file.read_text().replace(
                state["next_action"],
                "A different action",
            ))
            rejected = run_script(
                "checkpoint_context.py",
                "--project-root", str(project),
                "--reason", "manual",
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("next_action verbatim", rejected.stderr)

    def test_context_budget_tracks_actions_and_reported_usage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project, mode="greenfield").returncode, 0)
            delivery = project / ".prodloop"

            for _ in range(7):
                tracked = run_script("track_context_budget.py", "--project-root", str(project))
                self.assertEqual(tracked.returncode, 0, tracked.stdout + tracked.stderr)
                self.assertFalse(json.loads(tracked.stdout)["checkpoint_due"])
            tracked = run_script("track_context_budget.py", "--project-root", str(project))
            payload = json.loads(tracked.stdout)
            self.assertTrue(payload["checkpoint_due"])
            self.assertIn("action-interval", payload["reasons"])

            checkpoint = run_script(
                "checkpoint_context.py",
                "--project-root", str(project),
                "--reason", "action-interval",
            )
            self.assertEqual(checkpoint.returncode, 0, checkpoint.stdout + checkpoint.stderr)
            state = json.loads((delivery / "STATE.json").read_text())
            self.assertEqual(state["material_actions_since_checkpoint"], 0)
            self.assertFalse(state["context_checkpoint_due"])

            tracked = run_script(
                "track_context_budget.py",
                "--project-root", str(project),
                "--reported-context-k", "96",
            )
            payload = json.loads(tracked.stdout)
            self.assertTrue(payload["checkpoint_due"])
            self.assertIn("soft-limit", payload["reasons"])

    def test_v5_requires_context_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(initialize(project).returncode, 0)
            delivery = project / ".prodloop"
            context_path = delivery / "CONTEXT.md"
            context_content = context_path.read_text()
            context_path.unlink()

            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("Missing CONTEXT.md", validation.stdout)

            context_path.write_text(context_content)
            manifest_path = delivery / "DELIVERY_MANIFEST.yaml"
            before, after = manifest_path.read_text().split("context_management:\n", 1)
            _, suffix = after.split("required_gates:", 1)
            manifest_path.write_text(before + "required_gates:" + suffix)
            validation = run_script("validate_state.py", "--project-root", str(project))
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn("Missing context_management configuration", validation.stdout)

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
