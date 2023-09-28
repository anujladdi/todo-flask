from flask import Flask 
from flask import render_template,redirect,request
import mysql.connector
import os

mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="todo"
        
    )
mycursor=mydb.cursor()


app=Flask(__name__)

@app.route('/')
def home():
    mycursor.execute("select * from second;")
    data=mycursor.fetchall()
    return render_template("home.html",mydata=data)


@app.route('/data')
def data():
     zx = request.args.get('q')
     if zx:
        mycursor.execute(f"select * from second where title = '{zx}'")
        data = mycursor.fetchall()
     else:
        mycursor.execute("select * from second")
        data = mycursor.fetchall()

     return render_template("data.html", mydata = data)


    # mycursor.execute("select * from second;")
    # data=mycursor.fetchall()
    # return render_template("data.html",mydata=data)
    

@app.route('/savedata', methods = ["POST",])
def savedata():
    
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        img= request.files.get("img")
        if img: 
            img.save(os.path.join("static/images", img.filename))

            zx = os.path.join("static/images/", img.filename)
            mycursor.execute(f"insert into second values('{title}','{desc}','{zx}')")
           
        mydb.commit()
        return redirect("/")
        
    return "save data"


@app.route("/delete/<todo>", methods = ["POST",])
def deletethis(todo):
    if request.method == "POST":
        mycursor.execute(f"delete from second where title = '{todo}'")
        return redirect("/")
    
@app.route("/update/<todo>", methods = ["POST", ])
def updatenow(todo):
    mycursor.execute(f"select * from second where title = '{todo}'")
    zx = mycursor.fetchone()
    return render_template("update.html", data = zx)

@app.route("/updatethis/<t>", methods=["POST",] )
def updatethis(t):
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        img= request.files.get("img")
        if img: 
            img.save(os.path.join("static/images", img.filename))

            zx = os.path.join("static/images/", img.filename)
            # mycursor.execute(f"update into second values('{title}','{desc}','{zx}')")
           
        mycursor.execute(f"update second set title = '{title}',description='{desc}',image='{zx}' where title = '{t}'")
        mydb.commit()
        return redirect("/")

if __name__ == '__main__':
    app.run(debug = True)

