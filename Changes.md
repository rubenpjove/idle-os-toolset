## Summary of changes

- `new_vagrant.sh` now creates the VM, collects MAC/IP, calls `get_os_info.py` (LLM) and automatically executes `update_info_file.sh` with the info obtained from the LLM. This info includes OS_Family, Os_Type and Os_Version. It now also has compatibility with macOS.
- `os_info.py` provides both CLI (`cli_mode.py`) and GUI (`gui_mode.py`) viewers to inspect/edit the info obtained from the LLM.
- Also added `get_vm_names.py` and `create_multiple_boxes.sh` to automate the creation of virtual machines from Vagrant boxes.
- All scripts are adapted to run as user `vmuser` and use paths under `~/data/virtual_machines/`.
