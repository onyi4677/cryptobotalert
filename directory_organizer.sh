#!/bin/bash

target_dir="$HOME/Downloads"
if [[ ! -d "$target_dir" ]]; then
  echo "Error: Downloads directory not found!" >&2
  exit 1
fi

mkdir -p "$target_dir/Images" "$target_dir/Documents" "$target_dir/Archives" "$target_dir/Code"

mv -v "$target_dir"/*.{jpg,jpeg,png,gif,webp} "$target_dir/Images" 2>/dev/null
mv -v "$target_dir"/*.{pdf,docx,txt,md,odt} "$target_dir/Documents" 2>/dev/null
mv -v "$target_dir"/*.{zip,tar.gz,rar,7z} "$target_dir/Archives" 2>/dev/null
mv -v "$target_dir"/*.{sh,py,js,cpp,html,css} "$target_dir/Code" 2>/dev/null

echo "✅ Downloads organized successfully!"
