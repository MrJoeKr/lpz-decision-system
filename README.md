# LPZ Decision System
AI system for deciding whether to fix diagnosis from LPZ (List o Prohlídce Zemřelého – List of Deceased's Examination) by diagnosis from NOR (Národní Onkologický Registr – National Oncological Registry). 
Trained on expert decisions.

## Requirements
- Python $\ge 3.10$

## Installation
Clone the repository.

### Windows
Run the file `install.ps1`. Either by right-clicking and selecting `Run with PowerShell` or by running the command in PowerShell:
```powershell
.\install.ps1
```

### Linux
Create a virtual environment and activate it (optional but recommended):
```bash
python -m venv venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

Install the requirements:
```bash
pip install .
```

## Usage

### Windows
Run the file `run.bat`. Either by double-clicking or by running the command in PowerShell:
```powershell
.\run.bat
```

### Linux
Run the command:
```bash
lpz run
```
For more information, run:
```bash
lpz -h
```