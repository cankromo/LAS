from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox
from visitor import Visitor
from PIL import Image, ImageTk
from datetime import datetime
from register import add_new_user, resend_qr_code
from db import change_user_data_in_db
from data import *
import matplotlib.pyplot as plt
import tkinter as tk
import sys, threading, register, scanning

df = get_time_frame()

#############MAIN WINDOW PART###############
window = tk.Tk()
style = ttk.Style(window)

window.geometry("900x500")
window.title("LAS")
window.resizable(False, False)

##########OPTIONS#############

options_frame=tk.Frame(window, bg="white")
options_frame.pack()

options_frame.pack_propagate(False)

options_frame.place(x=15,y=0)
options_frame.configure(width=270, height=30)

main_frame = tk.Frame(
    master = window, 
    highlightbackground="white",
    highlightthickness="3"
    )

main_frame.pack(side=tk.BOTTOM)
main_frame.pack_propagate(False)

main_frame.configure(height=450, width= 900)

##########FUNCTION FOR INDICATOR FRAMES##########
def indicate(lb, page):
    hide_indicators()
    lb.config(bg="black")
    page()

def hide_indicators():
    register_indicate.config(bg="white")
    general_indicate.config(bg="white")
    live_indicate.config(bg="white")
    exit_indicate.config(bg="white")

#####################BUTTONS IN OPTION FRAME###########################

register_button = tk.Button(options_frame, text="Register", font=("Bold",10),fg="black",bd=0,bg="white",command=lambda: indicate(register_indicate, register_page))
register_button.place(x=10,y=5)
register_indicate = tk.Label(options_frame, text="",bg="white")
register_indicate.place(x=10, y=5, width=55, height= 5)

general_button=tk.Button(options_frame, text="General", font=("Bold", 10),fg="black",bd=0,bg="white",command=lambda: indicate(general_indicate, general_page))
general_button.place(x=80,y=5)
general_indicate = tk.Label(options_frame, text="",bg="white")
general_indicate.place(x=80, y=5, width=53, height= 5)

live_button=tk.Button(options_frame, text="Live", font=("Bold", 10),fg="black",bd=0,bg="white",command=lambda: indicate(live_indicate, live_page))
live_button.place(x=150,y=5)
live_indicate = tk.Label(options_frame, text="",bg="white")
live_indicate.place(x=150, y=5, width=30, height= 5)


def on_scan():
    if register.scanning_in_progress:
        messagebox.showinfo("Info", "Scanning is already in progress")
        return

    register.scanning_in_progress = True

    # start scanning in a new thread
    thread = threading.Thread(target=scanning.scan)
    thread.start()

def on_exit():
    if register.scanning_in_progress:
        messagebox.showinfo("Info", "Scanning is in progress. Please wait.")
        return

    sys.exit()
    
exit_button=tk.Button(options_frame, text="Exit", font=("Bold", 10),fg="black",bd=0,bg="white",command=on_exit)
exit_button.place(x=200,y=5)

exit_indicate = tk.Label(options_frame, text="",bg="white")
exit_indicate.place(x=200, y=5, width=30, height= 5)


#################REGISTER PART#############

def register_page():
    # Delete the widgets from previous page
    for widget in main_frame.winfo_children():
        widget.destroy()
        
    # Create a special frame for register page
    register_frame = tk.Frame(main_frame,bg="grey")
    register_frame.pack(fill="both", expand=True)

    label1 = tk.Label(register_frame, text="Name", bg="grey", font=("Arial", 14), fg="black")
    label1.place(x=275, y=100)
    Name = tk.Entry(register_frame)
    Name.place(x=400, y=100, width=200, height=25)

    label3 = tk.Label(register_frame, text="Surname", bg="grey", font=("Arial", 14), fg="black")
    label3.place(x=275, y=150)
    Surname = tk.Entry(register_frame)
    Surname.place(x=400, y=150, width=200, height=25)

    label2 = tk.Label(register_frame, text="Age:", bg="grey", font=("Arial", 14), fg="black")
    label2.place(x=275, y=200)
    Age = tk.Entry(register_frame)
    Age.place(x=400, y=200, width=200, height=25)

    label4 = tk.Label(register_frame, text="E-mail", bg="grey", font=("Arial", 14), fg="black")
    label4.place(x=275, y=250)
    Email = tk.Entry(register_frame)
    Email.place(x=400, y=250, width=200, height=25)
    
    def get_values() -> str | None:
        """
        Get the values from the entries and return them as a string.
        """

        # check if the inputs are valid
        name_value = Name.get().strip()
        surname_value = Surname.get().strip()
        age_value = Age.get().strip()
        email_value = Email.get().strip()

        # delete the values from the entries
        Name.delete(0, tk.END)
        Surname.delete(0, tk.END)
        Age.delete(0, tk.END)
        Email.delete(0, tk.END)

        if name_value == "" or surname_value == "" or age_value == "" or email_value == "":
            messagebox.showerror("Error", "Please fill all the fields.")
            return None
        
        name_check = name_value.replace(" ", "")
        if not name_check.isalpha() or not surname_value.isalpha():
            messagebox.showerror("Error", "Name and surname can only contain letters.")
            return None
        
        if not age_value.isdigit():
            messagebox.showerror("Error", "Age can only contain digits.")
            return None
        
        return name_value + ";" + surname_value + ";" + age_value + ";" + email_value
        
    ##########################REGISTER BUTTON#####################################
    
    button= tk.Button(register_frame,text= "Register",font=("Arial", 12), bg="white", command=lambda: add_new_user(str(get_values())))
    button.place(x=275, y=325)
    
    # create a button with an image for the main function
    image = Image.open("imgs/scan.png")
    register_page.photo = ImageTk.PhotoImage(image)

    button1 = tk.Button(register_frame, image=register_page.photo, command=on_scan)
    button1.place(x=500, y=325, width=100, height=100)


