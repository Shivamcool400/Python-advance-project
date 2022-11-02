import os  # for creating directories Customer if it is not exists.
import tkinter as tk
from tkinter import *


# Backend python functions code starts :
def is_valid(customer_account_number):
    try:
        customer_database = open("./database/Customer/customerDatabase.txt")
    except FileNotFoundError:
        os.makedirs("./database/Customer/customerDatabase.txt", exist_ok=True)
        print("# Customer database doesn't exists!\n# New Customer database created automatically.")
        customer_database = open("./database/Customer/customerDatabase.txt", "a")
    else:  # if customer account  number is already allocated then this will return false. otherwise true.
        if check_credentials(customer_account_number, "DO_NOT_CHECK", 2, True):
            return False
        else:
            return True
    customer_database.close()


def display_account_summary(identity, choice):  # choice 1 for full summary; choice 2 for only account balance.
    flag = 0
    customer_database = open("./database/Customer/customerDatabase.txt")
    output_message = ""
    for line in customer_database:
        if identity == line.replace("\n", ""):
            if choice == 2:
                customer_database.readline()  # skipped pin
                output_message += "Current balance : " + customer_database.readline().replace("\n", "") + "\n"
            flag = 1
            break

        else:
            for index in range(11):
                fetched_line = customer_database.readline()
                if fetched_line is not None:
                    continue
                else:
                    break
    if flag == 0:
        print("\n# No account associated with the entered account number exists! #")
    return output_message


def delete_customer_account(identity, choice):  # choice 1 for admin, choice 2 for customer
    customer_database = open("./database/Customer/customerDatabase.txt")
    data_collector = ""
    flag = 0
    for line in customer_database:
        if identity == line.replace("\n", ""):
            flag = 1
            for index in range(11):
                customer_database.readline()  # skipping the line
        else:
            data_collector += line
            for index in range(11):
                data_collector += customer_database.readline()
    customer_database = open("./database/Customer/customerDatabase.txt", "w")
    customer_database.write(data_collector)
    if flag == 1:
        output_message = "Account with account no." + str(identity) + " closed successfully!"
        if choice == 1:
            adminMenu.printMessage_outside(output_message)
        print(output_message)
    else:
        output_message = "Account not found !"
        if choice == 1:
            adminMenu.printMessage_outside(output_message)
        print(output_message)

def change_PIN(identity, new_PIN):
    customer_database = open("./database/Customer/customerDatabase.txt")
    data_collector = ""
    for line in customer_database:
        if identity == line.replace("\n", ""):
            data_collector += line  # ID
            data_collector += str(new_PIN) + "\n"  # PIN changed
            customer_database.readline()
            for index in range(10):
                data_collector += customer_database.readline()
        else:
            data_collector += line
            for index in range(11):
                data_collector += customer_database.readline()
    customer_database.close()
    customer_database = open("./database/Customer/customerDatabase.txt", "w")
    customer_database.write(data_collector)

    output_message = "PIN changed successfully."
    customerMenu.printMessage_outside(output_message)
    print(output_message)


def transaction(identity, amount, choice):  # choice 1 for deposit; choice 2 for withdraw
    customer_database = open("./database/Customer/customerDatabase.txt")
    data_collector = ""
    balance = 0
    for line in customer_database:
        if identity == line.replace("\n", ""):
            data_collector += line  # ID
            data_collector += customer_database.readline()  # PIN
            balance = float(customer_database.readline().replace("\n", ""))
            if choice == 2 and balance - amount < 10000:  # Minimum balance 10000
                return -1
            else:
                if choice == 1:
                    balance += amount
                else:
                    balance -= amount
            data_collector += str(balance) + "\n"
            for index in range(9):
                data_collector += customer_database.readline()
        else:
            data_collector += line
            for index in range(11):
                data_collector += customer_database.readline()

    customer_database.close()
    customer_database = open("./database/Customer/customerDatabase.txt", "w")
    customer_database.write(data_collector)
    return balance


