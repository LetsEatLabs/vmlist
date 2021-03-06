import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import uuid
from src import compcalc
from src import logger as lg

# Connection function for each load
def sqlcon():
    """
    Returns connections object to vm.db
    """
    connection = sqlite3.connect("./vm.db", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection

with sqlcon() as connection:
    cursor = connection.cursor()

    # Create sqlite db if it does not exist. Generate initially used tables as well.
    try:
        cursor.execute("""CREATE TABLE vms (uuid TEXT, name TEXT, creator TEXT, purpose TEXT, 
                        ip TEXT, fqdn TEXT, cpu_cores INTEGER, rammb INTEGER, os TEXT, active TEXT)""")
    except:
        pass

    try:
        cursor.execute("CREATE TABLE pc (zero INTEGER, rammb INTEGER, cpus INTEGER)")
        cursor.execute("INSERT INTO pc(zero, rammb, cpus) VALUES(?,?,?)", (0, 1024, 2))
    except:
        pass
    


# Load flask
app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())

lg.write("Application has started.")

# Root page
@app.route("/")
def listrender():
    with sqlcon() as conn:

        cursor = conn.cursor()
        curr_vms = cursor.execute("SELECT * FROM vms").fetchall()
        cpus_used = cursor.execute("SELECT SUM(cpu_cores) from vms WHERE active='yes'").fetchone()
        ram_used = cursor.execute("SELECT SUM(rammb) from vms WHERE active='yes'").fetchone()
        cpuinfo = cursor.execute("SELECT cpus FROM pc WHERE zero = 0").fetchone()
        raminfo = cursor.execute("SELECT rammb FROM pc WHERE zero = 0").fetchone()
        
        return render_template('index.html', 
                                vms=curr_vms, 
                                total_cpus=cpuinfo[0], 
                                total_ram=raminfo[0],
                                ram_used=ram_used,
                                cpus_used=cpus_used)



@app.route("/delete/<string:vmid>", methods=["POST"])
def delete(vmid):
    with sqlcon() as conn:
        cursor = conn.cursor()
        
        vmdetails = cursor.execute("SELECT name, purpose FROM vms WHERE uuid = ?", (vmid,)).fetchone()
        vmname = vmdetails[0]
        vmpurpose = vmdetails[1]

        cursor.execute('DELETE FROM vms WHERE uuid = ?', (vmid,))
        cursor.execute("COMMIT")

        lg.write(f"VM {vmid} ({vmname} - {vmpurpose}) has been deleted by {request.remote_addr}")

        flash(f"VM ID {vmid} was successfully deleted!")
        return redirect(url_for('listrender'))



@app.route("/add/", methods=["POST"])
def add():
    
    with sqlcon() as conn:
        ## Build our query
        vmuuid = str(uuid.uuid4().hex.lower())
        vmname = request.form['vmname']
        creator = request.form['creator']
        purpose = request.form['purpose']
        ip = request.form['ipaddr']
        cpu_cores = request.form['cpus']
        rammb = request.form['rammb']
        ops = request.form['ops']

        lg.write(f"VM {vmuuid} created from {request.remote_addr} - Name: {vmname} Creator: {creator} \
                    Purpose: '{purpose}' IP: {ip} CPU_Cores: {cpu_cores} RAM: {rammb} OS: {ops}")
        
        conn.execute("""INSERT INTO vms(uuid, name, creator, purpose, ip, cpu_cores, rammb, os, active) 
                        VALUES(?,?,?,?,?,?,?,?,?)""", (vmuuid, vmname, creator, purpose, ip, cpu_cores, rammb, ops, "yes"))
        conn.commit()
    
    return redirect(url_for('listrender'))

@app.route("/logs/")
def getlogs():
    logfile = [x.strip() for x in open("./vmlist.log", "r").readlines()]
    return render_template("logs.html", logfile=logfile)

@app.route("/view/<string:vmid>")
def view(vmid):

    with sqlcon() as conn:

        cursor = conn.cursor()
        curr_vm = cursor.execute("SELECT * FROM vms WHERE uuid = ?", (vmid,)).fetchone()

    return render_template("view.html", vm=curr_vm)

@app.route("/modify/<string:vmid>", methods=["POST"])
def modify(vmid):

    with sqlcon() as conn:
        ## Build our query
        vmname = request.form['vmname']
        creator = request.form['creator']
        purpose = request.form['purpose']
        ip = request.form['ipaddr']
        fqdn = request.form['fqdn']
        cpu_cores = request.form['cpus']
        rammb = request.form['rammb']
        ops = request.form['ops']

        lg.write(f"VM {vmid} modified from {request.remote_addr} - Name: {vmname} \
                    Creator: {creator} Purpose: '{purpose}' IP: {ip} FQDN: {fqdn} CPU_Cores: {cpu_cores} RAM: {rammb} OS: {ops}")

        cursor = conn.cursor()
        cursor.execute("""UPDATE vms 
                        SET name = ?, creator = ?, purpose = ?, ip = ?, fqdn = ?, cpu_cores = ?, rammb = ?, os = ? 
                        WHERE uuid = ?""", (vmname, creator, purpose, ip, fqdn, cpu_cores, rammb, ops, vmid))

        return redirect(url_for('listrender'))


@app.route("/activate/<string:vmid>", methods=["POST"])
def activate(vmid):
    with sqlcon() as conn:
        cursor = conn.cursor()
        vmstate = cursor.execute("SELECT active FROM vms WHERE uuid = ?", (vmid,)).fetchone()[0]

        if vmstate != "yes":
            cursor.execute("""UPDATE vms SET active = ? WHERE uuid = ?""", ("yes", vmid))
            conn.commit()
            vmstate = "yes"

            lg.write(f"VM {vmid} has been marked as active={vmstate} by {request.remote_addr}")

        else:
            cursor.execute("""UPDATE vms SET active = ? WHERE uuid = ?""", ("no", vmid))
            conn.commit()
            vmstate = "no"

            lg.write(f"VM {vmid} has been marked as active={vmstate} by {request.remote_addr}")

    return redirect(url_for('listrender'))

@app.route("/cpuinfo/")
def set_pc_info():

    with sqlcon() as conn:

        cursor = conn.cursor()
        cpuinfo = cursor.execute("SELECT cpus FROM pc WHERE zero = 0").fetchone()
        raminfo = cursor.execute("SELECT rammb FROM pc WHERE zero = 0").fetchone()

    return render_template("pcinfo.html", cpuinfo=cpuinfo[0], raminfo=raminfo[0])

@app.route("/cpuinfo/modify", methods=['POST'])
def change_pc_info():
    with sqlcon() as conn:
        cursor = conn.cursor()

        raminfo = request.form['raminfo']
        cpuinfo = request.form['cpuinfo']

        cursor.execute("""UPDATE pc SET rammb = ?, cpus = ? WHERE zero = ?""", (raminfo, cpuinfo, 0))
        lg.write(f"Host information has been modified. New configuration is {cpuinfo} CPUs and {raminfo} \
                    MBs of memory. Change made by {request.remote_addr}")

    return redirect(url_for('listrender'))

        
