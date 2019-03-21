from flask import Flask, render_template, json, request, session, redirect
import datetime
from flaskext.mysql import MySQL

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
userinfo=[]
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
    _hometown = request.form['inputHometown']    

 
    # validate the received values
    # if _name and _email and _password:
    #     return json.dumps({'html':'<span>All fields good !!</span>'})
    # else:
    #     return json.dumps({'html':'<span>Enter the required fields</span>'})

    cursor.callproc('sp_createUser4',(_name,_password,_phno,_email,_hometown))
    data = cursor.fetchall()

    

    #cursor.callproc('sp_createUser2',(_name,_password,_phno,_email))
	#cursor.callproc('sp_createUser',(_name,_email,_password))

    #data=cursor.fetchall()

	#data = cursor.fetchall()
	 
    print("Data is",data)
    if len(data)>0:
        cursor.callproc('sp_validateLogin1',(_email,))
        data = cursor.fetchall()
        conn.commit()
        #print("Data is",data)
        session['user'] = data[0][0];
        return render_template('alert.html',userinfo=userinfo, message = "Account Created! Please Log In!")
        #return json.dumps({'message':'User created successfully !'})
    else:
        #print("In else")
        return render_template('error.html',error = 'Email Address or Phone Number already in use.')
        #return json.dumps({'error':str(data[0])})

@app.route('/userHome')
def userHome():
    print('entered here\n')
    if session.get('user'):
        print(userinfo)
        return render_template('userHome.html',userinfo=userinfo)
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
        cursor.callproc('sp_validateLogin1',(_username,))
        data = cursor.fetchall()
 
 


        print("Data is ",data,str(data[0][2]),_password,str(data[0][2])==_password)
        userinfo.append(data[0][0])
        userinfo.append(str(data[0][1]))
        userinfo.append(str(data[0][3]))
        userinfo.append(_username)	
        userinfo.append(str(data[0][5]))

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

src=[]
dest=[]
dictcost={}
distance=[]
@app.route('/showBookTrain')
def showBookTrain():
	return render_template('booktrain.html')

@app.route('/bookTrain1',methods=['POST','GET'])
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

	cursor.execute("Select Place_ID from Places where Place_Name ='"+_src+"' ")
	place1 = cursor.fetchone()

	cursor.execute("Select Place_ID from Places where Place_Name = '"+_dest+"' ")
	place2 = cursor.fetchone()


	if(place1 is None or place2 is None):
		return render_template('alert.html',message = 'Sorry, Place names are incorrect or no train is available')
	
	print(place1[0],place2[0])
	_src = place1[0]
	_dest = place2[0]
	cursor.execute("Select * from Train where Src_Code = '"+_src+"' and Dest_Code = '"+_dest+"' and distance > 100")
	data=cursor.fetchall()


	if(len(src)==0):
		src.append(_src)
	else:
		src[0]=_src

	if(len(dest)==0):
		dest.append(_dest)
	else:
		dest[0]=_dest

		
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
		return render_template('alert.html',message = 'Sorry, Place names are incorrect or no train is available')
	

@app.route('/verifyTrain1',methods=['POST'])
def verifyTrain1():
	_TrainNo=request.form['TrainNo']
	_Date=request.form['Date']
	_type=request.form['type']
	_number=request.form['number']

	datenow=(datetime.datetime.now().date())

	if(_Date<datenow.strftime('%Y-%m-%d')):
		return render_template('alert.html', message = "Specified Date is before Current Date, Booking Not Confirmed")

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
		return render_template('alert.html',message='Tickets are booked.')
	else:
		return render_template('error.html',error = 'Sorry, Seat not available')



@app.route('/showBookHotel')
def showBookHotel():
	cursor.execute("select distinct Fare_Room_Type from Fare_Hotel")
	roomtype = cursor.fetchall()
	cursor.execute("select distinct Fare_AC from Fare_Hotel")
	ac = cursor.fetchall()
	return render_template('bookhotel.html', roomtype = roomtype, ac = ac)

