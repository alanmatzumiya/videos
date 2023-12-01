#!/bin/bash


if ! [ -d venv ]; then

    virtualenv venv

fi

if [[ -f requirements.txt ]]; then

    source venv/bin/activate && pip install -r requirements.txt

fi