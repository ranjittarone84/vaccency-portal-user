from flask import Flask, render_template,request,redirect,session
import os
from werkzeug.utils import secure_filename

import mysql.connector

cnx = mysql.connector.connect(user='root',password='',host='localhost',database='vacencyportal')
cursor=cnx.cursor()


app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload/'
app.secret_key = "webgurukul"

@app.route('/userregister')
def register():
	return render_template('/userregister.html')

@app.route('/getdata', methods=['post'])
def getdata():
	b=request.form['fname']
	c=request.form['lname']
	d=request.form['email']
	e=request.form['password']
	f=request.form['mobile']
	g=request.form['user_type']
	h=request.form['company_name']
	j=request.form['gender']
	k=request.form['address']
	l=request.form['landmark']
	m=request.form['city']
	n=request.form['state']
	o=request.form['pincode']
	p=request.form['dob']
	file = request.files['profile_photo']
	filename = secure_filename(file.filename)
	ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
	ext =filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	if ext:
		img_path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(img_path)
		query= "INSERT INTO users VALUES(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())"
		cursor.execute(query,(b,c,d,e,f,g,h,img_path,j,k,l,m,n,o,p))
		cnx.commit()
		return redirect('/userview')
	else:
		return "Error occured"

@app.route('/')
@app.route('/login')
def login():
	return render_template('login.html')
 
@app.route('/check',methods=['post'])
def check():
	email = request.form['email']
	password=request.form['password']
	query="SELECT * FROM users WHERE email_id=%s AND password=%s"
	cursor.execute(query,(email,password))
	try:
		result=cursor.fetchone()
		cnx.commit()
		if result[1]==email and result[2]==password:
			session['loggedIn']=True
			return redirect('/welcome')
		else:
			return "Invalid user!"
	except Exception as e:
		return redirect('/logout')
	

@app.route('/welcome')
def welcome():
	try:
		if session['loggedIn']==True:
			return render_template('welcome.html')
	except Exception as e:
		return redirect('/login')

@app.route('/logout')
def logout():
	try:
		session.pop('loggedIn')
		return redirect('/login')
	except Exception as e:
		return redirect('/login')

@app.route('/userview')
def view():
	query="SELECT * FROM users"
	cursor.execute(query)
	result=cursor.fetchall()
	return render_template('/userview.html', data=result)

@app.route('/delete')
def delete():
	id = request.args['id']
	query = "DELETE FROM users WHERE id="+id
	cursor.execute(query)
	cnx.commit()
	return redirect('/userview') 


app.run(debug=True)

