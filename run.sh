#!/bin/bash

# for ((i=0; i<40; i+=10)); do
#   echo "Submitting jobs $i to $((i+9))"

#   for ((j=i; j<i+10 && j<40; j++)); do
#     CHUNK_NUMBER=$j envsubst < job.yaml | kubectl apply -f -
#   done

#   echo "Waiting for jobs $i to $((i+9)) to complete..."

#   for ((j=i; j<i+10 && j<40; j++)); do
#     kubectl wait --for=condition=complete --timeout=600s job/scraper-job-$j
#   done

#   echo "Batch $i to $((i+9)) complete."
# done



start=0
end=5

for ((i=start; i<=end; i++)); do
  echo "🔹 Processing CHUNK_NUMBER=$i"

  CHUNK_NUMBER=$i envsubst < job.yaml | kubectl apply -f -

  echo "⏳ Waiting for job scraper-job-$i to complete..."
  kubectl wait --for=condition=complete --timeout=600s job/scraper-job-$i

  echo "✅ Job scraper-job-$i completed."
done