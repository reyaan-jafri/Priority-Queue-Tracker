# Priority Queue Tracker (Python CLI)

Python task tracker that stores tasks in a JSON file so they persist between runs.  
You can add tasks with a due date in a priority queue, list them, mark them complete, and delete them.  
Covers key programming concepts like file I/O, data modeling with Python’s `dataclasses`, and modular code design.

## Features
- Add tasks with optional due date and priority (1 = high, 5 = low)
- List all tasks or filter by status (TODO / DONE)
- Mark tasks as complete
- Delete tasks by ID
- Persistent storage using JSON so tasks remain after restarting the program
- Menu-based interface for ease of use

## Technologies Used
- Python 3
- `dataclasses` for structured data modeling
- `json` for persistent data storage
- Modular CLI design for maintainability

## Project Structure
