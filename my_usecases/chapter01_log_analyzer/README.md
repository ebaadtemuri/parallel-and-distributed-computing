# Chapter 1 Log Analyzer

A Tkinter application that counts words and case-insensitive keyword occurrences in `.log` files. It compares serial, threaded, and process-pool execution.

## Run

From this directory:

```powershell
py main.py
```

Choose a folder containing `.log` files, enter a keyword, and select an execution mode. `Compare all` runs the same files through all three modes and displays counts and elapsed time.

This project uses Python standard-library modules only. Timings depend on the files and computer; process startup overhead can make multiprocessing slower for small inputs.
