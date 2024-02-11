export PYGAME_HIDE_SUPPORT_PROMPT=1

if [[ -n "$IS_EDITOR" ]]; then
  python -u ./editor.py
  exit
fi

if [[ -n "$IS_MULTIPLAYER" ]]; then
  python -u ./server.py
  exit
fi

python -u ./game.py
