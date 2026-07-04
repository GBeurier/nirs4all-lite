# Security policy

`nirs4all-lite` (being renamed to `nirs4all-core`) is a portable **aggregate distribution**: it
re-exports the Rust cores of `dag-ml`, `dag-ml-data`, `nirs4all-formats`, `nirs4all-io`,
`nirs4all-datasets`, and `nirs4all-methods` across Python / R / MATLAB / Octave / JS-WASM bindings.
It adds **no new parsers or algorithms**.

Because the security-relevant behavior lives in the aggregated components:

- File-parsing vulnerabilities belong to **`nirs4all-formats`** (see its `SECURITY.md`).
- Numerical-kernel issues belong to **`nirs4all-methods`** / **`dag-ml`**.
- This repo's own surface is packaging, the binding shims, and the WASM sandbox boundary.

## Reporting a vulnerability

Report privately to **nirs4all-admin@cirad.fr** (or the affected component repo's `SECURITY.md` if you
know which component is involved). Do not open a public issue.
