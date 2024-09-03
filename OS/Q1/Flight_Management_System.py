import tkinter as tk
# import pymysql
import random
from tkinter import messagebox

#--------Function-------

def connect_db():
    try:
        con = pymysql.connect(host="localhost", user="root", password="Shyamsql@123", database="Skyway_Flight")
        return con
    except pymysql.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def check_available_flight():
    print("Checking available flights...\n")
    start = input("Enter Start From: ")
    dist = input("Enter Destination: ")
    date = input("Enter date format yyyy-mm-dd : ")
    
    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        query = "SELECT Flight_NO, Fare, Plane_ID, Avail_Seat FROM flight_info WHERE Start=%s AND Destination=%s AND Flight_date=%s"
        cur.execute(query, (start, dist, date))
        
        flights = cur.fetchall()
        if flights:
            print("Available Flights:\n")
            for flight in flights:
                print(f"Flight No: {flight[0]}, Fare: {flight[1]}, Plane ID: {flight[2]}, Available Seats: {flight[3]}")
        else:
            print("No flights available for the given route and date.")
        
        a = "1"
        while a == "1":
            a = input("\nIf you want to know about the plane, enter 1 or any other character to continue: ")
            if a == "1":
                plane_id = input("Enter Plane ID:\n")
                plane_query = "SELECT * FROM plane_info WHERE Plane_ID=%s"
                cur.execute(plane_query, (plane_id,))
                plane_info = cur.fetchone()
                
                if plane_info:
                    print(f"Plane Information: {plane_info}")
                else:
                    print("No information found for the entered Plane ID.")
    
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        if con:
            con.close()

def insert_flight_info():
    print("Inserting flight info...")
    Flight_no = input("Enter the Flight No(integer value):  ")
    start = input("Enter Start From: ")
    dist = input("Enter Destination: ")
    fare = input("Enter the Fare for respective Flight: ")
    Avail = input("Enter the Available Flight(integer value):  ")
    date = input("Enter date format dd/mm/yyyy: ")
    plane_id = input("Enter the Plane ID: ")

    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO flight_info (Flight_NO, Start, Destination, Fare, Avail_Seat, Flight_date, Plane_ID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (Flight_no, start, dist, fare, Avail, date, plane_id))
        con.commit()
        print("Insertion Successful!")
    except pymysql.Error as e:
        print(e)
    finally:
        if con:
            con.close()

def delete_flight_info():
    print("Deleting flight info...")
    Flight_no = input("Enter the Flight No(integer value):  ")
    
    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM flight_info WHERE Flight_NO=%s", (Flight_no,))
        con.commit()
        print("Deletion Successful!")
    except pymysql.Error as e:
        print(e)
    finally:
        if con:
            con.close()

def check_all_flight_info():
    print("Checking all flight info...")
    
    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        query = "SELECT * FROM flight_info"
        cur.execute(query)
        flights = cur.fetchall()
        
        if flights:
            print("All Available Flights:\n")
            for flight in flights:
                print(f"Flight No: {flight[0]}, Start: {flight[1]}, Destination: {flight[2]}, Fare: {flight[3]}, Avail_Seat: {flight[4]}, Date: {flight[5]}, Plane_ID: {flight[6]}")
        else:
            print("No flights available.")
    except pymysql.Error as e:
        print(e)
    finally:
        if con:
            con.close()

def book_flight():
    print("Booking flight...")
    
    Flight_NO = input("Enter the Flight No (integer value): ")
    
    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM flight_info WHERE Flight_NO=%s", (Flight_NO,))
        flight_info = cur.fetchone()
        
        if flight_info:
            print(f"Flight Information: {flight_info}")
            No_of_seat = int(input("Enter the number of seats you want to book: "))
            
            if No_of_seat > flight_info[4]:
                print(f"Sorry, only {flight_info[4]} seats are available.")
                return
            
            Avail_Seat = flight_info[4] - No_of_seat
            cur.execute("UPDATE flight_info SET Avail_Seat=%s WHERE Flight_NO=%s", (Avail_Seat, Flight_NO))
            
            booking_list = []
            a = True
            while a:
                random_number = random.randint(10000, 99999)
                if random_number not in booking_list:
                    booking_list.append(random_number)
                    booking_id = random_number
                    print(f"Your Booking ID: {booking_id}")
                    a = False
                    
                    # Insert the booking information into the booking_info table
                    cur.execute("INSERT INTO booking_info (Booking_Id, Flight_NO, No_of_seat) VALUES (%s, %s, %s)", 
                                (booking_id, Flight_NO, No_of_seat))
                    con.commit()
                    print("Booking Successful!")
        
        else:
            print(f"Flight No {Flight_NO} not found. Please enter a correct flight number.")
    
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        if con:
            con.close()

