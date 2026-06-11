# External Operator Binding Contract

`nirs4all-lite` must expose external operators idiomatically in every target
language, but only when the execution layer can actually use them. The aggregate
must never pretend to execute an operator by reimplementing numerical behavior
locally.

## Gate

An external operator can be exposed as executable only when all of these are
true:

1. The owning upstream project declares the operator contract and version.
2. The relevant executor can plan or call the operator (`dag-ml`,
   `nirs4all-methods`, or the full Python `nirs4all` parity harness).
3. The binding can translate host-native inputs and outputs without lossy
   schema changes.
4. A parity fixture exists against the owning upstream implementation.

If any item is missing, the binding may expose metadata, but execution must fail
with a clear "capability unavailable" diagnostic.

## Capability Levels

Bindings should classify each external operator with one of these states:

- `metadata`: listed in catalogs only; cannot be planned or executed.
- `plan`: can appear in a DAG/execution descriptor, but not run in this binding.
- `execute-local`: can run in the current process through an upstream binding.
- `execute-remote`: can run through an upstream remote/controller boundary.
- `parity-validated`: has cross-runtime fixtures against the owning upstream and,
  when applicable, the full Python `nirs4all` pipeline.

Releases should not market an operator as available unless it is at least
`execute-local` or `execute-remote`.

## Language Idioms

Python:

- sklearn-style estimators/transformers with `fit`, `transform`, `predict`,
  `get_params`, and `set_params` where applicable.
- NumPy arrays and pandas data frames as first-class inputs.
- Optional extras for framework-specific integrations.

R:

- Formula/data-frame entry points where natural.
- S3 methods for `fit`, `predict`, `transform`, `print`, and `summary` where the
  operator has model-like state.
- Compatibility hooks for the R ecosystem should be wrappers over upstream
  behavior, not new algorithms.

Rust:

- Traits and typed builders, returning `Result`.
- Feature-gated upstream integrations when the dependency is optional.
- Explicit ownership for FFI handles and buffers.

JavaScript/WASM:

- Typed ESM exports with browser-safe async initialization.
- `TypedArray`-first numerical inputs; no DOM dependency in the package.
- Promise-returning execution when WASM or remote execution must initialize.

MATLAB/Octave:

- Matrix/table entry points plus explicit options structs.
- Function handles or small classes for stateful operators.
- Octave-safe public APIs unless the function is clearly marked MATLAB-only.

## Parity

Operator parity must compare the host idiom against the owning upstream
implementation. For pipeline operators, fixtures should also compare equivalent
pipelines against the full Python `nirs4all` library before `nirs4all-lite` is
used as a replacement core.
