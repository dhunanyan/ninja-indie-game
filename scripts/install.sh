rm -rf venv

pip install virtualenv
python -m venv venv

source venv/Scripts/activate
./venv/Scripts/python.exe -m pip install -U --upgrade pip

pip install -r requirements.txt