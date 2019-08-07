#!/usr/bin/env bash

VENV=venv

if [ ! -d "$VENV" ]
then

    PYTHON=`which python3.7`

    if [ ! -f $PYTHON ]
    then
        echo "could not find python 3.7"
    fi
    virtualenv -p $PYTHON $VENV

fi

. $VENV/bin/activate

pip install -r requirements.txt