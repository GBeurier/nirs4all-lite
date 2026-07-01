"""Release topology and core facade contract for the aggregate package."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

CORE_FACADE_EXPORTS: tuple[str, ...] = (
    "LazyUpstream",
    "PORTABLE_OPERATOR_CLASSES",
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
    "portable_class_names",
    "require_upstream",
    "upstream_status",
    "upstreams",
)

EXECUTION_ENGINE_EXPORTS: tuple[str, ...] = (
    "PortableDataset",
    "parse_execution_plan",
    "run_portable_pipeline",
)

TOPOLOGY_EXPORTS: tuple[str, ...] = (
    "CORE_FACADE_EXPORTS",
    "EXECUTION_ENGINE_EXPORTS",
    "TOPOLOGY_EXPORTS",
    "core_facade_exports",
    "execution_engine_exports",
    "release_topology_manifest",
    "validate_core_facade",
)

_RELEASE_TOPOLOGY_MANIFEST: dict[str, Any] = {
    "schema": "nirs4all-lite.release-topology.v1",
    "python": {
        "distribution": "nirs4all-lite",
        "canonical_import": "nirs4all_lite",
        "target_distribution": "nirs4all-core",
        "target_distribution_status": "release-gated",
        "additive_imports": ["n4a", "nirs4all_core"],
        "reserved_non_imports": ["nirs4all"],
    },
    "core_contract": {
        "import": "nirs4all_core",
        "backing_import": "nirs4all_lite",
        "allowed_roles": ["inspect", "validate", "capability", "facade"],
        "execution_engine": False,
        "public_exports": list(CORE_FACADE_EXPORTS),
        "topology_exports": list(TOPOLOGY_EXPORTS),
        "excluded_execution_exports": list(EXECUTION_ENGINE_EXPORTS),
        "compat_passthrough": True,
    },
    "install_distributions": [
        {
            "registry": "pypi",
            "name": "nirs4all-lite",
            "role": "portable aggregate",
            "status": "current",
        },
        {
            "registry": "pypi",
            "name": "nirs4all-core",
            "role": "portable aggregate target name",
            "status": "release-gated",
        },
        {
            "registry": "pypi",
            "name": "nirs4all-methods",
            "role": "numerical methods execution engine",
            "status": "upstream-explicit",
        },
        {
            "registry": "pypi",
            "name": "nirs4all-formats",
            "role": "vendor file readers",
            "status": "upstream-explicit",
        },
        {
            "registry": "pypi",
            "name": "nirs4all-io",
            "role": "dataset assembly bridge",
            "status": "upstream-explicit",
        },
        {
            "registry": "pypi",
            "name": "nirs4all-datasets",
            "role": "optional dataset catalog",
            "status": "external-optional",
        },
        {
            "registry": "pypi",
            "name": "dag-ml",
            "role": "DAG/ML coordinator",
            "status": "upstream-explicit",
        },
        {
            "registry": "pypi",
            "name": "dag-ml-data",
            "role": "sample-aligned data contracts",
            "status": "upstream-explicit",
        },
        {
            "registry": "crates.io/npm/cran/github-release",
            "name": "nirs4all",
            "role": "non-Python aggregate artifact name",
            "status": "current",
        },
    ],
}


def core_facade_exports() -> tuple[str, ...]:
    """Return the public exports in the release-gated core facade contract."""

    return CORE_FACADE_EXPORTS


def execution_engine_exports() -> tuple[str, ...]:
    """Return aggregate exports that are deliberately outside the core contract."""

    return EXECUTION_ENGINE_EXPORTS


def release_topology_manifest() -> dict[str, Any]:
    """Return a serializable manifest for package names and facade contracts."""

    return deepcopy(_RELEASE_TOPOLOGY_MANIFEST)


def validate_core_facade(module: Any) -> dict[str, tuple[str, ...]]:
    """Validate that a module advertises the no-engine core facade contract."""

    public_exports = set(getattr(module, "__all__", ()))
    return {
        "missing_core_exports": tuple(
            sorted(set(CORE_FACADE_EXPORTS) - public_exports)
        ),
        "unexpected_execution_exports": tuple(
            sorted(set(EXECUTION_ENGINE_EXPORTS) & public_exports)
        ),
    }
