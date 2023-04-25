import datetime
import csv
import tkinter as tk
from tkinter import ttk

# Define constants
CONFIG_FILE = "./config.cfg"
DATA_FILE = "./data.csv"
AREA_OPTIONS = []


# Define a class to represent the GUI form
class TimeCaptureForm:
    def __init__(self):
        # create the main window
        self.root = tk.Tk()
        self.root.title("Time Capture Form")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # create a label for current area
        self.area_label = tk.Label(self.root, text="Select Current Area")
        self.area_label.place(x=30, y=10)

        # create a label for current operator
        self.operator_label = tk.Label(self.root, text="Input Current Operator")
        self.operator_label.place(x=170, y=10)

        # create an input box for operator name
        self.operator_entry = tk.Entry(self.root, width=20, justify='center')
        self.operator_entry.insert(0, 'Enter Name')
        # bind the <FocusIn> event
        self.operator_entry.bind("<FocusIn>", self.clear_default_text)
        self.operator_entry.bind("<FocusOut>", self.remove_entry_focus)
        self.operator_entry.place(x=175, y=34)

        # create a button to submit operator name
        self.submit_button = tk.Button(self.root, text="Submit Name", command=self.submit_operator_name)
        self.submit_button.place(x=310, y=30)

        # create a StringVar to store the selected option
        self.selected_option = tk.StringVar(self.root)
        # set the initial value of the dropdown box
        self.selected_option.set("Select")
        # create the dropdown box
        self.area_dropdown = tk.OptionMenu(self.root, self.selected_option, *AREA_OPTIONS)
        self.area_dropdown.place(x=45, y=30)
        # bind the dropdown box to a function that updates the label text
        self.selected_option.trace("w", self.update_area_label)

        # run the main loop
        self.root.mainloop()

    def update_area_label(self, *args):
        # update the area label with the selected option or "select current area" if no option is selected
        selected_option = self.selected_option.get()
        if selected_option:
            self.area_label.config(text="Current area: {}".format(selected_option))
        else:
            self.area_label.config(text="Current area: select current area")

    def submit_operator_name(self):
        # update the operator label with the entered name or "None" if no name is entered
        operator_name = self.operator_entry.get()
        print(operator_name)
        if operator_name != "enter name" and operator_name != "" and operator_name != "Enter Name":
            self.operator_label.config(text="Current operator: {}".format(operator_name))
        else:
            self.operator_label.config(text="Input Current Operator")

    def clear_default_text(self, event):
        if self.operator_entry.get() == 'Enter Name':
            self.operator_entry.delete(0, tk.END)
            print("deleted")

    def remove_entry_focus(self, event):
        print("off")
        self.operator_entry.selection_clear()


if __name__ == '__main__':
    with open(CONFIG_FILE, "r") as csvfile:
        currentValues = csvfile.readline().split(",")
        current_area = currentValues[0]
        current_operator = currentValues[1]

        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if i % 2 == 0:
                AREA_OPTIONS.append(str(row[0]))

        print("area: {} operator: {}".format(current_area, current_operator))
        print("Areas: {}".format(AREA_OPTIONS))

    app = TimeCaptureForm()
