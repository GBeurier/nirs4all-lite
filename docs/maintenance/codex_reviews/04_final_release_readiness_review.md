# Codex Gate 4 — final release-readiness (nirs4all-lite)

Consolidated into the ecosystem-level **Gate 5**. Per-repo Codex effort was on **Gate 3** (no findings).

## ⛔ Release readiness: BLOCKED (governance hardened only)
`nirs4all-lite` was hardened for community-health/CI/governance, **not** for release. This review is
historical and superseded by the lite-to-core cutover: `nirs4all-lite` is now a retired audit checkout,
and no final PyPI compatibility/alias release is planned.

Canonical release readiness now belongs to `nirs4all-core` and the ecosystem cockpit:
- PyPI Trusted Publisher, crates.io/npm name ownership, and upstream dependency availability are tracked
  against `nirs4all-core`.
- Existing historical `nirs4all-lite` artifacts should remain available, but this repository must not be
  tagged or published.

Push-hardening is complete and CI-green; **do not tag/publish** until the blockers clear.
