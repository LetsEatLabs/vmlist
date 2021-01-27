import os
import subprocess
import psutil

def get_total_cpus():
    return psutil.cpu_count()

def get_total_ram():
    return round((psutil.virtual_memory().total / 1000000))