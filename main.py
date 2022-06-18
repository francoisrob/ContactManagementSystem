# Francois Robbertze 56PCNHFS4
# Contact managing system
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Main window
class MainWindow:
    def __init__(self, master):
        global tree
        self.root = master
        root.title('Contact Management System')
        root.columnconfigure(0, weight=3)
        root.geometry('550x280')
        root.resizable(False, False)

        # Create treeview
        columns1 = ('first_name', 'last_name', 'gender', 'age', 'address', 'contact_number')
        tree = ttk.Treeview(root, columns=columns1, show='headings')
        tree.heading('first_name', text='First Name')
        tree.heading('last_name', text='Last Name')
        tree.heading('gender', text='Gender')
        tree.heading('age', text='Age')
        tree.heading('address', text='Address')
        tree.heading('contact_number', text='Contact Number')
        tree.column('first_name', width=70)
        tree.column('last_name', width=80)
        tree.column('gender', width=60)
        tree.column('age', width=50)
        tree.column('address', width=110)
        tree.column('contact_number', width=100)
        tree.grid(row=0, column=0, columnspan=4, pady=10, padx=10, ipadx=40)
        viewTree()

        # Add Contact button
        btn_Add = tk.Button(root, text="Add Contact", command=ContactPage)
        btn_Add.grid(row=1, column=1, padx=5, sticky='E')
        # Create Update button
        btn_Update = tk.Button(root, text="Update Contact", command=lambda: UpdatePage(tree.focus()))
        btn_Update.grid(row=1, column=2, padx=5, sticky='E')
        # Create Delete button
        btn_Delete = tk.Button(root, text="Delete Contact", command=lambda: DeleteRecord(tree.focus()))
        btn_Delete.grid(row=1, column=3, padx=(5, 20), sticky='E')

# Display data in treeview object
def viewTree():
    # view database in tree
    # Connect to database
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='toor',
        database="main"
    )
    myCursor = mydb.cursor()
    myCursor.execute('SELECT * FROM contacts')
    sql = myCursor.fetchall()
    tree.delete(*tree.get_children())
    for x in sql:
        if x[6] % 2 == 0:
            tree.insert(parent='', index='end', iid=x[6], values=(x[0], x[1], x[2], x[3], x[4], x[5]))
        else:
            tree.insert(parent='', index='end', iid=x[6], values=(x[0], x[1], x[2], x[3], x[4], x[5]))
    mydb.commit()
    mydb.close()

# Delete Record
class DeleteRecord:
    def __init__(self, arg):
        if arg != '':
            if messagebox.askyesno('Confirmation', 'Are you sure you want to delete the current record?'):
                self.arg = int(arg)

        else:
            messagebox.showinfo(title=None, message="Please select a record to delete.")

