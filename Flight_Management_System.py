import tkinter as tk
import pymysql
import random
from PIL import Image, ImageTk
import cv2
from tkinter import messagebox
from tkinter import ttk

#---------Funnction-------widget--------
#function to delete the all widget 
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# funtion to create the widget for input frame adding plane info
def create_plane_info_widgets(frame):
    Label(frame, text="Plane ID:").grid(row=0, column=0)
    plane_id_entry = Entry(frame)
    plane_id_entry.grid(row=0, column=1)

    Label(frame, text="Plane Model:").grid(row=1, column=0)
    plane_model_entry = Entry(frame)
    plane_model_entry.grid(row=1, column=1)

    Label(frame, text="Total Seats:").grid(row=2, column=0)
    total_seats_entry = Entry(frame)
    total_seats_entry.grid(row=2, column=1)

    Label(frame, text="Year Manufactured:").grid(row=3, column=0)
    year_manufactured_entry = Entry(frame)
    year_manufactured_entry.grid(row=3, column=1)

    return plane_id_entry, plane_model_entry, total_seats_entry, year_manufactured_entry

# funtion to create the widget for input frame adding flight info
def create_flight_info_widgets(frame):
    Label(frame, text="Flight No:").grid(row=0, column=0)
    flight_no_entry = Entry(frame)
    flight_no_entry.grid(row=0, column=1)

    Label(frame, text="Start From:").grid(row=1, column=0)
    start_entry = Entry(frame)
    start_entry.grid(row=1, column=1)

    Label(frame, text="Destination:").grid(row=2, column=0)
    destination_entry = Entry(frame)
    destination_entry.grid(row=2, column=1)

    Label(frame, text="Fare:").grid(row=3, column=0)
    fare_entry = Entry(frame)
    fare_entry.grid(row=3, column=1)

    Label(frame, text="Available Seats:").grid(row=4, column=0)
    avail_seat_entry = Entry(frame)
    avail_seat_entry.grid(row=4, column=1)

    Label(frame, text="Date (yyyy-mm-dd):").grid(row=5, column=0)
    date_entry = Entry(frame)
    date_entry.grid(row=5, column=1)

    Label(frame, text="Plane ID:").grid(row=6, column=0)
    plane_id_entry = Entry(frame)
    plane_id_entry.grid(row=6, column=1)

    return flight_no_entry, start_entry, destination_entry, fare_entry, avail_seat_entry, date_entry, plane_id_entry

# funtion to create the widget for input frame deleting plane info
def create_delete_plane_info_widgets(frame):
    Label(frame, text="Plane ID:").grid(row=0, column=0)
    plane_id_entry = Entry(frame)
    plane_id_entry.grid(row=0, column=1)

    return plane_id_entry

# funtion to create the widget for input frame deletin flight info
def create_delete_flight_info_widgets(frame):
    Label(frame, text="Flight No:").grid(row=0, column=0)
    flight_no_entry = Entry(frame)
    flight_no_entry.grid(row=0, column=1)

    return flight_no_entry

# function to create the widget for in input frame check flight info
def create_check_flight_info_widgets(frame):
    Label(frame, text="Start From:").grid(row=0, column=0)
    start_entry = Entry(frame)
    start_entry.grid(row=0, column=1)

    Label(frame, text="Destination:").grid(row=1, column=0)
    destination_entry = Entry(frame)
    destination_entry.grid(row=1, column=1)

    Label(frame, text="Date (yyyy-mm-dd):").grid(row=2, column=0)
    date_entry = Entry(frame)
    date_entry.grid(row=2, column=1)

    return start_entry, destination_entry, date_entry

# function to create the widget for in input frame check plane info
def create_check_plane_info_widgets(frame):
    Label(frame, text="Plane ID:").grid(row=0, column=0)
    plane_id_entry = Entry(frame)
    plane_id_entry.grid(row=0, column=1)

    return plane_id_entry

