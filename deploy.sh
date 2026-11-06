#!/usr/bin/env bash
# Bygger reliningkoll och publicerar till BÅDA värdarna.
#   main     -> Vercel (produktion: reliningkoll.vercel.app)
#   gh-pages -> GitHub Pages (förhandsvisning: oskarhellmer-dev.github.io/reliningkoll)
#
# Användning:  ./deploy.sh "kort beskrivning av ändringen"
set -euo pipefail
cd /home/clawd/reliningkoll
PY=/usr/bin/python3
MSG="${1:-Uppdatering}"

echo "== 1/4 bygger sajten =="
$PY build_all.py | tail -1
$PY deploy_preview.py | tail -1

URL=$(git remote get-url origin)

echo "== 2/4 main -> Vercel =="
git add -A
if git diff --cached --quiet; then
  echo "   inga ändringar att committa"
else
  git -c user.email="oskarhellmer@gmail.com" -c user.name="oskarhellmer-dev" commit -q -m "$MSG"
fi
git push origin main

echo "== 3/4 _preview -> gh-pages =="
cd _preview
rm -rf .git
git init -q
git checkout -q -b gh-pages
git add -A
git -c user.email="oskarhellmer@gmail.com" -c user.name="oskarhellmer-dev" commit -q -m "$MSG"
git remote add origin "$URL"
git push -q -f origin gh-pages

echo "== 4/4 klart =="
echo "   Vercel (prod):   https://reliningkoll.vercel.app"
echo "   GH Pages (prev): https://oskarhellmer-dev.github.io/reliningkoll"
