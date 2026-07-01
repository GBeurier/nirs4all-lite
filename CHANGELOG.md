# Changelog

All notable changes to **nirs4all-lite** are documented here. The project
follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html). The Rust
crate `[package]` version in `bindings/rust/nirs4all/Cargo.toml` is the
single source of truth; `scripts/bump_version.sh` propagates it to every other
binding manifest.

## [Unreleased]

First safe `LOCK-GOV` slice — **additive only**, no legacy name removed and no
distribution rename (the `nirs4all-lite` → `nirs4all-core` cutover stays
release-gated on `LOCK-REL`).

### Added

- Python `n4a` import facade — a brand-aligned root (`import n4a`) that
  re-exports the full `nirs4all_lite` public surface and adds no behavior.
- Python `nirs4all_core` forward-compatible import alias for the
  `nirs4all-lite` → `nirs4all-core` direction; re-exports `nirs4all_lite`. The
  published distribution name is unchanged (`nirs4all-lite`).
- `docs/NAMING.md` documenting the per-language aggregate names, the lite→core
  direction, the facades, and the `n4a` token disambiguation (`n4a` import vs
  `.n4a` bundle extension vs `n4a-datasets` CLI) for `GOV-004`.
- `bindings/python/tests/test_facade.py` proving surface parity, object
  identity, `__getattr__` passthrough, and that legacy `nirs4all_lite` imports
  and the full-`nirs4all` coexistence rule are preserved.

### Fixed

- Removed the stale `License :: OSI Approved :: MIT License` trove classifier
  from the Python `pyproject.toml`; the SPDX `License-Expression`
  (`CeCILL-2.1 OR AGPL-3.0-or-later`) is authoritative (PEP 639). The wheel
  metadata is no longer self-contradictory.

## [0.2.0] - 2026-06-14

**Breaking** (pre-1.0 minor bump, 0.1.0 → 0.2.0) — coordinated with the breaking
**nirs4all-methods 1.0.0** (C ABI 2.0 + the `n4m.<role>` namespace). `nirs4all-lite`
re-exports the methods surface, so consumers must move to the methods 1.0.0 / ABI-2 surface.

### Changed (breaking)

- Re-exports the ABI-2 `nirs4all-methods` surface. The Python aggregate now
  imports methods through the new `n4m.<role>` namespace
  (e.g. `n4m.transform.scatter`, `n4m.transform.smoothing`,
  `n4m.model_selection.splitters`) instead of the old flat `n4m.sklearn.*`
  layout.
- The Rust/WASM bindings load the ABI-2 C symbols: `n4m_pp_*` preprocessing
  entry points are now `n4m_transform_*`, and `n4m_split_*` selection entry
  points are now `n4m_model_selection_*`.
- Pinned `nirs4all-methods >= 1.0.0` (was `>= 0.99.0`) in the Python
  `methods`, `all`, and bundled-aggregate extras.

### Versioning

- Bumped the lite project version `0.1.0` → `1.0.0` across every packaging
  manifest: the Rust crate (source of truth), the WASM `package.json` /
  `package-lock.json`, the Python `pyproject.toml`, and the R `DESCRIPTION`.
  The MATLAB/Octave archive version derives from the Rust crate version at
  build time.