# Function to Create Input Widgets for Booking a Flight
def create_book_flight_widgets(frame):
    Label(frame, text="Flight No:").grid(row=0, column=0)
    flight_no_entry = Entry(frame)
    flight_no_entry.grid(row=0, column=1)

    Label(frame, text="Number of Seats:").grid(row=1, column=0)
    num_seats_entry = Entry(frame)
    num_seats_entry.grid(row=1, column=1)

    return flight_no_entry, num_seats_entry

# Function to Create Input Widgets for Adding Customer Info
def create_add_customer_info_widgets(frame):
    Label(frame, text="Customer ID:").grid(row=0, column=0)
    customer_id_entry = Entry(frame)
    customer_id_entry.grid(row=0, column=1)

    Label(frame, text="First Name:").grid(row=1, column=0)
    first_name_entry = Entry(frame)
    first_name_entry.grid(row=1, column=1)

    Label(frame, text="Last Name:").grid(row=2, column=0)
    last_name_entry = Entry(frame)
    last_name_entry.grid(row=2, column=1)

    Label(frame, text="Booking ID:").grid(row=3, column=0)
    booking_id_entry = Entry(frame)
    booking_id_entry.grid(row=3, column=1)

    Label(frame, text="Contact Number:").grid(row=4, column=0)
    contact_number_entry = Entry(frame)
    contact_number_entry.grid(row=4, column=1)

    return customer_id_entry, first_name_entry, last_name_entry, booking_id_entry, contact_number_entry

# Function to Create Input Widgets for Canceling a Flight
def create_cancel_flight_widgets(frame):
    Label(frame, text="Booking No (5-digit integer):").grid(row=0, column=0)
    booking_no_entry = Entry(frame)
    booking_no_entry.grid(row=0, column=1)

    return booking_no_entry

#Function to Create Input Widgets for Deleting Customer Info
def create_delete_customer_info_widgets(frame):
    Label(frame, text="Customer ID:").grid(row=0, column=0)
    customer_id_entry = Entry(frame)
    customer_id_entry.grid(row=0, column=1)

    return customer_id_entry

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





#-----------------------------------------------




class BasePage(tk.Frame):
    def __init__(self, root, parent, title):
        super().__init__(root)
        self.parent = parent
        self.configure_frame(root)

        # Create the main title label
        self.mainTitle = tk.Label(self, text=title, bd=5, relief="groove", font=("Times New Roman", 40, "bold"), bg="#229799", fg="white")
        self.mainTitle.pack(side="top", fill="x")

        # Add background image
        self.add_background_image()

    def configure_frame(self, root):
        # Set window size to full screen and place frame
        self.place(x=0, y=0, width=root.winfo_screenwidth(), height=root.winfo_screenheight())

    def add_background_image(self):
        # Load the background image
        background_image = Image.open(r"C:\Users\Shyam\OneDrive\Desktop\Cognizance_2nd_Year_PT\OS\Q1\airplane.jpg")  # Replace with your image path
        background_image = background_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(background_image)

        # Create a label for the background image
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(x=0, y=72, relwidth=1, relheight=1)


