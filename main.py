#importing required modules
import tkinter as tk
from PIL import ImageTk,Image
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import os

#PDF file libraries  
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import  A4


#function for connecting with MySQL Database
def dbConnect():
    global con, cur
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="muarif",
            database="hotel_management_db"
            )
        cur = con.cursor()
    except Exception as e:
        print(e)

now = datetime.now()

def startApp():
    root.destroy()
    mainScr()

def handler(e):
    if root.focus_get() == uname:
        pwd.focus_set()
    elif root.focus_get() == pwd:
        loginF()


def exitF():
    hotel_status.config(bg="white")
    Reserve.config(bg="white")
    Rooms.config(bg="white")
    Payments.config(bg="white")
    hotel_staff.config(bg="white")
    log_out.config(bg="#e6ffe6")
    answer = messagebox.askyesno("Exit", "Are you sure to Exit?")
    if answer:
        root.destroy()
    else:
        log_out.config(bg="white")


#login function
def loginF():
    try:
        dbConnect()
        usrname = str(uname.get()).rstrip()
        passwrd  = str(pwd.get()).rstrip()
        get_login_info = "SELECT * FROM admin_login_info"
        cur.execute(get_login_info)
        f = cur.fetchall()
        admin_uname = f[0][0]
        admin_pswd = f[0][1]
        if (admin_uname == usrname) and (admin_pswd == passwrd):
            startApp()   
        else:
            messagebox.showwarning("Error", "Incorrect Username or Password")
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
        print(e)

    
#add room function
def addRoomF():
    room_no = roomNo.get()
    no_of_beds = noOfBeds.get()
    room_price = roomPrice.get()

    acVal = str(ac.get())
    tvVal = str(tv.get())
    wifiVal = str(wifi.get())

    room_no_list = []

    try:
        if room_no == "Enter Room Number *" or no_of_beds == "Number of Beds *" or room_price == "Room Price *":
            messagebox.showinfo("Incomplete", "Fill all the fields marked by *")
        else:
            dbConnect()
            allRoomNo = "select room_no from rooms_info"
            cur.execute(allRoomNo)
            all_room_no = cur.fetchall()
            for i in all_room_no:
                room_no_list.append(i[0])
            if int(room_no) in room_no_list:
                messagebox.showwarning("Oops!", "Room Number Already Exist!")
            else:
                insertRoom = "insert into rooms_info values ("+room_no+","+no_of_beds+","+acVal+","+tvVal+","+wifiVal+",'Available',"+room_price+");"
                cur.execute(insertRoom)
                con.commit()
                messagebox.showinfo("Success", "Room Added Successfully!")
                con.close()
                addRoomScr()
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
        print(e)


    
#add staff function
def addStaffF():
    dbConnect()
    sName = sname.get().rstrip().title()
    sContactNo = contactno.get().rstrip()
    sEmail = semail.get().rstrip()
    sAddress = saddr.get()
    departmnt = dept.get()
    jobRole = jobr.get().rstrip()
    jobDesc = jobdesc.get().rstrip()
    Dob = dob.get().rstrip()
    
    try:
        s_id_list = []
        get_s_id = "select staff_id from staff_info"
        cur.execute(get_s_id)
        all_s_id = cur.fetchall()
        for i in all_s_id:
            s_id_list.append(i[0])
        staff_Id_last_index = len(s_id_list)
        
        if staff_Id_last_index == 0:
            staff_Id = 1
            staff_Id = str(staff_Id)
        else:
            staff_Id_last_index = len(s_id_list)-1
            staff_Id = s_id_list[staff_Id_last_index]
            staff_Id = staff_Id + 1
            staff_Id = str(staff_Id)
        curTime = now.strftime("%d-%m-%Y %H:%M:%S")
        insertStaff = "insert into staff_info values ("+staff_Id+",'"+sName+"',"+sContactNo+",'"+sEmail+"','"+sAddress+"','"+Dob+"','"+departmnt+"','"+jobRole+"','"+jobDesc+"','"+curTime+"');"
        cur.execute(insertStaff)
        con.commit()
        messagebox.showinfo("Success", "Staff Added Successfully!")
        con.close()
        addStaffScr()
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
        print(e)




#search room function
def searchRoomF():
    try:
        sRoomNo = srch.get()
        dbConnect()
        searchRoom = "select * from rooms_info where room_no = "+sRoomNo+";"
        cur.execute(searchRoom)
        info = cur.fetchall()
        room_info = list(info[0])
        r_no = room_info[0]
        n_o_b = room_info[1]
        r_p = room_info[6]
        status = room_info[5]
        status = "Status: "+status

        if room_info[2]==1:
            ac_yes = "Yes"
        else:
            ac_yes = "No"

        if room_info[3]==1:
            tv_yes = "Yes"
        else:
            tv_yes = "No"

        if room_info[4]==1:
            wifi_yes = "Yes"
        else:
            wifi_yes = "No"
        

        tk.Label(rFrame, text="Room Number", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0, rely=0.2, relwidth=0.16, relheight=0.15)

        tk.Label(rFrame, text=r_no, font=("dubai", 25), bg="white",
                      fg="#00b38f").place(relx=0, rely=0.35, relwidth=0.16, relheight=0.35)

        tk.Label(rFrame, text="No. of Beds", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.17, rely=0.2, relwidth=0.16, relheight=0.15)

        tr = tk.Label(rFrame, text=n_o_b, font=("dubai", 25), bg="white",
                      fg="#00b38f").place(relx=0.17, rely=0.35, relwidth=0.16, relheight=0.35)

        tk.Label(rFrame, text="AC?", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.34, rely=0.2, relwidth=0.16, relheight=0.15)

        tk.Label(rFrame, text=ac_yes, font=("dubai", 25), bg="white",
                      fg="#00b38f").place(relx=0.34, rely=0.35, relwidth=0.16, relheight=0.35)

        tk.Label(rFrame, text="TV?", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.51, rely=0.2, relwidth=0.16, relheight=0.15)

        tk.Label(rFrame, text=tv_yes, font=("dubai", 25), bg="white",
                 fg="#00b38f").place(relx=0.51, rely=0.35, relwidth=0.16, relheight=0.35)

        tk.Label(rFrame, text="WiFi?", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.68, rely=0.2, relwidth=0.16, relheight=0.15)

        tr = tk.Label(rFrame, text=wifi_yes, font=("dubai", 25), bg="white",
                      fg="#00b38f").place(relx=0.68, rely=0.35, relwidth=0.16, relheight=0.35)

        tk.Label(rFrame, text="Price", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.85, rely=0.2, relwidth=0.15, relheight=0.15)

        tk.Label(rFrame, text=r_p, font=("dubai", 25), bg="white",
                 fg="#00b38f").place(relx=0.85, rely=0.35, relwidth=0.15, relheight=0.35)

        uBtn = tk.Button(rFrame, text="UPDATE", font=("dubai", 13), bg="cyan4", fg="white", command=updateRoomF)
        uBtn.place(relx=0.85, rely=0.77, relwidth=0.12, relheight=0.1)

        tk.Label(rFrame, text=status, font=("courier", 15), bg="#e6ffe6",
             fg="black").place(relx=0.02, rely=0.77)
 
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong")
        
    
#delete room function
def delRoomF():
    global sRoomNo
    sRoomNo = srch.get()
    try:
        sRoomNo = srch.get()
        dbConnect()
        searchRoom = "select * from rooms_info where room_no = "+sRoomNo+";"
        cur.execute(searchRoom)
        info = cur.fetchall()
        room_info = list(info[0])
        r_no = room_info[0]
        n_o_b = room_info[1]
        r_p = room_info[6]

        if room_info[2]==1:
            ac_yes = "Yes"
        else:
            ac_yes = "No"

        if room_info[3]==1:
            tv_yes = "Yes"
        else:
            tv_yes = "No"

        if room_info[4]==1:
            wifi_yes = "Yes"
        else:
            wifi_yes = "No"

        tk.Label(rFrame, text="Room Number", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0, rely=0.2, relwidth=0.16, relheight=0.15)

        tk.Label(rFrame, text=r_no, font=("dubai", 25), bg="white",
                      fg="#00b38f").place(relx=0, rely=0.35, relwidth=0.16, relheight=0.3)

        tk.Label(rFrame, text="No. of Beds", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.17, rely=0.2, relwidth=0.16, relheight=0.15)

        tr = tk.Label(rFrame, text=n_o_b, font=("dubai", 25), bg="white",
                      fg="#00b38f").place(relx=0.17, rely=0.35, relwidth=0.16, relheight=0.3)

        tk.Label(rFrame, text="AC?", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.34, rely=0.2, relwidth=0.16, relheight=0.15)

        tk.Label(rFrame, text=ac_yes, font=("dubai", 25), bg="white",
                      fg="#00b38f").place(relx=0.34, rely=0.35, relwidth=0.16, relheight=0.3)

        tk.Label(rFrame, text="TV?", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.51, rely=0.2, relwidth=0.16, relheight=0.15)

        tk.Label(rFrame, text=tv_yes, font=("dubai", 25), bg="white",
                 fg="#00b38f").place(relx=0.51, rely=0.35, relwidth=0.16, relheight=0.3)

        tk.Label(rFrame, text="WiFi?", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.68, rely=0.2, relwidth=0.16, relheight=0.15)

        tr = tk.Label(rFrame, text=wifi_yes, font=("dubai", 25), bg="white",
                      fg="#00b38f").place(relx=0.68, rely=0.35, relwidth=0.16, relheight=0.3)

        tk.Label(rFrame, text="Price", font=("dubai", 15), bg="#00b38f",
             fg="white").place(relx=0.85, rely=0.2, relwidth=0.15, relheight=0.15)

        tk.Label(rFrame, text=r_p, font=("dubai", 25), bg="white",
                 fg="#00b38f").place(relx=0.85, rely=0.35, relwidth=0.15, relheight=0.3)

        dBtn = tk.Button(rFrame, text="DELETE", font=("dubai", 13), bg="cyan4", fg="white", command=confirmDel)
        dBtn.place(relx=0.43, rely=0.75, relwidth=0.14, relheight=0.1)

    
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")


def confirmDel():
    answer = messagebox.askyesno("Delete", "Are you sure to delete?")
    if answer:
        delRoomF2()

def delRoomF2():
    dbConnect()
    delRoom = "delete from rooms_info where room_no = "+sRoomNo+";"
    cur.execute(delRoom)
    con.commit()
    con.close()
    messagebox.showinfo("success", "Room deleted Successfully!")
    delRoomScr()

