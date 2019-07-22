from flask import Flask , render_template , request, redirect
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="vijaygarg",
  passwd="Vijay@1234",
  database='mydatabase'
  
)


# mycursor.execute("CREATE DATABASE mydatabase")
# mycursor.execute("CREATE TABLE emp (empid VARCHAR(7) PRIMARY KEY NOT NULL, fname VARCHAR(20), lname VARCHAR(20), tech VARCHAR(20) )")

app=Flask(__name__)





posts=[]
@app.route("/",methods=['GET','POST'])
def layout():
        if(request.method=='POST'):
                empid=str(request.form['empid'])
                fname=request.form['fname']
                lname=request.form['lname']
                tech= request.form['tech']
                empid=empid.strip()
                fname=fname.strip()
                lname=lname.strip()
                tech=tech.strip()
                sql = "INSERT INTO emp (empid, fname, lname, tech) VALUES (%s, %s,%s, %s)"
                val=(empid,fname,lname,tech)
                mycursor = mydb.cursor()
                mycursor.execute(sql,val)
                mydb.commit()
                mycursor.close()
                return redirect('/')
               
        else:
                selectQuery = "select * from emp"
                cursor = mydb .cursor()
                cursor.execute(selectQuery)
                records = cursor.fetchall()
                posts=[]
                for row in records:
                        mypost={}
                        mypost['empid']=row[0]
                        mypost['fname']=row[1]
                        mypost['lname']=row[2]
                        mypost['tech']=row[3]
                        posts.append(mypost)
                cursor.close()
                return render_template('form.html',posts=posts)

@app.route('/update/<string:emp_id>', methods=['GET', 'POST'])
def update(emp_id):
       emp_id=emp_id.strip()
       if(request.method=='POST'):
                empid=str(emp_id)
                fname=request.form['fname']
                lname=request.form['lname']
                tech= request.form['tech']
                empid=empid.strip()
                fname=fname.strip()
                lname=lname.strip()
                tech=tech.strip()
                sql_Delete_query = """Delete from emp where empid = %s"""
                cursor = mydb .cursor()
                cursor.execute(sql_Delete_query,(empid,))
                cursor.close()
                mydb.commit()
                print("success")
                sql = "INSERT INTO emp (empid, fname, lname, tech) VALUES (%s, %s,%s, %s)"
                val=(empid,fname,lname,tech)
                mycursor = mydb.cursor()
                mycursor.execute(sql,val)
                mydb.commit()
                mycursor.close()
                print("success")
                return redirect('/')

       else:        
                sql_select_query = """select * from emp where empid = %s"""
                strid=str(emp_id).strip()
                cursor = mydb .cursor()
                cursor.execute(sql_select_query, (strid, ))
                record = cursor.fetchall()
                updatepost={'empid':'','fname':'','lname':'','tech':''}

                for row in record:
                        updatepost['empid']=row[0]
                        updatepost['fname']=row[1]
                        updatepost['lname']=row[2]
                        updatepost['tech']=row[3]
                cursor.close()
                return render_template('updateform.html', posts=posts,updatepost=updatepost)

@app.route('/delete/<string:emp_id>', methods=['GET', 'POST'])
def delete(emp_id):
        emp_id=emp_id.strip()
        sql_Delete_query = """Delete from emp where empid = %s"""
        strid=str(emp_id)
        cursor = mydb .cursor()
        cursor.execute(sql_Delete_query,(strid,))
        cursor.close()
        return redirect('/')

if __name__=='__main__':
        app.run(debug=True)