class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Management System")
        self.configure_root(root)

        # Initialize AdminPage, UserPage, AdminPage2, and UserPage2 frames
        self.admin_page = AdminPage(self.root, self)
        self.user_page = UserPage(self.root, self)
        self.admin_page2 = AdminPage2(self.root, self)
        self.user_page2 = UserPage2(self.root, self)

        # Home Page
        self.home_page = BasePage(self.root, self, "SkyWays AirLine")

        # Input Frame
        inputFrame = tk.Frame(self.home_page, bd=7, relief="groove", bg="sky blue")
        inputFrame.place(x=150, y=250, width=350, height=300)

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
                             command=self.go_to_admin_page)
        LogInbtn.grid(row=3, columnspan=2, padx=20, pady=25)

        # Create movable text and video frame
        self.create_movable_text()
        self.create_video_frame()

        # Show home page initially
        self.home_page.tkraise()

    def create_video_frame(self):
        # Create the video frame on the home page
        self.video_frame = tk.Frame(self.home_page, bd=7, relief="groove")
        self.video_frame.place(x=750, y=250, width=450, height=300)

        # Load and play the video
        self.video_source = cv2.VideoCapture(r"C:\Users\Shyam\OneDrive\Desktop\Cognizance_2nd_Year_PT\OS\Q1\Skyway Airlines!.mp4")  # Replace with your video file path
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(expand=True, fill="both")
        self.update_video()

    def update_video(self):
        # Read the next frame
        ret, frame = self.video_source.read()
        if ret:
            # Get the dimensions of the video_frame
            frame_width = self.video_frame.winfo_width()
            frame_height = self.video_frame.winfo_height()

            # Resize the frame to fit the video_frame
            frame = cv2.resize(frame, (frame_width, frame_height))

            # Convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert to Image
            frame_image = Image.fromarray(frame)
            frame_photo = ImageTk.PhotoImage(image=frame_image)

            # Update the label with the new image and adjust size
            self.video_label.config(image=frame_photo)
            self.video_label.image = frame_photo
            self.video_label.config(width=frame_width, height=frame_height)

            # Call this function again after 10 milliseconds
            self.root.after(10, self.update_video)
        else:
            # Restart video
            self.video_source.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.update_video()

    def configure_root(self, root):
        # Set window size to full screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")

    def go_to_admin_page(self):
        # Switch to AdminPage
        self.admin_page.tkraise()

    def create_movable_text(self):
        # Create a label with the text
        self.movable_text = tk.Label(self.home_page, text="Welcome to SkyWays Airline!", font=("Times New Roman", 30, "bold"), fg="black", bg="light yellow")
        self.movable_text.place(x=0, y=150)  # Initial position of the text

        # Start the movement
        self.move_text()

    def move_text(self):
        # Get the current x-coordinate of the text
        x = self.movable_text.winfo_x()

        # If the text has moved out of the window, reset it to start from the left again
        if x > self.root.winfo_screenwidth():
            x = -self.movable_text.winfo_width()

        # Move the text 2 pixels to the right
        self.movable_text.place(x=x + 2, y=150)

        # Call this function again after 50 milliseconds
        self.root.after(50, self.move_text)


class AdminPage(BasePage):
    def __init__(self, root, parent):
        super().__init__(root, parent, "SkyWays AirLine - Admin Page")

        # Button to go to UserPage
        next_page_btn = tk.Button(self, text="Go to User Page", font=("Arial", 15), command=self.go_to_user_page)
        next_page_btn.place(x=1100, y=73)

        # Button to go to AdminPage2
        admin_page2_btn = tk.Button(self, text="Go to AdminPage2", font=("Arial", 15), command=self.go_to_admin_page2)
        admin_page2_btn.place(x=920, y=73)

        # Button to go back to Home Page
        home_page_btn = tk.Button(self, text="Go to Home Page", font=("Arial", 15), command=self.go_to_home_page)
        home_page_btn.place(x=0, y=73)
        
        # Input Frame
        inputFrame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        inputFrame.place(x=20, y=220, width=300, height=270)
        headline = tk.Label(inputFrame, text="Admin Services", font=("Times New Roman", 20,"italic"))
        headline.pack(padx=10, pady=10)

        # Button for adding Plane Info
        add_plane_btn = tk.Button(inputFrame,width=20, text="Add Plane Info", font=("Arial", 15), command=self.go_to_user_page)
        add_plane_btn.pack(padx=10, pady=2)

        # Button to deleting plane Info
        delete_plane_btn = tk.Button(inputFrame,width=20, text="Delete Plane Info", font=("Arial", 15), command=self.go_to_user_page)
        delete_plane_btn.pack(padx=10, pady=2)
        # Button to add Flight Info
        add_flight_btn = tk.Button(inputFrame,width=20, text="Add Flight Info", font=("Arial", 15), command=self.go_to_user_page)
        add_flight_btn.pack(padx=10, pady=2)

        # Button to Delete Flight Info
        delete_flight_btn = tk.Button(inputFrame,width=20, text="Delete Flight Info", font=("Arial", 15), command=self.go_to_user_page)
        delete_flight_btn.pack(padx=10, pady=2)
        
        # Output Frames
        outputFrame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        outputFrame.place(x=400, y=120, width=850, height=240)
        output2Frame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        output2Frame.place(x=400, y=380, width=850, height=240)

    def go_to_user_page(self):
        # Switch to UserPage
        self.parent.user_page.tkraise()

    def go_to_home_page(self):
        # Switch back to Home Page
        self.parent.home_page.tkraise()

    def go_to_admin_page2(self):
        # Switch to AdminPage2
        self.parent.admin_page2.tkraise()


