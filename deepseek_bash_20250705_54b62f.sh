#!/bin/bash

backup_source="$HOME/Documents"
backup_dest="$HOME/Backups"
timestamp=$(date +%Y%m%d_%H%M%S)

if [[ ! -d "$backup_source" ]]; then
  echo "Error: Source directory missing!" >&2
  exit 1
fi

mkdir -p "$backup_dest"
tar -czf "$backup_dest/backup_$timestamp.tar.gz" "$backup_source" 2>/dev/null

if [ $? -eq 0 ]; then
  echo "📦 Backup created: $backup_dest/backup_$timestamp.tar.gz"
else
  echo "❌ Backup failed!" >&2
fi