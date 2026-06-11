#!/usr/bin/env bash
set -euo pipefail

out_dir="${1:-dist/matlab}"
version="$(sed -n 's/^version = \"\\(.*\\)\"/\\1/p' bindings/rust/nirs4all/Cargo.toml | head -1)"
version="${version:-0.0.0}"
archive="nirs4all-matlab-octave-${version}.zip"

mkdir -p "$out_dir"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

mkdir -p "$tmp_dir/nirs4all"
cp -R bindings/matlab/+nirs4all "$tmp_dir/nirs4all/"
cp bindings/matlab/README.md "$tmp_dir/nirs4all/"
cp bindings/matlab/LICENSE "$tmp_dir/nirs4all/"

(cd "$tmp_dir" && zip -qr "$OLDPWD/$out_dir/$archive" nirs4all)
echo "$out_dir/$archive"
