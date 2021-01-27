import datetime
import uuid

def write(write_str):
    now = datetime.datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
    with open("./vmlist.log", "a") as log:
        log.write(f"{now} {write_str} \n")



vmuuid = str(uuid.uuid4().hex.lower())
vmname = str(uuid.uuid4().hex.lower())
creator = str(uuid.uuid4().hex.lower())
purpose = str(uuid.uuid4().hex.lower())
ip = str(uuid.uuid4().hex.lower())
cpu_cores = str(uuid.uuid4().hex.lower())
rammb =str(uuid.uuid4().hex.lower())
ops = str(uuid.uuid4().hex.lower())

#write(f"VM {vmuuid} created - Name: {vmname} Creator: {creator} Purpose: '{purpose}' IP: {ip} CPU_Cores: {cpu_cores} RAM: {rammb} OS: {ops}")
