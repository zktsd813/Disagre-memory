#!/usr/bin/env python3

"""
   runqemu.py

    Created on: Dec. 15, 2018
        Author: Taekyung Heo <tkheo@casys.kaist.ac.kr>
"""

import argparse
import os
import socket
import subprocess
import paramiko
import signal
from time import sleep

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_memory_option(num_cores, num_nodes, fast_memory, slow_memory):
    option = ""

    if num_nodes == 1:
        if fast_memory != 0:
            memory_size_per_node = fast_memory
            option += " -numa node,cpus=0-%d,memdev=node1mem" % (num_cores-1)
            option += " -object memory-backend-ram,prealloc=on,id=node1mem,size=%dG,host-nodes=0,policy=bind"\
                % (memory_size_per_node)
        else:
            memory_size_per_node = slow_memory
            option += " -numa node,cpus=0-%d,memdev=node1mem" % (num_cores-1)
            option += " -object memory-backend-ram,prealloc=on,id=node1mem,size=%dG,host-nodes=2,policy=bind"\
                % (memory_size_per_node)

    elif num_nodes == 2:
        hostname = socket.gethostname()
        option += " -numa node,cpus=0-%d,memdev=node0mem" % (num_cores-1)
        option += " -numa node,memdev=node1mem"
        option += " -object memory-backend-ram,prealloc=on,id=node0mem,size=%dG,host-nodes=0,policy=bind"\
                % (fast_memory)
        option += " -object memory-backend-ram,prealloc=on,id=node1mem,size=%dG,host-nodes=1,policy=bind"\
                % (slow_memory)

    return option


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-drive_image_path", default="./ubuntu.img")
    parser.add_argument("-ssh_port", type=int, default=2222)
    parser.add_argument("-enable_kvm", type=str2bool, default=True)
    parser.add_argument("-num_cores", type=int, default=12)
    parser.add_argument("-num_nodes", type=int, default=2)
    parser.add_argument("-memory_size", type=int, default=128)
    parser.add_argument("-vnc_port", type=int, default=0)
    parser.add_argument("-serial_port", type=int, default=1234)
    parser.add_argument("-slow_memory", type=int, default=64)
    parser.add_argument("-fast_memory", type=int, default=64)
    parser.add_argument("-use_graphic", type=str2bool, default=False)
    args = parser.parse_args()

    cmd = "qemu-system-x86_64"
    cmd += " -drive file=%s,index=0,media=disk,format=raw" % (args.drive_image_path)
    cmd += " -netdev user,id=hostnet0,hostfwd=tcp::%d-:22" % (args.ssh_port)
    cmd += " -device virtio-net-pci,netdev=hostnet0,id=net0,bus=pci.0,addr=0x3"
    if args.enable_kvm:
        cmd += " -enable-kvm"
    cmd += " -smp %d" % (args.num_cores)
    cmd += " -cpu host"
    if (args.fast_memory + args.slow_memory) != args.memory_size:
       return 
    cmd += " -m %dG" % (args.memory_size)
    cmd += get_memory_option(args.num_cores, args.num_nodes, args.fast_memory, args.slow_memory)
    cmd += " -vnc :%d" % (args.vnc_port)
    cmd += " -serial tcp::%d,server,nowait" % (args.serial_port)
    if not args.use_graphic:
        cmd += " -nographic"

    print(cmd)
    cmd = "numactl --cpunodebind=0 %s" % (cmd)
    os.system(cmd)

if __name__ == '__main__':
    main()
