# nirs4all-lite

`nirs4all-lite` is the **portable aggregate distribution** of the nirs4all
ecosystem. It is a thin portability layer that exposes the same upstream
capabilities across **Rust, Python, R, MATLAB/Octave, and JavaScript/WASM** from
one canonical package surface — without becoming a second implementation of
parsing, datasets, ML orchestration, or numerical methods.

## What it re-exports

`nirs4all-lite` aggregates exactly six upstream libraries and delegates all real
work to them:

- [`dag-ml`](https://dag-ml.readthedocs.io/en/latest/) — reproducible,
  OOF/leakage-safe ML coordinator.
- [`dag-ml-data`](https://dag-ml-data.readthedocs.io/en/latest/) — typed,
  sample-aligned multi-source data contracts.
- [`nirs4all-formats`](https://nirs4all-formats.readthedocs.io/en/latest/) —
  Rust readers for NIRS/spectroscopy vendor file formats.
- [`nirs4all-io`](https://nirs4all-io.readthedocs.io/en/latest/) — dataset
  assembly bridge to a `SpectroDataset`.
- [`nirs4all-datasets`](https://nirs4all-datasets.readthedocs.io/en/latest/) —
  curated, DOI-pinned NIRS dataset catalog.
- [`nirs4all-methods`](https://nirs4all-methods.readthedocs.io/en/latest/) —
  portable C-ABI PLS/NIRS numerical engine (`libn4m`).

Each binding exposes these upstream domains directly as `formats`, `io`,
`datasets`, `methods`, `dag_ml`, and `dag_ml_data`.

:::{important}
**It only re-exports.** `nirs4all-lite` must **never** add a parser, estimator,
numerical kernel, dataset catalog, or DAG compiler of its own. The upstream
projects remain the single source of truth; this repository provides only a
canonical package surface, native bindings, release glue, and parity checks.
:::

## Package names

The Python distribution keeps the name `nirs4all-lite` (imported as
`nirs4all_lite`) so it does not collide with the full Python `nirs4all` library.
**Every other binding uses `nirs4all`.**

| Target | External name | Import / module name |
| --- | --- | --- |
| Python | `nirs4all-lite` | `nirs4all_lite` |
| Rust | `nirs4all` | `nirs4all` |
| JavaScript/WASM | `nirs4all` | `nirs4all` |
| R | `nirs4all` | `library(nirs4all)` |
| MATLAB/Octave | `nirs4all` | `+nirs4all` namespace |

In Python the aggregate additionally exposes two **additive, non-shadowing**
import facades (see [](NAMING.md)): the brand root `n4a` (`import n4a`) and the
`nirs4all_core` forward-compatible alias for the release-gated
`nirs4all-lite` → `nirs4all-core` direction. Both only re-export `nirs4all_lite`;
the published distribution stays `nirs4all-lite`.

:::{note}
This is the portable aggregate distribution. It is **not** `nirs4all-web` (the
standalone browser/WASM client) and **not** `nirs4all-studio` (the desktop/web
app). Those are separate projects that consume parts of this stack.
:::

## How the pieces fit

`nirs4all-lite` is the seam where the low-level ecosystem becomes one portable
surface. The aggregate composes upstream domains — it does not reimplement them:

```text
nirs4all-formats ─┐
nirs4all-io ──────┤
nirs4all-datasets ┤──►  nirs4all-lite  ──►  Python / Rust / R / MATLAB-Octave / JS-WASM
nirs4all-methods ─┤      (aggregate surface,      (one idiomatic API per host)
dag-ml ───────────┤       parity gates, release
dag-ml-data ──────┘       glue — no new logic)
```

The portable pipeline subset (Kennard-Stone, SNV, Savitzky-Golay, and a PLS
component sweep) is parsed from the same JSON/YAML definition envelope used by
the full Python `nirs4all`, then executed through `nirs4all-methods` and compared
against the full Python `nirs4all` oracle in every binding. See
[](PARITY.md) for the parity strategy and gates.

```{toctree}
:maxdepth: 2
:caption: Getting started

installation
getting_started
```

```{toctree}
:maxdepth: 2
:caption: Architecture

ARCHITECTURE
BINDINGS
NAMING
OPERATORS
COMPATIBILITY
```

```{toctree}
:maxdepth: 2
:caption: Parity & releases

PARITY
PUBLISHING
RELEASE
```

## The nirs4all ecosystem

<!-- nirs4all-lite re-exports the libraries below. RTD slugs are assumed equal to the repo name; edit a :link: URL if a slug differs at import. -->

::::{grid} 1 2 2 2
:gutter: 2

:::{grid-item-card} nirs4all
:link: https://nirs4all.readthedocs.io/en/latest/
Main Python modelling library — pipelines, SpectroDataset, predictions.
:::
:::{grid-item-card} nirs4all-formats
:link: https://nirs4all-formats.readthedocs.io/en/latest/
Rust readers for ~58 NIRS/spectroscopy file formats (re-exported).
:::
:::{grid-item-card} nirs4all-io
:link: https://nirs4all-io.readthedocs.io/en/latest/
Dataset-assembly bridge → SpectroDataset (re-exported).
:::
:::{grid-item-card} nirs4all-datasets
:link: https://nirs4all-datasets.readthedocs.io/en/latest/
Curated DOI-pinned NIRS dataset catalog (re-exported).
:::
:::{grid-item-card} nirs4all-methods
:link: https://nirs4all-methods.readthedocs.io/en/latest/
Portable C-ABI PLS/NIRS engine, libn4m (re-exported).
:::
:::{grid-item-card} dag-ml
:link: https://dag-ml.readthedocs.io/en/latest/
Reproducible, OOF/leakage-safe ML coordinator (re-exported).
:::
:::{grid-item-card} dag-ml-data
:link: https://dag-ml-data.readthedocs.io/en/latest/
Typed sample-aligned multi-source data contracts (re-exported).
:::
::::