def cancel_booking():
    print("Cancelling flight...")
    Book = input("Enter the Booking No (5-digit integer value): ")
    
    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        
        # Retrieve the Flight_NO and number of seats from the booking_info table
        cur.execute("SELECT Flight_NO, No_of_seat FROM booking_info WHERE Booking_Id=%s", (Book,))
        booking_info = cur.fetchone()
        
        if booking_info:
            Flight_NO, No_of_seat = booking_info
            
            # Update the Avail_Seat in the flight_info table
            cur.execute("UPDATE flight_info SET Avail_Seat = Avail_Seat + %s WHERE Flight_NO = %s", (No_of_seat, Flight_NO))
            con.commit()
            
            # Delete the booking entry
            cur.execute("DELETE FROM booking_info WHERE Booking_Id=%s", (Book,))
            con.commit()
            
            print("Cancellation Successful!")
        else:
            print("Booking ID not found. Please enter a correct booking number.")
    
    except pymysql.Error as e:
        print(e)
    
    finally:
        if con:
            con.close()


def insert_plane_info():
    print("Inserting plane info...")
    Plane_ID = input("Enter the Plane ID (integer value): ")
    Plane_Model = input("Enter the Plane Model: ")
    Total_Seat = input("Enter the Total Seats: ")
    Year_Manufactured = input("Enter the Year Manufactured (YYYY): ")

    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO PLANE_INFO (Plane_ID, Plane_Model, Total_Seat, Year_Manufactured) VALUES (%s, %s, %s, %s)",
                    (Plane_ID, Plane_Model, Total_Seat, Year_Manufactured))
        con.commit()
        print("Plane info inserted successfully!")
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        if con:
            con.close()

def delete_plane_info():
    print("Deleting plane info...")
    Plane_ID = input("Enter the Plane ID (integer value): ")

    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM PLANE_INFO WHERE Plane_ID=%s", (Plane_ID,))
        con.commit()
        print("Plane info deleted successfully!")
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        if con:
            con.close()

def insert_customer_info():
    print("Inserting customer info...")
    Customer_id = input("Enter the Customer ID (integer value): ")
    Fname = input("Enter First Name: ")
    Lname = input("Enter Last Name: ")
    Booking_ID = input("Enter Booking ID: ")
    Contact = input("Enter Contact Number: ")

    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO Customer_info (Customer_id, Fname, Lname, Booking_ID, Contact) VALUES (%s, %s, %s, %s, %s)",
                    (Customer_id, Fname, Lname, Booking_ID, Contact))
        con.commit()
        print("Customer info inserted successfully!")
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        if con:
            con.close()
def delete_customer_info():
    print("Deleting customer info...")
    Customer_id = input("Enter the Customer ID (integer value): ")

    con = connect_db()
    if not con:
        return
    
    try:
        cur = con.cursor()
        cur.execute("DELETE FROM Customer_info WHERE Customer_id=%s", (Customer_id,))
        con.commit()
        print("Customer info deleted successfully!")
    except pymysql.Error as e:
        print(f"Error: {e}")
    finally:
        if con:
            con.close()

# Main Program Execution 
# Program should continue until user press 0 to exit
 

#  PLANE_INFO (
#     Plane_ID INT PRIMARY KEY,         -- Unique identifier for each plane
#     Plane_Model VARCHAR(100),         -- Model of the plane
#     Total_Seat INT NOT NULL,          -- Total number of seats in the plane
#     Year_Manufactured YEAR            -- Year the plane was manufactured
# );

#  Customer_info (
#     Customer_id INT PRIMARY KEY,     -- Unique identifier for each customer
#     Fname VARCHAR(50),               -- First name of the customer
#     Lname VARCHAR(50),               -- Last name of the customer
#     Booking_ID INT,                  -- Booking ID associated with the customer
#     Contact VARCHAR(15)              -- Contact number of the customer
# );

