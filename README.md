# TimeCapture
This program is a simple graphical user interface (GUI) designed to capture and track the time employees spend working on different tasks for the Tioga LTD company. The program allows employees to input their name and the area they are working in, as well as track the amount of time they spend on a particular task.

### To Do:
1. Add Tioga logo as icon
2. Read and write `config.cfg` and `data.csv` from an external server
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
- `config.cfg` file with the area names and items for each area.
- `data.csv` file to store the captured data.

### How to use _**(Not needed if running the .exe)**_
1. Clone the repository.
2. Make sure you have the required prerequisites installed.
3. Set up the `config.cfg` file with the appropriate areas and items.
4. Run the main.py file.
5. Enter the employee name and select the area from the dropdown box.
6. Start the timer and pause, resume, or stop it as needed.
7. Once the form is completed, click the "Submit Form" button to save the data to the `data.csv` file.
8. Click the "Reset Form" button to clear the form and start over.

### How to use if running the .exe
1. Download the latest release
2. Extract the files
3. Make sure you have the `config.cfg` and `data.csv` files in the same folder as the .exe
4. Run the .exe

### How to compile into a .exe
1. Make sure that you have auto-py-to-exe installed on your computer. If you don't, you can install it using pip by running the following command in your terminal:
```batch
pip install auto-py-to-exe
```
2. Open auto-py-to-exe by typing the following command into your terminal:
```batch
auto-py-to-exe
```
3. The auto-py-to-exe GUI will open. 
   1. Click the "Browse" button next to the "Script Location" field.
   2. Select the main.py file.
   3. Click the "One file" option under "Output Type".
   4. Click the "Browse" button next to the "Output File" field and select a location to save the compiled .exe file.
   5. Click on the "Additional Files" section and add the `config.cfg` and `data.csv` files.
   6. Click the "Convert .py to .exe" button at the bottom of the GUI.
7. The .exe will be created in the folder you specified in step 3.iv.

### Notes
- The `config.cfg` and `data.csv` files should be in the same directory as the `main.py` file.
- The `config.cfg` file should be formatted as follows:
```cfg
Area1
Item1,Item2,Item3...
Area2
Item1,Item2,Item3...
```
- The areas can't have the same name but the items can
- The `data.csv` file should be formatted as follows:
```csv
current_operator,current_area,item,total_time,paused_time
```
- The program saves the operator's name, the area, item, time and time paused.
