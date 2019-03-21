drop database travel_website456;
create database travel_website456;
use travel_website456;


create table Hotel (
Name Varchar (70),
City Varchar(30),
Address Varchar(210),
Latitude Real,
Longitude Real,
Hid VARCHAR(40),
Overview Varchar(4500),
Stars INT,
Review Real,
Primary Key (Hid)
);

create table Fare_Hotel (
Fare_Rid int,
Fare_Hid VARCHAR(40),
Fare_AC VARCHAR(4),
Fare_Room_Type VARCHAR(20),
Fare int,
Primary Key(Fare_Rid,Fare_Hid,Fare_AC,Fare_Room_Type,Fare),
Foreign Key(Fare_Hid) references Hotel(Hid)

);

create table Hotel_Reservation (
ID BIGINT NOT NULL AUTO_INCREMENT,
Hid VARCHAR(40),
Cost INT,
Room_ID INT,
Start_Date Date,
End_Date Date,
User_ID BIGINT,
Primary Key(ID,Room_ID,Start_Date,End_Date,User_ID,Hid),
Foreign Key(Hid) references Hotel(Hid)

);

CREATE TABLE User(
	user_id BIGINT NOT NULL AUTO_INCREMENT,
	user_name VARCHAR(45) NOT NULL,
	user_password VARCHAR(45) NOT NULL,
	user_phno VARCHAR(12) NOT NULL,
	user_email VARCHAR(45) NOT NULL, 
	PRIMARY KEY (user_id),UNIQUE(user_phno,user_email));



create table Train (
Train_No INT,
Name Varchar(30),
Scheduled_Time Time,
NOAC INT,
NOEconomy INT,
NOSleeper INT,
Train_Type Varchar(30) NOT NULL,
Src_Code Varchar(10),
Distance INT,
Dest_Code Varchar(10),
Primary Key(Train_No,Scheduled_Time,Src_Code,Dest_Code)
);



create table Fare_Train (
Fare_ID INT,
Lower_Bound INT,
Upper_Bound INT,
Fare INT,
Seat_Type Varchar(10),
Train_Type Varchar(30),
Primary Key(Fare_ID)
);



create table History_Hotel (
History_ID BIGINT NOT NULL AUTO_INCREMENT,
UID BIGINT NOT NULL,
HID BIGINT NOT NULL,
Primary Key(History_ID),
Foreign Key(UID) references User (user_id),
Foreign Key(HID) references Hotel_Reservation(ID)

);

create table Train_Ticket (
TID BIGINT NOT NULL AUTO_INCREMENT,
Cost INT,
Date Date,
NOS INT,
NOAC INT,
NOSleeper INT,
NOEconomy INT,
UID BIGINT,
Train_No INT,
Primary Key(TID),
Foreign Key (UID) references User(user_id),
Foreign Key(Train_No) references Train(Train_no)
);


create table History_Train (
History_ID BIGINT NOT NULL AUTO_INCREMENT,
UID BIGINT NOT NULL,
TID BIGINT NOT NULL,
Primary Key(History_ID),
Foreign Key(UID) references User (user_id),
Foreign Key(TID) references Train_Ticket(TID)

);



create table Places (
Place_Name Varchar(30),
Place_ID Varchar(10) Unique,
Primary Key(Place_Name)
);

create table Src_Dest(
Train_No INT,
Source_ID Varchar(5),
Dest_ID Varchar(5),
Primary Key(Source_ID,Dest_ID,Train_No),
Foreign Key(Train_No) References Train (Train_No),
Foreign Key(Source_ID) References Places(Place_ID),
Foreign Key(Dest_ID) References Places(Place_ID)


);


create table Room (
Room_ID INT,
Hotel_ID VARCHAR(40),
Room_Type VARCHAR(20),
AC VARCHAR(4),
Foreign Key (Hotel_ID) References Hotel(Hid),
Primary Key (Room_ID,Hotel_ID));




alter table Hotel_Reservation
ADD Foreign Key(Room_ID) references Room(Room_ID);
alter table Hotel_Reservation
ADD Foreign Key(User_ID) references User1(user_id);


CREATE TABLE User1(
    user_id BIGINT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(45) NOT NULL,
    user_password VARCHAR(45) NOT NULL,
    user_phno VARCHAR(12) NOT NULL,
    user_email VARCHAR(45) NOT NULL,
    user_hometown VARCHAR(45) NOT NULL, 
    PRIMARY KEY (user_id),UNIQUE(user_phno,user_email));





DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser4`(
    IN p_name VARCHAR(45),
    IN p_password VARCHAR(45),
    IN p_phno VARCHAR(20),
    IN p_email VARCHAR(45),
    IN p_hometown VARCHAR(45)
)
BEGIN
    if ( select exists (select 1 from User1 where user_phno = p_phno) ) THEN
        select 'Phone Number Already Exists';
    END IF;

    if (select exists (select 1 from User1 where user_email = p_email) ) THEN
        select 'Email Already Exists';
    END IF;

   if (select not exists (select 1 from User1 where user_email = p_email) and not exists(select 1 from User1 where user_phno = p_phno)) THEN
     
        insert into User1
        (
            user_name,
            user_password,
            user_phno,
            user_email,
            user_hometown
        )
        values
        (
            p_name,
            p_password,
            p_phno,
            p_email,
            p_hometown
        );
        select * from User1 where user_email = p_email;
    END IF;
END$$
DELIMITER ;





DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin1`(
IN p_username VARCHAR(45)
)
BEGIN
    select * from User1 where user_email = p_username;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser2`(
    IN p_name VARCHAR(45),
    IN p_password VARCHAR(45),
    IN p_phno VARCHAR(20),
    IN p_email VARCHAR(45)
)
BEGIN
    if ( select exists (select 1 from User where user_phno = p_phno) ) THEN
        select 'Phone Number Already Exists';
    END IF;

    if (select exists (select 1 from User where user_email = p_email) ) THEN
        select 'Email Already Exists';
    END IF;

   if (select not exists (select 1 from User where user_email = p_email) and not exists(select 1 from User where user_phno = p_phno)) THEN
     
        insert into User
        (
            user_name,
            user_password,
            user_phno,
            user_email
        )
        values
        (
            p_name,
            p_password,
            p_phno,
            p_email
        );
     
    END IF;
END$$
DELIMITER ;


DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
IN p_username VARCHAR(45)
)
BEGIN
    select * from User where user_email = p_username;
END$$
DELIMITER ;
