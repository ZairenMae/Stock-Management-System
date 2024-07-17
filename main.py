from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import random
import pymysql
import csv
from datetime import datetime

window = Tk()
window.title("Stock Management System")
window.geometry("720x640")

# Set the window to be resizable
window.resizable(True, True)

my_tree = ttk.Treeview(window, show='headings', height=20)
style = ttk.Style()

# Use StringVar for the placeholders
placeholderArray = [StringVar() for _ in range(5)]
numeric = '1234567890'
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='zairen',
        db='dbstockmanagementsystem'
    )

def read():
    conn = connection()
    cursor = conn.cursor()
    cursor.connection.ping()
    sql = "SELECT item_id, name, price, quantity, category, date FROM stocks ORDER BY id DESC"
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results

def refreshTable():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for array in read():
        my_tree.insert(parent='', index='end', iid=array, text="", values=(array), tag="orow")
    my_tree.tag_configure('orow', background="#EEEEEE")
    my_tree.pack()

def setph(word, num):
    placeholderArray[num].set(word)

def generateRand():
    itemId = ''
    for i in range(0, 3):
        randno = random.randrange(0, len(numeric))
        itemId += str(numeric[randno])
    randno = random.randrange(0, len(alpha))
    itemId += '-' + str(alpha[randno])
    setph(itemId, 0)

def save():
    conn = connection()
    cursor = conn.cursor()
    itemId = str(placeholderArray[0].get())
    name = str(placeholderArray[1].get())
    price = str(placeholderArray[2].get())
    qnt = str(placeholderArray[3].get())
    cat = str(placeholderArray[4].get())
    valid = True

    if not (itemId and itemId.strip()) or not (name and name.strip()) or not (price and price.strip()) or not (qnt and qnt.strip()) or not (cat and cat.strip()):
        messagebox.showwarning("", "Please fill up all entries")
        return

    if len(itemId) < 5 or itemId[3] != '-' or not all(c in numeric for c in itemId[:3]) or itemId[4] not in alpha:
        messagebox.showwarning("", "Invalid Item Id")
        return

    try:
        cursor.connection.ping()
        sql = f"SELECT * FROM stocks WHERE item_id = '{itemId}'"
        cursor.execute(sql)
        checkItemNo = cursor.fetchall()
        if len(checkItemNo) > 0:
            messagebox.showwarning("", "Item Id already used")
            return
        sql = f"INSERT INTO stocks (item_id, name, price, quantity, category) VALUES ('{itemId}', '{name}', '{price}', '{qnt}', '{cat}')"
        cursor.execute(sql)
        conn.commit()
        for num in range(0, 5):
            setph('', num)
    except Exception as e:
        messagebox.showwarning("", "Error while saving ref: " + str(e))
    finally:
        cursor.close()
        conn.close()
    refreshTable()

def update():
    conn = connection()
    cursor = conn.cursor()
    selectedItemId = ''

    try:
        selectedItem = my_tree.selection()[0]
        selectedItemId = str(my_tree.item(selectedItem)['values'][0])
    except:
        messagebox.showwarning("", "Please select a data row")
        return

    itemId = str(placeholderArray[0].get())
    name = str(placeholderArray[1].get())
    price = str(placeholderArray[2].get())
    qnt = str(placeholderArray[3].get())
    cat = str(placeholderArray[4].get())

    if not (itemId and itemId.strip()) or not (name and name.strip()) or not (price and price.strip()) or not (qnt and qnt.strip()) or not (cat and cat.strip()):
        messagebox.showwarning("", "Please fill up all entries")
        return

    if selectedItemId != itemId:
        messagebox.showwarning("", "You can't change Item ID")
        return

    try:
        cursor.connection.ping()
        sql = f"UPDATE stocks SET name = '{name}', price = '{price}', quantity = '{qnt}', category = '{cat}' WHERE item_id = '{itemId}'"
        cursor.execute(sql)
        conn.commit()
        for num in range(0, 5):
            setph('', num)
    except Exception as err:
        messagebox.showwarning("", "Error occurred ref: " + str(err))
    finally:
        cursor.close()
        conn.close()
    refreshTable()

def delete():
    conn = connection()
    cursor = conn.cursor()
    try:
        if my_tree.selection()[0]:
            decision = messagebox.askquestion("", "Delete the selected data?")
            if decision != 'yes':
                return
            selectedItem = my_tree.selection()[0]
            itemId = str(my_tree.item(selectedItem)['values'][0])
            sql = f"DELETE FROM stocks WHERE item_id = '{itemId}'"
            cursor.execute(sql)
            conn.commit()
            messagebox.showinfo("", "Data has been successfully deleted")
    except Exception as e:
        messagebox.showinfo("", "Sorry, an error occurred: " + str(e))
    finally:
        cursor.close()
        conn.close()
    refreshTable()

def select():
    try:
        selectedItem = my_tree.selection()[0]
        itemId = str(my_tree.item(selectedItem)['values'][0])
        name = str(my_tree.item(selectedItem)['values'][1])
        price = str(my_tree.item(selectedItem)['values'][2])
        qnt = str(my_tree.item(selectedItem)['values'][3])
        cat = str(my_tree.item(selectedItem)['values'][4])
        setph(itemId, 0)
        setph(name, 1)
        setph(price, 2)
        setph(qnt, 3)
        setph(cat, 4)
    except:
        messagebox.showwarning("", "Please select a data row")