@app.route('/BookHotel1',methods=['POST'])
def BookHotel1():
	city = request.form['city']
	start_date = request.form['sdate']
	end_date = request.form['edate']


	room_type = request.form['rtype']
	ac = request.form['ac']
	datenow=(datetime.datetime.now().date())

	if(start_date<datenow.strftime('%Y-%m-%d')):
		return render_template('alert.html', message = "Specified Date is before Current Date, Booking Not Confirmed")
	elif(end_date>start_date):
		cursor.execute("select distinct Fare_Hid from Fare_Hotel, Hotel where Hotel.City like '{}' and Fare_Hotel.Fare_Hid = Hotel.Hid".format(city))
		Hotel_Ids = cursor.fetchall()
		query_result = []
		for i in Hotel_Ids:
			
			cursor.execute("drop view IF EXISTS temp1")
			cursor.execute("drop view IF EXISTS temp2")
			cursor.execute("create view temp1 as select Hid,Room_ID from Hotel_Reservation where '{}' between Start_Date and End_Date union select Hid,Room_ID from Hotel_Reservation where '{}' between Start_Date and End_Date".format(start_date, end_date))
			cursor.execute("create view temp2 as select Fare_Rid,Fare_Hid from Fare_Hotel where Fare_Hid like '{}' and Fare_Room_Type like '{}' and Fare_Ac like '{}'".format(i[0], room_type, ac))

			cursor.execute("select count(*) from temp1 where exists (select Fare_Rid from temp2 where Fare_Rid = temp1.Room_ID ) and exists (select Fare_Hid from temp2 where Fare_Hid = temp1.Hid)")
			count1 = cursor.fetchall()
			#print count1
			cursor.execute("select count(*) from temp2")
			count2 = cursor.fetchall()
			#print count2

			if count1!=count2:
				cursor.execute("select distinct Name, Fare, Stars, Address, Overview, Hid from Fare_Hotel, Hotel where Fare_Hid like '{}' and Hid like '{}' and Fare_Room_Type like '{}' and Fare_Ac like '{}'".format(i[0], i[0] , room_type, ac))
				query_result.append(cursor.fetchall())
			
		return render_template('bookhotel1.html', query_result = query_result, ac = ac, room_type = room_type, start_date = start_date, end_date = end_date, city = city)
	else:
		return render_template('alert.html', message = "Dates Invalid, Booking Not Confirmed")

		


@app.route('/BookHotel2',methods=['POST'])
def BookHotel2():
	hid = request.form['hid']
	ac = request.form['ac']
	room_type = request.form['rtype']
	start_date = request.form['sd']
	end_date = request.form['ed']
	city = request.form['city']
	cursor.execute("drop view IF EXISTS temp1")
	cursor.execute("drop view IF EXISTS temp2")
	cursor.execute("create view temp1 as select Hid,Room_ID from Hotel_Reservation where '{}' between Start_Date and End_Date union select Hid,Room_ID from Hotel_Reservation where '{}' between Start_Date and End_Date".format(start_date, end_date))
	cursor.execute("create view temp2 as select Fare_Rid,Fare_Hid from Fare_Hotel where Fare_Hid like '{}' and Fare_Room_Type like '{}' and Fare_Ac like '{}'".format(hid, room_type, ac))
	cursor.execute(" select Fare_Rid from temp2 as t2 where Fare_Rid not in(select t2.Fare_Rid from temp1 where t2.Fare_Rid=Room_ID and t2.Fare_Hid=Hid);")
	Room_allotted = cursor.fetchall()
	cursor.execute("select Fare from Fare_Hotel where Fare_Hid like '{}' and Fare_Rid = {}".format(hid, Room_allotted[0][0]))
	Cost = cursor.fetchall()
	s_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') 
	e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') 
	T_cost = (e_date-s_date)*Cost[0][0]
	T_cost = T_cost.days

	#print T_cost
	cursor.execute("insert into Hotel_Reservation (Hid, Cost, Room_ID, Start_Date, End_Date, User_ID) values ('{}',{},{},'{}','{}',{})".format(hid,T_cost,Room_allotted[0][0], start_date, end_date, userinfo[0]))
	conn.commit()

	return render_template('Bookhotel2.html', city = city, src = userinfo[4])

