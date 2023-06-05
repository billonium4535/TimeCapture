import datetime
import csv
import os.path
import tkinter as tk

# Define constants
CONFIG_FILE = "./config.cfg"
DATA_FILE = None
AREA_OPTIONS = []
ITEM_OPTIONS = []


# Define a class to represent the GUI form
class TimeCaptureForm:
    def __init__(self):
        # create the main window
        # self.data_file = None
        self.first_timer_call = None
        self.current_operator = None
        self.current_area = None
        self.current_wo = ""
        self.current_item = None
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
        self.root.geometry("600x600")
        self.root.option_add("*font", "Arial 12")
        self.root.resizable(False, False)
        self.state = None

        line = 10

        # create a label for current area
        self.area_label = tk.Label(self.root, text="Area")
        self.area_label.place(x=30, y=line)

        # create a label for current operator
        self.operator_label = tk.Label(self.root, text="Operator")
        self.operator_label.place(x=325, y=line)

        line = line + 30

        # create an input box for operator name
        self.operator_entry = tk.Entry(self.root, width=20, justify='center', font='Arial 12')
        self.operator_entry.insert(0, current_operator)
        # bind the <FocusIn> event
        self.operator_entry.bind("<FocusIn>", self.clear_default_text)
        self.operator_entry.place(x=325, y=line)

        # create a button to saveoperator name
        self.save_button = tk.Button(self.root, text="Save", command=self.save_operator_name)
        self.save_button.place(x=530, y=line)

        line = 75
        # create a label for works order
        self.wo_label = tk.Label(self.root, text="Works Order")
        self.wo_label.place(x=325, y=line)

        line = line + 24
        # create an input box for works order
        current_wo = self.current_wo
        self.wo_entry = tk.Entry(self.root, width=20, justify='center')
        self.wo_entry.insert(0, current_wo)
        # bind the <FocusIn> event
        self.wo_entry.bind("<FocusIn>", self.clear_default_text)
        self.wo_entry.place(x=325, y=line)

        # create a StringVar to store the selected option
        self.selected_option = tk.StringVar(self.root)
        # set the initial value of the dropdown box
        self.selected_option.set(current_area)

        # create the dropdown box
        self.area_dropdown = tk.OptionMenu(self.root, self.selected_option, *AREA_OPTIONS)
        self.area_dropdown.place(x=45, y=30)
        # bind the dropdown box to a function that updates the label text
        self.selected_option.trace("w", self.update_area_label)
        self.update_area_label()

        line = 200
        # timer
        self.timer_label = tk.Label(self.root, text="")
        self.timer_label.place(x=375, y=line - 10)

        line = line + 25
        # timer buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer, width=7)
        self.start_button.place(x=375, y=line)

        self.stop_button = tk.Button(self.root, text="Finish", command=self.stop_timer, width=7)
        self.stop_button.place(x=490, y=line)

        line = line + 50
        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_timer, width=7)
        self.pause_button.place(x=375, y=line)

        self.resume_button = tk.Button(self.root, text="Resume", command=self.resume_timer, width=7)
        self.resume_button.place(x=490, y=line)

        line = line + 30
        self.ptimer_label = tk.Label(self.root, text="")
        self.ptimer_label.place(x=375, y=line + 10)

        # error message
        self.error_message_text = tk.Label(self.root, text="", anchor="e")
        self.error_message_text.place(x=310, y=560)

        # set the intial state
        self.set_state_idle()

        # run the main loop
        self.root.mainloop()

    def disable_radio_buttons(self):
        if self.radio_buttons:
            for button in self.radio_buttons:
                button.config(state="disabled")

    def enable_radio_buttons(self):
        if self.radio_buttons:
            for button in self.radio_buttons:
                button.config(state="normal")

    def set_state_idle(self):
        # idle - can enter information or start
        # disable controls
        self.stop_button.config(state='disabled')
        self.pause_button.config(state='disabled')
        self.resume_button.config(state='disabled')

        # enable controls
        self.start_button.config(state='normal')
        self.operator_entry.config(state='normal')
        self.wo_entry.config(state='normal')
        self.area_dropdown.config(state='normal')
        self.enable_radio_buttons()
        self.save_button.config(state='normal')

        # set the state
        self.state = "Idle"

    def set_state_started(self):
        # started - timer is running
        # disable controls
        self.start_button.config(state='disabled')
        self.resume_button.config(state='disabled')
        self.operator_entry.config(state='disabled')
        self.wo_entry.config(state='disabled')
        self.area_dropdown.config(state='disabled')
        self.disable_radio_buttons()
        self.save_button.config(state='disabled')

        # enable controls
        self.stop_button.config(state='normal')
        self.pause_button.config(state='normal')

        # set the state
        self.state = "Started"

    def update_area_label(self, *args):
        # display items according to area selected
        selected_option = self.selected_option.get()
        if selected_option:
            self.current_area = selected_option
            areanumber = self.selected_option.get()
            with open(CONFIG_FILE, "r") as areaFile:
                areareader = csv.reader(areaFile)
                for arearow in areareader:
                    if areanumber in arearow:
                        try:
                            next_line = next(areareader)
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
                radiobutton = tk.Radiobutton(self.root, text=option, variable=self.radioButton_selected_option,
                                             value=option)
                radiobutton.place(x=30, y=75 + (j * 25))
                self.radio_buttons.append(radiobutton)

    def save_operator_name(self):
        # save the operator name to the config file
        operator_name = self.operator_entry.get()
        if operator_name != "":
            # save to file - have to read then write
            # read all lines from the config file
            with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
                data = file.readlines()
            file.close()

            # replace the first line with the new operator name
            config_line = "file " + DATA_FILE + ",area " + self.current_area + ",op " + operator_name + ",\n"
            data[0] = config_line

            # write all lines to the config file
            with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
                file.writelines(data)
            file.close()

    def clear_default_text(self, event):
        if self.operator_entry.get() == 'Enter Name':
            self.operator_entry.delete(0, tk.END)

    def selected_item(self):
        return self.radioButton_selected_option.get()

    def start_timer(self):
        # start button pressed - validate we can start the timer
        an_error = False
        self.error_message_text.config(text="")
        if self.radioButton_selected_option is None:
            self.error_message_text.config(text="Error: Please select an item.")
            an_error = True
        if not (self.wo_entry.get().isnumeric()) or len(self.wo_entry.get()) != 5:
            self.error_message_text.config(text="Error: WO needs to be 5 digit numeric")
            an_error = True
        if self.operator_entry.get() in ['Enter Name', '', None]:
            self.error_message_text.config(text="Error: Please enter a valid operator name.")
            an_error = True

        if not an_error:
            # okay to start the timer
            self.start_time = datetime.datetime.now()

            # move to the started state
            self.set_state_started()
            self.first_timer_call = True
            self.update_timer_label()

    def stop_timer(self):
        # stop button pressed - store data to file
        if self.paused:
            self.paused = False
            self.total_paused_time = self.total_paused_time + self.elapsed_paused_time

        self.stop_time = datetime.datetime.now()
        the_date = datetime.date.today()
        with open(DATA_FILE, "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(
                [self.wo_entry.get(), self.operator_entry.get(), self.current_area, self.selected_item(),the_date,
                 str(self.elapsed_time).split(".")[0], str(self.total_paused_time).split(".")[0]])
            csvfile.close()

        self.elapsed_time = 0
        self.start_time = None
        self.total_paused_time = 0

        # move back to the idle state
        self.set_state_idle()

    def pause_timer(self):
        if self.state == "Started":
            if not self.paused:
                self.paused_time = datetime.datetime.now()
                self.paused = True
                self.pause_button.config(state='disabled')
                self.resume_button.config(state='normal')

    def resume_timer(self):
        if self.state == "Started":
            if self.paused:
                self.paused = False
                self.total_paused_time = self.total_paused_time + self.elapsed_paused_time
                self.pause_button.config(state='normal')
                self.resume_button.config(state='disabled')

    def update_timer_label(self):
        # update timers if running
        if self.state == "Started":
            if self.first_timer_call:
                self.first_timer_call = False
                self.start_time = datetime.datetime.now()
                self.elapsed_time = 0
                self.total_paused_time = datetime.timedelta()
                self.elapsed_paused_time = 0

            # update paused time if paused
            if self.paused:
                self.elapsed_paused_time = datetime.datetime.now() - self.paused_time
                self.ptimer_label.config(text=" Paused time: {}".format(
                    str(self.total_paused_time + self.elapsed_paused_time).split(".")[0]))

            else:
                # update elapsed time but remove paused time element
                self.elapsed_time = (datetime.datetime.now() - self.start_time) - self.total_paused_time
                self.timer_label.config(text="Elapsed time: {}".format(str(self.elapsed_time).split(".")[0]))

            # update again in 1 second
            self.root.after(1000, self.update_timer_label)

        else:
            # do nothing if timer not running
            self.timer_label.config(text="")
            self.ptimer_label.config(text="")


