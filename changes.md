## Summary of changes

- `new_vagrant.sh` now creates the VM, collects MAC/IP, calls `get_os_info.py` (LLM) and automatically updates the `vm_info` JSON and the traffic folder.
- `os_info.py` provides both CLI (`cli_mode.py`) and GUI (`gui_mode.py`) viewers to inspect/edit `os_info.json` and `commands_execute.json`.
- All scripts are adapted to run as user `vmuser` and use paths under `~/data/virtual_machines/`.
- `update_info_file.sh` validates the VM, merges fields into the JSON metadata and creates the `os_family__os_type__os_version` traffic folder.