def check_credentials(identity, password, choice,
                      admin_access):  # checks credentials of admin/customer and returns True or False
    folder_name = "./database/Admin" if (choice == 1) else "./database/Customer"
    file_name = "/adminDatabase.txt" if (choice == 1) else "/customerDatabase.txt"

    try:
        os.makedirs(folder_name, exist_ok=True)
        database = open(folder_name + file_name, "r")
    except FileNotFoundError:
        print("#", folder_name[2:], "database doesn't exists!\n# New", folder_name[2:],
              "database created automatically.")
        database = open(folder_name + file_name, "a")
        if choice == 1:
            database.write("admin\nadmin@123\n*\n")
    else:
        is_credentials_correct = False
        for line in database:
            id_fetched = line.replace("\n", "")
            password_fetched = database.__next__().replace("\n", "")
            if id_fetched == identity:
                if ((password == "DO_NOT_CHECK_ADMIN" and choice == 1 and admin_access == False) or (
                        password == "DO_NOT_CHECK" and choice == 2 and admin_access == True) or password_fetched == password):
                    is_credentials_correct = True
                    database.close()
                    return True
            if choice == 1:  # skips unnecessary lines in admin database.
                database.__next__()  # skipping line
            else:  # skips unnecessary lines in customer database.
                for index in range(10):
                    fetched_line = database.readline()
                    if fetched_line is not None:
                        continue
                    else:
                        break
        if is_credentials_correct:
            print("Success!")
        else:
            print("Failure!")

    database.close()
    return False


# Backend python functions code ends.

# Tkinter GUI code starts :  
class welcomeScreen:
    def __init__(self, window=None):
        self.master = window
        window.geometry("600x450+383+106")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Welcome to INDIAN BANK NETBANKING")
        p1 = PhotoImage(file='./images/bank1.png')
        window.iconphoto(True, p1)
        window.configure(background="#023047")
        window.configure(cursor="arrow")

        self.Canvas1 = tk.Canvas(window, background="#34349C", borderwidth="0", insertbackground="black",
                                 relief="ridge",
                                 selectbackground="blue", selectforeground="white")
        self.Canvas1.place(relx=0.190, rely=0.228, relheight=0.496, relwidth=0.622)

        self.Button2 = tk.Button(self.Canvas1, command=self.selectCustomer, activebackground="#ECC838",
                                 activeforeground="#000000", background="#023047", disabledforeground="#a3a3a3",
                                 foreground="#f9f9f9", borderwidth="0", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0",
                                 text='''LOGIN FOR NETBANKING''')
        self.Button2.configure(font="-family {Segoe UI} -size 10 -weight bold")
        self.Button2.place(relx=0.100, rely=0.583, height=24, width=300)

        self.Label1 = tk.Label(self.Canvas1, background="#ECC838", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 13 -weight bold", foreground="#000000",
                               text='''INDIAN BANKS'S NETBANKING SERVICES''')
        self.Label1.place(relx=-0.010, rely=0.224, height=31, width=400)

    def selectCustomer(self):
        self.master.withdraw()
        CustomerLogin(Toplevel(self.master))


class Error:
    def __init__(self, window=None):
        global master
        master = window
        window.geometry("411x117+485+248")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Error")
        window.configure(background="#f2f3f4")

        global Label2

        self.Button1 = tk.Button(window, background="#d3d8dc", borderwidth="1", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 9", foreground="#000000", highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''OK''', command=self.goback)
        self.Button1.place(relx=0.779, rely=0.598, height=24, width=67)

        global _img0
        _img0 = tk.PhotoImage(file="./images/error_image.png")
        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               image=_img0, text='''Label''')
        self.Label1.place(relx=0.024, rely=0.0, height=81, width=84)

    def setMessage(self, message_shown):
        Label2 = tk.Label(master, background="#f2f3f4", disabledforeground="#a3a3a3",
                          font="-family {Segoe UI} -size 16", foreground="#000000", highlightcolor="#646464646464",
                          text=message_shown)
        Label2.place(relx=0.210, rely=0.171, height=41, width=214)

    def goback(self):
        master.withdraw()


