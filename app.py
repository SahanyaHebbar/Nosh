from flask import Flask, redirect, render_template
from flask import request
from datetime import datetime
import sqlite3

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
    con=sqlite3.connect('NoshFlask.db')
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
    C_number=request.form.get("C_number")
    return render_template("Event_created.html",Name=Name,events=events,custom_event=custom_event,Date=Date,Time=Time,Venue=Venue,C_number=C_number)


@app.route('/dashboard', methods=["GET"])
def dashboard():
    EmailID=request.form.get('Useremail')
    con=sqlite3.connect('Nosh.db')
    cur=con.cursor()
    cur.execute("SELECT A.Event_ID ,A.No_of_Attendees from Event E,Attendees A, Organizer O where O.Email_ID=(?) AND E.phno=O.Phone_Number AND E.Event_ID=A.Event_ID",(EmailID,))
    details=cur.fetchall()
    return render_template("dashboard.html")

@app.route('/NGO',methods=['GET'])
def ngo():
    con=sqlite3.connect('NoshFlask.db')
    c=con.cursor()
    c.execute("SELECT * FROM NGO")
    data=c.fetchall()
    return render_template("ngo.html",value=data)

@app.route('/success',methods=['GET'])
def success():
    return render_template("success.html")
