#!/bin/bash

for i in {0..19}; do
  CHUNK_NUMBER=$i envsubst < job.yaml | kubectl apply -f -
done