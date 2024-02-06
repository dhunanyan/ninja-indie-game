export PYGAME_HIDE_SUPPORT_PROMPT=1

if [[ -z "$IS_EDITOR" ]]; then
  python -u game.py
  exit
fi

python -u editor.py