# Update record button
class UpdatePage:
    def __init__(self, arg):
        global values
        if arg != '':
            self.arg = int(arg)
            try:
                # Connect to database
                mydb = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='toor',
                    database="main"
                )
                myCursor = mydb.cursor(buffered=True)
                myCursor.execute(f'SELECT * FROM contacts WHERE ID = {self.arg}')
                values = myCursor.fetchone()
                mydb.commit()
                mydb.close()
            except Exception as e:
                print(e)
            self.frame = tk.Toplevel(root)
            self.frame.title('Update Contact')
            self.frame.geometry('290x340')
            self.frame.resizable(False, False)
            self.frame.focus_force()

            # Create text boxes
            self.first_name = tk.Entry(self.frame, width=20)
            self.first_name.grid(row=0, column=1, padx=5, pady=(10, 1))
            self.first_name.focus()
            self.last_name = tk.Entry(self.frame, width=20)
            self.last_name.grid(row=2, column=1, pady=1)
            self.gender = tk.Entry(self.frame, width=20)
            self.gender.grid(row=4, column=1, pady=1)
            self.age = tk.Entry(self.frame, width=20)
            self.age.grid(row=6, column=1, pady=1)
            self.address = tk.Entry(self.frame, width=20)
            self.address.grid(row=8, column=1, pady=1)
            self.contact_number = tk.Entry(self.frame, width=20)
            self.contact_number.grid(row=10, column=1, pady=1)

            # Add data to Entries
            self.first_name.insert(0, values[0])
            self.last_name.insert(0, values[1])
            self.gender.insert(0, values[2])
            self.age.insert(0, values[3])
            self.address.insert(0, values[4])
            self.contact_number.insert(0, values[5])

            # label variables
            self.name_invalid = tk.StringVar()
            self.lastname_invalid = tk.StringVar()
            self.gender_invalid = tk.StringVar()
            self.age_invalid = tk.StringVar()
            self.contact_invalid = tk.StringVar()

            # Add correction label
            self.f_name_invalid_label = tk.Label(self.frame, textvariable=self.name_invalid, fg='#f00')
            self.f_name_invalid_label.grid(row=1, column=1, pady=(0, 2))
            self.l_name_invalid_label = tk.Label(self.frame, textvariable=self.lastname_invalid, fg='#f00')
            self.l_name_invalid_label.grid(row=3, column=1, pady=(0, 2))
            self.gender_invalid_label = tk.Label(self.frame, text='')
            self.gender_invalid_label.grid(row=5, column=1, pady=(0, 2))
            self.age_invalid_label = tk.Label(self.frame, textvariable=self.age_invalid, fg='#f00')
            self.age_invalid_label.grid(row=7, column=1, pady=(0, 2))
            self.address_invalid_label = tk.Label(self.frame, text='')
            self.address_invalid_label.grid(row=9, column=1, pady=(0, 2))
            self.contact_invalid_number_label = tk.Label(self.frame, textvariable=self.contact_invalid, fg='#f00')
            self.contact_invalid_number_label.grid(row=11, column=1, pady=(0, 2))

            # Add Labels
            f_name_label = tk.Label(self.frame, text="First Name*")
            f_name_label.grid(row=0, column=0, sticky='E')
            l_name_label = tk.Label(self.frame, text="Last Name*")
            l_name_label.grid(row=2, column=0, sticky='E')
            gender_label = tk.Label(self.frame, text="Gender")
            gender_label.grid(row=4, column=0, sticky='E')
            age_label = tk.Label(self.frame, text="Age*")
            age_label.grid(row=6, column=0, sticky='E')
            address_label = tk.Label(self.frame, text="Address")
            address_label.grid(row=8, column=0, sticky='E')
            contact_number_label = tk.Label(self.frame, text="Contact Number*")
            contact_number_label.grid(row=10, column=0, padx=(20, 0), sticky='E')
            # Add contact Button
            btn_update_contact = tk.Button(self.frame, text="Update Contact", command=lambda: self.updateContact())
            btn_update_contact.grid(row=12, column=1, pady=10, padx=20, ipadx=20)
        else:
            messagebox.showinfo(title=None, message="Please select a record to update.")

    def updateContact(self):
        invalid = False
        self.name_invalid.set('')
        self.lastname_invalid.set('')
        self.age_invalid.set('')
        self.contact_invalid.set('')

        # Data Validation
        if (not self.contact_number.get().isdigit()) or (len(self.contact_number.get()) != 10):
            invalid = True
            self.contact_number.delete(0, 'end')
            self.contact_invalid.set("invalid contact number")
            self.contact_number.focus()
        if not self.age.get().isdigit():
            invalid = True
            self.age.delete(0, 'end')
            self.age_invalid.set("invalid Age")
            self.age.focus()
        if not self.last_name.get().isalpha():
            invalid = True
            self.last_name.delete(0, 'end')
            self.lastname_invalid.set("invalid lastname")
            self.last_name.focus()
        if not self.first_name.get().isalpha():
            invalid = True
            self.first_name.delete(0, 'end')
            self.name_invalid.set("invalid name")
            self.first_name.focus()

        # Try adding data to db
        if invalid:
            messagebox.showwarning(title='ERROR', message='An error occurred while trying to update the contact')
        else:
            try:
                first_name = str(self.first_name.get())
                last_name = str(self.last_name.get())
                gender = str(self.gender.get())
                age = int(self.age.get())
                address = str(self.address.get())
                contact_number = str(self.contact_number.get())
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="toor",
                    database="main"
                )
                cursor = mydb.cursor()
                sql = '''UPDATE contacts 
                         SET
                         first_name = %s,
                         last_name = %s,
                         gender = %s,
                         age = %s,
                         address = %s,
                         contact_number = %s
                         WHERE ID = %s
                      '''
                val = (first_name, last_name, gender, age, address, contact_number, self.arg)
                cursor.execute(sql, val)
                mydb.commit()
                mydb.close()
                messagebox.showinfo(title="Successful", message='Successfully updated the contact!')
                viewTree()
                self.frame.destroy()
            except Exception as e:
                print(e)
                messagebox.showerror(title='ERROR', message='An error occurred while trying to update the contact')

