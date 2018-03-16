from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
import psycopg2 as pg
from wtforms import Form, StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
app=Flask('__name__')

@app.route('/')
def home():
	if 'uname' in session:
		return render_template("Recently.html",name=session['uname'])
	
	return render_template('OL.html')

@app.route('/About')
def About():
	if 'uname' in session:
		return render_template('About.html',name=session['uname'])
	else:
		return render_template(redirect(url_for('home')))
@app.route('/signout')
def Signout():
	if 'uname' in session:
		session.pop('uname',None)
		return redirect(url_for('home'))
	else:
		return redirect(url_for('home'))
@app.route('/Summary')
def Summary():
	return render_template('Summa.html',name=session['uname'])

@app.route('/home')
def login():
	if 'uname' in session:
		return render_template("Recently.html",name=session['uname'])
	return render_template('signin.html')
@app.route('/register',methods=['GET','POST'])
def register():
	if request.method=='POST':
		try:
			#use prepared statement 
			conn=pg.connect("dbname='database1' user='postgres' password='postgre'")
			curr=conn.cursor()
			email=str(request.form['email'])
			pwd=str(request.form['password'])
			first=str(request.form['first'])
			last=str(request.form['last'])
			curr.execute("select * from login where name=%s",(email))
			li=curr.fetchall()
			if(len(li)==0):
				curr.execute("insert into login (name,password,first,last) values(%s,%s,%s,%s)",(email,pwd,first,last))
				conn.commit()
			curr.close()
			conn.close()
			return redirect(url_for('home'))
		except Exception:
			print("insert error")




	return render_template('register.html')

@app.route('/search',methods=['GET','POST'])
def Search():
	if request.method=='POST':
		name=str(request.form['Query'])
		conn=pg.connect("dbname='database1' user='postgres' password='postgre'")
		curr=conn.cursor()
		curr.execute("select * from books where bname=%s or author=%s or isbn=%s",(name,name,name))
		results=curr.fetchall()
		return render_template('searchresults.html',results=results)
	return redirect(url_for('Dashboard'))



@app.route('/Dashboard',methods=['GET','POST'])
def Dashboard():
	
	if request.method=='POST':
		try:
			pwd=str(request.form['inputPassword'])
			email=str(request.form['inputEmail'])
			conn=pg.connect("dbname='database1' user='postgres' password='postgre'")
			curr=conn.cursor()
			
			curr.execute("select * from login where name=%s and password=%s",(email,pwd))
			li=curr.fetchall()
			curr.close()
			conn.close()

			if len(li)>0:
				session['uname']=li[0][2]	
				return render_template("Recently.html",name=li[0][2])
				
			else:
				return redirect(url_for('register'))
				
		except Exception:
			print('select Exception')

		
	else:
		if 'uname' in session:
			return render_template("Recently.html",name=session['uname'])
		else:
			return redirect(url_for('home'))
	



if __name__=='__main__':
	app.secret_key='secret12345'
	app.run(debug=True)