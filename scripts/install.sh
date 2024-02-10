VENV_PATH="${VENV_PATH:-venv}"

if [ ! -d "$VENV_PATH" ]; then
  pip install virtualenv
  python -m venv $VENV_PATH
fi

source $VENV_PATH/Scripts/activate
"./$VENV_PATH/Scripts/python.exe" -m pip install -U --upgrade pip

python -m pip install -r requirements.txt -U