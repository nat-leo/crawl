# !/bin/bash
python -m venv .venv && source .venv/bin/activate   # (on Windows: .venv\Scripts\activate)
python -m pip install -U pip
python -m pip install -e . ipykernel
