# Release checklist — nirs4all-lite

> ⛔ **RELEASE IS BLOCKED — do not tag/publish yet.** (Ecosystem Gate 0 blocker.) This repo was hardened
> for governance/CI only; the items below must be cleared by a maintainer/admin before any release.

## Release blockers (external / admin)

- [ ] **`nirs4all-lite → nirs4all-core` rename cutover** completed (stale `nirs4all-lite.readthedocs.io`
      slug + pyproject/Cargo URLs still point at the old name).
- [ ] **PyPI Trusted Publisher for `nirs4all-core`** created (does not exist yet).
- [ ] **crates.io `nirs4all` + npm `nirs4all`** names owned/claimed; `@nirs4all` npm org secured.
- [ ] Every pinned upstream is **published at a compatible version**: `dag-ml` 0.2.0, `dag-ml-data` 0.2.0
      (crates.io), and `nirs4all-formats` / `nirs4all-io` / `nirs4all-datasets` / **`nirs4all-methods` ≥ 1.0.0**
      — `methods` is on a publish-hold, which paces this whole aggregate.

## Once unblocked (normal release)

- [ ] Green gate + CI green (see `quality_gates.md`); cross-binding versions in sync.
- [ ] `CHANGELOG.md` `[Unreleased]` → dated version.
- [ ] Dry-run each registry via `workflow_dispatch`; then tag `vX.Y.Z` on the exact release commit.
- [ ] Multi-registry immutable fan-out — on a partial failure, re-run the failed job, do not re-tag.
