#!/usr/bin/env bash
# Governance harness cho flow-trace-genesis (bản lean, cutoff từ Lending).
# Chỉ dùng grep -F thuần POSIX — KHÔNG phụ thuộc rg/ugrep (bài học Lending:
# harness gọi `rg` tạo 86 false failures trên máy không có binary ripgrep).

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENTS_DIR="$ROOT/.agents"

failures=0

fail() {
  failures=$((failures + 1))
  printf '[governance] FAIL: %s\n' "$*" >&2
}

note() {
  printf '[governance] %s\n' "$*"
}

require_file() {
  local path="$1"
  [[ -f "$path" ]] || fail "missing file: ${path#$ROOT/}"
}

require_text() {
  local file="$1" text="$2" reason="$3"
  if [[ ! -f "$file" ]]; then
    fail "${file#$ROOT/} not found (cần cho: $reason)"
    return
  fi
  if ! grep -qF -- "$text" "$file"; then
    fail "${file#$ROOT/} missing '$text' ($reason)"
  fi
}

note "validating required files"
require_file "$ROOT/CLAUDE.md"
require_file "$ROOT/AGENTS.md"
require_file "$ROOT/LICENSE"
require_file "$AGENTS_DIR/AGENTS.md"
require_file "$AGENTS_DIR/progress.md"
require_file "$AGENTS_DIR/CHANGELOG.md"
require_file "$AGENTS_DIR/changes/README.md"

note "validating Claude Code entrypoint shim"
require_text "$ROOT/CLAUDE.md" "@AGENTS.md" "CLAUDE.md phải là import shim, không duplicate nội dung"

note "validating routing entrypoint"
require_text "$ROOT/AGENTS.md" ".agents/AGENTS.md" "root AGENTS.md phải route về luật lõi"
require_text "$ROOT/AGENTS.md" "governance-harness.sh" "root AGENTS.md phải yêu cầu chạy harness sau thay đổi governance"
require_text "$ROOT/AGENTS.md" "github.com/mthang1801/flow-trace-genesis" "khai báo remote chính thức"

note "validating safety rules"
require_text "$AGENTS_DIR/AGENTS.md" "NO AUTO-COMMIT" "cấm tự commit"
require_text "$AGENTS_DIR/AGENTS.md" "NO AUTO-PUBLISH" "cấm tự publish/release"
require_text "$AGENTS_DIR/AGENTS.md" "GROUP 1" "phân nhóm lệnh nguy hiểm cần user duyệt"

note "validating commit rules"
require_text "$AGENTS_DIR/AGENTS.md" "Conventional Commits" "chuẩn commit message"
require_text "$AGENTS_DIR/AGENTS.md" "Co-authored-by: Claude <noreply@anthropic.com>" "co-author trailer Claude"
require_text "$AGENTS_DIR/AGENTS.md" "Co-authored-by: Codex <noreply@openai.com>" "co-author trailer Codex"

note "validating workflow gates"
require_text "$AGENTS_DIR/AGENTS.md" "Executor gate" "cấm viết sản phẩm trước khi plan được duyệt"
require_text "$AGENTS_DIR/AGENTS.md" "Grill gate" "kết thúc việc có ý nghĩa bằng tóm tắt + câu hỏi + recommended answer"
require_text "$AGENTS_DIR/AGENTS.md" "golden-flow gate" "skill sinh ra chỉ Verified sau khi user chấm flow đạt"

note "validating product invariants"
require_text "$AGENTS_DIR/AGENTS.md" "Evidence tier" "Read + file:line là bằng chứng duy nhất"
require_text "$AGENTS_DIR/AGENTS.md" "CORE/PROFILE" "regenerate phải bảo toàn PROFILE"
require_text "$AGENTS_DIR/AGENTS.md" "Degrade gracefully" "thiếu tool thì fallback, không fail cứng"
require_text "$AGENTS_DIR/AGENTS.md" "Sanitize" "profiles nội bộ không lộ khi public"

note "validating change record contract"
require_text "$AGENTS_DIR/changes/README.md" "proposal.md" "change record contract"
require_text "$AGENTS_DIR/changes/README.md" "plans.md" "change record contract"
require_text "$AGENTS_DIR/changes/README.md" "tasks.md" "change record contract"
require_text "$AGENTS_DIR/changes/README.md" "evidence.md" "change record contract"

note "validating progress dashboard"
require_text "$AGENTS_DIR/progress.md" "Activity Log" "dashboard phải có activity log"
require_text "$AGENTS_DIR/progress.md" "Active Change Registry" "dashboard phải có registry"
require_text "$AGENTS_DIR/progress.md" "Execution Queue" "dashboard phải có queue"

note "validating status vocabulary"
for status in Open "In Progress" Blocked Review Done Parked Canceled; do
  require_text "$AGENTS_DIR/AGENTS.md" "$status" "status vocabulary đầy đủ"
done

if [[ "$failures" -gt 0 ]]; then
  note "$failures failure(s)"
  exit 1
fi

note "pass"
