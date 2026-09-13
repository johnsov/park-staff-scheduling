# Park Staff Scheduling

Optimization-based staff scheduling and workload assignment system for protected-area control posts.

This project was developed to automate the assignment of personnel to operational control posts in **Farallones de Cali National Natural Park, Colombia**, considering staff availability, operational requirements, gender distribution, driving qualifications, organizational strategies, workload balance, and shift compatibility.

The system uses **Python**, **Google OR-Tools CP-SAT**, and **Excel** to generate feasible staff schedules while minimizing workload imbalance and undesirable assignments.

---

## Project Overview

Assigning personnel to protected-area control posts involves multiple operational constraints:

- Different posts require different numbers of people.
- Some posts operate continuously for several days.
- Other posts operate only on weekends and holidays.
- Certain positions require vehicle drivers.
- Some posts require personnel from specific strategies.
- Some employees cannot work at particular posts or days.
- Staff members cannot be assigned to overlapping shifts.
- Workload should be distributed according to each employee's professional role.
- Shift changes must preserve operational continuity.

Manually managing all these conditions is complex and error-prone.

This project models the scheduling problem as a **constraint optimization problem** and uses Google OR-Tools to find feasible and balanced assignments.

---

## Main Features

- Automated staff assignment to operational control posts.
- Constraint programming with Google OR-Tools CP-SAT.
- Excel-based input configuration.
- Configurable post opening dates.
- Support for multi-day work blocks.
- Support for weekend and holiday shifts.
- Gender composition constraints.
- Vehicle-driver requirements.
- Strategy-based eligibility rules.
- Individual employee restrictions.
- Prevention of overlapping assignments.
- Workload calculation in days worked.
- Workload distribution according to professional role.
- Validation of generated solutions.
- Excel export of assignments and workload summaries.
- Reproducible or randomized solutions using an optional seed.

---

## Technology Stack

- **Python 3**
- **Google OR-Tools**
- **CP-SAT Solver**
- **pandas**
- **openpyxl**
- **Jupyter Notebook**
- **Excel**

---

## Input Data

The main input file is: **data/cerebro_farallones.xlsx**

The workbook contains information about personnel, calendar dates, and post configuration.

Personnel information

The personnel data includes fields such as:

* Name.
* Gender (M/F)
* Professional role (PROFESIONAL/OPERARIO/TECNICO)
* Strategy (MONITOREO/ECOTURISMO/RELACIONAMIENTO/ETC)
* Active status (SI/NO)
* Vehicle-driving qualifications (SI/NO)
* Ecoturismo membership (SI/NO)
* Motorcycle-driving qualifications (SI/NO)

Calendar information

The calendar defines:

* Date.
* Day type.
* Holidays.

The system uses the calendar instead of hardcoding dates, allowing the schedule to be adapted to different months or planning periods.

Post configuration

Post configuration includes fields such as:

* Post name.
* Opening date.
* Required number of people.
* Shift duration.

This allows operational posts to be configured without rewriting the scheduling engine.


---

## Project Structure

```text
park-staff-scheduling/
│
├── main.ipynb
│
├── src/
│   ├── cargar_datos.py
│   ├── crear_turnos.py
│   ├── modelo.py
│   ├── restricciones_bloques.py
│   ├── restricciones_puestos.py
│   ├── objetivo.py
│   ├── validar_solucion.py
│   ├── reportes.py
│   └── exportar_resultados.py
│
├── data/
│   └── cerebro_farallones.xlsx
│
├── outputs/
│
├── requirements.txt
│
├── README.md
│
└── .gitignore

```

---

## Author

**John Sebastian Ovalle**

Biologist | Data Science | Biodiversity Conservation

This project combines operational experience in protected-area management with optimization, data analysis, and software development.

---

## License

This project is intended for educational, professional portfolio, and research purposes.

A formal license can be added depending on the intended use and distribution of the source code and data.