# foreo_task_new
Task for junior data engineer

- folder .idea contains files generated in pycharm project

- file main.py contains the function that creates the postgresql database table,
  read the data from the excel file and import the data to the postgresql table
  
- file settings.json contains user information to access the postgresql table
  (other information like host, port, etc. could be specified in this file
  as well but for demonstration I just included username and password)
 
- the program won't work unless the .json file is modified with information
  related to your postgresql database (note that hostname and port may also
  vary)
