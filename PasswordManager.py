# Ideia copied from Kalle Hallden youtube channel
# Changes: User interface; 
#          More choices on the program

# To do: encrypt passwords on database (comming soon)

import sqlite3
from hashlib import sha256
import tkinter as tk

import sys

ADMIN_PASSWORD = "" #Add a password of you choice to autheticate your db


def second_window():

    app = tk.Tk()

    app.geometry("700x500+350+150")

    canvas = tk.Canvas(app, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tk.Frame(app, bg="grey")
    frame.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

    entry = tk.Entry(frame, font=40, bg="white")
    entry.place(relx=0.25, rely=0.65, relwidth=0.5, relheight=0.1)

    button1 = tk.Button(frame, text="Store Pass", bg='white', command=lambda: add_password(entry.get(), ADMIN_PASSWORD, instruction, entry))
    button1.place(relx=0.1, rely=0.35, relwidth=0.2, relheight=0.15)

    button2 = tk.Button(frame, text="Get Pass", bg='white', command=lambda: get_password(ADMIN_PASSWORD, entry.get(), instruction, entry))
    button2.place(relx=0.4, rely=0.35, relwidth=0.2, relheight=0.15)

    button3 = tk.Button(frame, text="Delete Pass", bg='white', command=lambda: delete_password(entry.get(), ADMIN_PASSWORD, instruction, entry))
    button3.place(relx=0.7, rely=0.35, relwidth=0.2, relheight=0.15)

    button4 = tk.Button(frame, text="Quit", bg='white', command=lambda: quit())
    button4.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.15)

    label = tk.Label(frame, text="WELCOME TO DB\nWhat do you like to do?", bg="white")
    label.place(relx=0.15, rely=0.025, relwidth=0.7, relheight=0.25)

    instruction = tk.Label(frame, text="Write here ⬇", bg="white")
    instruction.place(relx=0.15, rely=0.53, relwidth=0.7, relheight=0.1)

    app.mainloop()

def checkpass(entry):

    if entry != ADMIN_PASSWORD:
        p_label["text"] = "Wrong...\nPassword: "

    else:
        try:
            conn.execute('''CREATE TABLE KEYS
            (PASS_KEY TEXT PRIMARY KEY NOT NULL)''')
            print("New db created...")
            p_app.destroy()
        except:
            print("Using existing...")
            p_app.destroy()

        second_window()

def create_password(pass_key, service, admin_pass):
    return sha256(admin_pass.encode("utf-8") + service.lower().encode("utf-8")).hexdigest()[10:21]


def get_hex_key(admin_pass, service):
    return sha256(admin_pass.encode("utf-8") + service.lower().encode("utf-8")).hexdigest()


def get_password(admin_pass, service, instruction, entry):

    if (service == ""):
        instruction["text"] = "What's the name of the service?"

    else:
        secret_key = get_hex_key(admin_pass, service)

        cursor = conn.execute("SELECT * from KEYS")

        for row in cursor:
            if secret_key == row[0]:
                conn.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')
                file_string = ""
                for row in cursor:
                    file_string = row[0]

                valor = create_password(file_string, service, admin_pass)
                fim = '"' + service.capitalize() + '"' + " password:\n " + str(valor)
                instruction["text"] = fim
                entry.delete(0, tk.END)
                return

        error = "You don't have any password in " + '"' + service + '"' + " service."
        instruction["text"] = error
        entry.delete(0, tk.END)



def add_password(service, admin_pass, instruction, entry):

    if (service == ""):
        instruction["text"] = "What's the name of the service?"

    else:

        secret_key = get_hex_key(admin_pass, service)

        cursor = conn.execute("SELECT * from KEYS")

        for row in cursor:
            if secret_key == row[0]:
                conn.execute("SELECT * from KEYS WHERE PASS_KEY=" + '"' + secret_key + '"')
                file_string = ""
                for row in cursor:
                    file_string = row[0]

                valor = create_password(file_string, service, admin_pass)
                fim = "Password already in db, password:\n" + str(valor)
                instruction["text"] = fim
                return

        conn.execute("INSERT INTO KEYS (PASS_KEY) VALUES (%s)" % ('"' + secret_key + '"'))

        conn.commit()
        instruction["text"] = '"' + service.capitalize() + '"' + " password created:\n " + create_password(secret_key, service, admin_pass)
        entry.delete(0, tk.END)

def delete_password(service, admin_pass, instruction, entry):
    if (service == ""):
        instruction["text"] = "What's the name of the service?"

    else:
        secret_key = get_hex_key(admin_pass, service)

        cursor = conn.execute("SELECT * from KEYS")

        for row in cursor:
            if secret_key == row[0]:
                conn.execute("DELETE FROM KEYS WHERE PASS_KEY = (%s)" % ('"' + secret_key + '"'))
                conn.commit()
                instruction["text"] = "Password from " + '"' + service + '"' + " deleted"
                entry.delete(0, tk.END)
                return

        error = "You don't have any password in " + '"' + service + '"' + " service."
        instruction["text"] = error
        entry.delete(0, tk.END)

def quit():
    sys.exit()

p_app = tk.Tk()

conn = sqlite3.connect('pass_manager.db')

p_app.geometry("700x500+350+150")

HEIGHT = 500
WIDTH = 700

canvas = tk.Canvas(p_app, height=HEIGHT, width=WIDTH)
canvas.pack()

p_frame = tk.Frame(p_app, bg="grey")
p_frame.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

p_entry = tk.Entry(p_frame, font=40, bg="white")
p_entry.place(relx=0.25, rely=0.45, relwidth=0.5, relheight=0.1)

p_button = tk.Button(p_frame, text="Check", bg='white', command=lambda: checkpass(p_entry.get()))
p_button.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.15)

p_button = tk.Button(p_frame, text="Quit", bg='white', command=lambda: quit())
p_button.place(relx=0.4, rely=0.8, relwidth=0.2, relheight=0.15)

p_label = tk.Label(p_frame, text="WELCOME TO DB\n\nPassword:", bg="white")
p_label.place(relx=0.15, rely=0.025, relwidth=0.7, relheight=0.25)

p_app.mainloop()
