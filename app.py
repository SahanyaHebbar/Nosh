from flask import Flask, redirect, render_template
from flask import request
from datetime import datetime
import sqlite3
import random 

def id():
    number = random.randint(1000,9999)
    return number

app=Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)

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
    Event_ID=id()
    con=sqlite3.connect('Nosh.db')
    cur=con.cursor()
    cur.execute("SELECT * from Event where Event_ID=(?)",(Event_ID,))
    data=cur.fetchall()
    if data:
        Event_created()
    Organizer_name = request.form.get("Organizer_name")
    Event_name = request.form.get("Event_name")
    if Event_name=="Custom event":
        Event_name = request.form.get("Custom_event")
    Date = request.form.get("Date")
    Time = request.form.get("Time")
    Venue = request.form.get("Venue")
    Phno=request.form.get("Phno")
    No_of_attendees=0
    cur.execute("Insert into event values(?,?,?,?,?,?,?,?)",(Phno,Event_ID,Event_name,Organizer_name,Venue,Date,Time,No_of_attendees))
    con.commit()
    return render_template("Event_created.html",Event_ID=Event_ID,Organizer_name=Organizer_name,Event_name=Event_name,Date=Date,Time=Time,Venue=Venue,Phno=Phno)


@app.route('/dashboard', methods=["GET"])
def dashboard():
    EmailID=request.form.get('Useremail')
    con=sqlite3.connect('Nosh.db')
    cur=con.cursor()
    cur.execute("SELECT E.Event_ID ,E.No_of_Attendees from Event E, Organizer O where O.Email_ID=(?) AND E.phno=O.Phone_Number",(EmailID,))
    details=cur.fetchall()
    return render_template("dashboard.html",details=details)

@app.route('/NGO',methods=['GET'])
def ngo():
    con=sqlite3.connect('Nosh.db')
    c=con.cursor()
    c.execute("SELECT * FROM NGO")
    data=c.fetchall()
    return render_template("ngo.html",value=data)

@app.route('/success',methods=['GET'])
def success():
    return render_template("success.html")