class CustomerLogin:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+338+92")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Customer")
        window.configure(background="#00254a")

        global Canvas1
        Canvas1 = tk.Canvas(window, background="#ffffff", insertbackground="black", relief="ridge",
                            selectbackground="blue", selectforeground="white")
        Canvas1.place(relx=0.108, rely=0.142, relheight=0.715, relwidth=0.798)

        Label1 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3",
                          font="-family {Segoe UI} -size 14 -weight bold", foreground="#00254a",
                          text="Individual Login")
        Label1.place(relx=0.135, rely=0.142, height=41, width=154)

        global Label2
        Label2 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        Label2.place(relx=0.067, rely=0.283, height=181, width=233)
        global _img0
        _img0 = tk.PhotoImage(file="./images/customer.png")
        Label2.configure(image=_img0)

        self.Entry1 = tk.Entry(Canvas1, background="#e2e2e2", borderwidth="2", disabledforeground="#a3a3a3",
                               font="TkFixedFont", foreground="#000000", highlightbackground="#b6b6b6",
                               highlightcolor="#004080", insertbackground="black")
        self.Entry1.place(relx=0.607, rely=0.453, height=20, relwidth=0.26)

        self.Entry1_1 = tk.Entry(Canvas1, show='*', background="#e2e2e2", borderwidth="2",
                                 disabledforeground="#a3a3a3", font="TkFixedFont", foreground="#000000",
                                 highlightbackground="#d9d9d9", highlightcolor="#004080", insertbackground="black",
                                 selectbackground="blue", selectforeground="white")
        self.Entry1_1.place(relx=0.607, rely=0.623, height=20, relwidth=0.26)

        self.Label3 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label3.place(relx=0.556, rely=0.453, height=21, width=34)

        global _img1
        _img1 = tk.PhotoImage(file="./images/user1.png")
        self.Label3.configure(image=_img1)

        self.Label4 = tk.Label(Canvas1)
        self.Label4.place(relx=0.556, rely=0.623, height=21, width=34)
        global _img2
        _img2 = tk.PhotoImage(file="./images/lock1.png")
        self.Label4.configure(image=_img2, background="#ffffff")

        self.Label5 = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        self.Label5.place(relx=0.670, rely=0.142, height=71, width=74)
        global _img3
        _img3 = tk.PhotoImage(file="./images/bank1.png")
        self.Label5.configure(image=_img3)

        self.Button = tk.Button(Canvas1, text="Login", borderwidth="0", width=10, background="#ECC838",
                                foreground="#ffffff",
                                font="-family {Segoe UI} -size 10 -weight bold",
                                command=lambda: self.login(self.Entry1.get(), self.Entry1_1.get()))
        self.Button.place(relx=0.765, rely=0.755)

        self.Button_back = tk.Button(Canvas1, text="Back", borderwidth="0", width=10, background="#ECC838",
                                     foreground="#ffffff",
                                     font="-family {Segoe UI} -size 10 -weight bold",
                                     command=self.back)
        self.Button_back.place(relx=0.545, rely=0.755)

        global customer_img
        customer_img = tk.PhotoImage(file="./images/customer.png")

    def back(self):
        self.master.withdraw()
        welcomeScreen(Toplevel(self.master))

    @staticmethod
    def setImg():
        settingIMG = tk.Label(Canvas1, background="#ffffff", disabledforeground="#a3a3a3", foreground="#000000")
        settingIMG.place(relx=0.067, rely=0.283, height=181, width=233)
        settingIMG.configure(image=customer_img)

    def login(self, customer_account_number, customer_PIN):
        if check_credentials(customer_account_number, customer_PIN, 2, False):
            global customer_accNO
            customer_accNO = str(customer_account_number)
            self.master.withdraw()
            customerMenu(Toplevel(self.master))
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid Credentials!")
            self.setImg()

