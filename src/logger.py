import datetime

def write(write_str):
    now = datetime.datetime.now().strftime("[%d-%m-%Y %H:%M:%S]")
    with open("./vmlist.log", "a") as log:
        log.write(f"{now} {write_str} \n")
