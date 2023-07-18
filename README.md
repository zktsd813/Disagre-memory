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
```