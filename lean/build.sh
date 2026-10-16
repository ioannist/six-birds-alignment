#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
export LEAN_PATH="$PWD/vendor_cache/lib/lean${LEAN_PATH:+:$LEAN_PATH}"
lake build
lake env lean AxiomAudit.lean > trust_base.txt.tmp
mv trust_base.txt.tmp trust_base.txt
if rg -n '\bsorry\b|^axiom ' Alignment Alignment.lean; then
    echo "Unresolved hole or axiom declaration" >&2
    exit 1
fi
echo "PASS: build and axiom audit"
