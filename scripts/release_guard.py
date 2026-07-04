#!/usr/bin/env python3
"""Resolve whether this checkout may publish canonical release artifacts."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOPOLOGY_PATH = ROOT / "bindings/python/src/nirs4all_lite/_topology.py"


def _load_manifest() -> dict[str, object]:
    spec = importlib.util.spec_from_file_location("nirs4all_lite_topology", TOPOLOGY_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load topology module from {TOPOLOGY_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.release_topology_manifest()


def _bool_text(value: bool) -> str:
    return "true" if value else "false"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--github-repository", required=True)
    parser.add_argument("--event-name", default="")
    parser.add_argument("--github-output")
    args = parser.parse_args()

    manifest = _load_manifest()
    policy = manifest["release_policy"]
    publish_from_repo = str(policy["publish_from_repo"])
    legacy_repo = str(policy["legacy_repo"])
    current_repo = args.github_repository
    allow_publish = current_repo == publish_from_repo

    if allow_publish:
        reason = (
            f"{current_repo} matches the canonical release repo "
            f"{publish_from_repo}; publish steps may proceed."
        )
    elif current_repo == legacy_repo:
        reason = (
            f"{current_repo} is the legacy repo; canonical publish is disabled "
            f"until the GitHub rename/cutover lands on {publish_from_repo}."
        )
    else:
        reason = (
            f"{current_repo} is not the canonical release repo {publish_from_repo}; "
            "canonical publish is disabled."
        )

    outputs = {
        "allow_publish": _bool_text(allow_publish),
        "current_repo": current_repo,
        "legacy_repo": legacy_repo,
        "publish_from_repo": publish_from_repo,
        "event_name": args.event_name,
        "reason": reason,
    }

    for key, value in outputs.items():
        print(f"{key}={value}")

    if args.github_output:
        output_path = Path(args.github_output)
        with output_path.open("a", encoding="utf-8") as handle:
            for key, value in outputs.items():
                handle.write(f"{key}={value}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
