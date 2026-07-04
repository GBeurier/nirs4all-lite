# Repository audit — nirs4all-lite

> Generated from the automated pre-release audit (workflow wf_1fc87351-29f); the **Deepest hardening roadmap** section records the fullest realistic hardening even where the pragmatic pass does not implement it. Reviewed at Codex Gate 1.

- **Mode:** IN SCOPE — pragmatic hardening + push
- **Baseline HEAD:** `ba959a1`
- **Role:** Portable aggregate distribution: a thin re-export/portability layer (Rust workspace + Python/R/MATLAB-Octave/JS-WASM bindings) over the nirs4all ecosystem (dag-ml, dag-ml-data, nirs4all-formats, nirs4all-io, nirs4all-datasets, nirs4all-methods). Adds no parsers, estimators, kernels, or DAG logic of its own.
- **Stack:** Rust 2021 workspace (single crate bindings/rust/nirs4all, libloading shim, deps dag-ml 0.2.2 / dag-ml-data 0.2.3 + serde_json/serde_yaml). Python 3.11+ pure-python wheel (hatchling backend, dist name nirs4all-core, import roots nirs4all_lite + n4a + nirs4all_core, dep PyYAML>=6, optional extras for each upstream). JS/WASM pure-ESM (node 22, TypeScript 5.9 typecheck, yaml dep, upstream *-wasm optional peer deps). R pure-R binding (NeedsCompilation: no). MATLAB/Octave source facade. Build orchestration via Makefile; docs via Sphinx/MyST on Read the Docs. Versions all at 0.2.4, single-source-of-truth = Rust crate version propagated by scripts/bump_version.sh.

## Release-readiness verdict
nirs4all-core (legacy nirs4all-lite alias line) is a mature, well-instrumented aggregate distribution: CI is green across Rust/Python/npm/R/Octave plus a strict cross-language numerical-parity job against a full-Python oracle, and all six tag-triggered release workflows are already hardened (OIDC/Trusted Publishing for PyPI, npm provenance, CycloneDX SBOM + keyless Sigstore attestation + SHA256SUMS, least-privilege permissions, dry-run gates, and a version-guard that forbids un-tagged version bumps on main). The dominant release blockers are external/administrative rather than code: the PyPI Trusted Publisher for nirs4all-core does not yet exist, the final nirs4all-lite alias release must still be cut, the crates.io/npm 'nirs4all' names must be owned, and every pinned upstream (dag-ml, dag-ml-data, formats, io, methods, datasets) must already be published at its exact version or both install and publish fail. Governance hygiene is the main low-risk gap: SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, CITATION.cff, dependabot, editorconfig, pre-commit, and issue/PR templates are all absent, and ci.yml alone lacks a least-privilege permissions block and runs a heavy parity job on every push. No secrets or real vulnerabilities were found. Push safety is strong for main (no publish on branch push) but sharp for tags: a single v*.*.* tag fans out to six immutable-registry publishers, so tag pushes must go through the dry-run path first.

## Gate commands (detected)
| key | value |
|---|---|
| `install` | npm ci --prefix bindings/wasm  (no unified installer; per-binding: cargo fetch for Rust, pip install -e bindings/python for Python, npm ci for wasm) |
| `test` | make test |
| `lint` | cargo clippy --workspace --all-targets -- -D warnings |
| `typecheck` | npm run typecheck --prefix bindings/wasm  (tsc --project bindings/wasm/tsconfig.typecheck.json; no Python mypy configured) |
| `format` | cargo fmt --all --check |
| `docs_build` | sphinx-build -b html docs docs/_build/html  (RTD uses docs/conf.py per .readthedocs.yaml; no in-repo make target) |
| `package_build` | make build  (build-python + build-npm + build-r + build-matlab + package-rust; cargo package -p nirs4all for the crate alone) |

