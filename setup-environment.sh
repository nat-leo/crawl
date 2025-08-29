# !/bin/bash
python -m venv crawl-venv
source crawl-venv/bin/activate   # (on Windows: .venv\Scripts\activate)
python -m pip install -U pip
python -m pip install -e .

python -m pip install notebook
jupyter notebook