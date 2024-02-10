VENV_PATH="${VENV_PATH:-venv}"
BUILD_PATH=./build
DIST_PATH=./dist
GAME_SPEC_PATH=./game.spec

VENV_PATH=$VENV_PATH sh ./scripts/install.sh

rm -rf $BUILD_PATH $DIST_PATH $GAME_SPEC_PATH

echo "Y" | "./$VENV_PATH/Scripts/python.exe" -m PyInstaller ./game.py --noconsole