def live_page():
    # Delete the widgets from previous page
    for widget in main_frame.winfo_children():
        widget.destroy()

    image = Image.open("imgs/aybu.png")
    image = image.resize((142,110), Image.LANCZOS)

    live_page.photo = ImageTk.PhotoImage(image)
    
    live_frame = tk.Frame(main_frame, bg="grey", width=1000, height=450)
    live_frame.pack_propagate(False)
    live_frame.pack()

    label1_live_page = tk.Label(live_frame,image=live_page.photo, width=142, height=110)
    label1_live_page.place(x=35,y=10)


    ################CURRENT OCCUPANCY GRAPH#########################
    fig, ax = plt.subplots()
    
    rate=["occupancy"]
    positions = get_presense_data()[1][1]

    plt.bar(rate, positions)

    ax.set_ylim(bottom=0, top=50)
    fig.subplots_adjust(left=0.26)

    canvas = FigureCanvasTkAgg(fig, master=live_frame)
    canvas.draw()   
    
    canvas.get_tk_widget().place(x=35, y=130, width=150, height=300)
    canvas.get_tk_widget().config(highlightthickness=3, highlightbackground="green")

    plt.close(fig)

    #################CURRENT USERS TABLE#############################

    cols = ["ID", "Name", "Surname", "Age", "E-mail", "Last", "Time"]

    # make treeview widget and define its columns and headings
    treeview = ttk.Treeview(live_frame, show="headings", columns=cols, height=20)
    treeview.place(x=300,y=10)

    rows = get_user_data(True)

    for row in rows:
        vis = Visitor(
            id= row[0],
            name= row[1],
            surname= row[2],
            age= row[3],  
            email= row[4]
        )

        tup = vis.return_tuple()

        # get the last time entered and the time difference
        last_time_entered = row[5].split(";")[-1].split('&')[0].strip()
        specific_time = datetime.strptime(last_time_entered, '%H:%M:%S')

        time_difference = datetime.combine(datetime.today(), datetime.now().time()) - datetime.combine(datetime.today(), specific_time.time())
        time_difference = str(time_difference).split(".")[0]

        # add the last time entered and the time difference to the tuple
        tup = tup + (last_time_entered, time_difference)
        treeview.insert("", "end", text=row[0], values=tup)


    treeview.column("Age", width=30)
    treeview.column("ID", width=20)
    treeview.column("Name", width=80)
    treeview.column("Surname", width=60)
    treeview.column("E-mail", width=180)
    treeview.column("Last", width=80)
    treeview.column("Time", width=100)

    for col in cols:
        treeview.heading(col, text=col)


