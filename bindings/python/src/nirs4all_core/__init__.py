"""``nirs4all_core`` -- forward-compatible import alias for the aggregate.

LOCK-GOV direction (target-state): the portable nirs4all aggregate -- shipped
today as the ``nirs4all-lite`` distribution (import ``nirs4all_lite``) -- is to
be promoted to ``nirs4all-core``. The actual distribution rename is gated on the
release lock (``LOCK-REL``) and is intentionally **not** performed in this
slice: the project keeps publishing the aggregate as ``nirs4all-lite`` and only
adds this additive ``nirs4all_core`` import alias so downstream code can adopt
the target import name early, without breakage.

Importing ``nirs4all_core`` is equivalent to importing ``nirs4all_lite``::

    import nirs4all_core as n4a_core

    n4a_core.upstream_status()

The legacy ``nirs4all_lite`` import surface is unchanged and fully supported.
"""

from __future__ import annotations

from typing import Any

import nirs4all_lite as _aggregate
from nirs4all_lite import (
    PORTABLE_OPERATOR_CLASSES,
    LazyUpstream,
    PipelineDefinition,
    PortableDataset,
    Upstream,
    available_upstreams,
    dag_ml,
    dag_ml_data,
    datasets,
    formats,
    import_upstream,
    io,
    load_pipeline_definition,
    methods,
    parse_execution_plan,
    portable_class_names,
    require_upstream,
    run_portable_pipeline,
    upstream_status,
    upstreams,
)

#: Import package currently backing this alias (``nirs4all_lite``). The
#: distribution rename ``nirs4all-lite`` -> ``nirs4all-core`` is release-gated
#: (LOCK-REL); this alias forwards to the shipped aggregate until then.
__aggregate_import__ = _aggregate.__name__

__all__ = [
    "LazyUpstream",
    "PORTABLE_OPERATOR_CLASSES",
    "PortableDataset",
    "PipelineDefinition",
    "Upstream",
    "available_upstreams",
    "dag_ml",
    "dag_ml_data",
    "datasets",
    "formats",
    "import_upstream",
    "io",
    "load_pipeline_definition",
    "methods",
    "parse_execution_plan",
    "portable_class_names",
    "require_upstream",
    "run_portable_pipeline",
    "upstream_status",
    "upstreams",
]


def __getattr__(name: str) -> Any:
    """Forward any non-re-exported attribute to the backing aggregate package."""

    return getattr(_aggregate, name)