class UserPage(BasePage):
    def __init__(self, root, parent):
        super().__init__(root, parent, "SkyWays AirLine - User Page")

        # Button to go back to Admin Page
        back_page_btn = tk.Button(self, text="Go back to Admin Page", font=("Arial", 12, "bold"), command=self.go_back_to_admin_page)
        back_page_btn.place(x=1080, y=73)

        # Button to go to UserPage2
        user_page2_btn = tk.Button(self, text="Go to UserPage2", font=("Arial", 15), command=self.go_to_user_page2)
        user_page2_btn.place(x=920, y=73)

        # Button to go back to Home Page
        home_page_btn = tk.Button(self, text="Go to Home Page", font=("Arial", 15), command=self.go_to_home_page)
        home_page_btn.place(x=0, y=73)
        
        # Input Frame
        inputFrame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        inputFrame.place(x=20, y=220, width=300, height=350)
        headline = tk.Label(inputFrame, text="User Services", font=("Times New Roman", 20,"italic"))
        headline.pack(padx=10, pady=10)

        # Button for Check Plane Info
        add_plane_btn = tk.Button(inputFrame,width=20, text="Check Plane Info", font=("Arial", 15))
        add_plane_btn.pack(padx=10, pady=2)
        # Button to Check Flight Info
        add_flight_btn = tk.Button(inputFrame,width=20, text="Check Flight Info", font=("Arial", 15))
        add_flight_btn.pack(padx=10, pady=2)

        # Button to  Book Flight
        book_flight_btn = tk.Button(inputFrame,width=20, text="Book Flight", font=("Arial", 15))
        book_flight_btn.pack(padx=10, pady=2)


        # Button to Cancel Flight
        cancel_flight_btn = tk.Button(inputFrame,width=20, text="Cancel Flight", font=("Arial", 15))
        cancel_flight_btn.pack(padx=10, pady=2)

        # Button to  Add Customer Info
        add_cutomer_btn = tk.Button(inputFrame,width=20, text="Add Cutomer Info", font=("Arial", 15))
        add_cutomer_btn.pack(padx=10, pady=2)


        # Button to delete Customer Info
        delete_customer_btn = tk.Button(inputFrame,width=20, text="Delete Customer Info", font=("Arial", 15))
        delete_customer_btn.pack(padx=10, pady=2)


        # Output Frames
        outputFrame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        outputFrame.place(x=400, y=120, width=850, height=240)
        output2Frame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        output2Frame.place(x=400, y=380, width=850, height=240)


    #     # Drop-down boxes
    #     self.initialize_dropdowns(inputFrame)

    # def initialize_dropdowns(self, frame):
    #     # Example options for the dropdowns
    #     options1 = ["Option 1A", "Option 1B", "Option 1C"]
    #     options2 = ["Option 2A", "Option 2B", "Option 2C"]
    #     options3 = ["Option 3A", "Option 3B", "Option 3C"]
    #     options4 = ["Option 4A", "Option 4B", "Option 4C"]

    #     # Drop-down 1
    #     self.selected_option1 = tk.StringVar()
    #     self.selected_option1.set("Select an option")
    #     dropdown1 = ttk.OptionMenu(frame, self.selected_option1, *options1, command=self.dummy_function1)
    #     dropdown1.pack(pady=10)

    #     # Drop-down 2
    #     self.selected_option2 = tk.StringVar()
    #     self.selected_option2.set("Select an option")
    #     dropdown2 = ttk.OptionMenu(frame, self.selected_option2, *options2, command=self.dummy_function2)
    #     dropdown2.pack(pady=10)

    #     # Drop-down 3
    #     self.selected_option3 = tk.StringVar()
    #     self.selected_option3.set("Select an option")
    #     dropdown3 = ttk.OptionMenu(frame, self.selected_option3, *options3, command=self.dummy_function3)
    #     dropdown3.pack(pady=10)

    #     # Drop-down 4
    #     self.selected_option4 = tk.StringVar()
    #     self.selected_option4.set("Select an option")
    #     dropdown4 = ttk.OptionMenu(frame, self.selected_option4, *options4, command=self.dummy_function4)
    #     dropdown4.pack(pady=10)

    # # Dummy functions for the dropdown actions
    # def dummy_function1(self, value):
    #     print(f"Dropdown 1 selected: {value}")

    # def dummy_function2(self, value):
    #     print(f"Dropdown 2 selected: {value}")

    # def dummy_function3(self, value):
    #     print(f"Dropdown 3 selected: {value}")

    # def dummy_function4(self, value):
    #     print(f"Dropdown 4 selected: {value}")

    def go_back_to_admin_page(self):
        # Switch back to AdminPage
        self.parent.admin_page.tkraise()

    def go_to_home_page(self):
        # Switch back to Home Page
        self.parent.home_page.tkraise()

    def go_to_user_page2(self):
        # Switch to UserPage2
        self.parent.user_page2.tkraise()

