# LPZ Decision System
<a href="https://github.com/MrJoeKr/lpz-decision-system/archive/refs/heads/main.zip">
    <img src="https://img.shields.io/badge/Code-Download%20ZIP-green" alt="Download ZIP" style="display: inline-block; margin: 0; padding: 0;"/>
</a>

AI system for deciding whether to fix diagnosis from LPZ (List o Prohlídce Zemřelého – List of Deceased's Examination) by diagnosis from NOR (Národní Onkologický Registr – National Oncological Registry). 
Trained on expert decisions.

## Requirements
- Python $\ge 3.10$

## Installation
Install the package either by:

- Downloading the repository as a ZIP file by clicking the on the badge at the beginning of this `README` file.
- Cloning the repository.

### Windows
Run the file `install.ps1` either by right-clicking and selecting `Run with PowerShell` or by running the command in PowerShell:
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
Run the file `run.ps1` either by right-clicking and selecting `Run with PowerShell` or by running the command in PowerShell:
```powershell
.\run.ps1
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