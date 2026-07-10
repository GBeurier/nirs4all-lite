# Release checklist — retired nirs4all-lite checkout

> ⛔ **RELEASE IS BLOCKED PERMANENTLY FOR THIS REPOSITORY.** This checkout is retained for
> audit/history only. Canonical aggregate releases now originate from `nirs4all-core`; do
> not tag or publish from `nirs4all-lite`.

## Current policy

- [x] `nirs4all-core` is the canonical repo for the portable aggregate.
- [x] No new `nirs4all-lite` PyPI compatibility/alias release is part of the RC target.
- [x] Existing historical `nirs4all-lite` versions are left intact; do not yank them.
- [x] Registry ownership, Trusted Publisher setup, and dependency ordering now belong to
      the `nirs4all-core` release checklist and ecosystem cockpit.

## Historical checklist shape

The old release checklist expected green CI, synchronized cross-binding versions, dry-run
publishing, and immutable multi-registry fan-out from this repository. That flow is
superseded: perform those checks only in `nirs4all-core`.