@app.route('/showHotelHistory')
def showHotelHistory():
	cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid".format(userinfo[0]))
	result=cursor.fetchall()
	print(result)
	cursor.execute("SELECT distinct h.name FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid".format(userinfo[0]))
	hotelname=cursor.fetchall()
	cursor.execute("SELECT distinct h.city FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid".format(userinfo[0]))
	cityn=cursor.fetchall()
	print('hotel name',hotelname)
	print("city name",cityn)
	cursor.execute("SELECT sum(Cost),count(*) from Hotel_Reservation where User_ID={}".format(userinfo[0]))
	cost1=cursor.fetchall()
	cost=cost1[0][0]
	count=cost1[0][1]
	print(cost)
	print(count)
	return render_template('hotelhistory.html',result=result,city=cityn,hotelname=hotelname,cost=cost,count=count)

@app.route('/filterhotelhistory',methods=['POST'])
def filterhhistory():
	filterh=request.form['filter']
	data=''
	hotelname=()
	cityn=()
	print(filterh)
	if(filterh=="Hotel Name"):
		data=request.form['HName']
		print(data,type(data))
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid and h.name='{}' ".format(userinfo[0],data))
		result=cursor.fetchall()
	elif(filterh=="Date After"):
		data=request.form['sdate']
		print(data,type(data))
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid and Start_Date > '{}' ".format(userinfo[0],data))
		result=cursor.fetchall()
	elif(filterh=="Date Before"):
		data=request.form['edate']
		print(data,type(data))
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid and Start_Date < '{}' ".format(userinfo[0],data))
		result=cursor.fetchall()
	elif(filterh=="City"):
		data=request.form['City']
		print(data,type(data))
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid and h.city='{}' ".format(userinfo[0],data))
		result=cursor.fetchall()
	elif(filterh=="StartDEndDate"):
		data=request.form['sdate']
		data2=request.form['edate']
		if(data<data2):
			cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid and Start_Date > '{}' and End_Date <'{}' ".format(userinfo[0],data,data2))
			result=cursor.fetchall()
		else:
			result=()
	elif(filterh=='HandC'):
		data=request.form['Hname']
		data2=request.form['City']
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid and h.city='{}' and h.name='{}'".format(userinfo[0],data2,data))
		result=cursor.fetchall()
	else:
		data=request.form['AC']
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid and Fare_AC='{}'".format(userinfo[0],data))
		result=cursor.fetchall()
	cursor.execute("SELECT distinct h.name FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid".format(userinfo[0]))
	hotelname=cursor.fetchall()
	cursor.execute("SELECT distinct h.city FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid".format(userinfo[0]))
	cityn=cursor.fetchall()
	cursor.execute("SELECT sum(Cost),count(*) from Hotel_Reservation where User_ID={}".format(userinfo[0]))
	cost1=cursor.fetchall()
	cost=cost1[0][0]
	count=cost1[0][1]
	print(cost)
	print(count)
	return render_template('hotelhistory.html',result=result,city=cityn,hotelname=hotelname,cost=cost,count=count)
  
