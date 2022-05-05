from flask import Flask, render_template,request,redirect,session
import mysql.connector
cnx = mysql.connector.connect(user='root',password='',host='localhost',database='vacencyportal')
cursor=cnx.cursor()


app=Flask(__name__)

app.secret_key = "webgurukul"

@app.route('/register')
def register():
	return render_template('/register.html')

@app.route('/getdata')
def getdata():
	b=request.args['fname']
	c=request.args['lname']
	d=request.args['email']
	e=request.args['mobile']
	f=request.args['dob']
	g=request.args['course_name']
	h=request.args['course_status']
	i=request.args['ssc_percentage']
	
	k=request.args['hsc_percentage']
	
	m=request.args['graduate_percentage']
	
	o=request.args['technical skill']
	p=request.args['resume path']
	q=request.args['photo path']
	r=request.args['created_at']
	s=request.args['updated_at']
	query= "INSERT INTO students VALUES(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	cursor.execute(query,(b,c,d,e,f,g,h,i,k,m,o,p,q,r,s))
	cnx.commit()
	return redirect('/view')

@app.route('/')
@app.route('/login')
def login():
	return render_template('login.html')
	return redirect('/view')
 
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

@app.route('/view')
def view():
	query="SELECT * FROM students"
	cursor.execute(query)
	result=cursor.fetchall()
	return render_template('view.html', data=result)

@app.route('/delete')
def delete():
	id = request.args['id']
	query = "DELETE FROM students WHERE id="+id
	cursor.execute(query)
	cnx.commit()
	return redirect('/login') 


app.run(debug=True)