def general_page():
    
    def change_user_data() -> None:
        """
        Change user data in database.
        """
        # Get the selected item
        selected_item = treeview.selection()[0]
        values = treeview.item(selected_item, "values")

        # Create a new window
        window = tk.Toplevel()
        window.geometry("320x215")
        window.title("Change user data")
        window.resizable(False, False)
        
        # Create the labels and entries
        label1 = tk.Label(window, text="Name:", font=("Arial", 14), fg="black")
        label1.place(x=10, y=10)
        Name = tk.Entry(window)
        Name.place(x=150, y=10, width=150, height=25)
        Name.insert(0, values[1])

        label2 = tk.Label(window, text="Surname:", font=("Arial", 14), fg="black")
        label2.place(x=10, y=50)
        Surname = tk.Entry(window)
        Surname.place(x=150, y=50, width=150, height=25)
        Surname.insert(0, values[2])

        label3 = tk.Label(window, text="Age:", font=("Arial", 14), fg="black")
        label3.place(x=10, y=90)
        Age = tk.Entry(window)
        Age.place(x=150, y=90, width=150, height=25)
        Age.insert(0, values[3])

        label4 = tk.Label(window, text="E-mail:", font=("Arial", 14), fg="black")
        label4.place(x=10, y=130)
        Email = tk.Entry(window)
        Email.place(x=150, y=130, width=150, height=25)
        Email.insert(0, values[4])

        change_button = tk.Button(window, text="Change", font=("Arial", 12), bg="gray", command=lambda: change_user_data_in_db(values[0], Name.get(), Surname.get(), Age.get(), Email.get()))
        change_button.place(x=20, y=170)

        resend_button = tk.Button(window, text="Resend", font=("Arial", 12), bg="gray", command=lambda: resend_qr_code(values[0], Name.get(), Surname.get(), Age.get(), Email.get()))
        resend_button.place(x=220, y=170)


    # Delete the widgets from previous page
    for widget in main_frame.winfo_children():
        widget.destroy()


    general_frame = tk.Frame(main_frame, bg="grey", width=1000, height=450)
    general_frame.pack_propagate(False)
    general_frame.pack()
    
    myframe=tk.Frame(general_frame, relief=tk.GROOVE,width=250,height=100,bd=1)
    myframe.place(x=5,y=5)

    canvas=tk.Canvas(myframe,width=290,height=420)
    inner_frame=tk.Frame(canvas)

    myscrollbar=tk.Scrollbar(myframe,orient="vertical",command=canvas.yview,width=5)
    canvas.configure(yscrollcommand=myscrollbar.set)

    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side="left",fill="y")
    canvas.create_window((0,0),window=inner_frame,anchor='nw')
    inner_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))


    ################PIE MONTHS GRAPH##################
    fig, ax = plt.subplots()
    slices = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    share = get_per_month(df)

    explode = [0] * len(share)
    plt.pie(share, labels=slices, explode=explode)

    canvas_pie = FigureCanvasTkAgg(fig, master=inner_frame)
    canvas_pie.draw()

    plt.subplots_adjust(top=0.8)
    plt.title("User per month", fontdict={'fontsize': 8}, loc='center')

    canvas_pie.get_tk_widget().grid(row=0, column=0, pady=20, padx=10)
    canvas_pie.get_tk_widget().config(highlightthickness=3, highlightbackground="green", width=270, height=150)

    plt.close(fig)


    ################DAYS COLUMN GRAPH#################
    fig, ax = plt.subplots()

    # Get the keys and values of the dictionary using items() method
    days, counts = zip(*get_users_per_day(df).items()) # '*' is used to unzip the list???

    # the days are not in sorted order
    plt.bar(days, counts)
    ax.set_ylim(bottom=0, top=50)
    plt.title("User per days", fontdict={'fontsize': 8}, loc='center')

    canvas1 = FigureCanvasTkAgg(fig, master=inner_frame)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=1, column=0, pady=20, padx=10)
    canvas1.get_tk_widget().config(highlightthickness=3, highlightbackground="green", width=270, height=270)

    plt.close(fig)

    #######################POPULAR HOURS TABLE#######################
    fig, ax = plt.subplots()
    values_of_rate=[i for i in get_by_hour(df).values()]
    hours=[i for i in get_by_hour(df).keys()]

    # Plot the x-axis line
    plt.plot(hours, values_of_rate, color='black', linewidth=1)
    plt.title("Users by hours", fontdict={'fontsize': 8}, loc='center')

    # Remove y-axis line, ticks, and data points
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    ax.yaxis.grid(True, linestyle='dashed', color='gray', alpha=0.5)
    
    plt.xticks([9,12,15,18,21])
    plt.yticks([10,20,30,40,50])

    canvas3 = FigureCanvasTkAgg(fig, master=inner_frame)
    fig.subplots_adjust(left=0.26)

    canvas3.draw()
    
    canvas3.get_tk_widget().grid(row=2,column=0, pady=20,padx=10)
    canvas3.get_tk_widget().config(highlightthickness=3, highlightbackground="green",width=270,height=270)
    
    plt.close(fig)

    #############################################################################
    
    # define treeview columns
    cols = ["ID", "Name", "Surname", "Age", "E-mail"]

    # make treeview widget and define its columns and headings
    treeview = ttk.Treeview(general_frame, show="headings", columns=cols, height=20)
    treeview.place(x=330,y=5)

    rows = get_user_data(False)

    for row in rows:
        vis = Visitor(
            id= row[0],
            name= row[1],
            surname= row[2],
            age= row[3],  
            email= row[4]
        )

        tup = vis.return_tuple()
        treeview.insert("", "end", text=row[0], values=tup)

    treeview.column("Age", width=50)
    treeview.column("ID", width=50)
    treeview.column("Name", width=120)
    treeview.column("Surname", width=100)
    treeview.column("E-mail", width=200)

    for col in cols:
        treeview.heading(col, text=col)

    # bind the double click event to the function change_user_data
    treeview.bind("<Double-1>", lambda event: change_user_data())


register_page()
window.mainloop()