@app.route('/sortbyhotelhistory',methods=['POST'])
def sortbytable():
	data=request.form['Sortby']
	data2=request.form['Sorttype']
	sort=""
	if(data2=="Sort Ascending"):
		sort="ASC"
	else:
		sort="DESC"
	if(data=="Booking ID"):
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid order by(hr.ID) {}".format(userinfo[0],sort))
		result=cursor.fetchall()
		print(result)
	elif(data=="HotelName"):
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid order by(h.name) {}".format(userinfo[0],sort))
		result=cursor.fetchall()
		print(result)
	elif(data=="AC"):
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid order by(Fare_AC) {}".format(userinfo[0],sort))
		result=cursor.fetchall()
		print(result)
	elif(data=="Start Date"):
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid order by(Start_Date) {}".format(userinfo[0],sort))
		result=cursor.fetchall()
		print(result)
	elif(data=="End Date"):
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid order by(End_Date) {}".format(userinfo[0],sort))
		result=cursor.fetchall()
		print(result)
	elif(data=="City"):
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid order by(h.city) {}".format(userinfo[0],sort))
		result=cursor.fetchall()
		print(result)
	else:
		cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid order by(Cost) {}".format(userinfo[0],sort))
		result=cursor.fetchall()
		print(result)
	cursor.execute("SELECT distinct h.name FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid".format(userinfo[0]))
	hotelname=cursor.fetchall()
	cursor.execute("SELECT distinct h.city FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid".format(userinfo[0]))
	cityn=cursor.fetchall()
	cursor.execute("SELECT sum(Cost),count(*) from Hotel_Reservation where User_ID={}".format(userinfo[0]))
	cost1=cursor.fetchall()
	cost=cost1[0][0]
	count=cost1[0][1]
	print(cost)
	print(count)
	return render_template('hotelhistory.html',result=result,city=cityn,hotelname=hotelname,cost=cost,count=count)
@app.route('/canceltickets',methods=["POST"])
def cancelhotel():
	datenow=(datetime.datetime.now().date())
	result=()
	print(datenow)
	cursor.execute("SELECT hr.ID,h.name,h.city,Room_ID,Fare_AC,Cost,Start_Date,End_Date FROM Hotel_Reservation hr NATURAL JOIN User u NATURAL JOIN Hotel h,Fare_Hotel where hr.User_ID={} and Fare_Rid=Room_ID and Fare_Hid=Hid and Start_Date > '{}'".format(userinfo[0],datenow.strftime('%Y-%m-%d')))
	result=cursor.fetchall()
	print(result)
	return render_template('hotelhistorycancellation.html',result=result)
@app.route('/cancelticketstrain',methods=["POST"])
def canceltrainticket():
	datenow=(datetime.datetime.now().date())
	result=()
	print(datenow)
	cursor.execute("select h_1.TID,t_1.Date,t_1.Train_No from History_Train h_1 natural join Train_Ticket t_1 where h_1.UID ={} and t_1.Date > '{}'".format(userinfo[0],datenow.strftime('%Y-%m-%d')))
	data = cursor.fetchall()
	send_data = (data)
	print('send data is',send_data)
	return render_template('trainhistorycancellation.html',data = send_data)
@app.route('/confirmedcancellationtrain',methods=["POST"])
def confirmcanceltrain():
	data=request.form['IDCancel']
	data=int(data)
	cursor.execute("DELETE FROM History_Train where TID={}".format(data))
	cursor.execute("DELETE FROM Train_Ticket where TID={}".format(data))
	conn.commit()
	return render_template('alert.html',message="Train Reservation cancelled.") 
@app.route('/confirmedcancellation',methods=["POST"])
def confirmcancel():
	data=request.form['IDCancel']
	data=int(data)
	cursor.execute("DELETE FROM Hotel_Reservation where ID={}".format(data))
	conn.commit()
	return render_template('alert.html',message="Hotel Reservation cancelled.")

@app.route('/showTrainHistory')
def showTrainHistory():
    return render_template('trainhistory.html') 

@app.route('/showTrainHistoryByDate',methods = ['GET','POST'])
def showTrainHistoryByDate():
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    print(str(start_date))
    conn.commit()
    cursor.execute("select h_1.TID,t_1.Date,t_1.Train_No from History_Train h_1 natural join Train_Ticket t_1 where h_1.UID = {} and t_1.Date between '".format(userinfo[0])+str(start_date)+"' and '"+str(end_date)+"';")
    data = cursor.fetchall()
    send_data = (('Ticket_ID','Date','Train Number'),data)
    print(send_data)
    return render_template('trainhistory.html',data = send_data)  

