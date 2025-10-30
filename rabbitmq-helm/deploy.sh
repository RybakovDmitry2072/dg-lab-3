#!/bin/bash

set -a
source .env
set +a

helm secrets --evaluate-templates -b vals  \
     upgrade --install \
     my-rabbitmq oci://registry-1.docker.io/cloudpirates/rabbitmq \
       -n rabbitmq --create-namespace \
       -f values.yaml