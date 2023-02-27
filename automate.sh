#!/bin/bash

source /home/marcus/.bashrc
source /home/marcus/anaconda3/bin/activate gisbob


cd /home/marcus/EACODE/WAVE

python datea.py

python wavesauto.py
python bwavesauto.py

source /home/marcus/anaconda3/bin/activate gis

python uploadWWdayn.py