@app.route('/showTrainHistoryByCost',methods = ['GET','POST'])
def showTrainHistoryByCost():
    start_cost = request.form['startCost']
    end_cost = request.form['endCost']
    print(str(start_cost))
    conn.commit()
    cursor.execute("select h_1.TID,t_1.Cost,t_1.Date,t_1.Train_No from History_Train h_1 natural join Train_Ticket t_1 where h_1.UID = {} and t_1.Cost between '".format(userinfo[0])+(start_cost)+"' and '"+(end_cost)+"'")
    data = cursor.fetchall()
    send_data = (('Ticket_ID','Cost','Date','Train Number'),data)
    return render_template('trainhistory.html',data = send_data)

@app.route('/showTrainHistoryByDistance',methods = ['GET','POST'])
def showTrainHistoryByDistance():
    start_distance = request.form['startDistance']
    end_distance = request.form['endDistance']
    query = "select History_Train.TID,t.Distance,t.Src_Code,t.Dest_Code,t.Train_No,Train_Ticket.Date from History_Train natural join Train_Ticket inner join Train t on t.Train_No = Train_Ticket.Train_No and t.Src_Code=Train_Ticket.Src_Code and t.Dest_Code=Train_Ticket.Dest_Code where t.distance between '"+str(start_distance)+"' and '"+str(end_distance)+"' and History_Train.UID = {}".format(userinfo[0]);
    print(query)
    conn.commit()

    cursor.execute(query)
    data = cursor.fetchall()
    send_data = (('Ticket ID','Distance','Source','Destination','Train Number','Date'),data)
    return render_template('trainhistory.html',data = send_data)

@app.route('/showTrainHistoryByPlace',methods = ['GET','POST'])
def showTrainHistoryByPlace():
    start_place = request.form['startPlace']
    end_place = request.form['endPlace']
    conn.commit()

    cursor.execute("select Place_ID from Places where Place_Name = '"+start_place+"';")
    s_code = cursor.fetchall()
    s = ""
    for i in s_code:
        s = s+ "'"+i[0]+"',"
    s = s[:len(s)-1]
    print(s)
    conn.commit()



    cursor.execute("select Place_ID from Places where Place_Name = '"+end_place+"';")
    e_code = cursor.fetchall()
    e = ""
    for i in e_code:
        e = e+ "'"+i[0]+"',"
    e = e[:len(e)-1]
    print(e)


    print(",".join(e_code[0]))
    query = "select h_1.TID,t_1.Src_Code,t_1.Dest_Code,t_1.Train_No,t_1.Date from History_Train h_1 natural join Train_Ticket t_1 where h_1.UID = {} and t_1.Src_Code in (".format(userinfo[0])+s+") and t_1.Dest_Code in ("+e+");"
    print(query)
    conn.commit()

    cursor.execute(query)
    data = cursor.fetchall()
    send_data = (('Ticket ID','Source','Destination','Train Number','Date'),data)
    print(data)
    return render_template('trainhistory.html',data = send_data)  


@app.route('/showTrainHistoryByStationCode',methods = ['GET','POST'])
def showTrainHistoryByStationCode():
    start_station = request.form['startStationCode']
    end_station = request.form['endStationCode']
    query = "select h_1.TID,t_1.Src_Code,t_1.Dest_Code,t_1.Train_No,t_1.Date from History_Train h_1 natural join Train_Ticket t_1 where h_1.UID = {} and t_1.Src_Code = '".format(userinfo[0])+start_station+"' and t_1.Dest_Code = '"+end_station+"';"
    conn.commit()	
    cursor.execute(query)
    data = cursor.fetchall()
    send_data = (('Ticket ID','Source Station','Destination Station','Train Number','Date'),data)
    return render_template('trainhistory.html',data = send_data)    
if __name__ == "__main__":
    app.run()# @app.route('/showTrainHistory')
# def showTrainHistory():
#     return render_template('trainhistory.html') 

# @app.route('/showTrainHistoryByDate',methods = ['GET','POST'])
# def showTrainHistoryByDate():
#     start_date = request.form['startDate']
#     end_date = request.form['endDate']
#     print(str(start_date))
#     cursor.execute("select h_1.TID,t_1.Date,t_1.Train_No from History_Train h_1 natural join Train_Ticket t_1 where h_1.UID = {} and t_1.Date between '".format(userinfo[0])+str(start_date)+"' and '"+str(end_date)+"';")
#     data = cursor.fetchall()
#     send_data = (('Ticket_ID','Date','Train Number'),data)
#     print(send_data)
#     return render_template('trainhistory.html',data = send_data)  

