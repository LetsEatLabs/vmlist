import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
import uuid
from src import compcalc

# Connection function for each load
def sqlcon():
    connection = sqlite3.connect("./vm.db", check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection

with sqlcon() as connection:
    cursor = connection.cursor()

    # Create sqlite db if it does not exist
    try:
        cursor.execute("CREATE TABLE vms (uuid TEXT, name TEXT, creator TEXT, purpose TEXT, ip TEXT, cpu_cores INTEGER, rammb INTEGER, os TEXT)")
    except:
        pass


# Load flask
app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())

# Root page
@app.route("/")
def listrender():
    conn = sqlcon()
    cursor = conn.cursor()
    curr_vms = cursor.execute("SELECT * FROM vms").fetchall()
    cpus_used = cursor.execute("SELECT SUM(cpu_cores) from vms").fetchone()
    ram_used = cursor.execute("SELECT SUM(rammb) from vms").fetchone()
    return render_template('index.html', 
                            vms=curr_vms, 
                            total_cpus=compcalc.get_total_cpus(), 
                            total_ram=compcalc.get_total_ram(),
                            ram_used=ram_used,
                            cpus_used=cpus_used)

@app.route("/<string:vmid>/delete", methods=["POST"])
def delete(vmid):
    with sqlcon() as conn:
        conn.execute('DELETE FROM vms WHERE uuid = ?', (vmid,))
        conn.execute("COMMIT")
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

        conn.execute("""INSERT INTO vms(uuid, name, creator, purpose, ip, cpu_cores, rammb, os) VALUES(?,?,?,?,?,?,?,?)""", (vmuuid, vmname, creator, purpose, ip, cpu_cores, rammb, ops))
        conn.commit()
        return redirect(url_for('listrender'))
