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
echo "║       ai-toolbox — sincronizando     ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Garante que ~/.claude existe
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/guidelines"

# ─── Arquivos de contexto raiz ─────────────────────────────────────────────
ROOT_FILES=(CLAUDE.md CONTEXT.md)

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

# ─── Limpeza de itens legados ──────────────────────────────────────────────
# legacy.txt lista skills/guidelines removidas ou renomeadas no repositório.
# Só os nomes listados são apagados de ~/.claude; nada mais é tocado.
LEGACY_FILE="$REPO_DIR/legacy.txt"

if [[ -f "$LEGACY_FILE" ]]; then
  legacy_count=0
  while read -r kind name _; do
    [[ -z "${kind:-}" || "$kind" == \#* ]] && continue

    # Nome simples apenas: sem caminhos, sem "..", sem curingas
    if [[ -z "${name:-}" || ! "$name" =~ ^[A-Za-z0-9._-]+$ || "$name" == .* ]]; then
      log_err "legacy.txt: entrada inválida ignorada → $kind ${name:-}"
      continue
    fi

    case "$kind" in
      skill)
        src="$REPO_DIR/skills/$name"; dst="$CLAUDE_DIR/skills/$name" ;;
      guideline)
        src="$REPO_DIR/guidelines/$name"; dst="$CLAUDE_DIR/guidelines/$name" ;;
      *)
        log_err "legacy.txt: tipo desconhecido ignorado → $kind $name"
        continue ;;
    esac

    if [[ -e "$src" ]]; then
      log_info "legacy.txt: $kind/$name ainda existe no repositório — não será apagado"
      continue
    fi

    if [[ -e "$dst" ]]; then
      rm -rf -- "$dst"
      log_ok "legado removido → $dst"
      ((legacy_count++)) || true
    fi
  done < "$LEGACY_FILE"
  [[ $legacy_count -eq 0 ]] && log_info "Nenhum item legado para remover"
fi

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

    # Copia SKILL.md e arquivos de apoio (ex.: references/), preservando a estrutura
    changed=0
    while IFS= read -r -d '' src_file; do
      rel="${src_file#"$skill_dir"}"
      dst_file="$dst_skill_dir/$rel"
      if [[ -f "$dst_file" ]] && diff -q "$src_file" "$dst_file" > /dev/null 2>&1; then
        continue
      fi
      mkdir -p "$(dirname "$dst_file")"
      cp "$src_file" "$dst_file"
      changed=1
    done < <(find "$skill_dir" -type f -print0)

    if [[ $changed -eq 0 ]]; then
      log_ok "skill/$skill_name já está atualizada"
    else
      log_ok "skill/$skill_name sincronizada → $dst_skill_dir"
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