class AdminPage2(BasePage):
    def __init__(self, root, parent):
        super().__init__(root, parent, "SkyWays AirLine - User Page")

        # Button to go back to Admin Page
        back_page_btn = tk.Button(self, text="Go back to Admin Page", font=("Arial", 12, "bold"), command=self.go_back_to_admin_page)
        back_page_btn.place(x=1080, y=73)

        # Button to go back to Home Page
        home_page_btn = tk.Button(self, text="Go to Home Page", font=("Arial", 15), command=self.go_to_home_page)
        home_page_btn.place(x=0, y=73)
        # ----Input Frame--------
        inputFrame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        inputFrame.place(x=20, y=120, width=300, height=500)        
        #------OutputFrame---------
        outputFrame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        outputFrame.place(x=400, y=120, width=850, height=240)

        #------OutputFrame-----------
        output2Frame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        output2Frame.place(x=400, y=380, width=850, height=240)

    def go_back_to_admin_page(self):
        # Switch back to AdminPage
        self.parent.admin_page.tkraise()

    def go_to_home_page(self):
        # Switch back to Home Page
        self.parent.home_page.tkraise()



class UserPage2(BasePage):
    def __init__(self, root, parent):
        super().__init__(root, parent, "SkyWays AirLine - Admin Page")

        # Button to go to UserPage
        next_page_btn = tk.Button(self, text="Go to User Page", font=("Arial", 15), command=self.go_to_user_page)
        next_page_btn.place(x=1100, y=73)

        # Button to go back to Home Page
        home_page_btn = tk.Button(self, text="Go to Home Page", font=("Arial", 15), command=self.go_to_home_page)
        home_page_btn.place(x=0, y=73)
        # ----Input Frame--------
        inputFrame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        inputFrame.place(x=20, y=120, width=300, height=500)        
        #------OutputFrame---------
        outputFrame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        outputFrame.place(x=400, y=120, width=850, height=240)

        #------OutputFrame-----------
        output2Frame = tk.Frame(self, bd=7, relief="groove", bg="sky blue")
        output2Frame.place(x=400, y=380, width=850, height=240)
    def go_to_user_page(self):
        # Switch to UserPage
        self.parent.user_page.tkraise()

    def go_to_home_page(self):
        # Switch back to Home Page
        self.parent.home_page.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()
