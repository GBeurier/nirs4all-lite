# Final hardening report — nirs4all-lite

**Date:** 2026-07-04 · **Branch:** `main` · **Operator:** Claude (Opus 4.8) · **Reviewer:** Codex CLI 0.142.5

## Summary
Governance/CI hardening of the portable Rust aggregate (re-exports the ecosystem cores across bindings):
added the community-health set and SHA-pinned every third-party action across all 8 workflows.
**No code/re-export/release changes.** **Release stays BLOCKED** (see `release_checklist.md` / Codex Gate 4).

## Baseline / commit
- **Baseline HEAD:** `ba959a1` (origin/main, CI-green).
- **Commit:** *(this commit)* — community-health + 55 SHA-pins + docs/maintenance.

## Files
Added: `CODE_OF_CONDUCT.md`, `CITATION.cff`, `SECURITY.md`, `CONTRIBUTING.md`, `.editorconfig`,
`.pre-commit-config.yaml`, `.github/dependabot.yml` (github-actions + cargo + pip + npm),
`docs/maintenance/{repository_audit,quality_gates,release_checklist,final_report}.md` + `codex_reviews/{03,04}`.
Modified: all 8 `.github/workflows/*.yml` (55 SHA-pins, at current majors v6/v7). CHANGELOG already current (`[Unreleased]`).

## Checks
- YAML/CFF validated. Non-code change; Rust build/tests + surface gates run in CI (authoritative). Baseline CI green at `ba959a1`.
- **Codex Gate 3** — no findings; pins verified to resolve to advertised tags.
- **Codex Gate 4** — release BLOCKED (documented); consolidated into ecosystem Gate 5.

## GitHub Actions (this push)
Branch-push gating runs (no publish): `ci` (Rust + surface gates), `version-guard`. Verified green post-push.

## Residual risks
- **RELEASE BLOCKED** — nirs4all-core rename, PyPI Trusted Publisher, crates/npm names, held `methods` (see checklist).
- `rust-toolchain@stable` intentionally unpinned.

## 12-month maintenance
- Merge weekly Dependabot PRs after CI-green. Keep `CHANGELOG.md` `[Unreleased]` current.
- **Before any release:** clear the Gate-0 blockers in `release_checklist.md`.