class customerMenu:
    def __init__(self, window=None):
        self.master = window
        window.geometry("743x494+329+153")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Customer Section")
        window.configure(background="#00254a")

        self.Labelframe1 = tk.LabelFrame(window, relief='groove', font="-family {Segoe UI} -size 13 -weight bold",
                                         foreground="#000000", text='''Select your option''', background="#fffffe")
        self.Labelframe1.place(relx=0.081, rely=0.081, relheight=0.415, relwidth=0.848)

        self.Button1 = tk.Button(self.Labelframe1, command=self.selectWithdraw, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Send Money''')
        self.Button1.place(relx=0.667, rely=0.195, height=34, width=181, bordermode='ignore')

        self.Button2 = tk.Button(self.Labelframe1, command=self.selectDeposit, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Deposit/Add Money''')
        self.Button2.place(relx=0.04, rely=0.195, height=34, width=181, bordermode='ignore')

        self.Button3 = tk.Button(self.Labelframe1, command=self.exit, activebackground="#ececec",
                                 activeforeground="#000000",
                                 background="#071051",
                                 borderwidth="0", disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11",
                                 foreground="#fffffe", highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''LOG OUT''')
        self.Button3.place(relx=0.667, rely=0.683, height=34, width=181, bordermode='ignore')

        self.Button4 = tk.Button(self.Labelframe1, command=self.selectChangePIN, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Change PIN''')
        self.Button4.place(relx=0.04, rely=0.439, height=34, width=181, bordermode='ignore')

        self.Button5 = tk.Button(self.Labelframe1, command=self.selectCloseAccount, activebackground="#ececec",
                                 activeforeground="#000000", background="#39a9fc", borderwidth="0",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Close account''')
        self.Button5.place(relx=0.667, rely=0.439, height=34, width=181, bordermode='ignore')

        self.Button6 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000",
                                 background="#39a9fc", borderwidth="0", disabledforeground="#a3a3a3",
                                 font="-family {Segoe UI} -size 11", foreground="#fffffe",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0",
                                 text='''Check your balance''', command=self.checkBalance)
        self.Button6.place(relx=0.04, rely=0.683, height=34, width=181, bordermode='ignore')

        global Frame1_1_2
        Frame1_1_2 = tk.Frame(window, relief='groove', borderwidth="2", background="#fffffe")
        Frame1_1_2.place(relx=0.081, rely=0.547, relheight=0.415, relwidth=0.848)

    def selectDeposit(self):
        depositMoney(Toplevel(self.master))

    def selectWithdraw(self):
        withdrawMoney(Toplevel(self.master))

    def selectChangePIN(self):
        changePIN(Toplevel(self.master))

    def selectCloseAccount(self):
        self.master.withdraw()
        closeAccount(Toplevel(self.master))

    def exit(self):
        self.master.withdraw()
        CustomerLogin(Toplevel(self.master))

    def checkBalance(self):
        output = display_account_summary(customer_accNO, 2)
        self.printMessage(output)
        print("check balance function called.")

    def printMessage(self, output):
        # clearing the frame
        for widget in Frame1_1_2.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1_1_2, text=output, background="#fffffe")
        output_message.pack(pady=20)

    def printMessage_outside(output):
        # clearing the frame
        for widget in Frame1_1_2.winfo_children():
            widget.destroy()
        # getting output_message and displaying it in the frame
        output_message = Label(Frame1_1_2, text=output, background="#fffffe")
        output_message.pack(pady=20)


class depositMoney:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+519+278")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Deposit money")
        p1 = PhotoImage(file='./images/deposit_icon.png')
        window.iconphoto(True, p1)
        window.configure(borderwidth="2")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 9", foreground="#000000", borderwidth="0",
                               text='''Enter amount to deposit :''')
        self.Label1.place(relx=0.146, rely=0.171, height=21, width=164)

        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black", selectforeground="#ffffffffffff")
        self.Entry1.place(relx=0.535, rely=0.171, height=20, relwidth=0.253)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", borderwidth="0", foreground="#ffffff",
                                 highlightbackground="#000000",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.56, rely=0.598, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", font="-family {Segoe UI} -size 9", foreground="#ffffff",
                                 highlightbackground="#d9d9d9", borderwidth="0", highlightcolor="black", pady="0",
                                 text='''Back''',
                                 command=self.back)
        self.Button2.place(relx=0.268, rely=0.598, height=24, width=67)

    def submit(self, amount):
        if amount.isnumeric():
            if 25000 >= float(amount) > 0:
                output = transaction(customer_accNO, float(amount), 1)
            else:
                Error(Toplevel(self.master))
                if float(amount) > 25000:
                    Error.setMessage(self, message_shown="Limit exceeded!")
                else:
                    Error.setMessage(self, message_shown="Positive value expected!")
                return
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid amount!")
            return
        if output == -1:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Transaction failed!")
            return
        else:
            output = "Amount of rupees " + str(amount) + " deposited successfully.\nUpdated balance : " + str(output)
            customerMenu.printMessage_outside(output)
            self.master.withdraw()

    def back(self):
        self.master.withdraw()


class withdrawMoney:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+519+278")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Withdraw money")
        p1 = PhotoImage(file='./images/withdraw_icon.png')
        window.iconphoto(True, p1)
        window.configure(borderwidth="2")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3",
                               font="-family {Segoe UI} -size 9", foreground="#000000",
                               text='''Enter amount to withdraw :''')
        self.Label1.place(relx=0.146, rely=0.171, height=21, width=164)

        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black", selectforeground="#ffffffffffff")
        self.Entry1.place(relx=0.535, rely=0.171, height=20, relwidth=0.253)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", borderwidth="0", foreground="#ffffff",
                                 highlightbackground="#000000",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.56, rely=0.598, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", borderwidth="0", font="-family {Segoe UI} -size 9",
                                 foreground="#ffffff",
                                 highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Back''',
                                 command=self.back)
        self.Button2.place(relx=0.268, rely=0.598, height=24, width=67)

    def submit(self, amount):
        if amount.isnumeric():
            if 25000 >= float(amount) > 0:
                output = transaction(customer_accNO, float(amount), 2)
            else:
                Error(Toplevel(self.master))
                if float(amount) > 25000:
                    Error.setMessage(self, message_shown="Limit exceeded!")
                else:
                    Error.setMessage(self, message_shown="Positive value expected!")
                return
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid amount!")
            return
        if output == -1:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Transaction failed!")
            return
        else:
            output = "Amount of rupees " + str(amount) + " withdrawn successfully.\nUpdated balance : " + str(output)
            customerMenu.printMessage_outside(output)
            self.master.withdraw()

    def back(self):
        self.master.withdraw()