# Create add contact frame
class ContactPage:
    def __init__(self):
        self.frame = tk.Toplevel(root)
        self.frame.title('Add Contact')
        self.frame.geometry('270x340')
        self.frame.resizable(False, False)
        self.frame.focus_force()

        # Create text boxes
        self.first_name = tk.Entry(self.frame, width=20)
        self.first_name.grid(row=0, column=1, padx=5, pady=(10, 1))
        self.first_name.focus()
        self.last_name = tk.Entry(self.frame, width=20)
        self.last_name.grid(row=2, column=1, pady=1)
        self.gender = tk.Entry(self.frame, width=20)
        self.gender.grid(row=4, column=1, pady=1)
        self.age = tk.Entry(self.frame, width=20)
        self.age.grid(row=6, column=1, pady=1)
        self.address = tk.Entry(self.frame, width=20)
        self.address.grid(row=8, column=1, pady=1)
        self.contact_number = tk.Entry(self.frame, width=20)
        self.contact_number.grid(row=10, column=1, pady=1)

        # label variables
        self.name_invalid = tk.StringVar()
        self.lastname_invalid = tk.StringVar()
        self.gender_invalid = tk.StringVar()
        self.age_invalid = tk.StringVar()
        self.contact_invalid = tk.StringVar()
        # Add correction label
        self.f_name_invalid_label = tk.Label(self.frame, textvariable=self.name_invalid, fg='#f00')
        self.f_name_invalid_label.grid(row=1, column=1, pady=(0, 2))
        self.l_name_invalid_label = tk.Label(self.frame, textvariable=self.lastname_invalid, fg='#f00')
        self.l_name_invalid_label.grid(row=3, column=1, pady=(0, 2))
        self.gender_invalid_label = tk.Label(self.frame, text='')
        self.gender_invalid_label.grid(row=5, column=1, pady=(0, 2))
        self.age_invalid_label = tk.Label(self.frame, textvariable=self.age_invalid, fg='#f00')
        self.age_invalid_label.grid(row=7, column=1, pady=(0, 2))
        self.address_invalid_label = tk.Label(self.frame, text='')
        self.address_invalid_label.grid(row=9, column=1, pady=(0, 2))
        self.contact_invalid_number_label = tk.Label(self.frame, textvariable=self.contact_invalid, fg='#f00')
        self.contact_invalid_number_label.grid(row=11, column=1, pady=(0, 2))

        # Add Labels
        f_name_label = tk.Label(self.frame, text="First Name*")
        f_name_label.grid(row=0, column=0, sticky='E')
        l_name_label = tk.Label(self.frame, text="Last Name*")
        l_name_label.grid(row=2, column=0, sticky='E')
        gender_label = tk.Label(self.frame, text="Gender")
        gender_label.grid(row=4, column=0, sticky='E')
        age_label = tk.Label(self.frame, text="Age*")
        age_label.grid(row=6, column=0, sticky='E')
        address_label = tk.Label(self.frame, text="Address")
        address_label.grid(row=8, column=0, sticky='E')
        contact_number_label = tk.Label(self.frame, text="Contact Number*")
        contact_number_label.grid(row=10, column=0, padx=(20, 0), sticky='E')
        # Add contact Button
        btn_add_contact = tk.Button(self.frame, text="Add Contact", command=lambda: self.addContacts())
        btn_add_contact.grid(row=12, column=1, pady=10, padx=20, ipadx=20)

    # Adds user input into table
    def addContacts(self):
        invalid = False
        self.name_invalid.set('')
        self.lastname_invalid.set('')
        self.age_invalid.set('')
        self.contact_invalid.set('')

        # Data Validation
        if (not self.contact_number.get().isdigit()) or (len(self.contact_number.get()) != 10):
            invalid = True
            self.contact_number.delete(0, 'end')
            self.contact_invalid.set("invalid contact number")
            self.contact_number.focus()
        if not self.age.get().isdigit():
            invalid = True
            self.age.delete(0, 'end')
            self.age_invalid.set("invalid Age")
            self.age.focus()
        if not self.last_name.get().isalpha():
            invalid = True
            self.last_name.delete(0, 'end')
            self.lastname_invalid.set("invalid lastname")
            self.last_name.focus()
        if not self.first_name.get().isalpha():
            invalid = True
            self.first_name.delete(0, 'end')
            self.name_invalid.set("invalid name")
            self.first_name.focus()

        # Try adding data to db
        if invalid:
            messagebox.showwarning(title='ERROR', message='An error occurred while trying to add the contact')
        else:
            try:
                first_name = str(self.first_name.get())
                last_name = str(self.last_name.get())
                gender = str(self.gender.get())
                age = int(self.age.get())
                address = str(self.address.get())
                contact_number = str(self.contact_number.get())
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="toor",
                    database="main"
                )
                cursor = mydb.cursor()
                sql = 'INSERT INTO contacts (first_name, last_name, gender, age, address, contact_number) VALUES ' \
                      '(%s, %s, %s, %s, %s, %s)'
                val = (first_name, last_name, gender, age, address, contact_number)
                cursor.execute(sql, val)
                mydb.commit()
                mydb.close()
                messagebox.showinfo(title="Successful", message='Successfully added the contact!')
                viewTree()
                self.frame.destroy()
            except Exception as e:
                print(e)
                messagebox.showerror(title='ERROR', message='An error occurred while trying to add the contact')


root = tk.Tk()
main_window = MainWindow(root)
root.mainloop()
