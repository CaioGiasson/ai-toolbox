#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}✔${NC} $1"; }
log_info() { echo -e "${YELLOW}→${NC} $1"; }
log_err()  { echo -e "${RED}✖${NC} $1"; }

echo ""
echo "╔══════════════════════════════════════╗"
echo "║       claude-sync — sincronizando    ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Garante que ~/.claude existe
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/guidelines"

# ─── Arquivos de contexto raiz ─────────────────────────────────────────────
ROOT_FILES=(CLAUDE.md CONTEXT.md ARCHITECTURE_MAP.md)

for file in "${ROOT_FILES[@]}"; do
  src="$REPO_DIR/$file"
  dst="$CLAUDE_DIR/$file"

  if [[ ! -f "$src" ]]; then
    log_info "Pulando $file (não encontrado no repositório)"
    continue
  fi

  if [[ -f "$dst" ]] && diff -q "$src" "$dst" > /dev/null 2>&1; then
    log_ok "$file já está atualizado"
  else
    cp "$src" "$dst"
    log_ok "$file sincronizado → $dst"
  fi
done

# ─── Guidelines ────────────────────────────────────────────────────────────
GUIDELINES_SRC="$REPO_DIR/guidelines"
GUIDELINES_DST="$CLAUDE_DIR/guidelines"

if [[ -d "$GUIDELINES_SRC" ]]; then
  for file in "$GUIDELINES_SRC"/*.md; do
    [[ -f "$file" ]] || continue
    filename="$(basename "$file")"
    dst="$GUIDELINES_DST/$filename"

    if [[ -f "$dst" ]] && diff -q "$file" "$dst" > /dev/null 2>&1; then
      log_ok "guidelines/$filename já está atualizado"
    else
      cp "$file" "$dst"
      log_ok "guidelines/$filename sincronizado → $dst"
    fi
  done
else
  log_info "Pasta guidelines/ não encontrada no repositório — pulando"
fi

# ─── Skills ────────────────────────────────────────────────────────────────
# Cada skill é um subdiretório com SKILL.md: skills/<nome>/SKILL.md
# Isso é exigido pelo Claude Code para reconhecer skills como slash commands.
SKILLS_SRC="$REPO_DIR/skills"
SKILLS_DST="$CLAUDE_DIR/skills"

if [[ -d "$SKILLS_SRC" ]]; then
  skill_count=0
  for skill_dir in "$SKILLS_SRC"/*/; do
    [[ -d "$skill_dir" ]] || continue           # ignora se não for diretório
    [[ -f "$skill_dir/SKILL.md" ]] || continue  # ignora subdir sem SKILL.md

    skill_name="$(basename "$skill_dir")"
    dst_skill_dir="$SKILLS_DST/$skill_name"
    dst_skill_file="$dst_skill_dir/SKILL.md"

    mkdir -p "$dst_skill_dir"

    if [[ -f "$dst_skill_file" ]] && diff -q "$skill_dir/SKILL.md" "$dst_skill_file" > /dev/null 2>&1; then
      log_ok "skill/$skill_name já está atualizada"
    else
      cp "$skill_dir/SKILL.md" "$dst_skill_file"
      log_ok "skill/$skill_name sincronizada → $dst_skill_file"
      ((skill_count++)) || true
    fi
  done
  [[ $skill_count -eq 0 ]] && log_info "Nenhuma skill nova para sincronizar"
else
  log_info "Pasta skills/ não encontrada no repositório — pulando"
fi

echo ""
echo "Sincronização concluída."
echo ""
