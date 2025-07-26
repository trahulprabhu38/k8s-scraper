#!/bin/bash

# Apply PVC once
kubectl apply -f k8s/pvc.yaml

# Loop to submit one job per chunk
for i in {0..9}; do
  export CHUNK_NUMBER=$i
  envsubst < k8s/scraper-job.yaml | kubectl apply -f -
done
