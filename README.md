# Disaggregated Memory System experiment
The purpose of this project is to understand the effect of disaggregated memory when limited amount of local memory is given.
### 1. Prepare source code
```
$ git clone https://github.com/zktsd813/Disagre-memory.git
$ git submodule update --init --recursive
```

### 2. Install QEMU
```
$ cd QEMU
$ sudo sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list
$ sudo apt -y update && sudo apt -y build-dep qemu
$ mkdir build
$ cd build
$ ../configure --target-list=x86_64-softmmu
$ make -j$(nproc)
$ sudo make install
```

### 3. Create a Guest Virtual Machine
```
$ wget https://releases.ubuntu.com/20.04.6/ubuntu-20.04.6-live-server-amd64.iso
$ qemu-img create ubuntu.img 100G
$ qemu-system-x86_64 \
  -enable-kvm \
  -drive file=ubuntu.img,index=0,media=disk,format=raw \
  -netdev user,id=hostnet0,hostfwd=tcp::2222-:22 \
  -device virtio-net-pci,netdev=hostnet0,id=net0,bus=pci.0,addr=0x3 \
  -m 4096 \
  -boot d -cdrom ./ubuntu-20.04.6-live-server-amd64.iso \
  -vnc :0
```
You should install ubuntu image through VNC by yourself.<br>
After you have executed last command, you can connect the guest machine with VNC port.<br>
You should remember your name and password when installing ubuntu image.


### 3. Setting Guest Machine
```
# 1. Start guest machine
$ python3 run_qemu.py

You should open another terminal to connect.
# 2. Connect VM with SSH
$ ssh <your name>@localhost -p2222

# 3. Change supervisor password
$ sudo passwd root
$ Type password you want

# 4. Permit sudo login through ssh
$ sudo vim /etc/ssh/sshd_config
$ #PermitRootLogin prohibit-password -> PermitRootLogin y

# 5. Restart service
$ sudo service sshd restart
```

### 4. Install TPP on Guest Machine
```
# 1. Connect to VM through root password
$ ssh root@localhost -p2222

# 2. Install required packages
$ apt install -y build-essential libncurses5-dev libssl-dev bc bison flex libelf-dev

# 3. Cloning linux kernel with TPP (This will be updated through git)
$ git clone https://github.com/zktsd813/TPP-5.15.git

# 4. Copy current configuration to kernel folder
$ cd TPP-5.15
$ cp /boot/config-$(uname -r) .config
$ make olddefconfig

# 5. Compile the kernel
$ make all -j$(nproc)

# 6. Install kernel
$ make INSTALL_MOD_STRIP=1 modules_install -j$(proc)
$ make install

# 7. reboot and check TPP is installled
$ reboot now
$ uname -r 
"uname -r" should print "5.15xxx"
```