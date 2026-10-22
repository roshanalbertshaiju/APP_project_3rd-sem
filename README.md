# ExamOpt

ExamOpt is a desktop application for managing examination data and generating examination timetables. It is built with Python, Tkinter, and SQLite for SRM Institute of Science and Technology, Tiruchirappalli Campus.

The application includes two desktop themes, an academic constraint validator, timetable scheduling and optimization tools, CSV/Excel/PDF exports, and an optional TCP server.

## Features

- Manage students, subjects, enrollments, faculty, rooms, and time slots.
- Generate timetables with the heuristic scheduling engine and validate assignments for conflicts and availability.
- Evaluate and optimize schedules with functional scoring, a genetic algorithm, and parallel candidate search.
- Review symbolic objective-function calculations with SymPy.
- Export timetables to CSV, Excel (`.xlsx`), and PDF.
- Use the bundled sample dataset for demonstrations and testing.
- Launch the optional TCP socket server for framed JSON requests.

## Requirements

- Python 3 with Tkinter available.
- The third-party packages used by the application:
  - `sympy`
  - `openpyxl`
  - `reportlab`

Install the packages from the project directory:

```powershell
python -m pip install sympy openpyxl reportlab
```

On Windows, if `python` is not available, use the Python launcher:

```powershell
py -m pip install sympy openpyxl reportlab
```

The project does not currently include a dependency lockfile or `requirements.txt`.

## Run the application

From the project directory, launch the default modern GUI:

```powershell
python main.py
```

Choose a theme explicitly:

```powershell
python main.py --theme modern
python main.py --theme classic
```

On Windows, the included batch launchers provide the same options:

- `run_examopt.bat` — default modern GUI
- `run_modern_gui.bat` — modern GUI
- `run_classic_gui.bat` — classic GUI

The GUI lets you manage the input data, generate and validate a timetable, run optimization and review tools, and export results. Load the sample dataset from the application when you want example data.

## Command-line options

Run these from the project directory:

```powershell
python main.py --cli         # End-to-end demonstration using sample data
python main.py --scenarios   # Run the academic review scenarios
python main.py --verify-100  # Alias for running the review scenarios
python main.py --ga          # Run genetic-algorithm optimization
python main.py --parallel    # Search candidate schedules in parallel
python main.py --benchmark   # Compare sequential and parallel search
python main.py --export-all  # Generate CSV, Excel, and PDF timetable exports
python main.py --server      # Start the TCP server on the default port
python main.py --server --port 8080
```

For help on all command-line options:

```powershell
python main.py --help
```

The `--cli`, `--ga`, `--parallel`, `--benchmark`, and `--export-all` modes load the bundled sample dataset before running. The server defaults to `127.0.0.1:8080`; choose a different port with `--port`.

## Data and exports

The SQLite database is created automatically when the application starts. By default, it is `examopt.db` in the project directory. Set `EXAMOPT_DB` to use a different database path:

```powershell
$env:EXAMOPT_DB = "C:\data\examopt.db"
python main.py
```

The `--export-all` command writes `schedule.csv`, `schedule.xlsx`, and `schedule.pdf` into the `exports` directory.

## Run tests

Run the test suite with Python's built-in `unittest` runner:

```powershell
python -m unittest discover -s tests -v
```

## Project layout

```text
.
├── config.py                 # Application settings and database path
├── main.py                   # GUI and command-line entry point
├── database/                 # SQLite schema and persistence
├── models/                   # Domain models
├── services/                 # Application service layer
├── scheduling/               # Timetable generation and optimization
├── validation/               # Timetable constraint validation
├── optimization/             # SymPy symbolic objective model
├── networking/               # TCP client, server, and message protocol
├── gui/                      # Tkinter application and views
├── utils/                    # Sample data and export helpers
├── tests/                    # Automated tests and review scenarios
└── exports/                  # Generated timetable files
```

## Project team

- Suhas V A
- Subaash G
- Roshan Albert Shaiju
