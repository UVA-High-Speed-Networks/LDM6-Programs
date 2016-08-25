#!/bin/bash

date '+%X' >> log_cpu_mem_usage.txt
ps -eo pcpu,pmem,rsz,vsz,time,time,pid,args | grep "ldmd" >> log_cpu_mem_usage.txt