x = True
while(x):
    print("Enter the choice for performing the following actions:\n")
    a = """ 1. Check Available Flights
    2. Insert Flight Info
    3. Delete Flight Info
    4. Check All Flight Info
    5. Book Flight
    6. Cancel Booking
    7. Insert Plane Info   
    8. Delete Plane Info
    9.Insert Customer Info
    10.Delete Customer Info
    0. Exit"""
    print(a)

    b = int(input())

    if b == 1:
        check_available_flight()
    elif b == 2:
        insert_flight_info()
    elif b == 3:
        delete_flight_info()
    elif b == 4:
        check_all_flight_info()
    elif b == 5:
        book_flight()
    elif b == 6:
        cancel_booking()
    elif b == 7:
        insert_plane_info()
    elif b == 8:
        delete_plane_info()
    elif b == 9:
        insert_customer_info()
    elif b == 10:
        delete_customer_info()
    elif b == 0:
        print("Exiting the program...")
        x = False
    else:
        print("Invalid choice. Please enter a number between 1 and 10.")




-----------------------------------------------

class BasePage(tk.Frame):
    def __init__(self, root, parent, title):
        super().__init__(root)
        self.parent = parent
        self.configure_frame(root)

        # Create the main title label
        self.mainTitle = tk.Label(self, text=title, bd=5, relief="groove", font=("Times New Roman", 40, "bold"), bg="#229799", fg="white")
        self.mainTitle.pack(side="top", fill="x")

    def configure_frame(self, root):
        # Set window size to full screen and place frame
        self.place(x=0, y=0, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Management System")
        self.configure_root(root)

        # Initialize PageOne and PageTwo frames first
        self.page_one = PageOne(self.root, self)
        self.page_two = PageTwo(self.root, self)

        # Home Page (merged from previous code)
        self.home_page = BasePage(self.root, self, "SkyWays AirLine")

        #---------Input Frame----------
        inputFrame = tk.Frame(self.home_page, bd=7, relief="groove", bg="sky blue")
        inputFrame.place(x=20, y=90, width=350, height=300)

        # User ID Label and Entry
        nameLabel = tk.Label(inputFrame, text="User ID:", bg="sky blue", font=("Arial", 12, "bold"))
        nameLabel.grid(row=0, column=0, padx=16, pady=30)
        self.nameIn = tk.Entry(inputFrame, bd=2, font=("Arial", 15), width=12)
        self.nameIn.grid(row=0, column=1, padx=3, pady=30)

        # Password Label and Entry
        idLabel = tk.Label(inputFrame, text="Password:", bg="sky blue", font=("Arial", 12, "bold"))
        idLabel.grid(row=1, column=0, padx=16, pady=30)
        self.idIn = tk.Entry(inputFrame, bd=2, font=("Arial", 15), width=12, show='*')
        self.idIn.grid(row=1, column=1, padx=3, pady=20)

        # Login Button
        LogInbtn = tk.Button(inputFrame, bg="light gray", text="LogIn", width=25, font=("Times New Roman", 15, "bold", "italic"),
                            command=self.go_to_page_one)
        LogInbtn.grid(row=3, columnspan=2, padx=20, pady=25)

        # Show home page initially
        self.home_page.tkraise()

    def configure_root(self, root):
        # Set window size to full screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")

    def go_to_page_one(self):
        # Switch to PageOne
        self.page_one.tkraise()

class PageOne(BasePage):
    def __init__(self, root, parent):
        super().__init__(root, parent, "SkyWays AirLine - Page One")
        next_page_btn = tk.Button(self, text="Go to Page Two", font=("Arial", 15), command=self.go_to_page_two)
        next_page_btn.pack(pady=20)

    def go_to_page_two(self):
        # Switch to PageTwo
        self.parent.page_two.tkraise()

class PageTwo(BasePage):
    def __init__(self, root, parent):
        super().__init__(root, parent, "SkyWays AirLine - Page Two")
        back_page_btn = tk.Button(self, text="Go back to Page One", font=("Arial", 15), command=self.go_back_to_page_one)
        back_page_btn.pack(pady=20)

    def go_back_to_page_one(self):
        # Switch back to PageOne
        self.parent.page_one.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()




