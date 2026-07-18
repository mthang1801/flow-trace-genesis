#!/usr/bin/env bash
# check-render-sync.sh — verify N copies of a directory tree are byte-identical.
#
# The "no-fork" rule for render/ (build.py/check.py/templates/assets) says every
# mirror — Lending's .agents + .claude copies, this plugin's copy, any target repo's
# installed copy — must stay identical; fixes land upstream and get re-synced, never
# patched locally in just one place. This script turns that rule into a check any of
# those locations can run.
#
#   ./scripts/check-render-sync.sh <dir1> <dir2> [<dir3> ...]
#
# Exits 0 if every dir has the same relative file set with the same content: exits 1
# and prints the first divergence otherwise. Needs only find/sort/md5sum — no deps.
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "usage: $0 <dir1> <dir2> [<dir3> ...]" >&2
  exit 2
fi

treesum() { # treesum <dir> — one hash for the whole relative file tree
  ( cd "$1" && find . -type f -print0 | sort -z | xargs -0 md5sum ) | md5sum | cut -d' ' -f1
}

first="$1"; first_sum="$(treesum "$first")"
status=0
for dir in "$@"; do
  [ -d "$dir" ] || { echo "not a directory: $dir" >&2; exit 2; }
  sum="$(treesum "$dir")"
  if [ "$sum" != "$first_sum" ]; then
    echo "DRIFT: $dir differs from $first" >&2
    diff <(cd "$first" && find . -type f | sort) <(cd "$dir" && find . -type f | sort) >&2 || true
    status=1
  fi
done

if [ "$status" = 0 ]; then
  echo "OK — $# copies identical ($first_sum)"
else
  echo "render/ mirrors have drifted — fix upstream, then re-sync every copy" >&2
fi
exit "$status"
