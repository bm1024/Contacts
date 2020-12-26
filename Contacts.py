"""
Author: Bianca Magyar
Date: 12/26/2020
Description: Python program for a database of contacts 
             to add, delete, or update any contact names, 
             addresses, phones, or emails.
References: Codemy
"""

from tkinter import Label, Text, Entry, END, Button, Tk, E, W, LEFT, Scrollbar, RIGHT, Y
import sqlite3


if __name__ == "__main__":
    
    #add a contact to database
    def add():
        
        #save added contact
        def save_add():
            
            #connect to database and create cursor 
            conn = sqlite3.connect("contacts.db")
            c = conn.cursor()
            
            #insert into table 
            c.execute("INSERT INTO contacts VALUES (:f_name, :l_name, :phone, :email, :address, :city, :state, :zipcode)",
                      {
                          'f_name': f_name.get(),
                          'l_name': l_name.get(),
                          'phone': phone.get(),
                          'email': email.get(),
                          'address': address.get(),
                          'city': city.get(),
                          'state': state.get(),
                          'zipcode': zipcode.get()
                      }         
            )
            
            conn.commit()
            conn.close()
            
            addgui.destroy()
        
        #set up window to add contacts
        addgui = Tk()
        addgui.title("Add Contacts")
        addgui.iconbitmap("contacts-icon1.ico")
        addgui.geometry("360x240")
        
        #create text boxes
        f_name = Entry(addgui, width=30)
        f_name.grid(row=0, column=1, padx=20, pady=(10,0))
        
        l_name = Entry(addgui, width=30)
        l_name.grid(row=1, column=1, padx=20, pady=(5,0))
        
        phone = Entry(addgui, width=30)
        phone.grid(row=2, column=1, padx=20, pady=(5,0))
        
        email = Entry(addgui, width=30)
        email.grid(row=3, column=1, padx=20, pady=(5,0))
        
        address = Entry(addgui, width=30)
        address.grid(row=4, column=1, padx=20, pady=(5,0))
        
        city = Entry(addgui, width=30)
        city.grid(row=5, column=1, padx=20, pady=(5,0))
        
        state = Entry(addgui, width=30)
        state.grid(row=6, column=1, padx=20, pady=(5,0))
        
        zipcode = Entry(addgui, width=30)
        zipcode.grid(row=7, column=1, padx=20, pady=(5,0))
        
        #create text box labels
        f_name_label = Label(addgui, text="First Name")
        f_name_label.grid(row=0, column=0)
        
        l_name_label = Label(addgui, text="Last Name")
        l_name_label.grid(row=1, column=0)
        
        phone_label = Label(addgui, text="Phone")
        phone_label.grid(row=2, column=0)
        
        email_label = Label(addgui, text="Email")
        email_label.grid(row=3, column=0)
        
        address_label = Label(addgui, text="Address")
        address_label.grid(row=4, column=0)
        
        city_label = Label(addgui, text="City")
        city_label.grid(row=5, column=0)
        
        state_label = Label(addgui, text="State")
        state_label.grid(row=6, column=0)
        
        zipcode_label = Label(addgui, text="Zipcode")
        zipcode_label.grid(row=7, column=0)
    
        #create an save button
        save_button = Button(addgui, text="Save Contact", command=save_add)
        save_button.grid(row=8, column=0, columnspan=2, pady=(5, 0), padx=10, ipadx=132)
    
    #query to show all contacts in database
    def query():
        
        #set up show window
        showgui = Tk()
        showgui.title("Show Contacts")
        showgui.iconbitmap("contacts-icon1.ico")
        showgui.geometry("360x290")
        
        #connect to database and create cursor 
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        
        #query the database and order contacts by last name then first name
        c.execute("SELECT *, oid FROM contacts ORDER BY last_name, first_name;")
        records = c.fetchall()
        print_records = ""
        for record in records:
            print_records += "%d\t%s , %s\n" % (record[8], record[1], record[0]) 
        
        #create scroll box to display all contacts     
        scroll = Scrollbar(showgui)
        scroll.pack(side=RIGHT, fill=Y)
        query_text = Text(showgui, height=200, width=300)
        query_text.pack(side=LEFT, fill=Y)
        scroll.config(command=query_text.yview)
        query_text.config(yscrollcommand=scroll.set)
        query_text.insert(END, print_records)
        
        conn.commit()
        conn.close()
    
    
    #create update function to edit a record    
    def update():
        
        #create save function to update changes to a record
        def save():
            
            #connect to database and create cursor 
            conn = sqlite3.connect("contacts.db")
            c = conn.cursor()
            
            record_id = selected_record.get()
            c.execute("""
                UPDATE contacts SET 
                    first_name = :first,
                    last_name = :last,
                    phone = :phone,
                    email = :email,
                    address = :address,
                    city = :city,
                    state = :state,
                    zipcode = :zipcode
                
                WHERE oid = :oid""",
                {
                    "first": f_name_update.get(),
                    "last": l_name_update.get(),
                    "phone": phone_update.get(),
                    "email": email_update.get(),
                    "address": address_update.get(),
                    "city": city_update.get(),
                    "state": state_update.get(),
                    "zipcode": zipcode_update.get(),
                    "oid": record_id
                }
            )
            
            conn.commit()
            conn.close()
            
            #clear text entry and re-insert prompt
            selected_record.delete(0, END) 
            selected_record.insert(0, "Enter contact ID number") 
            updategui.destroy()
            
        #create function to delete a record
        def delete():
            
            #store selected record id
            record_id = selected_record.get() 
            
            conn = sqlite3.connect("contacts.db")
            c = conn.cursor()
            
            #delete a record
            c.execute("DELETE from contacts WHERE oid = " + record_id)
            
            conn.commit()
            conn.close()
            
            #clear text entry and re-insert prompt
            selected_record.delete(0, END) 
            selected_record.insert(0, "Enter contact ID number") 
            
            updategui.destroy()
        
        #set up update window
        updategui = Tk()
        updategui.title("Update Contact")
        updategui.iconbitmap("contacts-icon1.ico")
        
        try: 
            #connect to database and create cursor 
            conn = sqlite3.connect("contacts.db")
            c = conn.cursor()
            
            record_id = selected_record.get()
            
            #query the database
            c.execute("SELECT * FROM contacts WHERE oid = " + record_id)
            records = c.fetchall()
            
            if records != []:
                updategui.geometry("360x275")
                
                #create text boxes
                f_name_update = Entry(updategui, width=30)
                f_name_update.grid(row=0, column=1, padx=20, pady=(10,0))
                
                l_name_update = Entry(updategui, width=30)
                l_name_update.grid(row=1, column=1, padx=20, pady=(5,0))
                
                phone_update = Entry(updategui, width=30)
                phone_update.grid(row=2, column=1, padx=20, pady=(5,0))
                
                email_update = Entry(updategui, width=30)
                email_update.grid(row=3, column=1, padx=20, pady=(5,0))
                
                address_update = Entry(updategui, width=30)
                address_update.grid(row=4, column=1, padx=20, pady=(5,0))
                
                city_update = Entry(updategui, width=30)
                city_update.grid(row=5, column=1, padx=20, pady=(5,0))
                
                state_update = Entry(updategui, width=30)
                state_update.grid(row=6, column=1, padx=20, pady=(5,0))
                
                zipcode_update = Entry(updategui, width=30)
                zipcode_update.grid(row=7, column=1, padx=20, pady=(5,0))
                
                
                #create text box labels
                f_name_label_update = Label(updategui, text="First Name")
                f_name_label_update.grid(row=0, column=0)
                
                l_name_label_update = Label(updategui, text="Last Name")
                l_name_label_update.grid(row=1, column=0)
                
                phone_label_update = Label(updategui, text="Phone")
                phone_label_update.grid(row=2, column=0)
                
                email_label_update = Label(updategui, text="Email")
                email_label_update.grid(row=3, column=0)
                
                address_label_update = Label(updategui, text="Address")
                address_label_update.grid(row=4, column=0)
                
                city_label_update = Label(updategui, text="City")
                city_label_update.grid(row=5, column=0)
                
                state_label_update = Label(updategui, text="State")
                state_label_update.grid(row=6, column=0)
                
                zipcode_label_update = Label(updategui, text="Zipcode")
                zipcode_label_update.grid(row=7, column=0)
                
                #loop through results to pre-fill entry boxes
                for record in records:
                    f_name_update.insert(0, record[0])
                    l_name_update.insert(0, record[1])
                    phone_update.insert(0, record[2])
                    email_update.insert(0, record[3])
                    address_update.insert(0, record[4])
                    city_update.insert(0, record[5])
                    state_update.insert(0, record[6])
                    zipcode_update.insert(0, record[7])
                
                #create an save button
                save_button = Button(updategui, text="Save Contact", command=save)
                save_button.grid(row=8, column=0, columnspan=2, pady=5, padx=10, ipadx=132)
                
                #create a delete button
                delete_button = Button(updategui, text="Delete Contact", command=delete)
                delete_button.grid(row=10, column=0, columnspan=2, padx=10, pady=5, ipadx=127)
                
            else:
                updategui.geometry("360x110")
                feedback_label = Label(updategui, text="Please try again and enter a valid value. Must be an integer assigned to a contact.", wraplength=300, justify=LEFT, font=("Calibri", 12))
                feedback_label.grid(row=0, column=0, columnspan=2, padx=40, pady=20)
            
            conn.commit()
            conn.close()
            
        except:
            updategui.geometry("360x110")
            feedback_label = Label(updategui, text="Please try again and enter a valid value. Must be an integer assigned to a contact.", wraplength=300, justify=LEFT, font=("Calibri", 12))
            feedback_label.grid(row=0, column=0, columnspan=2, padx=40, pady=20)
        
        
        
        
    def search():
        #connect to database and create cursor 
        conn = sqlite3.connect("contacts.db")
        c = conn.cursor()
        
        record_id = selected_record.get()
        
        #query the database
        c.execute("SELECT * FROM contacts WHERE oid = " + record_id)
        #records = c.fetchall()
        
        conn.commit()
        conn.close()    
    
    
    #MAIN
    #set up window for main program
    root = Tk()
    root.title("Contacts")
    root.iconbitmap("contacts-icon1.ico")
    root.geometry("365x120")
    
    #connect to database and create cursor 
    conn = sqlite3.connect('contacts.db')
    c = conn.cursor()
    
    #create table in database -- run the create table once
    c.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
        first_name text NOT NULL,
        last_name text NOT NULL,
        phone integer,
        email text,
        address text,
        city text,
        state text,
        zipcode integer
        )
    """)
    
    #search bar entry field
    selected_record = Entry(root, width=40)
    selected_record.grid(row=5, column=0, padx=(5,0), pady=5, sticky=E)
    selected_record.insert(0, "Enter contact ID number")
    
    #create search button
    search_button = Button(root, text="Search", command=update)
    search_button.grid(row=5, column=1, padx=(0,5), pady=5, ipadx=20, sticky=W)
    
    #create submit button 
    add_button = Button(root, text="Add Contact", command=add)
    add_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, ipadx=132)
    
    #create query button
    query_button = Button(root, text="Show Contacts", command=query)
    query_button.grid(row=7, column=0, columnspan=2, padx=10, pady=2, ipadx=127)
    
    #commit changes
    conn.commit()
    
    #close connection
    conn.close()
    
    
    root.mainloop()