def checkRoomNo():
    room_no_list = []
    r_number = srch.get()

    try:
        dbConnect()
        allRoomNo = "select room_no from rooms_info"
        cur.execute(allRoomNo)
        all_room_no = cur.fetchall()
        for i in all_room_no:
            room_no_list.append(i[0])
        if int(r_number) not in room_no_list:
            messagebox.showwarning("Oops!", "Room Number does not Exist!")
        else:
            if focusF == "srchF":
                searchRoomF()
            elif focusF == "delF":
                delRoomF()
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")


def checkStaffId():
    global staffid
    staff_id_list = []
    staffid = srch.get()

    try:
        dbConnect()
        allstaffId = "select staff_id from staff_info"
        cur.execute(allstaffId)
        all_staff_id = cur.fetchall()
        for i in all_staff_id:
            staff_id_list.append(i[0])
        if int(staffid) not in staff_id_list:
            messagebox.showwarning("Oops!", "Staff ID does not Exist!")
        else:
            if focusF == "delstaff":
                delStaffF()
            elif focusF == "updatestaff":
                updateStaffF()
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")

def delStaffF():
    global StaffID
    try:
        StaffID = srch.get()
        dbConnect()
        searchstaff = "select * from staff_info where staff_id = "+StaffID+";"
        cur.execute(searchstaff)
        info = cur.fetchall()
        staff_info = list(info[0])
        sname = staff_info[1]
        sdepartment = staff_info[6]
        sjobrole = staff_info[7]
        saddedon = staff_info[9]

        sInfo = "Name : "+sname+"\nDepartment : "+sdepartment+"\nJob Role : "+sjobrole

        tk.Label(rFrame, text="Name", font=("dubai", 18), bg="cyan4",
                 fg="white").place(relx=0, rely=0.203, relwidth=0.3, relheight=0.12)
        e1 = tk.Entry(rFrame, font=("dubai", 15))
        e1.place(relx=0.3, rely=0.203, relwidth=0.7, relheight=0.15)

        tk.Label(rFrame, text="Department", font=("dubai", 18), bg="cyan4",
                 fg="white").place(relx=0, rely=0.326, relwidth=0.3, relheight=0.12)
        e2 = tk.Entry(rFrame, font=("dubai", 15))
        e2.place(relx=0.3, rely=0.326, relwidth=0.7, relheight=0.15)

        tk.Label(rFrame, text="Job Role", font=("dubai", 18), bg="cyan4",
                 fg="white").place(relx=0, rely=0.449, relwidth=0.3, relheight=0.12)
        e3 = tk.Entry(rFrame, font=("dubai", 15))
        e3.place(relx=0.3, rely=0.449, relwidth=0.7, relheight=0.15)

        tk.Label(rFrame, text="Added on", font=("dubai", 18), bg="cyan4",
                 fg="white").place(relx=0, rely=0.572, relwidth=0.3, relheight=0.12)
        e4 = tk.Entry(rFrame, font=("dubai", 15))
        e4.place(relx=0.3, rely=0.572, relwidth=0.7, relheight=0.12)

        e1.insert(0,sname)
        e2.insert(0,sdepartment)
        e3.insert(0,sjobrole)
        e4.insert(0,saddedon)

        dBtn = tk.Button(rFrame, text="DELETE", font=("dubai", 13), bg="cyan4", fg="white", command=confirmDel2)
        dBtn.place(relx=0.43, rely=0.75, relwidth=0.14, relheight=0.1)

    except Exception as e:
        messagebox.showerror("Error", "something went wrong!")

def confirmDel2():
    answer = messagebox.askyesno("Delete", "Are you sure to delete?")
    if answer:
        delStaffF2()

def delStaffF2():
    dbConnect()
    delstaff = "delete from staff_info where staff_id = "+StaffID+";"
    cur.execute(delstaff)
    con.commit()
    con.close()
    messagebox.showinfo("success", "Staff deleted Successfully!")
    delStaffScr()