# @app.route('/showTrainHistoryByCost',methods = ['GET','POST'])
# def showTrainHistoryByCost():
#     start_cost = request.form['startCost']
#     end_cost = request.form['endCost']
#     print(str(start_cost))
#     conn.commit()
#     cursor.execute("select h_1.TID,t_1.Cost,t_1.Date,t_1.Train_No from History_Train h_1 natural join Train_Ticket t_1 where h_1.UID = {} and t_1.Cost between '".format(userinfo[0])+(start_cost)+"' and '"+(end_cost)+"'")
#     data = cursor.fetchall()
#     send_data = (('Ticket_ID','Cost','Date','Train Number'),data)
#     return render_template('trainhistory.html',data = send_data)

# @app.route('/showTrainHistoryByDistance',methods = ['GET','POST'])
# def showTrainHistoryByDistance():
#     start_distance = request.form['startDistance']
#     end_distance = request.form['endDistance']
#     query = "select History_Train.TID,t.Distance,t.Src_Code,t.Dest_Code,t.Train_No from History_Train natural join Train_Ticket inner join Train t on t.Train_No = Train_Ticket.Train_No and t.Src_Code=Train_Ticket.Src_Code and t.Dest_Code=Train_Ticket.Dest_Code where t.distance between '"+str(start_distance)+"' and '"+str(end_distance)+"' and History_Train.UID = {}".format(userinfo[0]);
#     print(query)
#     cursor.execute(query)
#     data = cursor.fetchall()
#     send_data = (('Ticket ID','Distance','Source','Destination','Train Number'),data)
#     return render_template('trainhistory.html',data = send_data)

# @app.route('/showTrainHistoryByPlace',methods = ['GET','POST'])
# def showTrainHistoryByPlace():
#     start_place = request.form['startPlace']
#     end_place = request.form['endPlace']
#     cursor.execute("select Place_ID from Places where Place_Name = '"+start_place+"';")
#     s_code = cursor.fetchall()
#     s = ""
#     for i in s_code:
#         s = s+ "'"+i[0]+"',"
#     s = s[:len(s)-1]
#     print(s)


#     cursor.execute("select Place_ID from Places where Place_Name = '"+end_place+"';")
#     e_code = cursor.fetchall()
#     e = ""
#     for i in e_code:
#         e = e+ "'"+i[0]+"',"
#     e = e[:len(e)-1]
#     print(e)


#     print(",".join(e_code[0]))
#     query = "select h_1.TID,t_1.Src_Code,t_1.Dest_Code,t_1.Train_No from History_Train h_1 natural join Train_Ticket t_1 where h_1.UID = {} and t_1.Src_Code in (".format(userinfo[0])+s+") and t_1.Dest_Code in ("+e+");"
#     print(query)
#     cursor.execute(query)
#     data = cursor.fetchall()
#     send_data = (('Ticket ID','Source','Destination','Train Number'),data)
#     print(data)
#     return render_template('trainhistory.html',data = send_data)  


# @app.route('/showTrainHistoryByStationCode',methods = ['GET','POST'])
# def showTrainHistoryByStationCode():
#     start_station = request.form['startStationCode']
#     end_station = request.form['endStationCode']
#     query = "select h_1.TID,t_1.Src_Code,t_1.Dest_Code,t_1.Train_No from History_Train h_1 natural join Train_Ticket t_1 where h_1.UID = {} and t_1.Src_Code = '".format(userinfo[0])+start_station+"' and t_1.Dest_Code = '"+end_station+"';"
#     cursor.execute(query)
#     data = cursor.fetchall()
#     send_data = (('Ticket ID','Source Station','Destination Station','Train Number'),data)
#     return render_template('trainhistory.html',data = send_data)    
# if __name__ == "__main__":
#     app.run()
