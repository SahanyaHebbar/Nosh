import sqlite3
from flask import Flask, render_template , request
import sqlite3
from datetime import datetime
import random




app=Flask(__name__)

def id():
    number = random.randint(1000,9999)
    return number


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Create_event')
def Create_event():
        return render_template("Create_event.html")

@app.route('/Enter_id')
def Enter_id():
    return render_template("enter_id.html")

@app.route('/loginSignup', methods=['POST','GET'])
def loginSignup():
    render_template('loginSignup.html')
    con=sqlite3.connect('Nosh.db')
    c=con.cursor()
    if request.method=='POST':
        if request.form['email']!="" and request.form['password']!="":      #Signup stuff
            EmailID=request.form['email']
            Password=request.form['password']
            c.execute("Select Email_ID, Password from Organizer where Email_ID=(?)",(EmailID,))
            data=c.fetchall()
            if data:
                return render_template("error.html")
            else:
                Name=request.form['Username']
                Phno=request.form['Phno']
                c.execute("INSERT INTO Organizer VALUES (?,?,?,?)",(Name,Phno,EmailID,Password))
                con.commit()
                con.close()
                return render_template('loginSignup.html')
    elif request.method=='GET':
        return render_template("loginSignup.html")


@app.route('/Event_created', methods=["POST"])
def Event_created():
    Name = request.form.get("Name")
    events = request.form.get("events")
    custom_event = request.form.get("custom_event")
    Date = request.form.get("Date")
    Time = request.form.get("Time")
    Venue = request.form.get("Venue")
    Phno=request.form.get("Phno")
    t=0
    cur.execute("INSERT INTO event VALUES(?,?,?,?,?,?,?,?) ",(Phno,Event_ID,Event_name,Organizer_name,Venue,Date,Time,t))
    con.commit()
    return render_template("Event_created.html",Organizer_name=Organizer_name,Event_name=Event_name,Custom_event=Event_name,Date=Date,Time=Time,Venue=Venue,Phno=Phno,Event_ID=Event_ID)

@app.route('/dashboard', methods=["GET"])
def dashboard():
    EmailID=request.form.get('Useremail')
    con=sqlite3.connect('Nosh.db')
    cur=con.cursor()
    cur.execute("SELECT E.Event_ID, E.No_of_Attendees from Event E, Organizer O where O.Email_ID=(?) AND E.Phno=O.Phone_Number",(EmailID,))
    details=cur.fetchall()
    print(details)
    return render_template("dashboard.html",details=details)