def updateStaffF2():
    try:
        dbConnect()
        updatestaff = "update staff_info set staff_id = "+ str(staffid) +", name = '"+ sname.get() +"', contact_no = "+ str(contactno.get()) +", email = '"+ semail.get() +"', address = '"+ saddr.get() +"', dob = '"+ dob.get() +"', department = '"+dept.get() +"', role = '"+jobr.get()+"', description = '"+jobdesc.get()+"' where staff_id = "+staffid
        cur.execute(updatestaff)
        con.commit()
        messagebox.showinfo("success", "saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
        print(e)

def updateStaffF():
    try:
        dbConnect()
        searchstaffinfo = "select * from staff_info where staff_id = "+staffid
        cur.execute(searchstaffinfo)
        info = cur.fetchall()
        staff_info = list(info[0])
        staff_id = staff_info[0]

        stfID = "Staff ID : "+str(staff_id)

        tk.Label(rFrame, text=stfID, font=("dubai", 15), bg="#e6ffe6", 
             fg="#006600").place(relx=0.05, rely=0.2)

        sname.delete(0, tk.END)
        contactno.delete(0, tk.END)
        semail.delete(0, tk.END)
        saddr.delete(0, tk.END)
        dob.delete(0, tk.END)
        jobr.delete(0, tk.END)
        jobdesc.delete(0, tk.END)

        sname.insert(0,staff_info[1])
        contactno.insert(0,staff_info[2])
        semail.insert(0,staff_info[3])
        saddr.insert(0,staff_info[4])
        dob.insert(0,staff_info[5])
        dept.set(staff_info[6])
        jobr.insert(0,staff_info[7])
        jobdesc.insert(0,staff_info[8])
        
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
        print(e)

#payment info function
def paymentInfoF():
    global reservationId
    try:
        reservationId = str(rId.get())
        dbConnect()
        get_info = "select * from reservation_info where reservation_id = "+reservationId
        cur.execute(get_info)
        f = cur.fetchall()
        nog.delete(0, tk.END)
        tot.delete(0, tk.END)
        ap.delete(0, tk.END)
        pm.delete(0, tk.END)   
        nog.insert(0, f[0][1])
        tot.insert(0, f[0][12])
        ap.insert(0, f[0][14])
        pm.insert(0, f[0][13])
        prBtn.config(command=printReceipt)
    except Exception as e:
        print(e)

def checkResId():
    res_id_list = []
    resId = str(rId.get())
    try:
        if resId == "":
            resId = "0"
        dbConnect()
        allResId = "select reservation_id from reservation_info"
        cur.execute(allResId)
        all_res_id = cur.fetchall()
        for i in all_res_id:
            res_id_list.append(i[0])
        if int(resId) not in res_id_list:
            messagebox.showwarning("Oops!", "Reservation ID not Found!")
        else:
            paymentInfoF()
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")       

#print receipt function
def printReceipt():
    try:
        dbConnect()
        get_info = "select * from reservation_info where reservation_id = "+reservationId
        cur.execute(get_info)
        f = cur.fetchall()
        all_info = "-- Bill --\n\nReservation ID : "+reservationId+"\n\nGuest Name : "+f[0][1]+"\nConact No : "+str(f[0][3])+"\nEmail : "+f[0][4]+"\nAddress : "+f[0][5]+"\n\nNumber of Children : "+str(f[0][6])+"\nNumber of Adults : "+str(f[0][7])+"\nNumber of Days of Stay : "+str(f[0][8])+"\n\nRoom Number : "+str(f[0][9])+"\nAmount Paid : Rs "+str(f[0][14])+"\nPayment Method : "+f[0][13]+"\nTime of Transaction : "+f[0][12]
        my_Style = ParagraphStyle('My Para style', fontName="Times-Roman", fontSize=16, alignment=0, borderWidth=2,
                                  borderColor='black', backColor = '#E6FFE6', borderPadding = (20, 20, 20),
                                  leading = 20)
        width, height = A4
        bill_path= 'bill-'+str(reservationId)+'.pdf'
        all_info=all_info.replace('\n','<BR/>')
        p1 = Paragraph(all_info, my_Style)
        c = canvas.Canvas(bill_path, pagesize=A4)
        p1.wrapOn(c, 300, 50)
        p1.drawOn(c, width-450,height-550)
        c.save()
        os.startfile(bill_path)
    except Exception as e:
        print(e)


#unreserve function
def confirmUnres():
    answer = messagebox.askyesno("Unreserve", "Unreserve Room?")
    if answer:
        unreserveF()

def unreserveF():
    curTime = now.strftime("%d-%m-%Y %H:%M:%S")
    dbConnect()
    upStatus = "update rooms_info set status = 'Available' where room_no = "+rno.get()
    cur.execute(upStatus)
    con.commit()
    upChkTime = "update reservation_info set check_out_time = '"+curTime+"' where room_no = "+rno.get()
    cur.execute(upChkTime)
    con.commit()
    messagebox.showinfo("Success", "Room Unreserved Successfully!")

    
#reservation function
def reservationF():
    global cancelBtn, resrveBtn, Price, Tax, Total, pMode, rd, guestName, firstName, lastName, age, contactNo, email, address, numberOfChildren, numberOfAdults, numberOfDays, roomNumber, Total
    try:
        firstName = fn.get().strip()
        lastName = ln.get().strip()
        age = str(ag.get()).strip()
        contactNo = str(cn.get()).strip()
        email = em.get().strip()
        address = ad.get().strip()
        numberOfChildren = str(noc.get()).strip()
        numberOfAdults = str(noa.get()).strip()
        numberOfDays = str(nod.get()).strip()
        roomNumber = str(rno.get()).strip()
        

        if email == "Email":
            email = "Not Provided"

        guestName = firstName + " " + lastName
        guestName = guestName.title()

        if firstName == "First Name *" or lastName == "Last Name *" or age == "Age *" or contactNo == "Contact Number *" or address == "Address *" or numberOfChildren == "Number of Children *" or numberOfAdults == "Number of Adults *" or numberOfDays == "Number of Days of Stay *" or roomNumber == "Enter Room Number *":
            messagebox.showinfo("Incomplete", "Fill all the fields marked by *")
        else:
            for widgets in resFr.winfo_children():
                widgets.destroy()

            tk.Label(resFr, text="Confirm Reservation", font=("dubai", 18), fg="white",
                     bg="cyan4").place(relx=0, rely=0, relwidth=1, relheight=0.15)

            rdFr = tk.Frame(resFr, bg="#e6ffe6", relief="solid", bd=1)
            rdFr.place(relx=0.025, rely=0.2, relwidth=0.5, relheight=0.75)

            rd = "Guest Name : "+guestName+"\nAge : "+age+"\nConact No : "+contactNo+"\nEmail : "+email+"\nAddress : "+address+"\nNumber of Children : "+numberOfChildren+"\nNumber of Adults : "+numberOfAdults+"\nNumber of Days of Stay : "+numberOfDays+"\nRoom Number : "+roomNumber

            tk.Label(rdFr, text=rd, font=("dubai", 11), bg="#e6ffe6", justify="left",
                     fg="black").place(relx=0.03, rely=0, relheight=1)

            tk.Label(resFr, text="Price : ", font=("dubai", 17), fg="black",
                     bg="#e6ffe6").place(relx=0.55, rely=0.2)
            
            Price = tk.Entry(resFr, font=("dubai",15), relief="solid", bd=1)
            Price.place(relx=0.65, rely=0.225, relwidth=0.12, relheight=0.07)

            tk.Label(resFr, text="Tax : ", font=("dubai", 17), fg="black",
                     bg="#e6ffe6").place(relx=0.8, rely=0.2)

            Tax = tk.Entry(resFr, font=("dubai",15), relief="solid", bd=1)
            Tax.place(relx=0.878, rely=0.225, relwidth=0.08, relheight=0.07)

            tk.Label(resFr, text="Total Amount : ", font=("dubai", 17), fg="black",
                     bg="#e6ffe6").place(relx=0.55, rely=0.375)
            
            Total = tk.Entry(resFr, font=("dubai",15), relief="solid", bd=1)
            Total.place(relx=0.765, rely=0.4, relwidth=0.193, relheight=0.07)

            pMode = tk.StringVar()
            pMode.set(None)

            r1 = tk.Radiobutton(resFr, text='Cash', font=("dubai", 15), bg="#e6ffe6", value='Cash', var=pMode)
            r2 = tk.Radiobutton(resFr, text='Card', font=("dubai", 15), bg="#e6ffe6", value='Card', var=pMode)
            r3 = tk.Radiobutton(resFr, text='UPI', font=("dubai", 15), bg="#e6ffe6", value='UPI', var=pMode)

            r1.place(relx=0.55, rely=0.64)
            r2.place(relx=0.7, rely=0.64)
            r3.place(relx=0.85, rely=0.64)

            tk.Label(resFr, text="-- Select Payment Method --", font=("courier", 15), fg="black",
                     bg="#e6ffe6").place(relx=0.55, rely=0.55, relwidth=0.408)

            cancelBtn = tk.Button(resFr, text="CANCEL", font=("dubai", 13), fg="white", bg="#ff8080", command=reserveScr)
            cancelBtn.place(relx=0.56, rely=0.82, relwidth=0.15, relheight=0.1)

            resrveBtn = tk.Button(resFr, text="RESERVE", font=("dubai", 13), fg="white", bg="#00cc99", command=checkPaymentMethod)
            resrveBtn.place(relx=0.808, rely=0.82, relwidth=0.15, relheight=0.1)

            for widgets in filterFr.winfo_children():
                widgets.destroy()

            dbConnect()
            getRp = "select room_price from rooms_info where room_no = "+roomNumber
            cur.execute(getRp)
            Rp = cur.fetchall()
            rp = Rp[0][0] * int(numberOfDays)

            Price.insert(0, rp)
            Tax.insert(0, "0")

            Total.insert(0, rp)

            def totalAmount(event):
                tx=Tax.get()
                if Tax.get()=="":
                    tx="0"
                ta = int(Price.get()) + int(tx)
                Total.delete(0, tk.END)
                Total.insert(0, str(ta))

            Total.bind('<KeyRelease>', totalAmount)
            Price.bind('<KeyRelease>', totalAmount)
            Tax.bind('<KeyRelease>', totalAmount)

    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
        print(e)


def reservationF2():
    global reservationId
    r_id_list = []
    try:
        checkOutTime = "-"
        dbConnect()
        get_r_id = "select reservation_id from reservation_info"
        cur.execute(get_r_id)
        all_r_id = cur.fetchall()
        for i in all_r_id:
            r_id_list.append(i[0])
        reservationId = len(all_r_id) + 1
        reservationId = str(reservationId)
        curTime = now.strftime("%d-%m-%Y %H:%M:%S")
        insertDetails = "insert into reservation_info values("+reservationId+",'"+guestName+"',"+age+","+contactNo+",'"+email+"','"+address+"',"+numberOfChildren+","+numberOfAdults+","+numberOfDays+","+roomNumber+",'"+curTime+"','"+checkOutTime+"','"+curTime+"','"+pMode.get()+"',"+Total.get()+");"
        cur.execute(insertDetails)
        con.commit()
        updateStatus = "update rooms_info set status = 'Reserved' where room_no = "+roomNumber
        cur.execute(updateStatus)
        con.commit()
        con.close()

        resrveBtn.config(state="disabled")
        
        Total.delete(0, tk.END)
        Price.delete(0, tk.END)
        Tax.delete(0, tk.END)
        Total.config(state="disabled")
        Price.config(state="disabled")
        Tax.config(state="disabled")
        
        resd = "RESERVATION ID : "+reservationId
        tk.Label(filterFr, text=resd, font=("courier", 18), fg="cyan4",
                 bg="#e6ffe6").place(relx=0, rely=0, relwidth=1, relheight=1)
        messagebox.showinfo("Reserved", "Reservation done successfully!")
        askForReceipt()
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")


def checkBeforeRes():
    room_no_list = []

    try:
        dbConnect()
        allRoomNo = "select room_no from rooms_info"
        cur.execute(allRoomNo)
        all_room_no = cur.fetchall()
        for i in all_room_no:
            room_no_list.append(i[0])
        if int(rno.get()) not in room_no_list:
            messagebox.showwarning("Oops!", "Room Number does not Exist!")
        else:
            checkStatus = "select status from rooms_info where room_no = "+rno.get()
            cur.execute(checkStatus)
            f = cur.fetchall()
            Status = f[0][0]
            if Status == "Available":
                reservationF()
            else:
                messagebox.showwarning("Unavailable", "Room is Already Reserved")
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
            
            
def checkPaymentMethod():
    if pMode.get()=="" or pMode.get()=="None":
        messagebox.showwarning("Warning", "Please select payment method!")
    else:
        reservationF2()

def askForReceipt():
    answer = messagebox.askyesno("Receipt", "Print Receipt?")
    if answer:
        printReceipt()

#find rooms function
def findRoomsF(): 
    nb = cNob.get()
    ac = cAc.get()
    tv = cTv.get()
    wifi = cWifi.get()
    acyes = "0"
    tvyes = "0"
    wifiyes = "0"
    if nb == "please select..." or ac == "please select..." or tv == "please select..." or wifi == "please select...":
        messagebox.showinfo("Warning", "please select all the options!")
    else:
        if ac == "Yes":
            acyes = "1"
        else:
            acyes = "0"
        
        if tv == "Yes":
            tvyes = "1"
        else:
            tvyes == "0"
        
        if wifi == "Yes":
            wifiyes = "1"
        else:
            wifiyes == "0"
        
        try:
            dbConnect()
            get_details = "select room_no,room_price,status from rooms_info where no_of_beds = "+nb+" and ac = "+acyes+" and tv = "+tvyes+" and wifi = "+wifiyes+" and status = 'Available' order by room_price asc"
            cur.execute(get_details)
            x = cur.fetchall()
            listofrooms.delete(0,tk.END)
            if x == []:
                listofrooms.insert(tk.END,'No Matching Found')
            for i in x :
                listofrooms.insert(tk.END,'Room Number '+str(i[0])+' - Price - '+str(i[1]))
        except Exception as e:
            messagebox.showerror("Error", "Something went wrong!")
            print(e)

#main screen
def mainScr():
    global root, screen_width, screen_height, contentFrame, hotel_status, Rooms, Reserve, Payments, log_out, hotel_staff
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2)-(1100/2)
    y = (screen_height/2)-(600/2)
    x = int(x)
    y = int(y)
    x = str(x)
    y = str(y)
    xandy = "+"+x+"+"+y
    gmtry = "1080x550" + xandy
    root.geometry(gmtry)

    root.resizable(0,0)
    root.title("Hotel Management System")
    root.config(bg="silver")

    headingFrame = tk.Frame(root, bg="black")
    headingFrame.place(relx=0, rely=0, relwidth=1, relheight=0.12)
    heading = tk.Label(headingFrame, text="Hotel Management System", font=("dubai", 25),
                       bg="#e6ffe6", fg="#333300")
    heading.place(relx=0, rely=0, relwidth=1, relheight=0.98)

    tabsFrame = tk.Frame(root)
    tabsFrame.place(relx=0, rely=0.12, relwidth=1, relheight=0.25)

    path1 = "Images/hotelstatus.png"
    img1 = ImageTk.PhotoImage(Image.open(path1))
    b1 = tk.Button(tabsFrame, image=img1, text="b1", bg="white", command=hotelStatusScr)
    b1.image = img1
    b1.place(relx=0, rely=0, relwidth=0.17)

    path2 = "Images/rooms.png"
    img2 = ImageTk.PhotoImage(Image.open(path2))
    b2 = tk.Button(tabsFrame, image=img2, text="b2", bg="white", command=roomsScr)
    b2.image = img2
    b2.place(relx=0.17, rely=0, relwidth=0.17)

    path3 = "Images/bookroom.png"
    img3 = ImageTk.PhotoImage(Image.open(path3))
    b3 = tk.Button(tabsFrame, image=img3, text="b3", bg="white", command=reserveScr)
    b3.image = img3
    b3.place(relx=0.34, rely=0, relwidth=0.17)

    path4 = "Images/payments.png"
    img4 = ImageTk.PhotoImage(Image.open(path4))
    b4 = tk.Button(tabsFrame, image=img4, text="b4", bg="white", command=paymentsInfoScr)
    b4.image = img4
    b4.place(relx=0.51, rely=0, relwidth=0.17)

    path5 = "Images/guests.png"
    img5 = ImageTk.PhotoImage(Image.open(path5))
    b5 = tk.Button(tabsFrame, image=img5, text="b5", bg="white", command=staffScr)
    b5.image = img5
    b5.place(relx=0.68, rely=0, relwidth=0.17)

    path6 = "Images/logout.png"
    img6 = ImageTk.PhotoImage(Image.open(path6))
    b6 = tk.Button(tabsFrame, image=img6, text="b5", bg="white", command=exitF)
    b6.image = img6
    b6.place(relx=0.85, rely=0, relwidth=0.155, relheight=0.77)

    hotel_status = tk.Label(tabsFrame, text="Hotel Status", font="dubai 12",
             bg="white")
    hotel_status.place(relx=0, rely=0.77, relwidth=0.17, relheight=0.23)
    Rooms = tk.Label(tabsFrame, text="Rooms", font="dubai 12",
             bg="white")
    Rooms.place(relx=0.17, rely=0.77, relwidth=0.17, relheight=0.23)
    Reserve = tk.Label(tabsFrame, text="Reserve", font="dubai 12",
             bg="white")
    Reserve.place(relx=0.34, rely=0.77, relwidth=0.17, relheight=0.23)
    Payments = tk.Label(tabsFrame, text="Payments Info", font="dubai 12",
             bg="white")
    Payments.place(relx=0.51, rely=0.77, relwidth=0.17, relheight=0.23)
    hotel_staff = tk.Label(tabsFrame, text="Hotel Staff", font="dubai 12",
             bg="white")
    hotel_staff.place(relx=0.68, rely=0.77, relwidth=0.17, relheight=0.23)
    log_out = tk.Label(tabsFrame, text="Exit", font="dubai 12",
             bg="white")
    log_out.place(relx=0.85, rely=0.77, relwidth=0.15, relheight=0.23)

    contentFrame = tk.Frame(root, bg="silver")
    contentFrame.place(relx=0, rely=0.378, relwidth=1, relheight= 0.622)

    reserveScr()

    root.mainloop()

