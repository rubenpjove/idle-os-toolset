# Changelog

All notable changes in this repository are documented in this file.

### Added

- New VM creation from non-Vagrant images:
  - `scripts/new_image_vm.sh` to create a VM from a local `.zip`/`.7z` file containing an OVA, an exported VBOX folder, or a VDI disk, mirroring the `new_vagrant.sh` workflow for images downloaded from sites like osboxes.org or linuxvmimages.com.
  - `scripts/get_os_info_images.py`, the OS-detection counterpart to `get_os_info.py` for image-based VMs, connecting via SSH/WinRM/ADB.
- New fleet management helpers:
  - `scripts/boot_vm.sh` and `scripts/shutdown_vm.sh` to start/stop VMs without touching traffic capture or pcap processing, used in nmap scripts.
  - `scripts/resize_vm.sh` to change the CPU count and/or RAM of one or more powered-off VMs.
  - `scripts/set_network.sh` to switch a VM's NIC 1 between host-only and NAT networking.
  - `scripts/get_vms_config.sh` to list CPUs, memory, and NIC 1 mode for all registered VMs, with totals.
  - `scripts/check_vm_macs.sh` to detect duplicate NIC 1 MAC addresses across VMs and optionally randomize them.
- New nmap scripts:
  - `scripts/nmap.sh` to match running VMs to their IP (via ARP scan + MAC lookup) and run `nmap -O` against them, comparing the result to the VM's known ground-truth OS.
  - `scripts/nmap_batch_scan.sh` to orchestrate `nmap.sh` over VM ranges: boot the range, scan it, then shut it down before moving to the next range.
- New captured-data statistics helper: `scripts/get_pcaps_stats.sh`, computing per-pcap duration, packet count, size, and protocol hierarchy, matched against each VM's OS info.
- New script `scripts/capture_loop.sh` that allows to run `start_vm.sh` over several VM ranges one batch at a time, waiting for each batch to finish capturing and auto-stop before starting the next.
- New VM creation flow: `scripts/vm_list.csv` lists both Vagrant boxes and non-Vagrant images to create, distinguished by a `type` column. `scripts/get_vm_names.py` reads this file and picks the right prompt per row based on `type`, and `scripts/create_VMs.sh` reads it and calls `new_vagrant.sh` or `new_image_vm.sh` per row, also based on `type`.

### Changed

- `scripts/start_vm.sh` can now also select VMs by position in the full VM list using an `N-M` range, and gained `-w`/`--wait` to control the delay between starting each VM in a batch (default: 5 seconds).
- `scripts/stop_vm.sh` now strips malformed, short, or unreassembled packets from the pcap (via `tshark`) before finalizing the capture.
- `scripts/get_vm_names.py` now takes a `-m`/`--mode` option (`vagrant`, the default, or `image`), so besides suggesting VM names for `vagrant_list.txt` entries it can also fill in blank `vm_name` columns of `image_list.csv` based on each row's `zip` file name.
- `README.md` and `INSTALL.md` were updated with usage instructions and installation requirements for all the new scripts.
- `scripts/get_os_info.py` had its prompt improved for generating the OS-detection commands.

### Removed

- `scripts/vagrant_list.txt` and `scripts/create_multiple_boxes.sh`.

### Notes

- The Nmap fingerprinting pipeline support evaluating how well Nmap's own OS detection compares to the toolset's known ground-truth OS metadata, and give visibility into the size/composition of already-captured traffic.
- The new fleet-management scripts (`resize_vm.sh`, `set_network.sh`, `get_vms_config.sh`, `check_vm_macs.sh`) make it practical to reconfigure and audit large numbers of VMs at once, instead of doing it VM by VM through the VirtualBox GUI.
- The network traffic capture set was expanded with 19 new Android virtual machines, and all VMs from previous commits were combined into a single fleet.

