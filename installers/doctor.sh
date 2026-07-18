#!/usr/bin/env bash
# doctor.sh — check (and optionally install) the tools flow-trace-genesis can use.
#
#   ./installers/doctor.sh            # read-only scan: what's present, what's missed, how to fix
#   ./installers/doctor.sh --install  # interactively install USER-SPACE tools (npm/pip) — asks per tool
#
# Policy: system packages (python3, ripgrep, node, go...) are NEVER installed by this
# script — it only prints the exact command for you to run (a third-party script
# invoking sudo on its own is a red flag). User-space installs (pip --user, npm -g)
# run only after an explicit per-tool y/N confirmation. The plugin itself never
# installs anything: degrade-gracefully stays the default.
set -uo pipefail

MODE="doctor"
case "${1:-}" in
  --install) MODE="install" ;;
  -h|--help) sed -n '2,11p' "$0"; exit 0 ;;
  "") ;;
  *) echo "unknown arg: $1 (use --install or --help)" >&2; exit 1 ;;
esac

# ── detect system package manager (for printed suggestions only) ──
if   command -v dnf     >/dev/null 2>&1; then SYS="sudo dnf install -y"
elif command -v apt-get >/dev/null 2>&1; then SYS="sudo apt-get install -y"
elif command -v pacman  >/dev/null 2>&1; then SYS="sudo pacman -S --noconfirm"
elif command -v zypper  >/dev/null 2>&1; then SYS="sudo zypper install -y"
elif command -v brew    >/dev/null 2>&1; then SYS="brew install"
else SYS="<your package manager> install"; fi

GREEN=$'\033[32m'; RED=$'\033[31m'; DIM=$'\033[2m'; BOLD=$'\033[1m'; RST=$'\033[0m'
REQUIRED_MISSING=0
declare -a INSTALL_NAMES INSTALL_CMDS

row() { # row <ok:0|1> <required:0|1> <name> <tier> <note>
  local mark note
  if [ "$1" = 0 ]; then mark="${GREEN}[ OK ]${RST}"; note="$5"
  else
    mark="${RED}[MISS]${RST}"; note="$5"
    [ "$2" = 1 ] && REQUIRED_MISSING=1
  fi
  printf '%b %-28s %-10s %s\n' "$mark" "$3" "$4" "$note"
}

offer() { # offer <name> <install-cmd> — queue a user-space install candidate
  INSTALL_NAMES+=("$1"); INSTALL_CMDS+=("$2")
}

echo "${BOLD}flow-trace-genesis doctor${RST} — tool inventory ($(date +%F))"
echo "${DIM}Tiers: required = HTML render breaks without it · trace = better evidence/speed · optional = extra sections/ingest${RST}"
echo

# ── required ──
if command -v python3 >/dev/null 2>&1; then
  row 0 1 "python3" "required" "$(python3 --version 2>&1)"
  if python3 -c 'import yaml' >/dev/null 2>&1; then
    row 0 1 "PyYAML" "required" "import yaml OK"
  else
    row 1 1 "PyYAML" "required" "fix: python3 -m pip install --user pyyaml"
    offer "PyYAML" "python3 -m pip install --user pyyaml"
  fi
else
  row 1 1 "python3" "required" "fix: $SYS python3  (then re-run doctor for PyYAML)"
fi

# ── trace (Evidence tier) ──
if command -v rg >/dev/null 2>&1; then row 0 0 "ripgrep (rg)" "trace" "$(rg --version | head -1)"
else row 1 0 "ripgrep (rg)" "trace" "falls back to grep · fix: $SYS ripgrep"; fi

if command -v ast-grep >/dev/null 2>&1 || command -v sg >/dev/null 2>&1; then
  row 0 0 "ast-grep" "trace" "structural search available"
else
  row 1 0 "ast-grep" "trace" "falls back to grep · fix: npm install -g @ast-grep/cli"
  offer "ast-grep" "npm install -g @ast-grep/cli"
fi

if command -v uv >/dev/null 2>&1 || command -v uvx >/dev/null 2>&1; then
  row 0 0 "uv/uvx" "trace" "Serena + MarkItDown + Docling MCP run on demand via uvx"
else
  row 1 0 "uv/uvx" "trace" "MCP bundle (.mcp.json) unavailable · fix: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

if command -v gopls >/dev/null 2>&1; then row 0 0 "gopls" "trace" "Go LSP available"
elif command -v go >/dev/null 2>&1; then row 1 0 "gopls" "trace" "Go projects only · fix: go install golang.org/x/tools/gopls@latest"
else row 1 0 "gopls" "trace" "Go projects only (no go toolchain on this machine — skip unless tracing Go)"; fi

if command -v typescript-language-server >/dev/null 2>&1; then
  row 0 0 "typescript-language-server" "trace" "TS/JS LSP available"
else
  row 1 0 "typescript-language-server" "trace" "TS/JS projects only · fix: npm install -g typescript-language-server typescript"
  offer "typescript-language-server" "npm install -g typescript-language-server typescript"
fi

# ── optional (Candidate + Ingest tiers) ──
if command -v npx >/dev/null 2>&1; then
  row 0 0 "node/npx" "optional" "knowledge-graph section runs GitNexus via npx on demand"
else
  row 1 0 "node/npx" "optional" "handbook loses the interactive KG section · fix: $SYS nodejs"
fi

echo
if [ "$REQUIRED_MISSING" = 1 ]; then
  echo "${RED}${BOLD}Required tools missing${RST} — the HTML render pipeline will not work until fixed."
else
  echo "${GREEN}${BOLD}All required tools present${RST} — everything else only adds depth, the main flow works."
fi

# ── interactive user-space install ──
if [ "$MODE" = "install" ]; then
  echo
  if [ "${#INSTALL_NAMES[@]}" = 0 ]; then
    echo "Nothing installable in user-space is missing. System tools (if any) are listed above with their commands."
  else
    echo "${BOLD}User-space installs${RST} (pip --user / npm -g — no sudo run by this script):"
    for i in "${!INSTALL_NAMES[@]}"; do
      name="${INSTALL_NAMES[$i]}"; cmd="${INSTALL_CMDS[$i]}"
      printf '\n  %s\n  $ %s\n' "$name" "$cmd"
      printf '  Install? [y/N] '
      read -r ans </dev/tty 2>/dev/null || ans=""
      case "$ans" in
        y|Y|yes)
          if eval "$cmd"; then echo "  ${GREEN}installed${RST}"
          else echo "  ${RED}failed${RST} — plugin degrades gracefully without it (npm -g EACCES? use nvm or set npm prefix to \$HOME)"; fi ;;
        *) echo "  skipped" ;;
      esac
    done
  fi
fi

[ "$REQUIRED_MISSING" = 1 ] && exit 1 || exit 0
