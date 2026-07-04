# Contributing to nirs4all-lite

`nirs4all-lite` (→ `nirs4all-core`) is a **thin aggregate**: it re-exports the component crates and
exposes them across bindings. **It adds no new parsers, methods, or algorithms.**

- New readers → `nirs4all-formats`. New numerical kernels → `nirs4all-methods` / `dag-ml`.
  Dataset/IO logic → `nirs4all-io` / `nirs4all-datasets`. Fix the **component**, then bump the
  re-export here.
- Changes here are limited to: the re-export surface, binding shims (Python/R/MATLAB/Octave/WASM),
  packaging, and the version-propagation script (`scripts/bump_version.sh`).
- Green gate: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test`, plus the binding
  build/tests; keep the cross-binding version single-source-of-truth in sync.

By contributing you agree to the `CECILL-2.1 OR AGPL-3.0-or-later` license and `CODE_OF_CONDUCT.md`.
