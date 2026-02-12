### Instalación



Para poder ejecutar los scripts necesitamos un sistema operativo Linux que tenga instalado tanto VirtualBox como Vagrant junto al comando jq.



```

apt install virtualbox vagrant jq

```



Además debemos instalar los el módulo ``pyshark`` de Python.



```

pip install pyshark

```



Junto a la herramienta ipfixprobe.



```

apt-get install -y gawk bc autoconf automake gcc g++ libtool libxml2-dev make pkg-config libpcap-dev libidn11-dev bison flex

git clone --recursive https://github.com/CESNET/nemea

cd nemea

./bootstrap.sh

./configure

make

make install



apt install git make cmake g++ pkg-config rpm

apt install libunwind-dev liblz4-dev libssl-dev libfuse3-dev libatomic1



git clone https://github.com/CESNET/ipfixprobe.git

cd ipfixprobe

mkdir build && cd build

mkdir -p /usr/bin/nemea/

ln -s /usr/local/bin/ur_processor.sh /usr/bin/nemea/ur_processor.sh

cmake .. -DENABLE_NEMEA=ON DENABLE_OUTPUT_UNIREC=ON

make -j$(nproc)

make install

```



Una vez instaldo todos los paquetes debemos crear un usuario vmuser sin contraseña.



```

adduser vmuser --gecos

```



Modificamos el PAM para que no solicite la contraseña al hacer su. Añademos al principio del fichero ``/etc/pam.d/su``



```

auth sufficient pam_succeed_if.so user = vmuser

```





Además hay que crear la carpeta /data y todos sus directorios en los cuales se almacenarán todos los ficheros relacionados con estos scripts. Además, hay que dar permisos de escritura y lectura al usuario vmuser.



```

mkdir -p /data/virtual_machines/vagrant/

mkdir -p /data/virtual_machines/traffic/

mkdir -p /data/virtual_machines/scripts/

mkdir -p /data/virtual_machines/vm_info/

cp scripts/* /data/virtual_machines/scripts/

chown -R vmuser:vmuser /data

chmod -R 770 /data

```



Una vez hecho los pasos anteriores debemos dar permiso de ejecución a todos los scripts de la carpeta ``scripts``



```

chmod +x /data/virtual_machines/scripts/*.sh

```



 