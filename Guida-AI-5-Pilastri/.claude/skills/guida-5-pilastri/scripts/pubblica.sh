#!/usr/bin/env bash
# Pubblica solo la guida su GitHub Pages e aspetta che sia online.
# Uso: bash .claude/skills/guida-5-pilastri/scripts/pubblica.sh "messaggio del commit"
set -e
MSG="${1:?Serve il messaggio del commit}"
REPO="$(cd "$(dirname "$0")/../../../.." && pwd)"          # .../Consulenza-ai/Guida-AI-5-Pilastri
ROOT="$(cd "$REPO/.." && pwd)"                              # .../Consulenza-ai
FILE="Guida-AI-5-Pilastri/Guida-AI-5-Pilastri.html"
URL="https://puntospillo.github.io/Consulenza-ai/$FILE"

cd "$ROOT"
python3 "$REPO/.claude/skills/guida-5-pilastri/scripts/verifica.py"
REV="$(grep -o "const REV = '[^']*'" "$FILE" | head -1 | cut -d"'" -f2)"
echo "Pubblico la Rev. $REV"

git add "$FILE"
git commit -q -m "$MSG

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push origin main | tail -1

for i in $(seq 1 18); do
  if curl -s "$URL?v=$i$RANDOM" | grep -q "const REV = '$REV'"; then echo "✓ online: $URL"; exit 0; fi
  echo "attendo la pubblicazione ($i)…"
  perl -e 'select(undef,undef,undef,10)'
done
echo "⚠ non ancora online: ricontrolla fra qualche minuto $URL"
