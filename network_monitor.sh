#!/bin/bash

log_file="network_status.log"
targets=("google.com" "github.com" "8.8.8.8")

for target in "${targets[@]}"; do
  ping -c 2 "$target" &>/dev/null
  if [ $? -eq 0 ]; then
    latency=$(ping -c 4 "$target" | tail -1 | awk '{print $4}' | cut -d '/' -f 2)
    echo "[$(date)] ✅ $target: UP ($latency ms)" | tee -a "$log_file"
  else
    echo "[$(date)] ❌ $target: DOWN" | tee -a "$log_file"
  fi
done
