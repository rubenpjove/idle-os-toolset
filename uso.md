### Installation and Setup

All data and files related to this project (toolset code, VM definitions, traffic captures, etc.) are stored under a single directory, which will also be used as the home directory of the `vmuser` user. In the examples below we use `/mnt/ntfms` as that directory; if you prefer a different location, replace `/mnt/ntfms` with your own path consistently.

Optionally, define an environment variable to refer to this directory more easily:

```bash
export TOOLSET_ROOT=/mnt/ntfms   # change this if you use a different root path
```

#### 1. Install VirtualBox, Extension Pack, Vagrant and jq

```bash
apt install jq virtualbox

VB_VER=$(VBoxManage -v | cut -d'r' -f1)
wget "https://download.virtualbox.org/virtualbox/${VB_VER}/Oracle_VM_VirtualBox_Extension_Pack-${VB_VER}.vbox-extpack"
VBoxManage extpack install "Oracle_VM_VirtualBox_Extension_Pack-${VB_VER}.vbox-extpack"

wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
apt update && sudo apt install vagrant
```

#### 2. Install Python dependencies

Install the Python packages required by the scripts:

- `pyshark, pandas and tshark`: for processing network traffic captures and applying HTTP filters.
- `litellm`: for sending requests to the LLM provider (for example, Groq) used to classify or enrich OS information.
- `python3-tk`: to enable the graphical interface used by some scripts.
- `python-is-python3`: to have the `python` command point to Python 3.

```bash
pip install pyshark
pip install litellm
pip install pandas
apt install python3-tk
apt install python-is-python3
apt install tshark
```

In the `get_os_info.py` file you will find a template for the requests that use the Groq model. You must insert your API key in the corresponding environment variable. If you use a different model or provider, update both the model configuration and the environment variable name to match your new provider.

#### 3. Install NEMEA and ipfixprobe

The toolkit can integrate with `ipfixprobe` and NEMEA to process IPFIX/flow records. Install the required build dependencies and compile the tools as follows:

```bash
apt-get install -y gawk bc autoconf automake gcc g++ libtool libxml2-dev make pkg-config libpcap-dev libidn11-dev bison flex libpcap

cd "$TOOLSET_ROOT"

git clone --recursive https://github.com/CESNET/nemea
cd nemea

./bootstrap.sh
./configure
make
make install


apt install git make cmake g++ pkg-config rpm
apt install libunwind-dev liblz4-dev libssl-dev libfuse3-dev libatomic1

cd ..
git clone https://github.com/CESNET/ipfixprobe.git

cd ipfixprobe
mkdir build && cd build

mkdir -p /usr/bin/nemea/
ln -s /usr/local/bin/ur_processor.sh /usr/bin/nemea/ur_processor.sh

cmake .. -DENABLE_NEMEA=ON -DENABLE_INPUT_PCAP=ON -DENABLE_OUTPUT_UNIREC=ON
make -j"$(nproc)"
make install

cd ..
```

After this step, `ipfixprobe` and the NEMEA components will be available system-wide and can be used together with the scripts to process captured traffic.

#### 4. Create the `vmuser` user

Once all packages are installed, create the `vmuser` user (without a password). The home directory of `vmuser` must be the directory where you want to store everything related to this project (toolkit files, virtual machines, traffic captures, etc.). This directory must match the value you chose for `TOOLSET_ROOT`.

```bash
adduser vmuser --gecos --home "$TOOLSET_ROOT"
```

This user will own the data and scripts used to manage the virtual machines.

#### 5. Configure passwordless `su` for `vmuser`

To allow switching to `vmuser` without a password using `su`, modify PAM so that `vmuser` is exempt from authentication. Add the following line at the beginning of `/etc/pam.d/su`:

```bash
sed -i '1iauth sufficient pam_succeed_if.so user = vmuser' /etc/pam.d/su
```

This change only affects the `su` command when targeting `vmuser`.

#### 6. Install Android communication tools

To communicate with Android virtual machines and devices, install the following:

```bash
apt install android-tools-adb

su - vmuser -c "vagrant plugin install vagrant-dummy-communicator"
```

The `vagrant-dummy-communicator` plugin allows Vagrant to manage Android-based boxes that do not expose a standard SSH interface.

#### 7. Create data directories and set permissions

Create the data directory structure where all files related to these scripts will be stored, and give `vmuser` read and write permissions:

```bash
mkdir -p "$TOOLSET_ROOT"/data/virtual_machines/vagrant/
mkdir -p "$TOOLSET_ROOT"/data/virtual_machines/traffic/
mkdir -p "$TOOLSET_ROOT"/data/virtual_machines/scripts/
mkdir -p "$TOOLSET_ROOT"/data/virtual_machines/vm_info/
mkdir -p "$TOOLSET_ROOT"/data/virtual_machines/os_info/

cp scripts/* "$TOOLSET_ROOT"/data/virtual_machines/scripts/

chown -R vmuser:vmuser "$TOOLSET_ROOT"/

usermod -aG virtualbox vmuser
```

After this step, `vmuser` will own the entire project root directory (for example, `/mnt/ntfms`) and will belong to the `virtualbox` group, which allows it to manage VirtualBox virtual machines properly.

#### 8. Make shell scripts executable

Finally, give execution permissions to all shell scripts in the `scripts` directory:

```bash
chmod +x ./data/virtual_machines/scripts/*.sh
```

At this point, the environment should be ready to use the toolkit scripts in both CLI and GUI modes.

