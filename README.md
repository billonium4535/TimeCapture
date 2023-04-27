# TimeCapture
This program is a simple graphical user interface (GUI) designed to capture and track the time employees spend working on different tasks for the Tioga LTD company. The program allows employees to input their name and the area they are working in, as well as track the amount of time they spend on a particular task.

### To Do:
1. Add Tioga logo as icon
2. Read and write `config.cfg` and `data.cfg` from an external server
3. Full error check/bug fix

### Features
- Input the name of the employee and the area they are working in.
- Start, stop, pause, and resume a timer to track the amount of time an employee spends on a particular task.
- Display the elapsed time for the task.
- Display a list of items for the selected area.
- Submit the completed form, which writes the entered data to a CSV file.
- Reset the form to its initial state.

### Prerequisites
- Python 3 _**(Not needed if running the .exe)**_
- tkinter module _**(Not needed if running the .exe)**_
- config.cfg file with the area names and items for each area.
- data.csv file to store the captured data.

### How to use _**(Not needed if running the .exe)**_
1. Clone the repository.
2. Make sure you have the required prerequisites installed.
3. Set up the config.cfg file with the appropriate areas and items.
4. Run the main.py file.
5. Enter the employee name and select the area from the dropdown box.
6. Start the timer and pause, resume, or stop it as needed.
7. Once the form is completed, click the "Submit Form" button to save the data to the data.csv file.
8. Click the "Reset Form" button to clear the form and start over.

### How to use if running the .exe
1. Download the latest release
2. Extract the files
3. Make sure you have the config.cfg and data.csv files in the same folder as the .exe
4. Run the .exe

### Notes
- The config.cfg and data.csv files should be in the same directory as the main.py file.
- The config.cfg file should be formatted as follows:
```cfg
Area1
Item1,Item2,Item3...
Area2
Item1,Item2,Item3...
```
- The areas can't have the same name but the items can
- The data.csv file should be formatted as follows:
```csv
current_operator,current_area,item,total_time,paused_time
```
- The program saves the operator's name, the area, item, time and time paused.
