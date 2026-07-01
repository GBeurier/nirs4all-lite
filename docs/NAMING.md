# Naming & aggregate facade (LOCK-GOV)

This page records the governed naming of the portable aggregate and the
**additive** import facades introduced by the first `LOCK-GOV` slice. It is the
Python-facing companion to the ecosystem governance decisions (`GOV-003`
per-language source-of-truth names, `GOV-004` alias/token policy).

## Aggregate package names (current, shipping)

The aggregate is published under the bare `nirs4all` name in every host language
**except Python**, where the full `nirs4all` modelling library already owns that
import root. To avoid colliding with it, the Python aggregate ships as
`nirs4all-lite` (import `nirs4all_lite`).

| Target | Distribution / external name | Import / module name |
| --- | --- | --- |
| Python | `nirs4all-lite` | `nirs4all_lite` |
| Rust | `nirs4all` | `nirs4all` |
| JavaScript/WASM | `nirs4all` | `nirs4all` |
| R | `nirs4all` | `library(nirs4all)` |
| MATLAB/Octave | `nirs4all` | `+nirs4all` namespace |

## Direction: `nirs4all-lite` → `nirs4all-core` (target-state)

The governance direction is to promote the aggregate from `lite` to
**`nirs4all-core`**. This is a *concept* whose per-language spelling is pinned by
`GOV-003`; it is **not** a single literal rename across ecosystems (Rust/npm/R/
MATLAB already use the bare `nirs4all` name and are unaffected). Only the Python
distribution name is in question.

The actual Python distribution rename `nirs4all-lite` → `nirs4all-core` is
**release-gated (`LOCK-REL`)** and is deliberately *not* performed yet:

- The published Python distribution is still **`nirs4all-lite`**. No
  `nirs4all-core` distribution is announced or published by this slice.
- To let downstream code adopt the target import name early without breakage,
  the aggregate additionally exposes an **additive `nirs4all_core` import
  facade**. Its advertised public contract is deliberately core-only:
  inspection, validation, capability reporting, release topology, and facade
  access. Execution helpers from `nirs4all_lite` stay reachable through
  compatibility passthrough, but they are not part of `nirs4all_core.__all__`.

```python
import nirs4all_core          # forward-compatible alias (additive)
import nirs4all_lite          # canonical/legacy import — unchanged
assert nirs4all_core.upstreams is nirs4all_lite.upstreams
assert "run_portable_pipeline" not in nirs4all_core.__all__
```

## The `n4a` facade (additive brand root)

`n4a` is a short, brand-aligned Python import root (`n4a` = "nirs4all") that
re-exports the full public surface of the aggregate. It adds no behavior; it is
a facade over `nirs4all_lite`.

```python
import n4a

n4a.upstream_status()
plan = n4a.parse_execution_plan(config)
```

Both facades are **additive and non-shadowing**: they never remove or rename the
`nirs4all_lite` surface, and — per the Python strategic-path rule — they do
**not** define a top-level `nirs4all` Python module, so the full `nirs4all`
library and the aggregate continue to coexist.

The package exposes `release_topology_manifest()` as a machine-checkable summary
of this contract. It records that the current Python distribution remains
`nirs4all-lite`, the `nirs4all-core` distribution name is release-gated, and
the `nirs4all_core` import contract is not an execution engine.

## `n4a` token disambiguation (GOV-004)

The `n4a` stem is used in three different layers of the ecosystem. They are
intentionally consistent (`n4a` = "nirs4all") but must not be conflated:

| Token | Layer | Meaning |
| --- | --- | --- |
| `n4a` | Python import | The aggregate **import facade** documented here (`import n4a`). |
| `.n4a` | File extension | The pipeline/bundle **file format** produced by the full `nirs4all` library. |
| `n4a-datasets` | Console script | The **CLI** shipped by `nirs4all-datasets`. |

A `.n4a` file is data, `n4a-datasets` is an executable, and `n4a` is an import
root. None is an alias of another.
