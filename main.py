import datetime
import csv
import tkinter as tk

# Define constants
CONFIG_FILE = "./config.cfg"
DATA_FILE = "./data.csv"
AREA_OPTIONS = []
ITEM_OPTIONS = []


# Define a class to represent the GUI form
class TimeCaptureForm:
    def __init__(self):
        # create the main window
        self.current_operator = None
        self.current_area = None
        self.error_message = None
        self.elapsed_time = 0
        self.stop_time = None
        self.start_time = None
        self.elapsed_paused_time = datetime.timedelta()
        self.paused_time = None
        self.paused = None
        self.total_paused_time = datetime.timedelta()
        self.stopped = False
        self.radio_buttons = []
        self.radioButton_selected_option = None
        self.root = tk.Tk()
        self.root.title("Time Capture Form")
        self.root.geometry("400x500")
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

        # timer
        self.timer_label = tk.Label(self.root, text="Elapsed time: 0")
        self.timer_label.place(x=160, y=75)

        # timer buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer, width=7)
        self.start_button.place(x=150, y=100)

        self.stop_button = tk.Button(self.root, text="Finish", command=self.stop_timer, width=7)
        self.stop_button.place(x=215, y=100)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_timer, width=7)
        self.pause_button.place(x=150, y=130)

        self.resume_button = tk.Button(self.root, text="Resume", command=self.resume_timer, width=7)
        self.resume_button.place(x=215, y=130)

        # error message
        self.error_message_text = tk.Label(self.root, text="")
        self.error_message_text.place(x=160, y=160)

        # submit form button and text
        self.submit_form_button = tk.Button(self.root, text="Submit Form", command=self.write_data, width=15)
        self.submit_message_text = tk.Label(self.root, text="Form Submitted")

        # reset button
        self.reset_form_button = tk.Button(self.root, text="Reset Form", command=self.reset_form, width=15)

        # run the main loop
        self.root.mainloop()

    def update_area_label(self, *args):
        # update the area label with the selected option or "select current area" if no option is selected
        selected_option = self.selected_option.get()
        if selected_option:
            self.area_label.config(text="Current area: {}".format(selected_option))
            self.current_area = selected_option
            areaNumber = self.selected_option.get()
            with open(CONFIG_FILE, "r") as areaFile:
                areaReader = csv.reader(areaFile)
                for areaRow in areaReader:
                    if areaNumber in areaRow:
                        try:
                            next_line = next(areaReader)
                            ITEM_OPTIONS.clear()
                            for item in next_line:
                                ITEM_OPTIONS.append(item)
                        except StopIteration:
                            pass
            areaFile.close()
            for button in self.radio_buttons:
                button.destroy()
            self.radio_buttons.clear()
            self.radioButton_selected_option = tk.StringVar(value=ITEM_OPTIONS[0])
            for j, option in enumerate(ITEM_OPTIONS):
                radioButton = tk.Radiobutton(self.root, text=option, variable=self.radioButton_selected_option,
                                             value=option)
                radioButton.place(x=30, y=75 + (j * 20))
                self.radio_buttons.append(radioButton)
        else:
            self.area_label.config(text="Current area: select current area")

    def submit_operator_name(self):
        # update the operator label with the entered name or "None" if no name is entered
        operator_name = self.operator_entry.get()
        if operator_name != "enter name" and operator_name != "" and operator_name != "Enter Name":
            self.operator_label.config(text="Current operator: {}".format(operator_name))
            self.current_operator = operator_name
        else:
            self.operator_label.config(text="Input Current Operator")

    def clear_default_text(self, event):
        if self.operator_entry.get() == 'Enter Name':
            self.operator_entry.delete(0, tk.END)

    def get_radioButton_selected_option(self):
        return self.radioButton_selected_option.get()

    def start_timer(self):
        if self.radioButton_selected_option is not None and self.operator_entry.get() not in ['Enter Name', '', None]:
            if self.start_time is None:
                self.start_time = datetime.datetime.now()
                self.update_timer_label()
                self.area_dropdown.config(state='disabled')
                self.operator_entry.config(state='disabled')
                if self.radio_buttons:
                    for button in self.radio_buttons:
                        button.config(state="disabled")
                self.error_message_text.config(text="")
        else:
            if self.radioButton_selected_option is None:
                self.error_message_text.config(text="Error: Please select an item.")
            if self.operator_entry.get() in ['Enter Name', '', None]:
                self.error_message_text.config(text="Error: Please enter a valid operator name.")

    def stop_timer(self):
        if self.stop_time is None:
            self.stop_time = datetime.datetime.now()
            self.stopped = True

            self.submit_form_button.place(x=250, y=450)

    def pause_timer(self):
        if self.start_time is not None:
            if not self.paused:
                self.paused_time = datetime.datetime.now()
                self.paused = True

    def resume_timer(self):
        if self.start_time is not None:
            if self.paused:
                self.paused = False
                self.total_paused_time = self.total_paused_time + self.elapsed_paused_time

    def update_timer_label(self):
        if not self.stopped:
            if self.start_time is None:
                self.elapsed_time = 0

            if self.paused:
                self.elapsed_paused_time = datetime.datetime.now() - self.paused_time

            self.elapsed_time = (datetime.datetime.now() - self.start_time) - self.total_paused_time
            self.root.after(1000, self.update_timer_label)

            if not self.paused:
                self.timer_label.config(text="Elapsed time: {}".format(str(self.elapsed_time).split(".")[0]))

        elif self.stopped:
            self.timer_label.config(text="Total time: {}".format(str(self.elapsed_time).split(".")[0]))

    def write_data(self):
        with open(DATA_FILE, "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([self.current_operator, self.current_area, self.get_radioButton_selected_option(), str(self.elapsed_time).split(".")[0], str(self.total_paused_time).split(".")[0]])

        csvfile.close()
        self.submit_message_text.place(x=262, y=477)
        self.reset_form_button.place(x=250, y=450)

    def reset_form(self):
        # allow user to interact again
        self.area_dropdown.config(state='normal')
        self.operator_entry.config(state='normal')
        self.selected_option.set("Select")
        for button in self.radio_buttons:
            button.destroy()
        self.radio_buttons.clear()

        # reset time
        self.elapsed_time = 0
        self.paused = None
        self.elapsed_paused_time = datetime.timedelta()
        self.total_paused_time = datetime.timedelta()
        self.error_message = None
        self.stop_time = None
        self.start_time = None
        self.paused_time = None
        self.stopped = False

        # remove buttons and text
        self.submit_form_button.place(x=1000, y=1000)
        self.submit_message_text.place(x=1000, y=1000)
        self.reset_form_button.place(x=1000, y=1000)

        # Update text
        self.timer_label.config(text="Elapsed time: {}".format(str(self.elapsed_time).split(".")[0]))


if __name__ == '__main__':
    with open(CONFIG_FILE, "r") as cfgfile:
        currentValues = cfgfile.readline().split(",")
        current_area = currentValues[0]
        current_operator = currentValues[1]

        reader = csv.reader(cfgfile)
        for i, row in enumerate(reader):
            if i % 2 == 0:
                AREA_OPTIONS.append(str(row[0]))

    cfgfile.close()

    app = TimeCaptureForm()
