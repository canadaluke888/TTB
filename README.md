# 💾 Terminal Table Builder 💾

A terminal-based application that allows you to easily build and edit tabular data.

Easily view and edit tables in databases from the terminal.

## Connecting To A Database
![Connecting to a database](screenshots/TerminalTableBuilderDatabaseSetup.png)


## Searching Data
![Searching Data](screenshots/TerminalTableBuilderDatabaseSearchSS.png)


## Adding Data To A Table
![Adding data to a table](screenshots/TerminalTableBuilderAddDataSS.png)


## Prerequisites
- Python 3.9+

## Setup
1. **Clone the repository:** `git clone https://github.com/canadaluke888/TerminalTableBuilder.git`
2. **Set up virtual environment:** For Linux and Mac OS, `python3 -m venv .venv`. For Windows, `python -m venv .venv`
3. **Activate virtual environment:** For Linux and Mac OS, `soruce .venv/bin/activate`. For Windows, `.venv/Scripts/Activate`
4. **Install requirements:** `pip install -r requirements.txt`

## Usage


- **Starting the application:** For Linux and Max OS, `python3 main.py`. For Windows, `python main.py`.

## Database
- **Creating a new database:** In the main menu, enter the `database` command. Enter the `create database` command and then name the new database. Your database will automatically be selected as the working database.
- **Deleting a database:** Enter the `delete database` command and then select the database that you want to delete from the list.
- **Selecting an existing database:** Enter the `select database` command and then choose from the list of available databases.
- **Viewing the list of available databases:** Enter the `list databases` command.
- **Closing an active database:** Enter the `close database` command.
- **Viewing the current database:** Enter the `current database` command.
- **Serching the database:** Enter the `search` command and then enter a serch query. It will return information on the location if a match is found.

### Table Builder
- **Building a new table:** In the main menu, enter the `table builder` command. Enter a name for the table. From here you can add data to the table. Remember that the first column added is going to be the heading row each row.
- **Adding a column:** Enter the `add column` command. Enter the name for the column. Specify the data type for the column.
- **Changing the data type for a column:** Enter the `change type` command. Enter the number corresponding to the column that you want to change the data type for. Enter the number corresponding to the data type that you want to change the column to.
- **Adding a row:** Enter the `add row` command and the program will walk through each heading allowing you to enter data for each cell. Be sure to enter the correct data type that you specified for the column.
- **Removing a column:** Enter the `remove column` command. Enter the column name.
- **Removing a row:** Enter the `remove row` command. Enter the row index.
- **Editing a cell:** Enter the `edit cell` command. Enter the index for the cell that is dislpayed on the screen. For example, if you wanted to edit the second row of the second column, you would enter '2,2'. After entering the index for the cell, you can then enter the new information that you want in the cell.
- **Printing the table:** Enter the `print table` command.
- **Loading data from a CSV file:** Enter the `load csv` command. Enter the path to the CSV file.
- **Loading more than one CSV file:** Enter the `load csv batch` command. Enter the path to the directory that contains the CSV files. Specifiy if you want to add the CSV files in the subdirectories.
- **Saving data to a CSV file:** Enter the `save csv` command. You will be prompted on if you want to use the name of the table as the name of the CSV file. The CSV file will appear in the root directory of the app.
- **Saving a table to a PDF file:** Enter the `save pdf` command. You will be prompted on if you want to use the table name as the file name. The PDF file will appear in the root directory of the application.
- **Saving the table data to a JSON file:** Enter the `save json` command. Specify if you want to use the name of the table as the name for the JSON file. The file will appear in the root directory for the application.
- **Loading a table from the database:** Enter the `load table` command and then select from the list of available tables. Make sure that you have a database selected first.
- **Saving a table to a database:** Enter the `save table` command. The table should be saved to the currently selected database.
- **Viewing the available tables in the database:** Enter the `list tables` command.
- **Clearning the table:** Enter the `clear table` command.
- **Renaming the table:** Enter the `rename` command. Enter the new name for the table.
- **Viewing the JSON data for the table:** Enter the `print table data` command.
- **Exiting the app:** You can you use the `exit` command to exit the application and navigate through the diffrent parts of the app.

### Settings
- **Turning on autoprint:** Once in the settings, you can enter the `autoprint_table` command. You will then be promted if you want to turn autprint on or off. Tunring on autoprint_table will automatically print the table after a change has been made.