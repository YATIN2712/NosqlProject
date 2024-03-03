#!/bin/bash

read -p "Enter start date (day-month-year): " START_DATE
read -p "Enter end date (day-month-year): " END_DATE

{
  for file in ../Timeline_news/*.txt; do
      python3 mapper.py "$file" &
  done
  wait
} | python3 reducer.py "$START_DATE" "$END_DATE"> result.txt