#reservation screen
def reserveScr():
    global resFr, fn, ln, ag, cn, em, ad, noc, noa, nod, rno, filterFr, cNob, cTv, cAc, cWifi, listofrooms
    for widgets in contentFrame.winfo_children():
        widgets.destroy()
    hotel_status.config(bg="white")
    Reserve.config(bg="#e6ffe6")
    Rooms.config(bg="white")
    Payments.config(bg="white")
    hotel_staff.config(bg="white")
    log_out.config(bg="white")
    resFr = tk.Frame(contentFrame, bg="#e6ffe6")
    resFr.place(relx=0, rely=0, relwidth=0.678, relheight=1)
    
    tk.Label(resFr, text="Personal Information", font=("dubai", 15),
             bg="#e6ffe6").place(relx=0, rely=0, relwidth=1)
    fn = tk.Entry(resFr)
    fn.place(relx=0.1, rely=0.13, relwidth=0.2, relheight=0.08)
    ln = tk.Entry(resFr)
    ln.place(relx=0.4, rely=0.13, relwidth=0.2, relheight=0.08)
    ag = tk.Entry(resFr)
    ag.place(relx=0.7, rely=0.13, relwidth=0.2, relheight=0.08)
    fn.insert(0, "First Name *")
    ln.insert(0, "Last Name *")
    ag.insert(0, "Age *")

    def on_entry_click1(event):
        if fn.get() == 'First Name *' :
            fn.delete(0,tk.END)
            fn.insert(0,'')
    def on_entry_click2(event):
        if ln.get() == 'Last Name *' :
            ln.delete(0,tk.END)
            ln.insert(0,'')
    def on_entry_click3(event):
        if ag.get() == 'Age *' :
            ag.delete(0,tk.END)
            ag.insert(0,'')
    def on_exit1(event):
        if fn.get()=='':
            fn.insert(0,'First Name *')
    def on_exit2(event):
        if ln.get()=='':
            ln.insert(0,'Last Name *')
    def on_exit3(event):
        if ag.get()=='':
            ag.insert(0,'Age *')

    fn.bind('<FocusIn>', on_entry_click1)
    ln.bind('<FocusIn>', on_entry_click2)
    ag.bind('<FocusIn>', on_entry_click3)
    fn.bind('<FocusOut>',on_exit1)
    ln.bind('<FocusOut>',on_exit2)
    ag.bind('<FocusOut>',on_exit3)

    tk.Label(resFr, text="Contact Information", font=("dubai", 15),
             bg="#e6ffe6").place(relx=0, rely=0.27, relwidth=1)
    cn = tk.Entry(resFr)
    cn.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.08)
    em = tk.Entry(resFr)
    em.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.08)
    ad = tk.Entry(resFr)
    ad.place(relx=0.7, rely=0.4, relwidth=0.2, relheight=0.08)
    cn.insert(0, "Contact Number *")
    em.insert(0, "Email")
    ad.insert(0, "Address *")
    
    def on_entry_click4(event):
        if cn.get() == 'Contact Number *' :
            cn.delete(0,tk.END)
            cn.insert(0,'')
    def on_entry_click5(event):
        if em.get() == 'Email' :
            em.delete(0,tk.END)
            em.insert(0,'')
    def on_entry_click6(event):
        if ad.get() == "Address *" :
            ad.delete(0,tk.END)
            ad.insert(0,'')
    def on_exit4(event):
        if cn.get()=='':
            cn.insert(0,'Contact Number *')
    def on_exit5(event):
        if em.get()=='':
            em.insert(0,'Email')
    def on_exit6(event):
        if ad.get()=='':
            ad.insert(0,"Address *")

    cn.bind('<FocusIn>', on_entry_click4)
    em.bind('<FocusIn>', on_entry_click5)
    ad.bind('<FocusIn>', on_entry_click6)
    cn.bind('<FocusOut>',on_exit4)
    em.bind('<FocusOut>',on_exit5)
    ad.bind('<FocusOut>',on_exit6)

    tk.Label(resFr, text="Reservation Information", font=("dubai", 15),
             bg="#e6ffe6").place(relx=0, rely=0.54, relwidth=1)
    noc = tk.Entry(resFr)
    noc.place(relx=0.1, rely=0.67, relwidth=0.2, relheight=0.08)
    noa = tk.Entry(resFr)
    noa.place(relx=0.4, rely=0.67, relwidth=0.2, relheight=0.08)
    nod = tk.Entry(resFr)
    nod.place(relx=0.7, rely=0.67, relwidth=0.2, relheight=0.08)
    noc.insert(0, "Number of Children *")
    noa.insert(0, "Number of Adults *")
    nod.insert(0, "Number of Days of Stay *")

    def on_entry_click7(event):
        if noc.get() == 'Number of Children *' :
            noc.delete(0,tk.END)
            noc.insert(0,'')
    def on_entry_click8(event):
        if noa.get() == 'Number of Adults *' :
            noa.delete(0,tk.END)
            noa.insert(0,'')
    def on_entry_click9(event):
        if nod.get() == 'Number of Days of Stay *' :
            nod.delete(0,tk.END)
            nod.insert(0,'')
    def on_exit7(event):
        if noc.get()=='':
            noc.insert(0,'Number of Children *')
    def on_exit8(event):
        if noa.get()=='':
            noa.insert(0,'Number of Adults *')
    def on_exit9(event):
        if nod.get()=='':
            nod.insert(0,'Number of Days of Stay *')

    noc.bind('<FocusIn>', on_entry_click7)
    noa.bind('<FocusIn>', on_entry_click8)
    nod.bind('<FocusIn>', on_entry_click9)
    noc.bind('<FocusOut>',on_exit7)
    noa.bind('<FocusOut>',on_exit8)
    nod.bind('<FocusOut>',on_exit9)

    rno = tk.Entry(resFr)
    rno.place(relx=0.1, rely=0.85, relwidth=0.2, relheight=0.08)
    rno.insert(0, "Enter Room Number *")

    def on_entry_click10(event):
        if rno.get() == 'Enter Room Number *' :
            rno.delete(0,tk.END)
            rno.insert(0,'')
    def on_exit10(event):
        if rno.get()=='':
            rno.insert(0,'Enter Room Number *')
    rno.bind('<FocusIn>', on_entry_click10)
    rno.bind('<FocusOut>',on_exit10)

    res = tk.Button(resFr, text="Reserve", font=("dubai",13), bg=None, fg="cyan4", bd=3, command=checkBeforeRes)
    res.place(relx=0.4, rely=0.83, relwidth=0.15, relheight=0.1)
    unres = tk.Button(resFr, text="Unreserve", font=("dubai",13), bg=None, fg="cyan4", bd=3, command=confirmUnres)
    unres.place(relx=0.6, rely=0.83, relwidth=0.15, relheight=0.1)
    

    filterFr = tk.Frame(contentFrame, bg="#e6ffe6")
    filterFr.place(relx=0.682, rely=0, relwidth=0.318, relheight=1)
    
    tk.Label(filterFr, text="Filter", font=("dubai", 15),
             bg="#e6ffe6").place(relx=0, rely=0, relwidth=1)
    tk.Label(filterFr, text="Beds :", font=("dubai", 13),
             bg="#e6ffe6").place(relx=0.15, rely=0.12)
    cNob = ttk.Combobox(filterFr, values=["please select...", "1", "2", "3"], state="readonly")
    cNob.place(relx=0.35, rely=0.14, relwidth=0.4, relheight=0.06)
    cNob.current(0)
    tk.Label(filterFr, text="AC :", font=("dubai", 13),
             bg="#e6ffe6").place(relx=0.15, rely=0.22)
    cAc = ttk.Combobox(filterFr, values=["please select...", "Yes", "No"], state="readonly")
    cAc.place(relx=0.35, rely=0.24, relwidth=0.4, relheight=0.06)
    cAc.current(0)

    tk.Label(filterFr, text="TV :", font=("dubai", 13),
             bg="#e6ffe6").place(relx=0.15, rely=0.32)
    cTv = ttk.Combobox(filterFr, values=["please select...", "Yes", "No"], state="readonly")
    cTv.place(relx=0.35, rely=0.34, relwidth=0.4, relheight=0.06)
    cTv.current(0)

    tk.Label(filterFr, text="WiFi :", font=("dubai", 13),
             bg="#e6ffe6").place(relx=0.15, rely=0.42)
    cWifi = ttk.Combobox(filterFr, values=["please select...", "Yes", "No"], state="readonly")
    cWifi.place(relx=0.35, rely=0.44, relwidth=0.4, relheight=0.06)
    cWifi.current(0)

    findrooms = tk.Button(filterFr, text="Find Rooms", font=("dubai", 12), fg="cyan4", bg=None, command=findRoomsF)
    findrooms.place(relx=0.35, rely=0.55, relwidth=0.3, relheight=0.08)

    listofrooms = tk.Listbox(filterFr)
    listofrooms.place(relx=0.1, rely=0.68, relwidth=0.69, relheight=0.23)
    listofrooms.insert(1, "Rooms of your choice will appear here")
    listofrooms.insert(2, "once you apply filter")
    sc = tk.Scrollbar(filterFr)
    sc.place(relx=0.79, rely=0.68, relheight=0.23)

