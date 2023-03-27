#!/usr/bin/bash

if [ ! -d "./env" ] ; then
  virtualenv env
  source env/scripts/activate
  pip install -r requirements.txt
else
  source env/scripts/activate
fi

python search.py $*