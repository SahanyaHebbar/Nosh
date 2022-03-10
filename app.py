from flask import Flask, redirect, render_template, url_for
from flask import request
from datetime import datetime
import sqlite3
import random

current_username=None
current_pass=None
current_id=None

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

@app.route('/Enter_id',methods=['POST','GET'])
def Enter_id():
    global current_id
    data=None
    current_id='1234'
    render_template("Enter_id.html")
    con=sqlite3.connect('nosh.db')
    c=con.cursor()
    current_id=request.form.get("Event_ID")
    print(current_id)
    c.execute("Select Phno, Event_name, Organizer_name, Venue, EDate, ETime from Event where Event_ID=(?)",(current_id,))
    data=c.fetchall()
    print(data)
    return render_template("Enter_id.html",data=data)    

@app.route('/loginSignup', methods=['POST','GET'])
def loginSignup():
    global current_username
    global current_pass
    render_template("loginSignup.html")
    con=sqlite3.connect('nosh.db')
    c=con.cursor()
    if request.method=='POST':
        if "loginemail" in request.form:            #login stuff
            email=request.form['loginemail']
            password=request.form['loginpass']
            current_username=email
            current_pass=password
            if current_username:
                return redirect(url_for(".dashboard"))
        elif request.form['email']!="" and request.form['password']!="":      #Signup stuff
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
    con=sqlite3.connect('nosh.db')
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


@app.route('/dashboard')
def dashboard():
    global current_username
    global current_pass
    con=sqlite3.connect('nosh.db')
    cur=con.cursor()
    cur.execute("Select O.Phone_number from Organizer O where O.Email_ID=(?) and O.Password=(?)",(current_username,current_pass,))
    try:
        phoneNumber=cur.fetchall()[0]
        if(phoneNumber):
            print(phoneNumber)
            cur.execute("SELECT E.Event_ID, E.Event_name,E.No_of_Attendees from Event E where E.Phno=(?)",(phoneNumber[0],))
            details=cur.fetchall()
            return render_template("dashboard.html",details=details)
        else:
            return redirect(url_for(".error"))
    except:
        return redirect(url_for(".error"))
    #cur.execute("SELECT E.Event_ID, E.Event_name,E.No_of_Attendees from Event E where E.Phno=(Select O.Phone_number from Organizer O where O.Email_ID=? and O.Password=?)",(current_username,current_pass,))
    
    
@app.route('/NGO',methods=['GET'])
def ngo():
    con=sqlite3.connect('nosh.db')
    c=con.cursor()
    c.execute("SELECT * FROM NGO")
    data=c.fetchall()
    return render_template("ngo.html",value=data)

@app.route('/CAT',methods=['GET'])
def cat():
    con=sqlite3.connect('nosh.db')
    c=con.cursor()
    c.execute("SELECT * FROM caterers")
    data=c.fetchall()
    return render_template("caterer.html",value=data)


@app.route('/success',methods=['POST'])
def success():
    global current_id
    Anum=request.form.get("Anum")
    def updateAttendees(anum,current_id):
        con=sqlite3.connect('nosh.db')
        c=con.cursor()
        c.execute("select no_of_attendees from event where event_id=(?)",(current_id,))
        noa=int(c.fetchall()[0][0])
        noa=noa+int(anum)
        c.execute("update event set no_of_attendees = (?) where event_id=(?)",(noa,current_id))
        con.commit()
    updateAttendees(Anum,current_id)
    return render_template("success.html")

@app.route('/error',methods=['GET'])
def error():
    return render_template("Error.html")

@app.route('/aboutUs',methods=['GET'])
def aboutUs():
    return render_template("aboutUs.html")