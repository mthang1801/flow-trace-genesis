#!/usr/bin/env bash
# install.sh — cài skill flow-trace-genesis vào harness ngoài Claude Code marketplace.
# Usage: ./installers/install.sh --target codex|opencode|cursor|claude [--dry-run]
# v1 chủ đích đơn giản: copy file đúng layout từng harness (mapping: installers/README.md).
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_SRC="$REPO_DIR/plugins/flow-trace-genesis/skills/flow-trace-genesis"
CMD_SRC="$REPO_DIR/plugins/flow-trace-genesis/commands/flow-trace-genesis.md"

TARGET=""
DRY_RUN=0
while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help)
      echo "usage: $0 --target codex|opencode|cursor|claude [--dry-run]"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

case "$TARGET" in
  claude)   SKILL_DST="$HOME/.claude/skills/flow-trace-genesis"
            CMD_DST="$HOME/.claude/commands/flow-trace-genesis.md" ;;
  codex)    SKILL_DST="$HOME/.codex/skills/flow-trace-genesis"
            CMD_DST="$HOME/.codex/prompts/flow-trace-genesis.md" ;;
  opencode) SKILL_DST="$HOME/.config/opencode/skills/flow-trace-genesis"
            CMD_DST="$HOME/.config/opencode/commands/flow-trace-genesis.md" ;;
  cursor)   SKILL_DST="$HOME/.cursor/skills/flow-trace-genesis"
            CMD_DST="$HOME/.cursor/commands/flow-trace-genesis.md" ;;
  *) echo "cần --target codex|opencode|cursor|claude (mapping: installers/README.md)" >&2; exit 1 ;;
esac

[ -d "$SKILL_SRC" ] || { echo "không thấy skill source: $SKILL_SRC" >&2; exit 1; }

echo "[install] target : $TARGET"
echo "[install] skill  : $SKILL_SRC -> $SKILL_DST"
echo "[install] command: $CMD_SRC -> $CMD_DST"

if [ -e "$SKILL_DST" ]; then
  echo "[install] CẢNH BÁO: $SKILL_DST đã tồn tại — sẽ ghi đè nội dung trùng tên (không xóa file lạ)."
fi

if [ "$DRY_RUN" -eq 1 ]; then
  echo "[install] --dry-run: không ghi file. Danh sách sẽ copy:"
  ( cd "$SKILL_SRC" && find . -type f | sed "s|^\.|  $SKILL_DST|" )
  echo "  $CMD_DST"
  exit 0
fi

mkdir -p "$SKILL_DST" "$(dirname "$CMD_DST")"
cp -R "$SKILL_SRC/." "$SKILL_DST/"
cp "$CMD_SRC" "$CMD_DST"
echo "[install] xong. Kiểm tra harness đọc được skill (xem installers/README.md — mục verify per-harness)."
echo "[install] Lưu ý: MCP bundle (serena/markitdown/docling) KHÔNG tự cài — xem plugins/flow-trace-genesis/.mcp.json."