def close_box(root):
    root.destroy()


def error_message(error):
    root = tk.Tk()
    root.geometry("250x150")
    root.title("Error")

    label = tk.Label(root, text="Error: " + error, width=250, height=150)
    label.place(relx=0.5, rely=0.5, anchor="center")

    close_button = tk.Button(root, text="Close", command=lambda: close_box(root), width=10, height=1)
    close_button.place(relx=0.5, rely=0.9, anchor="center")

    #auto-py-to-exe allows icon to be set for program but can't replace feather in window or windows taskbar
    #this line doesn't seem to have any effect
    root.iconbitmap(r"Tioga_icons.ico")

    root.mainloop()


if __name__ == '__main__':
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as cfgfile:
            currentValues = cfgfile.readline().split(",")
            string = currentValues[0]
            DATA_FILE = string[5:]
            if os.path.exists(DATA_FILE):
                string = currentValues[1]
                current_area = string[5:]
                string = currentValues[2]
                current_operator = string[3:]

                reader = csv.reader(cfgfile)
                for i, row in enumerate(reader):
                    if i % 2 == 0:
                        AREA_OPTIONS.append(str(row[0]))

                cfgfile.close()

                app = TimeCaptureForm()
            else:
                error_message("Can't access data.csv")
    else:
        error_message("Can't access config.cfg")
