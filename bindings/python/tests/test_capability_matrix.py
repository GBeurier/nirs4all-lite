"""Honesty gate for the per-language capability ledger.

``compat/capabilities.toml`` declares, per language binding, the capability level
of the portable operator subset using the vocabulary defined in
``docs/OPERATORS.md``. This test makes those claims non-fictional:

* the capability vocabulary is sourced from ``docs/OPERATORS.md`` (no parallel
  taxonomy is invented here);
* the declared portable operator subset equals ``PORTABLE_OPERATOR_CLASSES``;
* every binding that claims ``execute-local`` or better exposes a real run
  symbol in its source, and every binding that claims ``parity-validated`` has a
  real parity gate on disk;
* the aggregate only claims ``metadata`` over the lazily re-exported upstream
  domains, matching the actual (delegating) implementation.

Because it reads binding sources directly, the gate runs in the required Python
suite without R, Node, Octave, or a Rust toolchain.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

import nirs4all_lite as n4lite

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - local Python < 3.11 fallback
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[3]
CAPABILITIES = ROOT / "compat/capabilities.toml"
OPERATORS_DOC = ROOT / "docs/OPERATORS.md"

EXPECTED_LANGUAGES = {"python", "rust", "wasm", "r", "matlab"}
# Levels from docs/OPERATORS.md that require a real, callable run symbol.
EXECUTABLE_LEVELS = {"execute-local", "execute-remote", "parity-validated"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _ladder_from_operators_doc() -> set[str]:
    """The capability vocabulary, parsed from the OPERATORS.md ladder list."""

    section = re.search(
        r"## Capability Levels\n(.*?)\n## ", _read(OPERATORS_DOC), re.DOTALL
    )
    if section is None:
        raise AssertionError("could not locate the Capability Levels section")
    return set(re.findall(r"(?m)^-\s+`([a-z-]+)`:", section.group(1)))


def _load_capabilities() -> dict:
    return tomllib.loads(_read(CAPABILITIES))


class CapabilityVocabularyTests(unittest.TestCase):
    def test_ladder_matches_operators_doc(self) -> None:
        ladder = _ladder_from_operators_doc()
        self.assertEqual(
            ladder,
            {"metadata", "plan", "execute-local", "execute-remote", "parity-validated"},
        )
        self.assertTrue(EXECUTABLE_LEVELS <= ladder)

    def test_every_declared_level_is_in_the_ladder(self) -> None:
        ladder = _ladder_from_operators_doc()
        caps = _load_capabilities()

        self.assertIn(caps["portable_pipeline"]["level"], ladder)
        self.assertIn(caps["upstream_domains"]["level"], ladder)
        for binding in caps["binding"]:
            with self.subTest(language=binding["language"]):
                self.assertIn(binding["level"], ladder)


class PortableSubsetLedgerTests(unittest.TestCase):
    def test_declared_subset_equals_python_portable_operator_classes(self) -> None:
        caps = _load_capabilities()
        self.assertEqual(
            sorted(caps["portable_operator_subset"]),
            sorted(n4lite.PORTABLE_OPERATOR_CLASSES),
        )

    def test_portable_pipeline_delegates_to_a_registered_upstream(self) -> None:
        caps = _load_capabilities()
        pipeline = caps["portable_pipeline"]

        self.assertEqual(pipeline["upstream"], "methods")
        self.assertIn(pipeline["upstream"], n4lite.upstreams)
        self.assertTrue((ROOT / pipeline["oracle"]).exists())


class BindingCapabilityHonestyTests(unittest.TestCase):
    def test_all_five_languages_are_declared_once(self) -> None:
        caps = _load_capabilities()
        languages = [binding["language"] for binding in caps["binding"]]

        self.assertEqual(len(languages), len(set(languages)), "duplicate language row")
        self.assertEqual(set(languages), EXPECTED_LANGUAGES)

    def test_run_symbol_exists_in_source_for_executable_claims(self) -> None:
        caps = _load_capabilities()
        for binding in caps["binding"]:
            with self.subTest(language=binding["language"]):
                self.assertIn(binding["level"], EXECUTABLE_LEVELS)
                source = ROOT / binding["run_source"]
                self.assertTrue(source.exists(), source)
                self.assertIn(binding["run_symbol"], _read(source))

    def test_parity_validated_claims_have_a_real_parity_gate(self) -> None:
        caps = _load_capabilities()
        for binding in caps["binding"]:
            if binding["level"] != "parity-validated":
                continue
            with self.subTest(language=binding["language"]):
                gate = ROOT / binding["parity_gate"]
                self.assertTrue(gate.exists(), gate)
                parity_symbol = binding.get("parity_symbol")
                if parity_symbol is not None:
                    self.assertIn(parity_symbol, _read(gate))


class UpstreamDomainHonestyTests(unittest.TestCase):
    def test_upstream_domains_only_claim_metadata(self) -> None:
        caps = _load_capabilities()
        domains = caps["upstream_domains"]

        # The aggregate re-exports these lazily and does not execute them itself.
        self.assertEqual(domains["level"], "metadata")

    def test_upstream_domain_keys_are_registered_and_exclude_methods(self) -> None:
        caps = _load_capabilities()
        keys = set(caps["upstream_domains"]["keys"])

        self.assertTrue(keys <= set(n4lite.upstreams))
        # `methods` is the executed upstream, not a metadata-only domain.
        self.assertNotIn("methods", keys)
        self.assertEqual(keys | {"methods"}, set(n4lite.upstreams))


if __name__ == "__main__":
    unittest.main()
