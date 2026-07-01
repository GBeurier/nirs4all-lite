import json
import unittest
from pathlib import Path

import nirs4all_core
import nirs4all_lite as n4lite

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - local Python < 3.11 fallback
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[3]


class ReleaseTopologyManifestTests(unittest.TestCase):
    def test_manifest_is_json_serializable_and_names_current_distribution(self) -> None:
        manifest = n4lite.release_topology_manifest()

        json.dumps(manifest)
        self.assertEqual(manifest["schema"], "nirs4all-lite.release-topology.v1")
        self.assertEqual(manifest["python"]["distribution"], "nirs4all-lite")
        self.assertEqual(manifest["python"]["canonical_import"], "nirs4all_lite")
        self.assertEqual(manifest["python"]["target_distribution"], "nirs4all-core")
        self.assertEqual(
            manifest["python"]["target_distribution_status"],
            "release-gated",
        )
        self.assertIn("n4a", manifest["python"]["additive_imports"])
        self.assertIn("nirs4all_core", manifest["python"]["additive_imports"])
        self.assertIn("nirs4all", manifest["python"]["reserved_non_imports"])

    def test_manifest_keeps_core_out_of_execution_engine_role(self) -> None:
        manifest = n4lite.release_topology_manifest()
        contract = manifest["core_contract"]

        self.assertEqual(contract["import"], "nirs4all_core")
        self.assertFalse(contract["execution_engine"])
        self.assertEqual(
            contract["allowed_roles"],
            ["inspect", "validate", "capability", "facade"],
        )
        self.assertEqual(contract["public_exports"], list(n4lite.core_facade_exports()))
        self.assertEqual(contract["topology_exports"], list(n4lite.TOPOLOGY_EXPORTS))
        self.assertEqual(
            contract["excluded_execution_exports"],
            list(n4lite.execution_engine_exports()),
        )
        self.assertEqual(
            n4lite.validate_core_facade(nirs4all_core),
            {"missing_core_exports": (), "unexpected_execution_exports": ()},
        )

    def test_pyproject_matches_python_release_topology(self) -> None:
        pyproject = tomllib.loads(
            (ROOT / "bindings/python/pyproject.toml").read_text()
        )
        manifest = n4lite.release_topology_manifest()

        self.assertEqual(
            pyproject["project"]["name"],
            manifest["python"]["distribution"],
        )
        self.assertNotEqual(pyproject["project"]["name"], "nirs4all-core")
        self.assertNotIn("nirs4all-core", pyproject["project"].get("dependencies", []))

        packages = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
        self.assertEqual(
            set(packages),
            {"src/nirs4all_lite", "src/n4a", "src/nirs4all_core"},
        )
        self.assertNotIn("src/nirs4all", packages)

    def test_install_distributions_remain_explicit(self) -> None:
        manifest = n4lite.release_topology_manifest()
        distributions = {
            item["name"]: item for item in manifest["install_distributions"]
        }

        self.assertEqual(distributions["nirs4all-lite"]["status"], "current")
        self.assertEqual(distributions["nirs4all-core"]["status"], "release-gated")
        self.assertEqual(
            distributions["nirs4all-methods"]["status"],
            "upstream-explicit",
        )
        self.assertEqual(distributions["nirs4all"]["status"], "current")
        self.assertEqual(distributions["nirs4all-datasets"]["status"], "external-optional")


if __name__ == "__main__":
    unittest.main()
