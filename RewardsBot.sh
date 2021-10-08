#!/usr/bin/env bash

cd "${0%/*}" || exit

poetry run python3 ./src/main.py
