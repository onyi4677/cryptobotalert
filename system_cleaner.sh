#!/bin/bash

# Safety check for root permissions
if [[ $EUID -ne 0 ]]; then
  echo "⚠️  Run as root for full cleanup!" 
  read -p "Proceed without root? (y/n) " -n 1 -r
  [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
  echo
fi

# Clean user cache
rm -rfv ~/.cache/* 

# System cleanup (if root)
if [[ $EUID -eq 0 ]]; then
  apt clean -y
  journalctl --vacuum-time=2d
else
  echo "ⓘ  Skipping system-level cleanup (run as root for full clean)"
fi

echo "♻️  System cleaned!"
