#!/bin/bash

log_dir="/var/log"
output_file="$(date +%Y-%m-%d)_log_report.txt"

if [[ ! -d "$log_dir" ]]; then
  echo "Error: Log directory missing!" >&2
  exit 1
fi

grep -r --color=always -i "error\|warning\|fail" "$log_dir" > "$output_file" 2>/dev/null

if [ -s "$output_file" ]; then
  echo "🔍 Log report generated: $output_file"
else
  echo "✅ No errors found in logs!"
  rm -f "$output_file"
fi
