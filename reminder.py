import os
from tkinter import *
from datetime import datetime
from tkinter.ttk import Combobox, Treeview, Style
from gtts import gTTS
from playsound import playsound
import messagebox
import json


class Reminder:

    def __init__(self, window):

        # GUI elements
        self.window = window
        self.window.title('Reminder')
        self.window.resizable(False, False)
        self.window.geometry("+1500+30")
        self.window.config(bg="#8FB9A8")
        self.style = Style(self.window)

        self.set_reminder_button = Button(self.window,
                                          text='Setare memento',
                                          command=self.set_reminder_data,
                                          highlightthickness=0,
                                          bg="#2d807a",
                                          fg="white",
                                          font=('Arial', 12, 'bold'))
        self.set_reminder_button.grid(column=0, row=5, columnspan=3, padx=10, pady=10)

        self.delete_reminder_button = Button(self.window,
                                             text='Sterge memento',
                                             command=self.delete_selected_reminder,
                                             highlightthickness=0,
                                             bg="#CC2A49",
                                             fg="white",
                                             font=('Arial', 12, 'bold'))
        self.delete_reminder_button.grid(column=0, row=7, columnspan=3, padx=10, pady=10)

        self.reminder_text = Entry(self.window,
                                   width=40,
                                   font=('Italic', 15), fg="grey")

        self.reminder_text.insert(0, "Introduceti memento aici...")
        self.reminder_text.bind("<FocusIn>", self.clear_reminder_input)
        self.reminder_text.grid(column=0, row=4, columnspan=3, padx=10, pady=10)

        # time data
        self.hours = tuple("0" + str(hour) for hour in range(0, 10) if hour < 10) + tuple(
            str(hour) for hour in range(10, 24))

        self.minutes = tuple("0" + str(minute) for minute in range(0, 10) if minute < 10) + tuple(
            str(minute) for minute in range(10, 60))

        self.months = ("Ianuarie", "Februarie", "Martie", "Aprilie", "Mai", "Iunie",
                       "Iulie", "August", "Septembrie", "Octombrie", "Noiembrie", "Decembrie")
        self.years = tuple(str(year) for year in range(2023, 2034))

        self.days = tuple(str(day) for day in range(1, 32))

        self.clock()
        self.select_hour_dropdown()
        self.select_minute_dropdown()
        self.select_day_dropdown()
        self.select_month_dropdown()
        self.select_years_dropdown()
        self.table()

    def select_hour_dropdown(self):
        global hours_menu, hours_dropdown, current_hour_value
        hours_menu = StringVar()
        current_hour_value = hour_now.split(':')[0]
        hours_menu.set(current_hour_value)
        hours_dropdown = Combobox(self.window, textvariable=hours_menu, values=self.hours, width=3)
        hours_dropdown.grid(column=0, row=1, pady=5, columnspan=2)
        set_time_label = Label(self.window, text="Selectati ora:", bg="#8FB9A8", fg="#2d807a",
                               font=('Arial', 12, 'bold'))
        set_time_label.place(x=28, y=198)

    def select_minute_dropdown(self):
        global minutes_menu, minutes_dropdown, current_minute_value
        minutes_menu = StringVar()
        current_minute_value = hour_now.split(':')[1]
        minutes_menu.set(current_minute_value)
        minutes_dropdown = Combobox(self.window, textvariable=minutes_menu, values=self.minutes, width=3)
        minutes_dropdown.grid(column=0, row=2, pady=5, columnspan=2)

    def select_day_dropdown(self):
        global days_menu, days_dropdown
        days_menu = StringVar()
        current_day = date_in_romanian.split()[0]
        days_menu.set(current_day)
        days_dropdown = Combobox(self.window, textvariable=days_menu, values=self.days, width=3)
        days_dropdown.grid(column=2, row=1, pady=5, )
        set_date_label = Label(self.window, text="Selectati data:", bg="#8FB9A8", fg="#2d807a",
                               font=('Arial', 12, 'bold'))
        set_date_label.place(x=300, y=218)

    def select_month_dropdown(self):
        global months_menu, months_dropdown
        months_menu = StringVar()
        current_month = date_in_romanian.split()[1]
        months_menu.set(current_month)
        months_dropdown = Combobox(self.window, textvariable=months_menu, values=self.months, width=8)
        months_dropdown.grid(column=2, row=2, pady=5, )

    def select_years_dropdown(self):
        global years_menu, years_dropdown
        years_menu = StringVar()
        current_year = date_in_romanian.split()[2]
        years_menu.set(current_year)
        years_dropdown = Combobox(self.window, textvariable=years_menu, values=self.years, width=5)
        years_dropdown.grid(column=2, row=3, pady=5, )

    def clear_reminder_input(self, _event):
        if self.reminder_text.get():
            self.reminder_text.delete(0, END)

    def clock(self):
        global hour_now, date_in_romanian
        # set a label to show current hour and date
        hour_and_date_label = Label(self.window,
                                    font=('Modern', 50, 'bold'),
                                    bg="#8FB9A8",
                                    padx=10,
                                    pady=10,
                                    fg="#2d807a")
        hour_and_date_label.grid(column=0, row=0, columnspan=3)
        # define a list with months names in romanian

        # get current hour
        hour_now = datetime.now().strftime("%H:%M:%S")
        # get current date in romanian format
        current_month_number = int(datetime.today().strftime("%m"))
        current_month_name = ''
        for _ in range(len(self.months)):
            current_month_name = self.months[current_month_number - 1]
        date_in_romanian = datetime.today().strftime(f"%d {current_month_name} %Y")
        # set label data
        hour_and_date_label.config(text=f'{hour_now}\n{date_in_romanian}')
        # set clock to update to 1 second
        hour_and_date_label.after(1000, self.clock)
        # reminder update to 1 seconds
        self.window.after(1000, self.execute_reminder)

    def set_reminder_data(self):
        global hours_dropdown, minutes_dropdown, days_dropdown, months_dropdown, years_dropdown
        # set hour and minute for reminder

        set_hour = f'{hours_dropdown.get()}:{minutes_dropdown.get()}'
        set_date = f'{days_dropdown.get()} {months_dropdown.get()} {years_dropdown.get()}'
        # define data to be saved in a json file
        new_data = {
            self.reminder_text.get(): {
                "date": set_date,
                "hour": set_hour,

            }
        }
        try:
            with open("data.json", "r") as file:
                # Reading old data
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(new_data, file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            self.reminder_text.delete(0, END)
            self.reminder_text.insert(0, "Introduceti memento aici...")
            hours_menu.set(f"{current_hour_value}")
            minutes_menu.set(f"{current_minute_value}")
            messagebox.showinfo(title="New reminder",
                                message="Un reminder nou a fost setat")
            self.window.after(1000, self.table)

    def execute_reminder(self):
        global hour_now, selected_data
        with open("data.json", "r") as file:
            # Reading data
            data = json.load(file)
        for remind in data.copy().items():
            if remind[1]["date"] == date_in_romanian:
                if remind[1]["hour"] == hour_now[0:5] and hour_now[6:] == "00":
                    self.voice_message(text=remind[0])
                    messagebox.showinfo("Reminder", f"{remind[0]}")
                    self.delete_reminder_after_run(reminder=remind[0], data=data)

    @staticmethod
    def voice_message(text):
        if text.strip():
            tts = gTTS(text=text, lang='ro', slow=False)
            tts.save("response.mp3")
            playsound("response.mp3")
            os.remove("response.mp3")

        else:
            print("Error: No text to speak")

    def table(self):
        # Create a Treeview widget
        global tree
        tree = Treeview(self.window)
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#8FB9A8",
                             fieldbackground="#8FB9A8", foreground="black", font=('Modern', 10, 'bold'))
        tree["height"] = 10
        scrollbar = Scrollbar(self.window, orient="vertical", command=tree.yview)
        # Configure the Treeview to use the scrollbar
        tree.configure(yscrollcommand=scrollbar.set)

        table_items = ("Memento", "Data", "Ora")

        # Define columns
        tree["columns"] = table_items

        # Format columns
        tree.column("#0", width=0, stretch=NO)
        tree.heading("#0", text="", anchor=W)
        for item in table_items:
            tree.column(item, anchor=CENTER, width=200)
            tree.heading(item, text=item, anchor=CENTER)

        # Insert data
        with open("data.json") as file:
            data = json.load(file)
            for remind in data.items():
                text = remind[0]
                date = remind[1]["date"]
                hour = remind[1]["hour"]
                tree.insert(parent="", index="end", values=(text, date, hour))

        # Pack the Treeview widget
        tree.grid(row=6, columnspan=3)
        scrollbar.grid(row=6, column=3, sticky="ns", )
        tree.bind("<<TreeviewSelect>>", self.select_reminder_from_table)

    @staticmethod
    def select_reminder_from_table(_event):
        global selected_data
        selected_item = tree.focus()
        if selected_item:
            selected_data = tree.item(selected_item, "values")
        else:
            with open("data.json", "r") as file:
                # Reading data
                data = json.load(file)
                last_reminder = data.popitem()
                last_reminder_text = last_reminder[0]
                selected_data = last_reminder_text

    def delete_selected_reminder(self):
        global selected_data
        with open("data.json", "r") as file:
            # Reading data
            data = json.load(file)
            for remind in data.copy():
                # used .copy() method to avoid to modify the size of a
                # dictionary during iteration and raise a RuntimeError
                if remind == selected_data[0]:
                    del data[remind]
                    with open("data.json", 'w') as new_file:
                        json.dump(data, new_file, indent=4)
                        self.window.after(1000, self.table)
                    messagebox.showinfo("", "Memento selectat a fost sters")

    def delete_reminder_after_run(self, reminder, data):
        del data[reminder]
        with open("data.json", 'w') as new_file:
            json.dump(data, new_file, indent=4)
            self.window.after(1000, self.table)
        messagebox.showinfo("", "Memento  va fi sters automat")


root = Tk()
app = Reminder(root)
root.mainloop()
