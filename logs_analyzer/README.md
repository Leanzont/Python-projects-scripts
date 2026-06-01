# README.md

# Python Log Analyzer

A simple Python project that analyzes log files, counts log levels, calculates percentages, and exports the results into a report file.

---

# Features

* Analyze `INFO`, `WARNING`, and `ERROR` logs
* Count log occurrences
* Calculate percentages
* Save results into a file
* Process logs line by line

---

# Technologies Used

* Python 3
* File Handling
* Dictionaries
* Lists
* Loops
* Conditional Statements

---

# Project Structure

```text
python_log_analyzer/
│
├── log_analyzer.py
├── logsTest.txt
├── info_logs.txt
└── README.md
```

---

# Example Input

```text
INFO User login successful
ERROR Failed login attempt
WARNING Disk space low
INFO File uploaded successfully
ERROR Database connection timeout
```

---

# Example Output

```text
***********************************
          Summary Logs
***********************************
INFO: 2
WARNING: 1
ERROR: 2
Total: 5

% Errors: 40.0%
% Info: 40.0%
% Warning: 20.0%
```

---

# How to Run

```bash
python3 log_analyzer.py
```

---

# Future Improvements

* Add support for custom log levels
* Export results in JSON format
* Add timestamp analysis
* Create graphical reports
* Add command-line arguments

---

# Skills Demonstrated

* Python programming
* File handling
* Data processing
* Log analysis
* Clean code structure
* Problem-solving

