from tkinter import *
from tkinter import messagebox
from random import randint, shuffle, choice
import pyperclip
import json

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Arial"
BG_COLOR = "#f0f0f0"
ENTRY_COLOR = "#ffffff"
BUTTON_COLOR = "#4a90e2"
BUTTON_HOVER = "#357abd"
TEXT_COLOR = "#333333"
ACCENT_COLOR = "#2ecc71"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def Generate_Password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for _ in range(randint(8, 10))]
    password_number = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letter + password_symbol + password_number
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    messagebox.showinfo(title="Copy", message="Password copied to clipboard!")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
        "email":email,
        "password":password
    }
    }


    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Empty Fields",
                             message="Please don't leave any fields empty!")
    else:
        try:
            with open("savedDetails.json", "r") as data_file:
                # loading the data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("savedDetails.json", "w") as data_file:
                data = json.dump(new_data, data_file, indent=4)
        else:
                # making an update
                data.update(new_data)
                with open("savedDetails.json", "w") as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)
        finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, bg=BG_COLOR)

# Make window slightly larger and center it
window.geometry("500x500")
window.resizable(False, False)

# Center the window on screen
window.eval('tk::PlaceWindow . center')

# Canvas for logo
canvas = Canvas(width=200, height=200, bg=BG_COLOR, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, pady=(0, 20))

# Labels
Label(text="Website:", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
Label(text="Email/Username:", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
Label(text="Password:", bg=BG_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)

# Entries
website_entry = Entry(width=27, bg=ENTRY_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10))
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(width=35, bg=ENTRY_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10), borderwidth=1, relief="solid")
email_entry.grid(row=2, column=1, columnspan=2, pady=5, sticky="ew")
email_entry.insert(0, "example@gmail.com")

password_entry = Entry(width=21, bg=ENTRY_COLOR, fg=TEXT_COLOR, font=(FONT_NAME, 10), borderwidth=1, relief="solid")
password_entry.grid(row=3, column=1, pady=5, sticky="ew")

# Buttons with hover effects
def on_enter(e, button):
    button['background'] = BUTTON_HOVER

def on_leave(e, button):
    button['background'] = BUTTON_COLOR

def find_password():
    website = website_entry.get()
    try:
        with open("savedDetails.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
            messagebox.showinfo(title="💔Error",message="No file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=f"🌴{website}",
                                message=f"Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="💔404", message="Website Not Found")

generate_password = Button(text="Generate Password",
                           width=15, command=Generate_Password,
                         bg=BUTTON_COLOR, fg="white", font=(FONT_NAME, 9, "bold"),
                         borderwidth=0, relief="flat", activebackground=BUTTON_HOVER)
generate_password.grid(row=3, column=2, padx=(10, 0), pady=5, sticky="ew")
generate_password.bind("<Enter>", lambda e: on_enter(e, generate_password))
generate_password.bind("<Leave>", lambda e: on_leave(e, generate_password))

add = Button(text="Add", width=36, command=save,
            bg=ACCENT_COLOR, fg="white", font=(FONT_NAME, 10, "bold"),
            borderwidth=0, relief="flat", activebackground="#27ae60")
add.grid(row=4, column=1, columnspan=2, pady=(10, 0), sticky="ew")
add.bind("<Enter>", lambda e: on_enter(e, add))
add.bind("<Leave>", lambda e: on_leave(e, add))

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)
# Add some padding to all widgets
for child in window.winfo_children():
    child.grid_configure(padx=5, pady=5)

window.mainloop()