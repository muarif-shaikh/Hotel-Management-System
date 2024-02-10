import mysql.connector

createdb = "CREATE DATABASE hotel_management_db"
usedb = "USE hotel_management_db"
create_admin_table = "CREATE TABLE admin_login_info(admin_uname VARCHAR(15) PRIMARY KEY, admin_pwd VARCHAR(15) NOT NULL)"
insert_admin_data = "INSERT INTO admin_login_info VALUES('admin', 'muarif')"
create_room_table = "CREATE TABLE rooms_info(room_no INT PRIMARY KEY, no_of_beds INT NOT NULL, ac INT NOT NULL, tv INT NOT NULL, wifi INT NOT NULL, status VARCHAR(10) NOT NULL, room_price INT NOT NULL)"
create_reservation_table = "CREATE TABLE reservation_info(reservation_id INT PRIMARY KEY, guest_name VARCHAR(45) NOT NULL, age INT NOT NULL, contact_no BIGINT NOT NULL, email VARCHAR(45) NOT NULL, address VARCHAR(100) NOT NULL, no_of_children INT NOT NULL, no_of_adults INT NOT NULL, no_of_days_of_stay INT NOT NULL, room_no INT NOT NULL, check_in_time VARCHAR(45) NOT NULL, check_out_time VARCHAR(45) NOT NULL, time_of_transaction VARCHAR(45) NOT NULL, mode_of_payment VARCHAR(10) NOT NULL, amount_paid BIGINT NOT NULL)"
create_staff_table = "CREATE TABLE staff_info(staff_id INT PRIMARY KEY, name VARCHAR(45) NOT NULL, contact_no BIGINT NOT NULL, email VARCHAR(45) NOT NULL, address VARCHAR(100) NOT NULL, dob VARCHAR(10) NOT NULL, department VARCHAR(50), role VARCHAR(50) NOT NULL, description VARCHAR(100) NOT NULL, added_on VARCHAR(30) NOT NULL)"


def createDb():
    mysqlPwd = input("Enter your mysql password: ")
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password=mysqlPwd
            )
        cur = con.cursor()
        cur.execute(createdb)
        con.commit()
        cur.execute(usedb)
        cur.execute(create_admin_table)
        cur.execute(insert_admin_data)
        cur.execute(create_room_table)
        cur.execute(create_reservation_table)
        cur.execute(create_staff_table)
        con.commit()
        con.close()
        print("Database Created Successfully!")
        print("Tables Created Successfully!")
    except Exception as e:
        print("Error:", e)

createDb()
