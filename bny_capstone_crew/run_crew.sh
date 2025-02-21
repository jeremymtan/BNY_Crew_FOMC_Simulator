#!/usr/bin/env bash

# Usage:
#   chmod +x run_crew.sh
#   ./run_crew.sh

COUNT=5

MD_FILE="output.md"           
JSON_PREFIX="rate_summary"    
RESULTS_FILE="results.txt"

echo "running 'crew ai run' $COUNT times and extracting JSON..."

for ((i=1; i<=COUNT; i++))
do
  crewai run
  
  echo "[$i] renaming rate_summary.json"
  mv rate_summary.json "${JSON_PREFIX}_${i}.json"
  
  crewai reset-memories --all

  echo "----"
done


echo "processing ALL JSON files in one go."

touch "$RESULTS_FILE"

PYTHON_OUTPUT=$(python Automated_metrics.py)

# append the Python script’s output to results.txt
{
  echo "finishing"
  echo "$PYTHON_OUTPUT"
  echo
} >> "$RESULTS_FILE"

echo "output appended to $RESULTS_FILE."