def find():
    conn = connection()
    cursor = conn.cursor()
    itemId = str(placeholderArray[0].get())
    name = str(placeholderArray[1].get())
    price = str(placeholderArray[2].get())
    qnt = str(placeholderArray[3].get())
    cat = str(placeholderArray[4].get())

    cursor.connection.ping()
    if itemId and itemId.strip():
        sql = f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE item_id LIKE '%{itemId}%'"
    elif name and name.strip():
        sql = f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE name LIKE '%{name}%'"
    elif price and price.strip():
        sql = f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE price LIKE '%{price}%'"
    elif qnt and qnt.strip():
        sql = f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE quantity LIKE '%{qnt}%'"
    elif cat and cat.strip():
        sql = f"SELECT item_id, name, price, quantity, category, date FROM stocks WHERE category LIKE '%{cat}%'"
    else:
        messagebox.showwarning("", "Please fill up one of the entries")
        return

    cursor.execute(sql)
    try:
        result = cursor.fetchall()
        for num in range(0, 5):
            setph(result[0][num], num)
    except:
        messagebox.showwarning("", "No data found")
    finally:
        cursor.close()
        conn.close()

def clear():
    for num in range(0, 5):
        setph('', num)

def exportExcel():
    conn = connection()
    cursor = conn.cursor()
    sql = "SELECT item_id, name, price, quantity, category, date FROM stocks ORDER BY id DESC"
    cursor.execute(sql)
    dataraw = cursor.fetchall()
    date = str(datetime.now()).replace(' ', '_').replace(':', '-')[0:16]
    with open(f"stocks_{date}.csv", 'a', newline='') as f:
        w = csv.writer(f, dialect='excel')
        for record in dataraw:
            w.writerow(record) 
    messagebox.showinfo("", f"Excel file downloaded: stocks_{date}.csv")
    cursor.close()
    conn.close()

# Create rounded button function
def create_rounded_button(parent, text, command, width=100, height=30, radius=15):
    button = Canvas(parent, width=width, height=height, bg="#6d1978", highlightthickness=0)
    button.create_arc(0, 0, radius*2, radius*2, start=90, extent=90, fill="#6d1978", outline="#6d1978")
    button.create_arc(width - radius*2, 0, width, radius*2, start=0, extent=90, fill="#6d1978", outline="#6d1978")
    button.create_rectangle(radius, 0, width - radius, height, fill="#6d1978", outline="#6d1978")
    button.create_arc(0, height - radius*2, radius*2, height, start=180, extent=90, fill="#6d1978", outline="#6d1978")
    button.create_arc(width - radius*2, height - radius*2, width, height, start=270, extent=90, fill="#6d1978", outline="#6d1978")
    button.create_text(width/2, height/2, text=text, fill='white', font=('Arial', 10))
    button.bind("<Button-1>", lambda e: command())
    return button

frame = Frame(window, bg="#7a0266")
frame.pack()

manageFrame = LabelFrame(frame, text="Manage", borderwidth=5)
manageFrame.grid(row=0, column=0, sticky="w", padx=[10, 200], pady=20, ipadx=[6])

# Create rounded buttons
create_rounded_button(manageFrame, "SAVE", save).grid(row=0, column=0, padx=5, pady=5, sticky='w')
create_rounded_button(manageFrame, "UPDATE", update).grid(row=0, column=1, padx=5, pady=5, sticky='w')
create_rounded_button(manageFrame, "DELETE", delete).grid(row=0, column=2, padx=5, pady=5, sticky='w')
create_rounded_button(manageFrame, "SELECT", select).grid(row=0, column=3, padx=5, pady=5, sticky='w')
create_rounded_button(manageFrame, "FIND", find).grid(row=0, column=4, padx=5, pady=5, sticky='w')
create_rounded_button(manageFrame, "CLEAR", clear).grid(row=0, column=5, padx=5, pady=5, sticky='w')
create_rounded_button(manageFrame, "EXPORT EXCEL", exportExcel).grid(row=0, column=6, padx=5, pady=5, sticky='w')

entriesFrame = LabelFrame(frame, text="Form", borderwidth=5)
entriesFrame.grid(row=1, column=0, sticky="w", padx=[10, 200], pady=[0, 20], ipadx=[6])

# Labels
labels = ["ITEM ID", "NAME", "PRICE", "QNT", "CATEGORY"]
for i, text in enumerate(labels):
    Label(entriesFrame, text=text, anchor="e", width=10).grid(row=i, column=0, padx=10)

categoryArray = ['Networking Tools', 'Computer Parts', 'Repair Tools', 'Gadgets']
itemIdEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[0])
nameEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[1])
priceEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[2])
qntEntry = Entry(entriesFrame, width=50, textvariable=placeholderArray[3])
categoryCombo = ttk.Combobox(entriesFrame, width=47, textvariable=placeholderArray[4], values=categoryArray)

itemIdEntry.grid(row=0, column=2, padx=5, pady=5)
nameEntry.grid(row=1, column=2, padx=5, pady=5)
priceEntry.grid(row=2, column=2, padx=5, pady=5)
qntEntry.grid(row=3, column=2, padx=5, pady=5)
categoryCombo.grid(row=4, column=2, padx=5, pady=5)

create_rounded_button(entriesFrame, "GENERATE ID", generateRand).grid(row=0, column=3, padx=5, pady=5)

style.configure(window)
my_tree['columns'] = ("Item Id", "Name", "Price", "Quantity", "Category", "Date")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Item Id", anchor=W, width=70)
my_tree.column("Name", anchor=W, width=125)
my_tree.column("Price", anchor=W, width=125)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Category", anchor=W, width=150)
my_tree.column("Date", anchor=W, width=150)
my_tree.heading("Item Id", text="Item Id", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)
my_tree.heading("Category", text="Category", anchor=W)
my_tree.heading("Date", text="Date", anchor=W)
my_tree.tag_configure('orow', background="#EEEEEE")
my_tree.pack()

refreshTable()

window.mainloop()