class changePIN:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x111+505+223")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Change PIN")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter new PIN:''')
        self.Label1.place(relx=0.243, rely=0.144, height=21, width=93)

        self.Label2 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Confirm PIN:''')
        self.Label2.place(relx=0.268, rely=0.414, height=21, width=82)

        self.Entry1 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.528, rely=0.144, height=20, relwidth=0.229)

        self.Entry2 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry2.place(relx=0.528, rely=0.414, height=20, relwidth=0.229)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get(), self.Entry2.get()))
        self.Button1.place(relx=0.614, rely=0.721, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text="Back", command=self.back)
        self.Button2.place(relx=0.214, rely=0.721, height=24, width=67)

    def submit(self, new_PIN, confirm_new_PIN):
        if new_PIN == confirm_new_PIN and str(new_PIN).__len__() == 4 and new_PIN.isnumeric():
            change_PIN(customer_accNO, new_PIN)
            self.master.withdraw()
        else:
            Error(Toplevel(self.master))
            if new_PIN != confirm_new_PIN:
                Error.setMessage(self, message_shown="PIN mismatch!")
            elif str(new_PIN).__len__() != 4:
                Error.setMessage(self, message_shown="PIN length must be 4!")
            else:
                Error.setMessage(self, message_shown="Invalid PIN!")
            return

    def back(self):
        self.master.withdraw()


class closeAccount:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+498+261")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Close Account")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter your PIN:''')
        self.Label1.place(relx=0.268, rely=0.256, height=21, width=94)

        self.Entry1 = tk.Entry(window, show="*", background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.511, rely=0.256, height=20, relwidth=0.229)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.614, rely=0.712, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text="Back", command=self.back)
        self.Button2.place(relx=0.214, rely=0.712, height=24, width=67)

    def submit(self, PIN):
        print("Submit pressed.")
        print(customer_accNO, PIN)
        if check_credentials(customer_accNO, PIN, 2, False):
            print("Correct accepted.")
            delete_customer_account(customer_accNO, 2)
            self.master.withdraw()
            CustomerLogin(Toplevel(self.master))
        else:
            print("Incorrect accepted.")
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Invalid PIN!")

    def back(self):
        self.master.withdraw()
        customerMenu(Toplevel(self.master))


class checkAccountSummary:
    def __init__(self, window=None):
        self.master = window
        window.geometry("411x117+498+261")
        window.minsize(120, 1)
        window.maxsize(1370, 749)
        window.resizable(0, 0)
        window.title("Check Account Summary")
        window.configure(background="#f2f3f4")

        self.Label1 = tk.Label(window, background="#f2f3f4", disabledforeground="#a3a3a3", foreground="#000000",
                               text='''Enter ID :''')
        self.Label1.place(relx=0.268, rely=0.256, height=21, width=94)

        self.Entry1 = tk.Entry(window, background="#cae4ff", disabledforeground="#a3a3a3", font="TkFixedFont",
                               foreground="#000000", insertbackground="black")
        self.Entry1.place(relx=0.511, rely=0.256, height=20, relwidth=0.229)

        self.Button1 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text='''Proceed''',
                                 command=lambda: self.submit(self.Entry1.get()))
        self.Button1.place(relx=0.614, rely=0.712, height=24, width=67)

        self.Button2 = tk.Button(window, activebackground="#ececec", activeforeground="#000000", background="#004080",
                                 disabledforeground="#a3a3a3", foreground="#ffffff", borderwidth="0",
                                 highlightbackground="#d9d9d9",
                                 highlightcolor="black", pady="0", text="Back", command=self.back)
        self.Button2.place(relx=0.214, rely=0.712, height=24, width=67)

    def back(self):
        self.master.withdraw()

    def submit(self, identity):
        if not is_valid(identity):
            adminMenu.printAccountSummary(identity)
        else:
            Error(Toplevel(self.master))
            Error.setMessage(self, message_shown="Id doesn't exist!")
            return
        self.master.withdraw()


root = tk.Tk()
top = welcomeScreen(root)
root.mainloop()

# Tkinter GUI code ends.
