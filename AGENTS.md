# Repository Guidelines

## Scope

`nirs4all-lite/` is the legacy compatibility checkout for the portable
aggregate that was renamed to `nirs4all-core`. The canonical portable aggregate
now lives in `GBeurier/nirs4all-core`; `GBeurier/nirs4all-lite` remains a
legacy/redirect line for compatibility and validation only.

Treat this checkout as an alias/transition surface over the same low-level
nirs4all stack. It wraps and re-exports `dag-ml`, `dag-ml-data`,
`nirs4all-formats`, `nirs4all-io`, `nirs4all-datasets`, and
`nirs4all-methods`, but releases must not originate from `nirs4all-lite`.
Local or CI validation may run here; canonical publishing belongs only to
`GBeurier/nirs4all-core` (see `bindings/python/src/nirs4all_lite/_topology.py`
and `scripts/release_guard.py`).

Do not implement new parsers, numerical methods, dataset loaders, or ML
coordinators here. Add that work to the owning upstream project, then expose it
through this aggregate.

## Structure

- `bindings/python`: Python distribution named `nirs4all-core` (canonical
  import `nirs4all_lite`; additive facades `n4a`, `nirs4all_core`).
- `bindings/rust`: Rust crate named `nirs4all`.
- `bindings/wasm`: npm/WASM package named `nirs4all`.
- `bindings/r`: R package skeleton named `nirs4all`.
- `bindings/matlab`: MATLAB/Octave `+nirs4all` namespace.
- `docs`: binding, parity, compatibility, and release contracts.
- `compat`: machine-readable upstream registry.

## Checks

Run the checks matching the touched area:

- `make test`
- `cargo test --workspace`
- `PYTHONPATH=bindings/python/src python -m unittest discover -s bindings/python/tests`
- `npm test --prefix bindings/wasm`
- `mkdir -p dist/r && cd dist/r && R CMD build ../../bindings/r && cd ../.. && R CMD check --no-manual dist/r/nirs4all_*.tar.gz`
- `octave --quiet --eval "run('bindings/matlab/tests/smoke.m')"`

When parity fixtures are added, run the native-vs-binding and
core-vs-python-`nirs4all` parity suites before publishing.

## Boundaries

- The native source of truth for PLS/NIRS methods is `nirs4all-methods`.
- File parsing belongs to `nirs4all-formats`.
- Dataset assembly belongs to `nirs4all-io`.
- Dataset catalog metadata belongs to `nirs4all-datasets`.
- Graph planning and leakage-safe ML orchestration belong to `dag-ml` and
  `dag-ml-data`.

Bindings translate idiomatic host objects to those upstream contracts only.
