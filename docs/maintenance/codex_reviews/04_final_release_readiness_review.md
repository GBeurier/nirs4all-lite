# Codex Gate 4 — final release-readiness (nirs4all-lite)

Consolidated into the ecosystem-level **Gate 5**. Per-repo Codex effort was on **Gate 3** (no findings).

## ⛔ Release readiness: BLOCKED (governance hardened only)
`nirs4all-lite` was hardened for community-health/CI/governance, **not** for release. Per ecosystem Gate 0,
its release is blocked on external/admin items (see `release_checklist.md`):
- `nirs4all-lite → nirs4all-core` rename cutover incomplete (stale RTD slug / URLs).
- PyPI Trusted Publisher for `nirs4all-core` not created; crates.io/npm `nirs4all` names unowned.
- Every pinned upstream must be published at a compatible version — **`nirs4all-methods` ≥ 1.0.0 is on a
  publish-hold**, which paces the whole aggregate; `io` is mid-refactor.

Push-hardening is complete and CI-green; **do not tag/publish** until the blockers clear.
