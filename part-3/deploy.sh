#!/bin/bash

set -a
source .env
set +a

helm secrets --evaluate-templates -b vals  \
     upgrade --install \
     app app \
       -n lab --create-namespace \
       -f app/values.yaml