#!/bin/bash
rm ../data/geth/ ../data/history
geth --datadir ../data/ --keystore ../data/keystore/ init ../config/fpm.json
