from flask import Flask, render_template, json, request, session, redirect

from flaskext.mysql import MySQL

import copy
app = Flask(__name__)   

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'travelwebsite'
app.config['MYSQL_DATABASE_DB'] = 'travel_website456'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.secret_key = 'Jesus of PES'

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/showSignin')
def showSignin():
	return render_template('signin.html')


@app.route("/")
def main():
	return render_template('index.html')
	#return "Welcome!"

@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
	
	print("In aoisjdasoidj\n")
	# read the posted values from the UI
	_name = request.form['inputName']
	_password = request.form['inputPassword']
	_phno = request.form['inputPhone']
	_email = request.form['inputEmail']
	

 
	# validate the received values
	# if _name and _email and _password:
	#     return json.dumps({'html':'<span>All fields good !!</span>'})
	# else:
	#     return json.dumps({'html':'<span>Enter the required fields</span>'})

	cursor.callproc('sp_createUser2',(_name,_password,_phno,_email))
	data = cursor.fetchall()

	

	#cursor.callproc('sp_createUser2',(_name,_password,_phno,_email))
	#cursor.callproc('sp_createUser',(_name,_email,_password))

	#data=cursor.fetchall()

	#data = cursor.fetchall()
	 
	print("Data is",data)
	if len(data) is 0:
		cursor.callproc('sp_validateLogin',(_email,))
		data = cursor.fetchall()
		conn.commit()
		#print("Data is",data)
		session['user'] = data[0][0];
		return render_template('userHome.html')
		#return json.dumps({'message':'User created successfully !'})
	else:
		#print("In else")
		return render_template('error.html',error = 'Email Address or Phone Number already in use.')
		#return json.dumps({'error':str(data[0])})

@app.route('/userHome')
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:
		return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('/')

	

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
	try:
		_username = request.form['inputEmail']
		_password = request.form['inputPassword']
 
 
 
		# connect to mysql
 
		con = mysql.connect()
		cursor = con.cursor()
		cursor.callproc('sp_validateLogin',(_username,))
		data = cursor.fetchall()
 
 


		print("Data is ",data,str(data[0][2]),_password,str(data[0][2])==_password)
		
		if len(data) > 0:

			print("Inside main if")
			if (str(data[0][2])==_password):
				print("Inside first if\n")
				session['user'] = data[0][0]
				
				return redirect('/userHome')
			else:
				return render_template('error.html',error = 'Wrong Email address or Password.')
		else:
			return render_template('error.html',error = 'Wrong Email address or Password.')
 
 
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:
		cursor.close()
		con.close()

@app.route('/showBookTrain')
def showBookTrain():
	return render_template('booktrain.html')

@app.route('/showBookHotel')
def showBookHotel():
	return render_template('bookhotel.html')

@app.route('/showHotelHistory')
def showHotelHistory():
	return render_template('hotelhistory.html')

@app.route('/showTrainHistory')
def showTrainHistory():
	return render_template('trainhistory.html')    
	


