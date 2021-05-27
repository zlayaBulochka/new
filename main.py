import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):

        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.edit_img = tk.PhotoImage(file='edit.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.edit_img,
                                    compound=tk.TOP, command=self.open_edit_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.png')
        btn_delete = tk.Button(toolbar, text='Удалить', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.png')
        btn_update = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.update_img,
                                compound=tk.TOP, command=self.view_records)
        btn_update.pack(side=tk.LEFT)

        self.tab_control = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Иностранные граждане')
        self.tree = ttk.Treeview(self, columns=(
        'ID', 'surname', 'nam', 'patronymic', 'citizenship', 'date_of_birth', 'place_of_birth', 'sex', 'profession',
        'phone'), height=15, show='headings')

        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('surname', width=180, anchor=tk.CENTER)
        self.tree.column('nam', width=150, anchor=tk.CENTER)
        self.tree.column('patronymic', width=120, anchor=tk.CENTER)
        self.tree.column('citizenship', width=160, anchor=tk.CENTER)
        self.tree.column('date_of_birth', width=100, anchor=tk.CENTER)
        self.tree.column('place_of_birth', width=170, anchor=tk.CENTER)
        self.tree.column('sex', width=30, anchor=tk.CENTER)
        self.tree.column('profession', width=150, anchor=tk.CENTER)
        self.tree.column('phone', width=110, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('surname', text='Фамилия')
        self.tree.heading('nam', text='Имя')
        self.tree.heading('patronymic', text='Отчество')
        self.tree.heading('citizenship', text='Гражданство')
        self.tree.heading('date_of_birth', text='Дата рождения')
        self.tree.heading('place_of_birth', text='Место рождения')
        self.tree.heading('sex', text='Пол')
        self.tree.heading('profession', text='Профессия')
        self.tree.heading('phone', text='Телефон')

        self.tree.pack()
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab2, text='Визы')
        lbl2 = tk.Label(self.tab2, text='Вкладка 2')
        lbl2.grid(column=0, row=0)
        self.tab_control.pack(expand=1, fill='both')

    def records(self, surname, nam, patronymic, citizenship, date_of_birth, place_of_birth, sex, profession, phone):
        self.db.insert_data(surname,  nam, patronymic, citizenship, date_of_birth, place_of_birth, sex, profession, phone)
        self.view_records()

    def edit_record(self, surname, nam,  patronymic, citizenship, date_of_birth, place_of_birth, sex, profession, phone):
        self.db.c.execute('''UPDATE fin SET surname=?, nam=?, patronymic=?, citizenship=?, date_of_birth=?, place_of_birth=?, sex=?, profession=?, phone=? WHERE ID=?''',
                          (surname, nam, patronymic, citizenship, date_of_birth, place_of_birth, sex, profession, phone, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM fin''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM fin WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, surname):
        surname = ('%' + surname + '%',)
        self.db.c.execute('''SELECT * FROM fin WHERE surname LIKE ? ''', surname)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_edit_dialog(self):
        Edit()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x400+400+300')
        self.resizable(False, False)

        label_surname = tk.Label(self, text='Фамилия:')
        label_surname.place(x=50, y=50)
        label_nam = tk.Label(self, text='Имя:')
        label_nam.place(x=50, y=80)
        label_patr = tk.Label(self, text='Отчество:')
        label_patr.place(x=50, y=110)
        label_select = tk.Label(self, text='Гражданство:')
        label_select.place(x=50, y=140)
        label_dofb = tk.Label(self, text='Дата рождения:')
        label_dofb.place(x=50, y=170)
        label_pofb = tk.Label(self, text='Место рождения')
        label_pofb.place(x=50, y=200)
        label_sex = tk.Label(self, text='Пол')
        label_sex.place(x=50, y = 230)
        label_prof = tk.Label(self, text='Профессия')
        label_prof.place(x=50, y=260)
        label_phone = tk.Label(self, text='Телефон')
        label_phone.place(x=50, y=290)


        self.entry_surname = ttk.Entry(self)
        self.entry_surname.place(x=200, y=50)

        self.entry_nam = ttk.Entry(self)
        self.entry_nam.place(x=200, y=80)

        self.entry_patr = ttk.Entry(self)
        self.entry_patr.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=['Австралия', 'Великобритания', 'Германия'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=140)

        self.entry_dofb = ttk.Entry(self)
        self.entry_dofb.place(x=200, y=170)

        self.entry_pofb = ttk.Entry(self)
        self.entry_pofb.place(x=200, y=200, width=180) #ширина окна ввода текста Entry

        self.entry_sex = ttk.Entry(self)
        self.entry_sex.place(x=200, y=230)

        self.entry_prof = ttk.Entry(self)
        self.entry_prof.place(x=200, y=260)

        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y =290)


        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=350)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=350)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_surname.get(),
                                                                       self.entry_nam.get(),
                                                                       self.entry_patr.get(),
                                                                       self.combobox.get(),
                                                                       self.entry_dofb.get(),
                                                                       self.entry_pofb.get(),
                                                                       self.entry_sex.get(),
                                                                       self.entry_prof.get(),
                                                                       self.entry_phone.get()))

        self.grab_set()
        self.focus_set()


