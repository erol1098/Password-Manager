

from textwrap import indent
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    p_text.delete(0, END)
    #Password Generator
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    caps =['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '*', '+']

    nr_letters= random.randint(6)
    nr_cap = random.randint(2)
    nr_symbols = random.randint(4)
    nr_numbers = random.randint(4)

    password_list =[]
    password = ""
    
    
    for _ in range(nr_letters):
        password_list.append(random.choice(letters))
    for _ in range(nr_cap):
        password_list.append(random.choice(caps))    
    for _ in range(nr_symbols):
        password_list.append(random.choice(symbols))
    for _ in range(nr_numbers):
        password_list.append(random.choice(numbers))

    for _ in range(len(password_list)):
        password += random.choice(password_list)

    p_text.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = w_text.get()
    email = e_text.get()
    password = p_text.get()
    
    new_entry ={
        website: {
            "email": email,
            "password": password,
        }
    }
    if not website or not password or not email:
        messagebox.showerror(title="Oops!", message=" There are empty fields.")
        return None
    
    is_true = messagebox.askokcancel(title=website, message=f"Correct?\n{website}\n{email}\n{password}\n")
    if is_true:
        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
                
        except json.JSONDecodeError:
            with open("data.json", mode="w") as file:    
                json.dump(new_entry, file, indent=4)
        except FileNotFoundError:
            with open("data.json", mode="w") as file:    
                json.dump(new_entry, file, indent=4)                
        else:
            data.update(new_entry)
            with open("data.json", mode="w") as file:    
                json.dump(new_entry, file, indent=4)
               
        w_text.delete(0, END)
        p_text.delete(0, END)
# ---------------------------- SEARCHING ------------------------------- #
def searching():
    website = w_text.get()
    
    try:
        with open("data.json", mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops!", message="File Not Found")
    else:      
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Search Result", message=f"Website: {website}\nEmail/Username: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Search Result", message="Record does not exist.")         

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")


picture = PhotoImage(file="./logo.png")
canvas = Canvas(height=200, width=200)
canvas.create_image(100, 100, image=picture)
canvas.grid(column=1, row=0)

website = Label(text="Website:")
mail_username = Label(text="Email/Username:")
password = Label(text="Password:")

website.grid(column=0, row=1)
mail_username.grid(column=0, row=2)
password.grid(column=0, row=3)


w_text = Entry(width=32)
e_text = Entry(width=50)
p_text = Entry(width=32)
generate_button = Button(text="Generate Password", command=password_generator)
add_button = Button(text="Add", width=43, command=save_password)
search_button = Button(text="Search", command=searching, width=13)
w_text.focus()
e_text.insert(END, "example@mail.com")


w_text.grid(column=1, row=1)
e_text.grid(column=1, row=2, columnspan=2)
p_text.grid(column=1, row=3)
generate_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, columnspan=2)
search_button.grid(column=2, row=1)



window.mainloop()