## CI
- **Latest status:** All green. gh run list --limit 8 shows CI and version-guard all [ok] on main; no failing runs to triage.
- **Workflows:**
- ci.yml (on: push + pull_request, NO branch filter, NO top-level permissions; jobs: rust, python matrix 3.11/3.12, npm, strict-parity [checks out GBeurier/nirs4all-methods @ pinned SHA + emscripten + octave + R], r, matlab-octave)
- version-guard.yml (push+PR on main and rc/**; permissions: contents:read; blocks in-repo version being AHEAD of latest git tag)
- release-source.yml (tag v*.*.* + dispatch; git-archive tarball/zip + CycloneDX SBOM via syft + SHA256SUMS + keyless Sigstore attestation)
- release-python.yml (tag v*.*.* + dispatch; pure-python wheel+sdist, PyPI OIDC Trusted Publishing via 'pypi' environment, non-prerelease only)
- release-npm.yml (tag v*.*.* + dispatch; strict-wasm-parity gate then npm publish with provenance, NPM_TOKEN secret)
- release-crates.yml (tag v*.*.* + dispatch; cargo publish -p nirs4all, CARGO_REGISTRY_TOKEN secret)
- release-r.yml (tag v*.*.* + dispatch)
- release-matlab.yml (tag v*.*.* + dispatch)
- **Gaps:**
- ci.yml has no top-level permissions: block (relies on repo default GITHUB_TOKEN scope) while every release workflow correctly sets least-privilege
- ci.yml triggers on every push to every branch with no path/branch filter; the heavy strict-parity job (emscripten SDK build + octave + R + external nirs4all-methods checkout) runs unconditionally on each push/PR
- No coverage measurement or threshold enforced in CI (coverage.xml exists locally but is gitignored and unused by CI)
- No docs build job in CI; Sphinx/RTD build is only exercised by Read the Docs, so doc breakage is invisible until an RTD build
- No CodeQL / dependency-review / OpenSSF Scorecard workflow

## Standard files
- **Present:** readme, changelog, license, gitignore
- **Missing:** contributing, security, code_of_conduct, citation, editorconfig, precommit, pr_template, issue_template, dependabot

## Packaging
- **name:** `nirs4all-core (PyPI) / nirs4all (crate, npm) / nirs4all (R, MATLAB)` — **version:** `0.2.4`
- **issues:**
- Final nirs4all-lite alias release remains pending after the canonical nirs4all-core publish; existing nirs4all-lite releases must not be yanked
- RELEASE BLOCKER (documented in release-python.yml header): the PyPI Trusted Publisher for project nirs4all-core does not exist yet; the old nirs4all-lite publisher does not carry over, so a tag push will fail to publish to PyPI until the maintainer creates it
- Three different published names across ecosystems (PyPI nirs4all-core, crates.io nirs4all, npm nirs4all) — each must be free/owned before first release; workflow comments flag this as an assumption
- Aggregate depends on upstreams that must already be published at the pinned versions: crate depends on dag-ml 0.2.2 + dag-ml-data 0.2.3 on crates.io; pyproject extras require nirs4all-formats>=0.2.2 / nirs4all-io>=0.1.6 / nirs4all-datasets>=0.3.3 / nirs4all-methods>=1.0.2 / dag-ml>=0.2.2 / dag-ml-data>=0.2.3 on PyPI — release/install fails if any is absent
- classifiers still Development Status :: 3 - Alpha
- Rust workspace [workspace.package] declares no version; the crate version lives only in bindings/rust/nirs4all/Cargo.toml (the declared single source of truth), propagated by scripts/bump_version.sh — a manual bump can drift bindings if the script is skipped

## Tests
- **framework:** Multi-language: Python unittest (7 test modules incl. large test_release_topology.py + cross-language surface/capability/parity), Node node:test (4 .test.js: index/execution/parity + methods-artifact), Rust #[test] in bindings/rust/nirs4all/src/lib.rs, R scripts (surface/upstreams/pipeline/parity.R via R CMD check), MATLAB/Octave (smoke.m + parity.m). Strict numerical parity is validated against a full-Python nirs4all oracle (tests/parity/expected/portable_python_oracle.json).
- **estimate:** Moderate: ~15 test files spanning 5 language bindings, surface + capability-matrix + cross-language + parity coverage; strong on contract/parity, thin on unit depth (the binding is a thin re-export shim so most logic lives upstream).
- **coverage:** No coverage threshold enforced anywhere; coverage.xml (102 KB) exists in the worktree but is gitignored and not produced or gated by CI.

## Docs
- **system:** Sphinx + MyST (myst_parser, sphinx_design, sphinx_copybutton, sphinxext-opengraph, furo theme) built by Read the Docs (.readthedocs.yaml, ubuntu-24.04 / python 3.12, docs/requirements.txt). Rich hand-written Markdown set: index, installation, getting_started, ARCHITECTURE, BINDINGS, CAPABILITIES, OPERATORS, PARITY, COMPATIBILITY, NAMING, CORE_RENAME, PUBLISHING, RELEASE.
- **status:** Looks buildable (self-consistent conf.py, pinned doc deps, static brand assets present). Weakness: no API autodoc (pure narrative), and no CI docs-build job so RTD is the only place breakage surfaces.

## Risks
| severity | area | detail |
|---|---|---|
| blocker | packaging/release | release-python.yml's own header states the PyPI Trusted Publisher for nirs4all-core is not yet created; the first vX.Y.Z tag will build+twine-check fine but the publish-pypi job (OIDC, environment: pypi) will fail. Same first-release exposure for crates.io name 'nirs4all' and npm name 'nirs4all' if not already owned. |
| high | dependency availability | The crate published by release-crates.yml declares dag-ml 0.2.2 + dag-ml-data 0.2.3 as hard deps; cargo publish (and any consumer build) fails unless those exact versions are already on crates.io. Likewise pyproject extras pin nirs4all-formats/io/methods/datasets + dag-ml(-data) versions that must exist on PyPI. Cross-repo release ordering is a coupling hazard. |
| medium | CI hardening | ci.yml (/.github/workflows/ci.yml) has no permissions: block, so GITHUB_TOKEN uses the repo default scope instead of least-privilege contents:read; every other workflow already sets explicit permissions. |
| medium | CI cost/reliability | ci.yml runs on every push to every branch with no branch/path filter; the strict-parity job builds the Emscripten SDK, checks out external GBeurier/nirs4all-methods, and installs octave/R on each run — slow, network-dependent, and prone to flaking on upstream availability. |
| low | supply-chain | Third-party actions are pinned only to floating major tags (softprops/action-gh-release@v2, anchore/sbom-action@v0, pypa/gh-action-pypi-publish@release/v1, dtolnay/rust-toolchain@stable, r-lib/actions/*), not commit SHAs; a compromised tag could execute in release jobs that hold contents:write / id-token:write. |
| low | secrets | npm publish uses a long-lived NPM_TOKEN repository secret (release-npm.yml) even though provenance is OIDC; PyPI and crates paths are token-minimized (PyPI is fully OIDC), so npm is the one remaining static-token publish path. |
| low | governance docs | No SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, CITATION.cff, or issue/PR templates; no dependabot/renovate config for the mixed Cargo + npm + pip toolchain. |

## Security
- **info** — Secret scan over tracked source (excluding tests/fixtures/docs/lockfiles) found no private keys, API keys, or embedded tokens. All credentials are GitHub secrets (NPM_TOKEN, CARGO_REGISTRY_TOKEN) or OIDC-minted.
- **low** — Release workflows correctly scope elevated permissions (id-token/attestations/contents:write) only to the publishing jobs; the main CI workflow is the only one missing an explicit least-privilege permissions block.
- **low** — Committed binary/build artifacts under .r-parity-lib/ (n4m.so, .rds) are gitignored patterns yet present in the worktree; confirm none are tracked (git ls-files shows only Cargo.lock tracked among artifacts, so this is clean but worth a periodic check).

## Quick wins (pragmatic scope — safe to apply now)
- Add a top-level permissions: {contents: read} block to .github/workflows/ci.yml to match the least-privilege stance of every other workflow.
- Restrict ci.yml's push trigger to branches (main, rc/**) and/or add paths-ignore for docs-only changes so the heavy strict-parity job doesn't run on every scratch-branch push.
- Add SECURITY.md (vulnerability disclosure -> nirs4all-admin@cirad.fr per ecosystem policy) — currently absent.
- Add CONTRIBUTING.md pointing at the make test / cargo fmt+clippy green gate, and a CODE_OF_CONDUCT.md.
- Add CITATION.cff (repo is a citable scientific aggregate with a homepage at nirs4all.org).
- Add .github/dependabot.yml covering cargo (root + bindings/rust), npm (bindings/wasm), and github-actions ecosystems.
- Add .editorconfig and a .pre-commit-config.yaml wrapping cargo fmt --check + ruff (if adopted) so contributors run the gate locally.
- Add .github issue templates and a PULL_REQUEST_TEMPLATE.md.
- Bump classifiers from 'Development Status :: 3 - Alpha' to Beta once the publishers and alias release land.

## Deepest hardening roadmap (fullest realistic hardening)
- Complete the remaining release cutover (docs/CORE_RENAME.md Phase R2): PyPI Trusted Publisher creation for nirs4all-core, claim crates.io + npm 'nirs4all' names, then publish the final nirs4all-lite alias release.
- Pin all third-party GitHub Actions to full commit SHAs (with a comment naming the version) across all 8 workflows; keep first-party actions/* on majors or SHA-pin those too.
- Add an OpenSSF Scorecard workflow, CodeQL (for the JS/TS binding + Python), and actions/dependency-review-action on PRs.
- Introduce coverage measurement per binding (Python coverage, cargo-llvm-cov, node --experimental-test-coverage) and set an enforced threshold gate; wire coverage.xml into CI instead of leaving it a stale local artifact.
- Add a docs-build CI job (sphinx-build -W docs docs/_build/html) so RTD breakage and broken cross-links fail PRs, plus a link checker.
- Formalize cross-repo release ordering: a release checklist / automation that verifies the pinned upstream versions (dag-ml, dag-ml-data, formats, io, methods, datasets) are actually published before tagging, to avoid a green build that can't install.
- Consider consolidating the 6 tag-triggered publish workflows behind a single release orchestrator or a shared reusable workflow to reduce drift and make the version-sync guarantee (scripts/bump_version.sh) enforceable in one place.
- Add a scheduled/dispatch reproducibility check that rebuilds the source tarball + SBOM and diffs against the released SHA256SUMS.
- Migrate npm publish off the long-lived NPM_TOKEN to npm OIDC/granular automation token once available; document token rotation.
- Adopt ruff+mypy (or at least ruff) for the Python binding to match the ecosystem's stated Python green gate, and run it in the python CI job.
- Expand parity fixtures/oracle coverage and add negative/error-path tests for the thin re-export surface to guard against silent upstream API drift.

## Push-safety notes
- Tag pushes matching v[0-9]*.[0-9]*.[0-9]* are the release trigger for SIX workflows simultaneously (release-source, release-python, release-npm, release-crates, release-r, release-matlab). Pushing such a tag auto-publishes to PyPI (nirs4all-core), npm (nirs4all), and crates.io (nirs4all) — crates.io and PyPI are IMMUTABLE. Never push a version tag casually; use the workflow_dispatch dry-run inputs first.
- version-guard.yml runs on every push/PR to main and rc/** and FAILS if bindings/rust/nirs4all/Cargo.toml [package] version is ahead of the latest git tag. Consequence: you cannot merge a version bump to main before its tag exists — bump and tag must land together, and scripts/bump_version.sh must be run so all binding manifests agree or the release-time tag-vs-version validation steps abort.
- Pushing to main does NOT itself publish (all publish jobs gate on refs/tags/v and non-pre-release), so main is safe from accidental release — but it DOES trigger the full CI including the expensive strict-parity job that clones external GBeurier/nirs4all-methods (pinned SHA f452d95 in ci.yml, and the compat/upstreams.toml ref in release-npm.yml) and builds emscripten/R/octave; upstream unavailability can turn a main push red.
- Cross-repo coupling: publishing this aggregate requires the pinned upstream versions to already exist on their registries; a tag push here can produce partial success (e.g. source+SBOM release attached) while crates/PyPI publish fails on a missing dependency, leaving an inconsistent release.
- No Read-the-Docs-blocking or Pages-deploy-on-push workflow exists in-repo (docs deploy is external RTD), so a main push will not break a live site directly — but the RTD build has no CI mirror, so doc regressions ship silently.
- No release-please / automated version-bump PR bot is present; versioning is manual via scripts/bump_version.sh, so the main risk is a human bumping the manifest and merging to main without the matching tag (blocked by version-guard) rather than an automation misfire.