def hotelStatusScr():
    for widgets in contentFrame.winfo_children():
        widgets.destroy()
    hotel_status.config(bg="#e6ffe6")
    Reserve.config(bg="white")
    Rooms.config(bg="white")
    Payments.config(bg="white")
    hotel_staff.config(bg="white")
    log_out.config(bg="white")

    try:
        dbConnect()
        rno_list = []
        get_all_rno = "select room_no from rooms_info"
        cur.execute(get_all_rno)
        all_rno=cur.fetchall()
        for i in all_rno:
            rno_list.append(i[0])
        trm = len(rno_list)

        avrm_list = []
        get_all_avrm = "select room_no from rooms_info where status = 'Available'"
        cur.execute(get_all_avrm)
        all_avrm=cur.fetchall()
        for i in all_avrm:
            avrm_list.append(i[0])
        avrm = len(avrm_list)

        tres_list = []
        get_all_tres = "select room_no from rooms_info where status = 'Reserved'"
        cur.execute(get_all_tres)
        all_tres=cur.fetchall()
        for i in all_tres:
            tres_list.append(i[0])
        tres = len(tres_list)

        tcs_list = []
        get_all_tcs = "select no_of_adults, no_of_children from reservation_info"
        cur.execute(get_all_tcs)
        all_tcs=cur.fetchall()
        for i in all_tcs:
            tcs_list.append(i[0])
            tcs_list.append(i[1])
        tcs = sum(tcs_list)

        tst_list = []
        get_all_tst = "select staff_id from staff_info"
        cur.execute(get_all_tst)
        all_tst=cur.fetchall()
        for i in all_tst:
            tst_list.append(i[0])
        tst = len(tst_list)
    
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
    
    frame1 = tk.Frame(contentFrame, bg="#e6ffe6")
    frame1.place(relx=0, rely=0, relwidth=1, relheight=1)

    tk.Label(frame1, text="Total Rooms", font=("dubai", 15), bg="cyan4",
             fg="white").place(relx=0, rely=0, relwidth=0.195, relheight=0.15)
    tk.Label(frame1, text="Available Rooms", font=("dubai", 15), bg="cyan4",
             fg="white").place(relx=0.2, rely=0, relwidth=0.195, relheight=0.15)
    tk.Label(frame1, text="Reservations", font=("dubai", 15), bg="cyan4",
             fg="white").place(relx=0.4, rely=0, relwidth=0.2, relheight=0.15)
    tk.Label(frame1, text="Customers", font=("dubai", 15), bg="cyan4",
             fg="white").place(relx=0.605, rely=0, relwidth=0.195, relheight=0.15)
    tk.Label(frame1, text="Total Staff", font=("dubai", 15), bg="cyan4",
             fg="white").place(relx=0.805, rely=0, relwidth=0.195, relheight=0.15)
    
    tr = tk.Label(frame1, text=trm, font=("dubai", 40), bg="white", fg="cyan4")
    tr.place(relx=0, rely=0.15, relwidth=0.195, relheight=0.5)

    ar = tk.Label(frame1, text=avrm, font=("dubai", 40), bg="white", fg="cyan4")
    ar.place(relx=0.2, rely=0.15, relwidth=0.195, relheight=0.5)

    trs = tk.Label(frame1, text=tres, font=("dubai", 40), bg="white", fg="cyan4")
    trs.place(relx=0.4, rely=0.15, relwidth=0.2, relheight=0.5)

    tc = tk.Label(frame1, text=tcs, font=("dubai", 40), bg="white", fg="cyan4")
    tc.place(relx=0.605, rely=0.15, relwidth=0.195, relheight=0.5)

    ts = tk.Label(frame1, text=tst, font=("dubai", 40), bg="white", fg="cyan4")
    ts.place(relx=0.805, rely=0.15, relwidth=0.195, relheight=0.5)

    vr = tk.Button(frame1, text="Record Book", font=("dubai", 13), bg="#00b38f", fg="white", command=resHistoryScr)
    vr.place(relx=0.885, rely=0.7, relwidth=0.1, relheight=0.1)

#staff screen
def staffScr():
    global rFrame
    for widgets in contentFrame.winfo_children():
        widgets.destroy()
    hotel_staff.config(bg="#e6ffe6")
    Reserve.config(bg="white")
    Rooms.config(bg="white")
    Payments.config(bg="white")
    hotel_status.config(bg="white")
    log_out.config(bg="white")
    
    frame1 = tk.Frame(contentFrame, bg="#e6ffe6")
    frame1.place(relx=0, rely=0, relwidth=0.22, relheight=1)

    b1 = tk.Button(frame1, text="ADD STAFF", font=("dubai", 13), bg=None, fg="cyan4", bd=3, command=addStaffScr)
    b1.place(relx=0.2, rely=0.15, relwidth=0.6, relheight=0.12)


    b2 = tk.Button(frame1, text="VIEW STAFF", font=("dubai", 13), bg=None, fg="cyan4", bd=3, command=viewStaffScr)
    b2.place(relx=0.2, rely=0.35, relwidth=0.6, relheight=0.12)

    b3 = tk.Button(frame1, text="DELETE STAFF", font=("dubai", 13), bg=None, fg="cyan4", bd=3, command=delStaffScr)
    b3.place(relx=0.2, rely=0.55, relwidth=0.6, relheight=0.12)

    b4 = tk.Button(frame1, text="UPDATE STAFF", font=("dubai", 13), bg=None, fg="cyan4", bd=3, command=updateStaffScr)
    b4.place(relx=0.2, rely=0.75, relwidth=0.6, relheight=0.12)

    rFrame = tk.Frame(contentFrame, bg="#e6ffe6")
    rFrame.place(relx=0.225, rely=0, relwidth=0.775, relheight=1)
    addStaffScr()


#view staff screen
def viewStaffScr():
    global tree, sby, sbar
    for widgets in rFrame.winfo_children():
        widgets.destroy()

    frame2 = tk.Frame(rFrame, bg="cyan4")
    frame2.place(relx=0, rely=0, relwidth=1, relheight=0.25)

    tk.Label(frame2, text="Search Staff :", font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0.03, rely=0.3)
    sbar = tk.Entry(frame2, font=("dubai", 12), fg="#666666", relief="solid", bd=1)
    sbar.place(relx=0.2, rely=0.34, relwidth=0.25, relheight=0.38)

    sby = ttk.Combobox(frame2, font=("dubai", 11), values=["Search By", "Staff ID", "Name", "Department", "Contact Number", "Email", "D.O.B", "Job Role"], state="readonly")
    sby.place(relx=0.48, rely=0.32, relwidth=0.15, relheight=0.4)
    sby.current(0)


    sbtn = tk.Button(frame2, text="Search", font=("dubai", 15), bg=None, fg="cyan4", bd=3, command=searchStaff)
    sbtn.place(relx=0.66, rely=0.32, relwidth=0.1, relheight=0.41)


    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=("dubai", 12), rowheight=35) 
    style.configure("mystyle.Treeview.Heading", font=('dubai', 15),background="lightyellow",foreground="cyan4") 

    tree=ttk.Treeview(rFrame, column=("c1","c2","c3","c4","c5","c6","c7","c8", "c9", "c10"),show="headings",style="mystyle.Treeview")
    tree.column("c1", anchor="center", width=80)
    tree.heading("c1", text="Staff ID")
    tree.column("c2", anchor="center")
    tree.heading("c2", text="Name")
    tree.column("c3", anchor="center")
    tree.heading("c3", text="Contact No")
    tree.column("c4", anchor="center")
    tree.heading("c4", text="Email")
    tree.column("c5", anchor="center")
    tree.heading("c5", text="Address")
    tree.column("c6", anchor="center")
    tree.heading("c6", text="Date of Birth")
    tree.column("c7", anchor="center")
    tree.heading("c7", text="Department")
    tree.column("c8", anchor="center")
    tree.heading("c8", text="Job Role")
    tree.column("c9", anchor="center")
    tree.heading("c9", text="Job Description")
    tree.column("c10", anchor="center")
    tree.heading("c10", text="Added On")


    tree.place(relx=0,rely=0.25,relwidth=1,relheight=0.75)

    s1 = tk.Scrollbar(tree,orient="horizontal")
    s1.pack(side="bottom",fill="x")
    s1.config(command=tree.xview)
    s2 = tk.Scrollbar(tree,orient="vertical")
    s2.pack(side="right", fill="y")
    s2.config(command=tree.yview)

    try:
        sid_list = []
        dbConnect()
        get_all_sid = "select staff_id from staff_info"
        cur.execute(get_all_sid)
        all_sid=cur.fetchall()
        for i in all_sid:
            sid_list.append(i[0])
        sidlen = len(all_sid)
        totalsid = "Total Staff : "+str(sidlen)
        tk.Label(frame2, text=totalsid, font=("dubai", 18), bg="cyan4"
                 ,fg="white").place(relx=0.78, rely=0.3)

        
    except Exception as e:
        print(e)

    try:
        dbConnect()
        get_st_details = "SELECT * FROM staff_info"
        cur.execute(get_st_details)
        for i in cur:
            tdata=[i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]]
            a=tdata[0]
            b=tdata[1]
            c=tdata[2]
            d=tdata[3]
            e=tdata[4]
            f=tdata[5]
            g=tdata[6]
            h=tdata[7]
            j=tdata[8]
            k=tdata[9]
            tree.insert('','end',values=(a,b,c,d,e,f,g,h,j,k))
    except Exception as e:
        messagebox.showerror("Error","Failed to fetch data")
        print(e)

#search staff
def searchStaff():
   
    for item in tree.get_children():
        tree.delete(item)
        
    searchBy = sby.get()
    searchValue = sbar.get()

    try:
        dbConnect()
        if searchBy == "Staff ID":
            searchstaff = "SELECT * FROM staff_info WHERE staff_id LIKE '%"+searchValue+"%'"
        if searchBy == "Name":
            searchstaff = "SELECT * FROM staff_info WHERE name LIKE '%"+searchValue+"%'"
        if searchBy == "Contact Number":
            searchstaff = "SELECT * FROM staff_info WHERE contact_no LIKE '%"+searchValue+"%'"
        if searchBy == "Email":
            searchstaff = "SELECT * FROM staff_info WHERE email LIKE '%"+searchValue+"%'"
        if searchBy == "D.O.B":
            searchstaff = "SELECT * FROM staff_info WHERE dob LIKE '%"+searchValue+"%'"
        if searchBy == "Job Role":
            searchstaff = "SELECT * FROM staff_info WHERE role LIKE '%"+searchValue+"%'"
        if searchBy == "Department":
            searchstaff = "SELECT * FROM staff_info WHERE department LIKE '%"+searchValue+"%'"
        if searchBy == "Search By":
            searchstaff = "SELECT * FROM staff_info WHERE staff_id = NULL"
            messagebox.showwarning("Warning", "Please select search by option")
    except Exception as e:
        messagebox.warning("Error", "Something went wrong!")
        print(e)

    try:
        dbConnect()
        cur.execute(searchstaff)
        for i in cur:
            tdata=[i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]]
            a=tdata[0]
            b=tdata[1]
            c=tdata[2]
            d=tdata[3]
            e=tdata[4]
            f=tdata[5]
            g=tdata[6]
            h=tdata[7]
            j=tdata[8]
            k=tdata[9]
            tree.insert('','end',values=(a,b,c,d,e,f,g,h,j,k))
    except Exception as e:
        messagebox.showerror("Error","Failed to fetch data")
        print(e)