class Edit(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=350)
        btn_edit.bind('<Button-1>', lambda event: self.view.edit_record(self.entry_surname.get(),
                                                                          self.entry_nam.get(),
                                                                          self.entry_patr.get(),
                                                                          self.combobox.get(),
                                                                          self.entry_dofb.get(),
                                                                          self.entry_pofb.get(),
                                                                          self.entry_sex.get(),
                                                                          self.entry_prof.get(),
                                                                          self.entry_phone.get()))

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM fin WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),)) #где[0] - это первый элемент кортежа возвращаемого методом select, а #1- это номер столбца в таблице по порядку, тобишь номер столбца содержащего айдишник
        row = self.db.c.fetchone() #возвращает кортеж значений с нужным ID, причем в питоне номер элемента начинается с 0.
        self.entry_surname.insert(0, row[1]) #вставляем в соответствующее текстовое поле 2ой элемент кортежа тобишь с индексом [1], тобишь на самрм деле это значение 1го столбца
        self.entry_nam.insert(0, row[2])  #по аналогии с предыдущей строкой берем третье значение кортежа, НО ДЛЯ ЭТОГО НУЖНО ВЕЗДЕ NAME ДОБАВИТЬ И ОПЕРАЦИИ С НИМ
        self.entry_patr.insert(0, row[3])
        if row[4] == 'Австралия' :   #сравниваем 4е значение из кортежа тобишь с индексом [3] со словом "Германия"
            self.combobox.current(0) #из 124 строки видим что в Combobox содержится 2 значения, соответственно под индексом (0)- Германия, что является первым значением, а под индексом (1) - второе значение, тобишь Великобритания. Если в полученном кортеже не Германия, то автоматически ставится Великобритания.
        if row[4] == 'Германия':
            self.combobox.current(2)
        if row[4] == 'Великобритания':
            self.combobox.current(1)
        self.entry_dofb.insert(0, row[5])
        self.entry_pofb.insert(0, row[6])
        self.entry_sex.insert(0, row[7])
        self.entry_prof.insert(0, row[8])
        self.entry_phone.insert(0, row[9])



class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('migreg.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS fin (id integer primary key, surname varchar, nam varchar,  patronymic varchar, citizenship varchar, date_of_birth date, place_of_birth varchar, sex varchar, profession varchar, phone integer) ''')
        self.conn.commit()

    def insert_data(self, surname, nam, patronymic, citizenship, date_of_birth, place_of_birth, sex, profession, phone):
        self.c.execute('''INSERT INTO fin(surname, nam, patronymic, citizenship, date_of_birth, place_of_birth, sex, profession, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (surname, nam, patronymic, citizenship, date_of_birth, place_of_birth, sex, profession, phone))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Миграционный учет")
    root.geometry("1210x600+100+200")
    root.resizable(False, False)

    root.mainloop()


