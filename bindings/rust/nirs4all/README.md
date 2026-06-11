# nirs4all

Rust aggregate surface for `nirs4all-lite`.

This crate exposes the low-level nirs4all upstream domains from one package:
`dag-ml`, `dag-ml-data`, `nirs4all-formats`, `nirs4all-io`,
`nirs4all-datasets`, and `nirs4all-methods`.

It does not implement parsers, dataset loaders, DAG scheduling, or numerical
methods. Those capabilities remain owned by the upstream crates and bindings.
