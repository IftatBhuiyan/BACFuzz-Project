#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
revision=$(cat upstream.lock)
dest=.upstream/BACFuzz
if [[ ! -d "$dest" ]]; then
  git clone https://github.com/websecfuzz/BACFuzz.git "$dest"
fi
[[ "$(git -C "$dest" remote get-url origin)" == "https://github.com/websecfuzz/BACFuzz.git" ]] || { echo 'Unexpected upstream origin'; exit 1; }
[[ -z "$(git -C "$dest" status --porcelain)" ]] || { echo 'Upstream has local changes; preserve them and inspect manually.'; exit 1; }
git -C "$dest" cat-file -e "$revision^{commit}"
git -C "$dest" checkout --detach "$revision"
git -C "$dest" rev-parse HEAD
