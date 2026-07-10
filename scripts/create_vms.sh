#!/usr/bin/bash

if [ -f vm_list.csv ]; then
  first_line=true
  while IFS= read -u 3 -r line; do
    if [ "$first_line" = true ]; then
      first_line=false
      continue
    fi
    if [ -n "$line" ]; then
      type=$(echo "$line" | awk -F "," '{print $1}')
      name=$(echo "$line" | awk -F "," '{print $2}')
      vm_name=$(echo "$line" | awk -F "," '{print $3}')
      hash=$(echo "$line" | awk -F "," '{print $4}')
      remote_user=$(echo "$line" | awk -F "," '{print $5}')
      remote_password=$(echo "$line" | awk -F "," '{print $6}')
      img_source=$(echo "$line" | awk -F "," '{print $7}')
      link=$(echo "$line" | awk -F "," '{print $8}')

      case "$type" in
        vagrant)
          echo "Creating virtual machine for vagrant box ${name} with name ${vm_name}..."
          ./new_vagrant.sh -v "$name" -b "$vm_name"
          ;;
        image)
          echo "Creating virtual machine for ${name} with name ${vm_name}..."
          ./new_image_vm.sh -z "$name" -b "$vm_name" -u "$remote_user" -p "$remote_password" -H "$hash" -s "$img_source" -l "$link"
          ;;
        *)
          echo "Unknown type '${type}' for entry '${name}'. Skipping (expected 'vagrant' or 'image')."
          ;;
      esac
    fi
  done 3< vm_list.csv
else
  echo "vm_list.csv not found. Please create a file named vm_list.csv with the list of VMs you want to create, with a header row followed by lines in the format: type,name,vm_name,hash,user,password,source,link"
  echo "For 'vagrant' rows, hash,user,password,source,link are not needed and can be left empty."
fi
