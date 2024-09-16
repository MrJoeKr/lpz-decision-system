# LPZ Decision System
AI system for deciding whether to fix diagnosis from LPZ (List o Prohlídce Zemřelého – List of Deceased's Examination) by diagnosis from NOR (Národní Onkologický Registr – National Oncological Registry). 
Trained on expert decisions.

## Requirements
- Python $\ge 3.10$

## Installation
Clone the repository.

Create a virtual environment and activate it (optional but recommended):
```bash
python -m venv venv
```
Activate the virtual environment:

Windows:
```bash
.\venv\Scripts\Activate
```
Linux:
```bash
source venv/bin/activate
```

Install the requirements:
```bash
pip install .
```

## Usage
To run the system, use the following command:
```bash
lpz run
```