src=[]
dest=[]
dictcost={}
distance=[]
@app.route('/bookTrain1',methods=['POST'])
def bookTrain1():
	_src = request.form['inputSrc']
	_dest = request.form['inputDest']
	if(len(src)==0):
		src.append(_src)
	else:
		src[0]=_src

	if(len(dest)==0):
		dest.append(_dest)
	else:
		dest[0]=_dest
 
 
		# connect to mysql
 
	con = mysql.connect()
	cursor = con.cursor()

	cursor.execute("Select * from Train where Src_Code = '"+_src+"' and Dest_Code = '"+_dest+"' and distance > 100")
	data=cursor.fetchall()

		
	print(data)
	cursor = con.cursor()
	cursor.execute("drop view if exists table1")
	cursor.execute("create view table1(Train_Type,distance) as select Train_Type,MAX(Distance) from Train where Src_Code = '"+_src+"' and Dest_Code = '"+_dest+"' group by Train_Type");
	cursor.execute("select distinct avg(Fare),Seat_Type,Train_Type from table1 natural join Fare_Train where distance between Lower_bound and Upper_bound group by Seat_Type,Train_Type ")
	data1=cursor.fetchall()
	cursor.execute("drop view table1")
	
	print("BEFORE DATA 1 is ",data1)

	data2 = []
	for i in data1:
		i=list(i)
		print("i[0] is ",i[0])
		j=str(i[0])
		j1=j.index('.')
		j=j[:j1]
		i[0]=j
		print("J is ",j)
		i=tuple(i)
		print("i is ",i)
		data2.append(i)

	temp=[]
	a=[i[1] for i in data2]
	print("a is ",a)
	data1=list(data1)
	print("Data 1 is ",data1);

	

	print("DAATA ! IS ",data2);
	if("Economy" not in a and len(a)>0):
		temp1=[]
		temp1.append("N/A")
		temp1.append("Economy")
		temp1.append(data1[0][2])
		print(temp1)
		tuple1=tuple(temp1)
		data2.append(tuple1)

	data2=tuple(data2)

	if("Sleeper" not in a and len(a)>0):
		temp1=[]
		temp1.append("N/A")
		temp1.append("Sleeper")
		temp1.append(data1[0][2])
		print(temp1)
		tuple1=tuple(temp1)
		data1.append(tuple1)

	data2=tuple(data2)

	if("AC" not in a and len(a)>0):
		temp1=[]
		temp1.append("N/A")
		temp1.append("AC")
		temp1.append(data1[0][2])
		print(temp1)
		tuple1=tuple(temp1)
		data1.append(tuple1)

	data2=tuple(data2)
	distance.append(data2)

	print("Data is ",data)
	print("Data 1 is ",data2);
	for i in data:
		for j in i:
			print(j,type(j))
	
	if len(data)>0:
		print("hello")
		return render_template('listtrain.html',trains=data,price=data2)

	else:
		return render_template('error.html',error = 'Sorry, Codes are incorrect or no train is available')
	

