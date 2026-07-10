# Quality gates — nirs4all-lite

A portable Rust aggregate re-exporting the ecosystem cores across Python/R/MATLAB/Octave/JS-WASM bindings.
The Rust `[package]` version in `bindings/rust/nirs4all/Cargo.toml` is the single source of truth
(`scripts/bump_version.sh` propagates it).

## Local green gate

```bash
cargo fmt --all --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
# bindings: python (maturin), wasm (wasm-pack), R — built/tested in CI
```

Optional local hygiene hooks: `uvx pre-commit run --all-files`.

## CI gates (`.github/workflows/`)

| workflow | trigger | gate |
|---|---|---|
| `ci.yml` | push/PR | Rust build/test + surface gates (statically gate the R/WASM/Python surfaces) |
| `version-guard.yml` | push/PR | manifest not ahead of latest tag |
| `release-{crates,python,npm,r,matlab,source}.yml` | **tag / dispatch** | build + publish — **never on branch push** |

All third-party actions are **SHA-pinned** (55 pins across 8 workflows) at their current majors
(`checkout@v6`, `setup-python@v6`, `upload-artifact@v7`, …); only `dtolnay/rust-toolchain@stable` is left
floating, by design. Dependabot covers github-actions + cargo + the python/wasm bindings.

## Deepest-hardening roadmap

- Keep this retired checkout aligned with the no-release policy in `release_checklist.md`.
  No new `nirs4all-lite` PyPI compatibility/alias release is part of the RC target.
- Coverage floor once the aggregate surface stabilizes.
