#!/bin/sh

. .venv/bin/activate

python3 -m venv .venv
pip3 install -r requirements/dev.txt

python3 -m coverage run --rcfile=.coveragerc -m py.test -c pytest.ini tests/unit