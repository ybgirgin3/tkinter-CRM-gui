from tkinter import *
from tkinter import ttk
import sqlite3


root = Tk()
root.geometry("800x500")


db_name = "tkinter_db.sqlite3"
# create db or connect one
conn = sqlite3.connect(db_name)
c = conn.cursor()

# create table
c.execute("""CREATE TABLE if not exists table1 (
	ID integer,
	numara INTEGER,
	adi TEXT,
	soyadi TEXT,
	telefonu INTEGER)
	""")

# commit changes
conn.commit()
conn.close()


def query_database():
	conn = sqlite3.connect(db_name)
	c = conn.cursor()

	c.execute("SELECT * FROM table1")
	records = c.fetchall()
	from pprint import pprint
	pprint(records)
	print()

	global count
	count = 0

	"""for record in records:
					print(recor  d)"""

	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent="", index="end", iid=count, text="", values = (record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',) )
		else:
			my_tree.insert(parent="", index="end", iid=count, text="", values = (record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',) )
		count += 1


	conn.commit()
	conn.close()





# add style
style = ttk.Style()
style.theme_use('default')
style.configure("Treeview", background="#D3D3D3D", foreground="black", rowheight=25, fieldbackground="#D3D3D3")

style.map("Treeview", background=[('selected', '#347083')])

tree_frame = Frame(root)
tree_frame.pack(pady=10)

tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

tree_scroll.config(command=my_tree.yview)

# columns
my_tree['columns'] = ('ID', 'Numara', 'Adi', 'Soyadi', 'Telefonu')
# formt colum
my_tree.column("#0", width=0)
my_tree.column("ID", anchor = W)
my_tree.column("Numara", anchor = W)
my_tree.column("Adi", anchor=CENTER)
my_tree.column("Soyadi",anchor=CENTER) 
my_tree.column("Telefonu",anchor=CENTER) 

# headings
my_tree.heading("#0", text="LABEL", anchor=W)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Numara", text="Numara", anchor=CENTER)
my_tree.heading("Adi", text="Adi", anchor=CENTER)
my_tree.heading("Soyadi", text="Soyadi", anchor=CENTER)
my_tree.heading("Telefonu", text="Telefonu", anchor=CENTER)

# add data
my_tree.tag_configure('oddrow', background='white')
my_tree.tag_configure('evenrow', background='lightblue')

# add record entry boxes
data_frame = LabelFrame(root, text="Kayıtlar")
data_frame.pack(fill="x", expand="yes", padx=20, side="left")

# labelları ekle

id_label = Label(data_frame, text="id")
id_label.grid(row=0, column=1, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=1, column=1, padx=10, pady=10)

# ogrenci no
ogrenci_no_label = Label(data_frame, text="Öğrenci No")
ogrenci_no_label.grid(row=2, column=1, padx=10, pady=10)
ogrenci_no_entry = Entry(data_frame)
ogrenci_no_entry.grid(row=3, column=1, padx=10, pady=10)

ogrenci_adi_label = Label(data_frame, text="Adi")
ogrenci_adi_label.grid(row=4, column=1, padx=10, pady=10)
ogrenci_adi_entry = Entry(data_frame)
ogrenci_adi_entry.grid(row=5, column=1, padx=10, pady=10)

ogrenci_soyadi_label = Label(data_frame, text="Soyadi")
ogrenci_soyadi_label.grid(row=6, column=1, padx=10, pady=10)
ogrenci_soyadi_entry = Entry(data_frame)
ogrenci_soyadi_entry.grid(row=7, column=1, padx=10, pady=10)

ogrenci_telefonu_label = Label(data_frame, text="Telefonu")
ogrenci_telefonu_label.grid(row=8, column=1, padx=10, pady=10)
ogrenci_telefonu_entry = Entry(data_frame)
ogrenci_telefonu_entry.grid(row=9, column=1, padx=10, pady=10)


# clear entry boxes
def clear_entries():
	id_entry.delete(0, END)
	ogrenci_no_entry.delete(0, END)
	ogrenci_adi_entry.delete(0, END)
	ogrenci_soyadi_entry.delete(0, END)
	ogrenci_telefonu_entry.delete(0, END)



# select records
def select_records(e):
	# clear entry boxes
	id_entry.delete(0, END)
	ogrenci_no_entry.delete(0, END)
	ogrenci_adi_entry.delete(0, END)
	ogrenci_soyadi_entry.delete(0, END)
	ogrenci_telefonu_entry.delete(0, END)

	# grap record nauber
	selected = my_tree.focus()
	# grap value
	values = my_tree.item(selected, "values")

	# output entry boxes
	id_entry.insert(0, values[0]),
	ogrenci_no_entry.insert(0, values[1])
	ogrenci_adi_entry.insert(0, values[2])
	ogrenci_soyadi_entry.insert(0, values[3])
	ogrenci_telefonu_entry.insert(0, values[4])	


def update_record():
	#selected = select_records()
	selected = my_tree.focus()
	print(selected)

	my_tree.item(selected, text="", values=(id_entry.get(), ogrenci_no_entry.get(), ogrenci_adi_entry.get(), ogrenci_soyadi_entry.get(), ogrenci_telefonu_entry.get()))

	conn = sqlite3.connect(db_name)
	c = conn.cursor()

	c.execute("""UPDATE table1 SET
		numara = :no,
		adi = :name,
		soyadi = :surname,
		telefonu = :phone
		WHERE oid = :oid""",
		{
		 'no': ogrenci_no_entry.get(),
		 'name': ogrenci_adi_entry.get(),
		 'surname': ogrenci_soyadi_entry.get(),
		 'phone': ogrenci_telefonu_entry.get(),
		 'oid': id_entry.get(), 
		})
	conn.commit()
	conn.close()
	clear_entries()
	id_entry.delete(0, END)
	ogrenci_no_entry.delete(0, END)
	ogrenci_adi_entry.delete(0, END)
	ogrenci_soyadi_entry.delete(0, END)
	ogrenci_telefonu_entry.delete(0, END)


# add new record
def add_record():
	conn = sqlite3.connect(db_name)
	c = conn.cursor()

	# control entry field
	if len(id_entry.get()) == 0:
		print("boş eleman")

	elif len(id_entry.get()) > 0:

		c.execute("INSERT INTO table1 VALUES (:id, :no, :name, :surname, :phone )",
			{
			'id': id_entry.get(),
			'no': ogrenci_no_entry.get(),
			'name': ogrenci_adi_entry.get(),
			'surname': ogrenci_soyadi_entry.get(),
			'phone': ogrenci_telefonu_entry.get(),
			})
		conn.commit()
		conn.close()

		id_entry.delete(0, END)
		ogrenci_no_entry.delete(0, END)
		ogrenci_adi_entry.delete(0, END)
		ogrenci_soyadi_entry.delete(0, END)
		ogrenci_telefonu_entry.delete(0, END)

		# clear tree view
		my_tree.delete(*my_tree.get_children())
		query_database()

def remove_record():
	# remove from tree
	x = my_tree.selection()[0]
	my_tree.delete(x)

	# remove from database
	conn = sqlite3.connect(db_name)
	c = conn.cursor()
	c.execute("DELETE from table1 WHERE oid=" + id_entry.get())


	conn.commit()
	conn.close()

	clear_entries()


# add buttons
button_frame = LabelFrame(root, text="Buttons")
button_frame.pack(fill='x', expand='yes', padx=20, side="right")

add_button = Button(button_frame, text="Ekle", command=add_record)
add_button.grid(row=0, column=0, padx=10, pady=10)

update_button = Button(button_frame, text="Güncelle", command=update_record)
update_button.grid(row=1, column=0, padx=10, pady=10)

delete_button = Button(button_frame, text="Sil", command=remove_record)
delete_button.grid(row=2, column=0, padx=10, pady=10)


# bind tree
my_tree.bind("<ButtonRelease-1>", select_records)


query_database()
update_record()

root.mainloop()