#add staff screen
def addStaffScr():
    global staffId, sname, dob, dept, contactno, semail, saddr, jobr, jobdesc
    for widgets in rFrame.winfo_children():
        widgets.destroy()

    try:
        dbConnect()
        s_id_list = []
        get_s_id = "select staff_id from staff_info"
        cur.execute(get_s_id)
        all_s_id = cur.fetchall()
        for i in all_s_id:
            s_id_list.append(i[0])
        staff_Id_last_index = len(s_id_list)
        
        if staff_Id_last_index == 0:
            staff_Id = 1
            staff_Id = str(staff_Id)
        else:
            staff_Id_last_index = len(s_id_list)-1
            staff_Id = s_id_list[staff_Id_last_index]
            staff_Id = staff_Id + 1
            staff_Id = str(staff_Id)
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong")

    stId = "STAFF ID : "+staff_Id

    tk.Label(rFrame, text="ADD STAFF", font=("dubai", 18), bg="cyan4", 
             fg="white").place(relx=0, rely=0, relwidth=1, relheight=0.15)

    tk.Label(rFrame, text=stId, font=("dubai", 15), bg="#e6ffe6", 
             fg="#006600").place(relx=0.05, rely=0.2)

    tk.Label(rFrame, text="Name :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.21, rely=0.2)
    sname = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    sname.place(relx=0.29, rely=0.22, relwidth=0.32, relheight=0.07)

    tk.Label(rFrame, text="Email :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.65, rely=0.2)
    semail = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    semail.place(relx=0.73, rely=0.22, relwidth=0.22, relheight=0.07)

    tk.Label(rFrame, text="Department :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.05, rely=0.5)

    dept = tk.StringVar()
    

    r1 = tk.Radiobutton(rFrame, text='Customer Executive', font=("dubai", 15), bg="#e6ffe6", value='customerexe', var=dept)
    r2 = tk.Radiobutton(rFrame, text='Restaurant', font=("dubai", 15), bg="#e6ffe6", value='restaurant', var=dept)
    r3 = tk.Radiobutton(rFrame, text='Room Service', font=("dubai", 15), bg="#e6ffe6", value='roomservice', var=dept)
    r4 = tk.Radiobutton(rFrame, text='Other', font=("dubai", 15), bg="#e6ffe6", value='-', var=dept)

    r1.place(relx=0.2, rely=0.52, relheight=0.08)
    r2.place(relx=0.45, rely=0.52, relheight=0.08)
    r3.place(relx=0.63, rely=0.52, relheight=0.08)
    r4.place(relx=0.83, rely=0.52, relheight=0.08)
    dept.set(None)

    tk.Label(rFrame, text="Contact No :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.05, rely=0.35)
    contactno = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    contactno.place(relx=0.185, rely=0.37, relwidth=0.15, relheight=0.07)

    tk.Label(rFrame, text="D.O.B :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.365, rely=0.35)
    dob = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    dob.place(relx=0.448, rely=0.37, relwidth=0.142, relheight=0.07)
    dob.insert(0, "dd-mm-yy")

    def on_entry_click13(event):
        if dob.get() == 'dd-mm-yy' :
            dob.delete(0,tk.END)
            dob.insert(0,'')
    def on_exit13(event):
        if dob.get()=='':
            dob.insert(0,'dd-mm-yy')
    dob.bind('<FocusIn>', on_entry_click13)
    dob.bind('<FocusOut>', on_exit13)

    tk.Label(rFrame, text="Address :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.627, rely=0.35)
    saddr = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    saddr.place(relx=0.73, rely=0.37, relwidth=0.22, relheight=0.07)

    tk.Label(rFrame, text="Job Role :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.05, rely=0.65)
    jobr = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    jobr.place(relx=0.16, rely=0.67, relwidth=0.2, relheight=0.07)

    tk.Label(rFrame, text="Job Description :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.39, rely=0.65)
    jobdesc = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    jobdesc.place(relx=0.565, rely=0.67, relwidth=0.385, relheight=0.07)

    addbtn = tk.Button(rFrame, text="Add Staff", font=("dubai", 14), bg="#00b386",
                           fg="white", bd=3, command=addStaffF)
    addbtn.place(relx=0.425, rely=0.82, relwidth=0.15, relheight=0.1)

#delete staff screen
def delStaffScr():
    global srch, focusF
    for widgets in rFrame.winfo_children():
        widgets.destroy()
    focusF = "delstaff"
    frame1 = tk.Frame(rFrame, bg="cyan4")
    frame1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
    tk.Label(frame1, text="Enter Staff ID :", font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0.25, rely=0, relheight=1)
    srch = tk.Entry(frame1, font=("dubai", 15), relief="solid", bd=1)
    srch.place(relx=0.44, rely=0.3, relwidth=0.15, relheight=0.4)
    srBtn = tk.Button(frame1, text="OK", font=("dubai", 14), bg=None, fg="cyan4", bd=3, command=checkStaffId)
    srBtn.place(relx=0.613, rely=0.3, relwidth=0.06, relheight=0.45)

#update staff screen
def updateStaffScr():
    global staffId, sname, dob, dept, contactno, semail, saddr, jobr, jobdesc, srch, focusF
    for widgets in rFrame.winfo_children():
        widgets.destroy()
    focusF = "updatestaff"
    frame1 = tk.Frame(rFrame, bg="cyan4")
    frame1.place(relx=0, rely=0, relwidth=1, relheight=0.15)
    tk.Label(frame1, text="Enter Staff ID :", font=("dubai", 16), bg="cyan4",
             fg="white").place(relx=0.27, rely=0, relheight=1)
    srch = tk.Entry(frame1, font=("dubai", 15), relief="solid", bd=1)
    srch.place(relx=0.44, rely=0.25, relwidth=0.15, relheight=0.5)
    srBtn = tk.Button(frame1, text="OK", font=("dubai", 14), bg=None, fg="cyan4", bd=3, command=checkStaffId)
    srBtn.place(relx=0.613, rely=0.25, relwidth=0.06, relheight=0.5)

    tk.Label(rFrame, text="Staff ID :", font=("dubai", 15), bg="#e6ffe6", 
             fg="#006600").place(relx=0.05, rely=0.2)

    tk.Label(rFrame, text="Name :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.21, rely=0.2)
    sname = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    sname.place(relx=0.29, rely=0.22, relwidth=0.32, relheight=0.07)

    tk.Label(rFrame, text="Email :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.65, rely=0.2)
    semail = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    semail.place(relx=0.73, rely=0.22, relwidth=0.22, relheight=0.07)

    tk.Label(rFrame, text="Department :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.05, rely=0.5)

    dept = tk.StringVar()
    
    r1 = tk.Radiobutton(rFrame, text='Customer Executive', font=("dubai", 15), bg="#e6ffe6", value='customerexe', var=dept)
    r2 = tk.Radiobutton(rFrame, text='Restaurant', font=("dubai", 15), bg="#e6ffe6", value='restaurant', var=dept)
    r3 = tk.Radiobutton(rFrame, text='Room Service', font=("dubai", 15), bg="#e6ffe6", value='roomservice', var=dept)
    r4 = tk.Radiobutton(rFrame, text='Other', font=("dubai", 15), bg="#e6ffe6", value='-', var=dept)

    r1.place(relx=0.2, rely=0.52, relheight=0.08)
    r2.place(relx=0.45, rely=0.52, relheight=0.08)
    r3.place(relx=0.63, rely=0.52, relheight=0.08)
    r4.place(relx=0.83, rely=0.52, relheight=0.08)
    dept.set(None)

    tk.Label(rFrame, text="Contact No :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.05, rely=0.35)
    contactno = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    contactno.place(relx=0.185, rely=0.37, relwidth=0.15, relheight=0.07)

    tk.Label(rFrame, text="D.O.B :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.365, rely=0.35)
    dob = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    dob.place(relx=0.448, rely=0.37, relwidth=0.142, relheight=0.07)
    tk.Label(rFrame, text="Address :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.627, rely=0.35)
    saddr = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    saddr.place(relx=0.73, rely=0.37, relwidth=0.22, relheight=0.07)

    tk.Label(rFrame, text="Job Role :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.05, rely=0.65)
    jobr = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    jobr.place(relx=0.16, rely=0.67, relwidth=0.2, relheight=0.07)

    tk.Label(rFrame, text="Job Description :", font=("dubai", 15), bg="#e6ffe6", 
             fg="black").place(relx=0.39, rely=0.65)
    jobdesc = tk.Entry(rFrame, font=("dubai", 12), relief="solid")
    jobdesc.place(relx=0.565, rely=0.67, relwidth=0.385, relheight=0.07)

    saveBtn = tk.Button(rFrame, text="SAVE", font=("dubai", 14), bg="#00b386",
                           fg="white", bd=3, command=updateStaffF2)
    saveBtn.place(relx=0.425, rely=0.82, relwidth=0.15, relheight=0.1)


#room screen
def roomsScr():
    global rFrame
    for widgets in contentFrame.winfo_children():
        widgets.destroy()
    hotel_status.config(bg="white")
    Reserve.config(bg="white")
    Rooms.config(bg="#e6ffe6")
    Payments.config(bg="white")
    hotel_staff.config(bg="white")
    log_out.config(bg="white")
    
    frame1 = tk.Frame(contentFrame, bg="#e6ffe6")
    frame1.place(relx=0, rely=0, relwidth=0.22, relheight=1)

    b1 = tk.Button(frame1, text="Search Room", font=("dubai", 15), bg=None, fg="cyan4", bd=3, command=searchRoomScr)
    b1.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.12)


    b2 = tk.Button(frame1, text="Add Room", font=("dubai", 15), bg=None, fg="cyan4", bd=3, command=addRoomScr)
    b2.place(relx=0.2, rely=0.4, relwidth=0.6, relheight=0.12)

    b3 = tk.Button(frame1, text="Delete Room", font=("dubai", 15), bg=None, fg="cyan4", bd=3, command=delRoomScr)
    b3.place(relx=0.2, rely=0.6, relwidth=0.6, relheight=0.12)

    rFrame = tk.Frame(contentFrame, bg="#e6ffe6")
    rFrame.place(relx=0.225, rely=0, relwidth=0.775, relheight=1)

    addRoomScr()

#add room screen
def addRoomScr():
    global roomNo, noOfBeds, roomPrice, ac, tv, wifi
    for widgets in rFrame.winfo_children():
        widgets.destroy()

    tk.Label(rFrame, text="ADD ROOM", font=("dubai", 18), bg="cyan4", 
             fg="white").place(relx=0, rely=0, relwidth=1, relheight=0.15)
    
    roomNo = tk.Entry(rFrame, font=("dubai", 15), fg=None)
    roomNo.place(relx=0, rely=0.15, relwidth=1, relheight=0.13)
    noOfBeds = tk.Entry(rFrame, font=("dubai", 15), fg=None)
    noOfBeds.place(relx=0, rely=0.28, relwidth=1, relheight=0.13)
    roomPrice = tk.Entry(rFrame, font=("dubai", 15), bd=0, fg=None)
    roomPrice.place(relx=0, rely=0.54, relwidth=1, relheight=0.13)
    
    roomNo.insert(0, "Enter Room Number *")
    noOfBeds.insert(0, "Number of Beds *")
    roomPrice.insert(0, "Room Price *")

    def on_entry_click10(event):
        if roomNo.get() == 'Enter Room Number *' :
            roomNo.delete(0,tk.END)
            roomNo.insert(0,'')
    def on_entry_click11(event):
        if noOfBeds.get() == 'Number of Beds *' :
            noOfBeds.delete(0,tk.END)
            noOfBeds.insert(0,'')
    def on_entry_click12(event):
        if roomPrice.get() == 'Room Price *' :
            roomPrice.delete(0,tk.END)
            roomPrice.insert(0,'')
    def on_exit10(event):
        if roomNo.get()=='':
            roomNo.insert(0,'Enter Room Number *')
    def on_exit11(event):
        if noOfBeds.get()=='':
            noOfBeds.insert(0,'Number of Beds *')
    def on_exit12(event):
        if roomPrice.get()=='':
            roomPrice.insert(0,'Room Price *')

    roomNo.bind('<FocusIn>', on_entry_click10)
    noOfBeds.bind('<FocusIn>', on_entry_click11)
    roomPrice.bind('<FocusIn>', on_entry_click12)
    roomNo.bind('<FocusOut>',on_exit10)
    noOfBeds.bind('<FocusOut>',on_exit11)
    roomPrice.bind('<FocusOut>',on_exit12)
    
    fcFrame = tk.Frame(rFrame, bg="white", relief="sunken", bd=1)
    fcFrame.place(relx=0, rely=0.41, relwidth=1, relheight=0.13)
    tk.Label(fcFrame, text="Facilities :", font=("dubai", 16), bg="white", 
             fg=None).place(relx=0, rely=0, relheight=1)

    ac = tk.IntVar()
    tv = tk.IntVar()
    wifi = tk.IntVar()
    
    c1 = tk.Checkbutton(fcFrame, text='AC', font=("dubai", 15), bg="white",
                        variable=ac, fg=None, onvalue=1, offvalue=0)
    c1.place(relx=0.15, rely=0, relheight=1)
    c2 = tk.Checkbutton(fcFrame, text='TV', font=("dubai", 15), bg="white",
                        variable=tv, fg=None, onvalue=1, offvalue=0)
    c2.place(relx=0.25, rely=0, relheight=1)
    c3 = tk.Checkbutton(fcFrame, text='WiFi', font=("dubai", 15), bg="white",
                          variable=wifi, fg=None, onvalue=1, offvalue=0)
    c3.place(relx=0.35, rely=0, relheight=1)

    addRoomBtn = tk.Button(rFrame, text="Add Room", font=("dubai", 16), bg="#00b386",
                           fg="white", bd=3, command=addRoomF)
    addRoomBtn.place(relx=0.425, rely=0.75, relwidth=0.15, relheight=0.12)


#search room screen
def searchRoomScr():
    global srch, focusF
    focusF = "srchF"
    for widgets in rFrame.winfo_children():
        widgets.destroy()
    frame1 = tk.Frame(rFrame, bg="cyan4")
    frame1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
    tk.Label(frame1, text="Enter Room Number :", font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0.2, rely=0, relheight=1)
    srch = tk.Entry(frame1, font=("dubai", 15), relief="solid", bd=1)
    srch.place(relx=0.47, rely=0.3, relwidth=0.15, relheight=0.4)
    srBtn = tk.Button(frame1, text="Search", font=("dubai", 14), bg=None, fg="cyan4", bd=3, command=checkRoomNo)
    srBtn.place(relx=0.645, rely=0.3, relwidth=0.1, relheight=0.45)


#delete room screen
def delRoomScr():
    global srch, focusF
    focusF = "delF"
    for widgets in rFrame.winfo_children():
        widgets.destroy()
    frame1 = tk.Frame(rFrame, bg="cyan4")
    frame1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
    tk.Label(frame1, text="Enter Room Number :", font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0.2, rely=0, relheight=1)
    srch = tk.Entry(frame1, font=("dubai", 15), relief="solid", bd=1)
    srch.place(relx=0.47, rely=0.3, relwidth=0.15, relheight=0.4)
    srBtn = tk.Button(frame1, text="OK", font=("dubai", 14), bg=None, fg="cyan4", bd=3, command=checkRoomNo)
    srBtn.place(relx=0.64, rely=0.3, relwidth=0.06, relheight=0.45)

#update room screen
def updateRoomScr():
    for widgets in rFrame.winfo_children():
        widgets.destroy()
    global ac, tv, wifi, roomno, roomprice, noofbeds
    tk.Label(rFrame, text="UPDATE ROOM", font=("dubai", 18), bg="cyan4", 
             fg="white").place(relx=0, rely=0, relwidth=1, relheight=0.15)
    tk.Label(rFrame, text="Room No", font=("dubai", 16), bg="cyan4", 
             fg="white").place(relx=0, rely=0.153, relwidth=0.3, relheight=0.13)
    roomno = tk.Entry(rFrame, font=("dubai", 15))
    roomno.place(relx=0.3, rely=0.153, relwidth=1, relheight=0.13)

    tk.Label(rFrame, text="Number of Beds", font=("dubai", 16), bg="cyan4", 
             fg="white").place(relx=0, rely=0.286, relwidth=0.3, relheight=0.13)
    noofbeds = tk.Entry(rFrame, font=("dubai", 15))
    noofbeds.place(relx=0.3, rely=0.286, relwidth=1, relheight=0.13)

    tk.Label(rFrame, text="Facilities", font=("dubai", 16), bg="cyan4", 
             fg="white").place(relx=0, rely=0.552, relwidth=0.3, relheight=0.13)
    fFrame  = tk.Frame(rFrame, bg="white")
    fFrame.place(relx=0.3, rely=0.552, relwidth=0.7, relheight=0.13)

    ac = tk.IntVar()
    tv = tk.IntVar()
    wifi = tk.IntVar()
    
    c1 = tk.Checkbutton(fFrame, text='AC', font=("dubai", 15), bg="white",
                        variable=ac, fg=None, onvalue=1, offvalue=0)
    c1.place(relx=0.1, rely=0, relheight=1)
    c2 = tk.Checkbutton(fFrame, text='TV', font=("dubai", 15), bg="white",
                        variable=tv, fg=None, onvalue=1, offvalue=0)
    c2.place(relx=0.3, rely=0, relheight=1)
    c3 = tk.Checkbutton(fFrame, text='WiFi', font=("dubai", 15), bg="white",
                          variable=wifi, fg=None, onvalue=1, offvalue=0)
    c3.place(relx=0.5, rely=0, relheight=1)

    tk.Label(rFrame, text="Room Price", font=("dubai", 16), bg="cyan4", 
             fg="white").place(relx=0, rely=0.419, relwidth=0.3, relheight=0.13)
    roomprice = tk.Entry(rFrame, font=("dubai", 15))
    roomprice.place(relx=0.3, rely=0.419, relwidth=1, relheight=0.13)
    saveBtn = tk.Button(rFrame, text="SAVE", font=("dubai", 15), bg="#00b386",
                           fg="white", bd=3, command=updateRoomF2)
    saveBtn.place(relx=0.45, rely=0.75, relwidth=0.125, relheight=0.1)
    

#update room function
def updateRoomF():
    global roomnumber
    roomnumber = str(srch.get()).rstrip()
    updateRoomScr()
    try:
        dbConnect()
        searchRoom = "select * from rooms_info where room_no = "+roomnumber+";"
        cur.execute(searchRoom)
        info = cur.fetchall()
        room_info = list(info[0])
        r_no = room_info[0]
        n_o_b = room_info[1]
        r_p = room_info[6]

        if room_info[2]==1:
            ac.set(1)

        if room_info[3]==1:
            tv.set(1)

        if room_info[4]==1:
            wifi.set(1)

        roomno.insert(0,roomnumber)
        roomprice.insert(0, r_p)
        noofbeds.insert(0, n_o_b)
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
    

def updateRoomF2():
    ac_ = str(ac.get())
    tv_ = str(tv.get())
    wifi_ = str(wifi.get())
    roomno_ = str(roomno.get()).rstrip()
    roomprice_ = str(roomprice.get()).rstrip()
    noofbeds_ = str(noofbeds.get()).rstrip()

    try:
        dbConnect()
        updateroom = "update rooms_info set room_no = "+ roomno_ +", no_of_beds = "+ noofbeds_ +", room_price = "+ roomprice_ +", ac = "+ ac_ +", tv = "+ tv_ +", wifi = "+ wifi_ +" where room_no = "+roomnumber
        cur.execute(updateroom)
        con.commit()
        messagebox.showinfo("success", "saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", "Something went wrong!")
        print(e)
    

#payment info screen
def paymentsInfoScr():
    global rId, nog, tot, ap, pm, prBtn
    for widgets in contentFrame.winfo_children():
        widgets.destroy()

    hotel_status.config(bg="white")
    Reserve.config(bg="white")
    Rooms.config(bg="white")
    Payments.config(bg="#e6ffe6")
    hotel_staff.config(bg="white")
    log_out.config(bg="white")
    
    frame1 = tk.Frame(contentFrame, bg="#e6ffe6")
    frame1.place(relx=0, rely=0, relwidth=1, relheight=1)

    frame2 = tk.Frame(frame1, bg="cyan4")
    frame2.place(relx=0, rely=0, relwidth=1, relheight=0.15)


    tk.Label(frame2, text="Enter Reservation ID :", font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0.3, rely=0, relheight=1)
    rId = tk.Entry(frame2, bd=1, relief="solid", font=("dubai", 10))
    rId.place(relx=0.515, rely=0.22, relwidth=0.17, relheight=0.56)
    okBtn = tk.Button(frame2, text="OK", font=("dubai", 13), fg="cyan4", bg=None, bd=3, command=checkResId)
    okBtn.place(relx=0.7, rely=0.22, relwidth=0.04, relheight=0.58)

    tk.Label(frame1, text="Name of the Guest", font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0, rely=0.153, relwidth=0.4, relheight=0.15)
    nog = tk.Entry(frame1, font=("dubai", 15))
    nog.place(relx=0.4, rely=0.153, relwidth=0.6, relheight=0.15)
    tk.Label(frame1, text="Time of transaction", font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0, rely=0.306, relwidth=0.4, relheight=0.15)
    tot = tk.Entry(frame1, font=("dubai", 15))
    tot.place(relx=0.4, rely=0.306, relwidth=0.6, relheight=0.15)
    tk.Label(frame1, text="Amount Paid", font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0, rely=0.459, relwidth=0.4, relheight=0.15)
    ap = tk.Entry(frame1, font=("dubai", 15))
    ap.place(relx=0.4, rely=0.459, relwidth=0.6, relheight=0.15)
    tk.Label(frame1, text="Payment Method", font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0, rely=0.612, relwidth=0.4, relheight=0.15)
    pm = tk.Entry(frame1, font=("dubai", 15))
    pm.place(relx=0.4, rely=0.612, relwidth=0.6, relheight=0.15)

    prBtn = tk.Button(frame1, text="Print Receipt", font=("dubai", 12), bg="#339966",
              fg="white")
    prBtn.place(relx=0.89, rely=0.8, relwidth=0.1, relheight=0.09)


def searchResHist():
    for item in tree.get_children():
        tree.delete(item)
        
    searchBy = sby.get()
    searchValue = sbar.get()

    try:
        dbConnect()
        if searchBy == "Reservation ID":
            searchResHist = "SELECT * FROM reservation_info WHERE reservation_id LIKE '%"+searchValue+"%'"
        if searchBy == "Guest Name":
            searchResHist = "SELECT * FROM reservation_info WHERE guest_name LIKE '%"+searchValue+"%'"
        if searchBy == "Contact Number":
            searchResHist = "SELECT * FROM reservation_info WHERE contact_no LIKE '%"+searchValue+"%'"
        if searchBy == "Email":
            searchResHist = "SELECT * FROM reservation_info WHERE email LIKE '%"+searchValue+"%'"
        if searchBy == "Address":
            searchResHist = "SELECT * FROM reservation_info WHERE address LIKE '%"+searchValue+"%'"
        if searchBy == "Room Number":
            searchResHist = "SELECT * FROM reservation_info WHERE room_no LIKE '%"+searchValue+"%'"
        if searchBy == "Booking Time":
            searchResHist = "SELECT * FROM reservation_info WHERE time_of_transaction LIKE '%"+searchValue+"%'"
        if searchBy == "Search By":
            searchResHist = "SELECT * FROM reservation_info WHERE reservation_id = NULL"
            messagebox.showwarning("Warning", "Please select search by option")
    except Exception as e:
        messagebox.warning("Error", "Something went wrong!")
        print(e)

    try:
        dbConnect()
        cur.execute(searchResHist)
        for i in cur:
            tdata=[i[0],i[1],i[3],i[4],i[5],i[9],i[12]]
            a=tdata[0]
            b=tdata[1]
            c=tdata[2]
            d=tdata[3]
            e=tdata[4]
            f=tdata[5]
            g=tdata[6]
            tree.insert('','end',values=(a,b,c,d,e,f,g))
    except Exception as e:
        messagebox.showerror("Error","Failed to fetch data")
        print(e)

#record book
def resHistoryScr():
    global tree, sby, sbar
    for widgets in contentFrame.winfo_children():
        widgets.destroy()
    frame1 = tk.Frame(contentFrame, bg="#e6ffe6")
    frame1.place(relx=0, rely=0, relwidth=1, relheight=1)

    frame2 = tk.Frame(frame1, bg="cyan4")
    frame2.place(relx=0, rely=0, relwidth=1, relheight=0.25)

    sbar = tk.Entry(frame2, font=("dubai", 12), fg="#666666", relief="solid", bd=1)
    sbar.place(relx=0.05, rely=0.3, relwidth=0.27, relheight=0.4)
    sbar.insert(0, "Search reservation details")

    def on_entry_click_14(event):
        if sbar.get() == 'Search reservation details' :
            sbar.delete(0,tk.END)
            sbar.insert(0,'')
    def on_exit_14(event):
        if sbar.get()=='':
            sbar.insert(0,'Search reservation details')
    sbar.bind('<FocusIn>', on_entry_click_14)
    sbar.bind('<FocusOut>',on_exit_14)


    sby = ttk.Combobox(frame2, font=("dubai", 11), values=["Search By", "Reservation ID", "Guest Name", "Contact Number", "Email", "Address", "Room Number", "Booking Time"], state="readonly")
    sby.place(relx=0.34, rely=0.3, relwidth=0.14, relheight=0.4)
    sby.current(0)


    sbtn = tk.Button(frame2, text="Search", font=("dubai", 15), bg=None, fg="cyan4", bd=3, command=searchResHist)
    sbtn.place(relx=0.5, rely=0.3, relwidth=0.1, relheight=0.41)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=("dubai", 12), rowheight=35) 
    style.configure("mystyle.Treeview.Heading", font=('dubai', 15),background="lightyellow",foreground="cyan4") 

    tree=ttk.Treeview(frame1, column=("c1","c2","c3","c4","c5","c6","c7"),show="headings",style="mystyle.Treeview")
    tree.column("c1", anchor="center")
    tree.heading("c1", text="Reservation ID")
    tree.column("c2", anchor="center")
    tree.heading("c2", text="Guest Name")
    tree.column("c3", anchor="center")
    tree.heading("c3", text="Contact Number")
    tree.column("c4", anchor="center")
    tree.heading("c4", text="Email")
    tree.column("c5", anchor="center")
    tree.heading("c5", text="Address")
    tree.column("c6", anchor="center")
    tree.heading("c6", text="Room Number")
    tree.column("c7", anchor="center")
    tree.heading("c7", text="Booking Time")
    

    tree.place(relx=0,rely=0.25,relwidth=1,relheight=0.75)

    s1 = tk.Scrollbar(tree,orient="horizontal")
    s1.pack(side="bottom",fill="x")
    s1.config(command=tree.xview)
    s2 = tk.Scrollbar(tree,orient="vertical")
    s2.pack(side="right", fill="y")
    s2.config(command=tree.yview)

    try:
        rid_list = []
        dbConnect()
        get_all_rid = "select reservation_id from reservation_info"
        cur.execute(get_all_rid)
        all_rid=cur.fetchall()
        for i in all_rid:
            rid_list.append(i[0])
        ridlen = len(rid_list)
        totalid = "Total reservations till date : "+str(ridlen)
        tk.Label(frame2, text=totalid, font=("dubai", 18), bg="cyan4",
             fg="white").place(relx=0.64, rely=0.28)
        
    except Exception as e:
        print(e)

    try:
        dbConnect()
        get_res_details = "select * from reservation_info"
        cur.execute(get_res_details)
        for i in cur:
            tdata=[i[0],i[1],i[3],i[4],i[5],i[9],i[12]]
            a=tdata[0]
            b=tdata[1]
            c=tdata[2]
            d=tdata[3]
            e=tdata[4]
            f=tdata[5]
            g=tdata[6]
            tree.insert('','end',values=(a,b,c,d,e,f,g))
    except Exception as e:
        messagebox.showerror("Error","Failed to fetch data")
        print(e)


#login screen
def loginScr():
    global root, uname, pwd
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2)-(450/2)
    y = (screen_height/2)-(550/2)
    x = int(x)
    y = int(y)
    x = str(x)
    y = str(y)
    xandy = "+"+x+"+"+y
    gmtry = "450x500" + xandy
    root.geometry(gmtry)

    root.resizable(0,0)
    root.title("Login")
    root.config(bg="#e6ffe6")

    image1 = Image.open("images/hotel.png")
    resize_image = image1.resize((175,175))
    test = ImageTk.PhotoImage(resize_image)
    label1 = tk.Label(root, image=test, bg="#e6ffe6")
    label1.image =test
    label1.place(rely=0.12, relwidth=1)

    l1 = tk.Label(root, text="HOTEL MANAGEMENT SYSTEM", font=("dubai", 15), bg="#00b386", fg="white")
    l1.place(relx=0, rely=0, relwidth=1, relheight=0.1)

    uname = tk.Entry(root, font=("dubai", 13), fg="#595959", relief="solid", bd=1)
    uname.place(relx=0.25, rely=0.5, relwidth=0.5, relheight=0.075)

    pwd = tk.Entry(root, font=("dubai", 13), fg="#595959", relief="solid", bd=1)
    pwd.place(relx=0.25, rely=0.63, relwidth=0.5, relheight=0.075)

    uname.insert(0, "Enter Username")
    pwd.insert(0, "Enter Password")

    def on_entry_click_uname(event):
        if uname.get() == 'Enter Username' :
            uname.delete(0,tk.END)
            uname.insert(0,'')
    def on_exit_uname(event):
        if uname.get()=='':
            uname.insert(0,'Enter Username')
    uname.bind('<FocusIn>', on_entry_click_uname)
    uname.bind('<FocusOut>',on_exit_uname)

    def on_entry_click_pwd(event):
        if pwd.get() == 'Enter Password' :
            pwd.delete(0,tk.END)
            pwd.insert(0,'')
            pwd.config(show="*")
    def on_exit_pwd(event):
        if pwd.get()=='':
            pwd.insert(0,'Enter Password')
            pwd.config(show="")
    pwd.bind('<FocusIn>', on_entry_click_pwd)
    pwd.bind('<FocusOut>',on_exit_pwd)

    lbtn = tk.Button(root, text="LOGIN", font=("dubai", 15), bg="#00cc99", fg="white", relief="solid", bd=1,command=loginF)
    lbtn.place(relx=0.375, rely=0.77, relwidth=0.25, relheight=0.08)

    root.bind('<Return>',handler)

    root.mainloop()

    
loginScr()
