#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p .cache/upstream/opensync-native-layout .cache/r0-evidence
if [[ ! -d .cache/upstream/opensync/.git ]]; then
  git clone --no-checkout --filter=blob:none https://github.com/plume-design/opensync.git .cache/upstream/opensync
fi
git -C .cache/upstream/opensync checkout --detach 78d8a7194d5e77635877cc456231e7be5cf03d68
if [[ ! -e .cache/upstream/opensync-native-layout/core ]]; then
  ln -s ../opensync .cache/upstream/opensync-native-layout/core
fi
export PATH="$PWD/.cache/upstream/openvswitch-4.0.0/ovsdb:$PATH"
# Build only. Do not run the upstream test.sh host-global /tmp database or boot scripts.
timeout 180 uv run --with kconfiglib==14.1.0 --with jinja2==3.1.6 -- \
  make -C .cache/upstream/opensync-native-layout/core TARGET=native src/owm ovsdb-create -j2 \
  > .cache/r0-evidence/build.log 2>&1
# A successful build is not manager/driver qualification; N02–N04 still apply.
