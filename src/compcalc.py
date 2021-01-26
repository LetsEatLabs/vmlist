import os
import subprocess
import psutil

def get_total_cpus():
    return psutil.cpu_count()
    #return int(subprocess.getoutput("cat /proc/cpuinfo | grep processor | wc -l"))

def get_total_ram():
    return round((psutil.virtual_memory().total / 1000000) - 1000) # Apparently it aims high by 1G



print(get_total_ram())