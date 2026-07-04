# Codex Gate 3 — main diff review (nirs4all-lite)

**Reviewer:** Codex CLI 0.142.5 — `codex exec review --uncommitted`, 2026-07-04 (background).

## Verdict
> "I did not find any discrete issues in the staged, unstaged, or untracked changes that would break
> existing behavior or CI. The workflow SHA pins resolve to the advertised action tags, and the added
> governance/maintenance files are syntactically valid."

No findings.

## Verified
- 55 action pins across 8 workflows at their **current majors** (`checkout@v6`, `setup-python@v6`,
  `upload-artifact@v7`, …); only `dtolnay/rust-toolchain@stable` left (floating by design).
- `publish-pypi` is gated to production `vX.Y.Z` tags only (`!contains('-')`, not `workflow_dispatch`) —
  a branch push never publishes. Gate 4 consolidated into ecosystem Gate 5.

## CI-runtime regression caught after push (Codex reviews diffs statically; it cannot run CI)
The first push (`d6cd151`) failed the `CI` job: `bindings/python/tests/test_release_topology.py`
identifies checkout steps by the exact string `uses == "actions/checkout@v4"`. SHA-pinning changed the
YAML-parsed `uses` value to the pinned SHA (the `# v4` is a comment), so the test found **0** checkout
steps for `nirs4all-methods` — a **false negative**; the release topology (methods IS vendored) is
unchanged. **Fix:** made the matcher pin-aware (`startswith("actions/checkout@")`), preserving the
"exactly one checkout of the sibling" contract while ignoring the incidental action version.
Re-ran `python -m unittest discover -s bindings/python/tests` locally: **54 tests OK**.
