# Student Name: Adarsha upreti, Student ID: 32206078
# COMP1003 - Programming Principles and Techniques
# Assessment 2 - Healthcare Worker Engagement Analyser
# Version: V1.2026

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import pandas as pd
import os
import math
import csv
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


# ──────────────────────────────────────────────────────────────────────────────
#  CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
DEVELOPER_NAME = "Adarsha upreti"
STUDENT_ID     = "32206078"
SYSTEM_VERSION = "V1.2026"
CSV_FILE       = "6343941.csv"   # keep CSV in same folder as this script


# ──────────────────────────────────────────────────────────────────────────────
#  ENUMERATIONS  (enum module — required by brief)
# ──────────────────────────────────────────────────────────────────────────────
class EducationLevel(Enum):
    """Maps numeric education codes to descriptive labels."""
    GCSE      = 1
    A_LEVELS  = 2
    BACHELOR  = 3
    MASTER    = 4
    DOCTORATE = 5


class WorkLifeBalanceLevel(Enum):
    """Maps numeric work-life balance codes to descriptive labels."""
    BAD    = 0
    GOOD   = 1
    BETTER = 2
    BEST   = 3


class AttritionStatus(Enum):
    """Attrition values as an enum."""
    YES = "Yes"
    NO  = "No"


class OverTimeStatus(Enum):
    """Overtime values as an enum."""
    YES = "Yes"
    NO  = "No"


# ──────────────────────────────────────────────────────────────────────────────
#  COLOUR PALETTE & FONTS
# ──────────────────────────────────────────────────────────────────────────────
BG_DARK     = "#0D1B2A"
BG_MID      = "#1B2A3B"
BG_CARD     = "#1E3448"
ACCENT_TEAL = "#00C9A7"
ACCENT_BLUE = "#4FC3F7"
TEXT_LIGHT  = "#E8F4FD"
TEXT_DIM    = "#7FA8C9"
BORDER_COL  = "#2D4A6A"

FONT_TITLE  = ("Georgia", 20, "bold")
FONT_SUB    = ("Georgia", 11, "italic")
FONT_BTN    = ("Courier New", 10, "bold")
FONT_LABEL  = ("Courier New", 9)
FONT_OUTPUT = ("Courier New", 10)

# ──────────────────────────────────────────────────────────────────────────────
#  HELPER: load CSV using the built-in csv module (required by brief)
# ──────────────────────────────────────────────────────────────────────────────
def load_csv_with_csv_module(filepath: str) -> list:
    """
    Load the CSV file using Python's built-in csv module.
    Returns a list of dicts (one per employee row).
    Satisfies the requirement to use the csv module.
    """
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


# ──────────────────────────────────────────────────────────────────────────────
#  HELPER: safe rounding using the math module (required by brief)
# ──────────────────────────────────────────────────────────────────────────────
def math_round(value: float, decimals: int = 2) -> float:
    """
    Round a float to given decimal places using math.floor.
    Satisfies the requirement to use the math module.
    """
    factor = math.pow(10, decimals)
    return math.floor(value * factor + 0.5) / factor


# ──────────────────────────────────────────────────────────────────────────────
#  HELPER: build summary dictionary from a Pandas DataFrame
#  (standalone so it can be unit-tested independently)
# ──────────────────────────────────────────────────────────────────────────────
def build_summary(df: pd.DataFrame) -> dict:
    """
    Compute all required summary statistics from the DataFrame.
    Returns a dictionary of key metrics.
    Uses math module for rounding and enum for label mapping.
    """
    total          = len(df)
    marital_counts = df["MaritalStatus"].value_counts()

    # Overtime counts using OverTimeStatus enum (column optional in this dataset)
    if "OverTime" in df.columns:
        ot_yes = int((df["OverTime"] == OverTimeStatus.YES.value).sum())
        ot_no  = int((df["OverTime"] == OverTimeStatus.NO.value).sum())
    else:
        ot_yes = 0
        ot_no  = 0

    # Education level label map from EducationLevel enum
    edu_map = {e.value: e.name.replace("_", "-") for e in EducationLevel}

    summary = {
        # General
        "total_employees"      : total,
        "unique_departments"   : sorted(df["Department"].unique().tolist()),
        "num_departments"      : df["Department"].nunique(),
        "education_levels"     : df["Education"].nunique(),
        "education_label_map"  : edu_map,
        "education_counts"     : df["Education"].value_counts().sort_index().to_dict(),

        # Marital status counts & percentages
        "single_count"         : int(marital_counts.get("Single",   0)),
        "married_count"        : int(marital_counts.get("Married",  0)),
        "divorced_count"       : int(marital_counts.get("Divorced", 0)),
        "single_pct"           : math_round(marital_counts.get("Single",   0) / total * 100, 1),
        "married_pct"          : math_round(marital_counts.get("Married",  0) / total * 100, 1),
        "divorced_pct"         : math_round(marital_counts.get("Divorced", 0) / total * 100, 1),

        # Years at company
        "years_min"            : math_round(float(df["YearsAtCompany"].min()), 2),
        "years_max"            : math_round(float(df["YearsAtCompany"].max()), 2),
        "years_avg"            : math_round(float(df["YearsAtCompany"].mean()), 2),

        # Distance from home
        "distance_min"         : math_round(float(df["DistanceFromHome"].min()), 2),
        "distance_max"         : math_round(float(df["DistanceFromHome"].max()), 2),
        "distance_avg"         : math_round(float(df["DistanceFromHome"].mean()), 2),

        # Hourly rate
        "hourly_min"           : math_round(float(df["HourlyRate"].min()), 2),
        "hourly_max"           : math_round(float(df["HourlyRate"].max()), 2),
        "hourly_avg"           : math_round(float(df["HourlyRate"].mean()), 2),

        # Work-life balance
        "avg_work_life_balance": math_round(float(df["WorkLifeBalance"].mean()), 2),
        "wlb_label"            : WorkLifeBalanceLevel(
                                     int(round(df["WorkLifeBalance"].mean()))
                                 ).name.capitalize(),

        # Overtime
        "overtime_yes"         : ot_yes,
        "overtime_no"          : ot_no,
        "overtime_pct"         : math_round(ot_yes / total * 100, 1),

        # Attrition
        "total_attritions"     : int((df["Attrition"] == AttritionStatus.YES.value).sum()),
        "attrition_rate_pct"   : math_round(
                                     float((df["Attrition"] == AttritionStatus.YES.value).sum())
                                     / total * 100, 1),

        # Breakdowns
        "dept_counts"          : df["Department"].value_counts().to_dict(),
        "gender_counts"        : df["Gender"].value_counts().to_dict(),
        "jobrole_counts"       : df["JobRole"].value_counts().to_dict(),
    }
    return summary