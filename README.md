### [**DOCUMENT OF THE PROJECT--NOT ALL INFO IS HERE JUST THE BASIC DETAILS**](https://docs.google.com/document/d/12abTFE48Og_o3m5Oh16NBYvLzybPCEJQoeuerxMw03k/edit?tab=t.0)



## **Introduction**

In this project, you will implement a **command-line** program to manage the Agent platform. You are required to use the Python MySQL connector to access and manipulate the database. 

The Python program should 
1) accept command-line arguments as the inputs, 
2) parse the inputs into SQL statements,  
3) execute the statements in the MySQL server, 
4) handle and print the results. 

**ER diagram** (please refer to the HW2 solution for the DDLs) :

<img width="640" height="566" alt="image" src="https://github.com/user-attachments/assets/34971e73-6a34-4f38-ab85-b2ed60b3f5f7" />


# **Dataset**

There will be one CSV file for each table. Each line represents one record, and the columns are separated by a comma ‘,’’. The order of columns follows the order of attributes in the DDL. 

The provided [dataset](https://drive.google.com/file/d/1G_wWXdNKswV0gWflR0--64mfc2D8x2ZI/view?usp=sharing) is for testing only, so you can make any changes to cover more cases. A hidden dataset (for evaluating Q1-Q8 only) will be used during the grading. 
In the zip file is an **instructions text file** which contains commands to run in MySQL in order to load CSV files into your database **after having run the DDL statements.**

Q9-Q10 are open questions, so no hidden dataset will be used to test the answer. Check the instructions for Q9-Q10 in the last two pages. 

# **Regulations and Assumptions**

- You can have any number of Python files, but the entry/main file must be named “project.py”
- The command to run the program will be
>python3 project.py <function name> [param1] [param2] …

The list of function names and their parameters is in the function requirements section. 	

  
- You can assume that the command-line input is always correct IN FORMAT ONLY. There won’t be a nonexistent function name as input, and the parameters will be given in the correct order and format. 
So you don’t need to handle unexpected input. However, input content can be faulty - e.g., given a duplicate netID for insertion. 
- You can assume that the dataset files are always correct IN FORMAT AND CONTENT. So there won’t be errors when parsing the file, or when inserting the records to DB. 
- Every date has the format YYYY-MM-DD, e.g. 2025-02-29, and every datetime has the format YYYY-MM-DD hh:mm:ss, e.g. 2025-02-29 14:10:34.
- Strings that contain spaces will be wrapped in quotation marks when calling the command, (e.g. "The Matrix") whereas strings with no spaces will not have quotation marks (e.g. Wicked).
- If the input is NULL, treat it as the None type in Python, not a string called “NULL”.
- **If the output is boolean**, print “Success” or “Fail”.
- **If the output is a result table**, print each record in one line and separate columns with ‘,’ - just like the format of the dataset file. 
- You must use Python 3. The standard Python libraries and mysql-connector-python will be installed in the autograder — other third-party packages are not allowed.

# **Setup Instructions**

Install MySQL server and test if you can run queries. [(instructions)](https://docs.google.com/document/d/1UWK9EMx_asZQ0OSLy13WGMYVkxEUEmbj/edit?usp=sharing&ouid=113044980042238275157&rtpof=true&sd=true)

Install mysql-connector-python and try running SQL queries from python. [(guide)](https://www.w3schools.com/python/python_mysql_getstarted.asp)