@app.route('/verifyTrain1',methods=['POST'])
def verifyTrain1():
	_TrainNo=request.form['TrainNo']
	_Date=request.form['Date']
	_type=request.form['type']
	_number=request.form['number']

	dict1={}
	dict1["NOAC"]=0;
	dict1["NOSleeper"]=0;
	dict1["NOEconomy"]=0;
	
	dict1[_type]=_number;
	print("Dictionary values")
	sum1=0;
	for i in dict1:
		print(i,dict1[i])
		sum1=sum1+int(dict1[i])
	print("HEGKLMEOF")
	print(_TrainNo,_Date,_type,_number,src,dest)

	#select sum(NOAC) from Train_Ticket where '2018-03-28' like date and Train_No=93103 group by Train_No;

	if(_type == "NOAC"):
		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("Select sum(NOAC) from Train_Ticket where Date like '"+_Date+"' and Train_No = '"+_TrainNo+"' and Src_Code = '"+src[0]+"' and Dest_Code = '"+dest[0]+"' group by Train_No")

		data=cursor.fetchall()

		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("select DISTINCT NOAC from Train where Train_No = '"+_TrainNo+"' ")

		data1 = cursor.fetchall()


	if(_type == "NOSleeper"):
		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("Select sum(NOSleeper) from Train_Ticket where Date like '"+_Date+"' and Train_No = '"+_TrainNo+"' and Src_Code = '"+src[0]+"' and Dest_Code = '"+dest[0]+"' group by Train_No")

		data=cursor.fetchall()

		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("select DISTINCT NOSleeper from Train where Train_No = '"+_TrainNo+"' ")

		data1 = cursor.fetchall()


	if(_type == "NOEconomy"):
		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("Select sum(NOEconomy) from Train_Ticket where Date like '"+_Date+"' and Train_No = '"+_TrainNo+"' and Src_Code = '"+src[0]+"' and Dest_Code = '"+dest[0]+"' group by Train_No")

		data=cursor.fetchall()

		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute("select DISTINCT NOEconomy from Train where Train_No = '"+_TrainNo+"' ")

		data1 = cursor.fetchall()



	print("Data 1 is ",data1)
	print("Distance is ",distance)
	print("Data is ",data)
	if(len(data)>0):
		if((int(data[0][0])+int(_number))>data1[0][0]):
			return render_template('error.html',error = 'Sorry, Seat not available')
	if(len(data) is 0):
		if(int(data1[0][0])<int(_number)):
			return render_template('error.html',error = 'Sorry, Seat not available')

	

	con = mysql.connect()
	cursor = con.cursor()

	cursor.execute("select distance,Train_Type from Train where Train_No = '"+_TrainNo+"' and Src_Code = '"+src[0]+"' and Dest_Code = '"+dest[0]+"' ")
	datatemp = cursor.fetchall()

	print("Datatemp is ",datatemp)

	cost=0
	for j in distance:
		for i in j:
			#rint("I is ",i,i[0],i[1],i[2],datatemp[0])
			print("Values are ",i[1],_type[2:],i[2],datatemp[0][1])
			if(i[1]==_type[2:] and i[2]==datatemp[0][1]):
				cost=int(i[0])
				break

	print("Cost is ",cost)

	cost=cost*int(_number)
	print("Cost is ",cost)
	# con = mysql.connect()
	# cursor = con.cursor()

	# cursor.execute("select Fare from Fare_Train where Train_Type = '"+datatemp[0][1]+"' and '"+datatemp[0][0]+"' between Lower_Bound and Upper_Bound and Seat_Type = '"+_type+"' ")

	# datafare=cursor.fetchall()
	# print("Datafare is ",datafare)
	if(len(data)>0):
		print("Data is ",data,data[0],data[0][0])
	if(len(data) is 0 or (int(data[0][0])+int(_number))<=data1[0][0]):
		print(session['user'])
		con = mysql.connect()
		cursor = con.cursor()
		# query = "Insert into `Train_Ticket`(`Cost`,`Date`,`NOS`,`NOAC`,`NOSleeper`,`NOEconomy`,`UID`,`Train_No`,`Src_Code`,`Dest_Code`) values ('"cost"','"_date"','"sum1"','"dict1["NOAC"]"','"dict1["NOSleeper"]"','"dict1["NOEconomy"]"','"session['user']"','"_TrainNo"','"src[0]"','"dest[0]"') "

		# query = "Insert into `Train_Ticket`
		# (`Cost`,`Date`,`NOS`,`NOAC`,`NOSleeper`,`NOEconomy`,`UID`,`Train_No`,`Src_Code`,`Dest_Code`) 
		# values ('"cost"','"_date"','"sum1"','"dict1["NOAC"]"','"dict1["NOSleeper"]"','"dict1["NOEconomy"]"','"session['user']"','"_TrainNo"','"src[0]"','"dest[0]"') "

		cursor.execute(
   		"""INSERT INTO 
        Train_Ticket (
            Cost,
            Date,
            NOS,
            NOAC,
            NOSleeper,
            NOEconomy,
            UID,
            Train_No,
            Src_Code,
            Dest_Code)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (cost, _Date, sum1, dict1["NOAC"], dict1["NOSleeper"], dict1["NOEconomy"],session['user'],_TrainNo,src[0],dest[0]))
		con.commit()

		con = mysql.connect()
		cursor = con.cursor()
		cursor.execute("select max(TID) from Train_Ticket")

		datat = cursor.fetchone()

		con = mysql.connect()
		cursor = con.cursor()

		cursor.execute(
   		"""INSERT INTO 
        History_Train (
            UID,TID)
    VALUES (%s,%s)""", (session['user'],datat[0]))
		con.commit()
		print("Datat is ",datat[0])
		return render_template('userHome.html')
	else:
		return render_template('error.html',error = 'Sorry, Seat not available')



if __name__ == "__main__":
	app.run()
