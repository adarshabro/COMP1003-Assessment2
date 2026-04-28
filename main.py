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

# ──────────────────────────────────────────────────────────────────────────────
#  MAIN APPLICATION CLASS
# ──────────────────────────────────────────────────────────────────────────────
class HealthcareAnalyserApp:
    """Main Tkinter GUI application for Healthcare Worker Engagement Analysis."""

    def __init__(self, root: tk.Tk):
        self.root    = root
        self.df      = None   # Pandas DataFrame
        self.summary = {}     # Summary dictionary
        self._configure_window()
        self._build_ui()

    # ── Window setup ──────────────────────────────────────────────────────────
    def _configure_window(self):
        # Title format: "Student's Name & Student's ID" as per brief
        self.root.title(f"{DEVELOPER_NAME} & {STUDENT_ID}")
        self.root.geometry("900x700")
        self.root.minsize(820, 600)
        self.root.configure(bg=BG_DARK)
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  // 2) - 450
        y = (self.root.winfo_screenheight() // 2) - 350
        self.root.geometry(f"+{x}+{y}")

    # ── Full UI ───────────────────────────────────────────────────────────────
    def _build_ui(self):
        self._build_header()
        self._build_button_panel()
        self._build_output_area()
        self._build_status_bar()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        header = tk.Frame(self.root, bg=BG_MID, pady=14)
        header.pack(fill="x")
        tk.Frame(header, bg=ACCENT_TEAL, width=5).pack(side="left", fill="y", padx=(12, 14))
        info = tk.Frame(header, bg=BG_MID)
        info.pack(side="left", fill="both", expand=True)
        tk.Label(info, text="Healthcare Worker Engagement Analyser",
                 font=FONT_TITLE, bg=BG_MID, fg=ACCENT_TEAL, anchor="w").pack(fill="x")
        tk.Label(info,
                 text=f"COMP1003 – Programming Principles and Techniques  |  {SYSTEM_VERSION}",
                 font=FONT_SUB, bg=BG_MID, fg=TEXT_DIM, anchor="w").pack(fill="x")
        badge = tk.Frame(header, bg=BG_CARD, padx=12, pady=6)
        badge.pack(side="right", padx=14)
        tk.Label(badge, text="Developer",
                 font=("Courier New", 7, "bold"), bg=BG_CARD, fg=TEXT_DIM).pack()
        tk.Label(badge, text=DEVELOPER_NAME,
                 font=("Courier New", 10, "bold"), bg=BG_CARD, fg=ACCENT_BLUE).pack()
        tk.Label(badge, text=STUDENT_ID,
                 font=("Courier New", 9), bg=BG_CARD, fg=TEXT_DIM).pack()
        tk.Frame(self.root, bg=ACCENT_TEAL, height=2).pack(fill="x")

    # ── Button panel ──────────────────────────────────────────────────────────
    def _build_button_panel(self):
        panel = tk.Frame(self.root, bg=BG_DARK, pady=16)
        panel.pack(fill="x", padx=20)
        buttons = [
            ("📂  Load Data",            self._load_data,       ACCENT_TEAL),
            ("⚙️   Process & Summarise", self._process_data,    ACCENT_BLUE),
            ("📊  Visualise Data",       self._visualise_data,  "#F4A261"),
            ("📄  Generate Report",      self._generate_report, "#E76F51"),
        ]
        for i, (label, cmd, color) in enumerate(buttons):
            col = tk.Frame(panel, bg=BG_DARK)
            col.grid(row=0, column=i, padx=8, sticky="ew")
            panel.columnconfigure(i, weight=1)
            btn = tk.Button(col, text=label, command=cmd,
                            font=FONT_BTN, bg=BG_CARD, fg=color,
                            activebackground=color, activeforeground=BG_DARK,
                            relief="flat", bd=0, padx=10, pady=10, cursor="hand2",
                            highlightthickness=1, highlightbackground=color)
            btn.pack(fill="x")
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.configure(bg=c, fg=BG_DARK))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.configure(bg=BG_CARD, fg=c))
        tk.Frame(self.root, bg=BORDER_COL, height=1).pack(fill="x", padx=20)

    # ── Output area ───────────────────────────────────────────────────────────
    def _build_output_area(self):
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.pack(fill="both", expand=True, padx=20, pady=(10, 0))
        tk.Label(outer, text="OUTPUT CONSOLE",
                 font=("Courier New", 8, "bold"),
                 bg=BG_DARK, fg=TEXT_DIM).pack(anchor="w", pady=(0, 4))
        self.output_text = scrolledtext.ScrolledText(
            outer, font=FONT_OUTPUT, bg=BG_CARD, fg=TEXT_LIGHT,
            insertbackground=ACCENT_TEAL, relief="flat", bd=0,
            padx=12, pady=10, state="disabled", wrap="word")
        self.output_text.pack(fill="both", expand=True)
        self.output_text.tag_config("heading", foreground=ACCENT_TEAL,
                                    font=("Courier New", 10, "bold"))
        self.output_text.tag_config("sub",     foreground=ACCENT_BLUE)
        self.output_text.tag_config("value",   foreground="#A8D8EA")
        self.output_text.tag_config("success", foreground="#00C9A7")
        self.output_text.tag_config("error",   foreground="#E76F51")
        self.output_text.tag_config("warn",    foreground="#F4A261")
        self._print("=" * 60 + "\n", "heading")
        self._print("  Healthcare Worker Engagement Analyser\n", "heading")
        self._print(f"  {SYSTEM_VERSION}  |  {DEVELOPER_NAME}  |  {STUDENT_ID}\n", "sub")
        self._print("=" * 60 + "\n\n", "heading")
        self._print("  Ready. Please click  📂 Load Data  to begin.\n", "value")

    # ── Status bar ────────────────────────────────────────────────────────────
    def _build_status_bar(self):
        bar = tk.Frame(self.root, bg=BG_MID, pady=4)
        bar.pack(fill="x", side="bottom")
        tk.Frame(bar, bg=ACCENT_TEAL, width=3).pack(side="left", fill="y")
        self.status_var = tk.StringVar(value="Status: Ready")
        tk.Label(bar, textvariable=self.status_var,
                 font=FONT_LABEL, bg=BG_MID, fg=TEXT_DIM,
                 anchor="w", padx=10).pack(side="left")
        tk.Label(bar, text=f"COMP1003  {SYSTEM_VERSION}",
                 font=FONT_LABEL, bg=BG_MID, fg=BORDER_COL,
                 anchor="e", padx=10).pack(side="right")

    # ── Console helpers ───────────────────────────────────────────────────────
    def _print(self, text: str, tag: str = ""):
        self.output_text.configure(state="normal")
        if tag:
            self.output_text.insert("end", text, tag)
        else:
            self.output_text.insert("end", text)
        self.output_text.see("end")
        self.output_text.configure(state="disabled")

    def _clear_output(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.configure(state="disabled")

    def _set_status(self, msg: str):
        self.status_var.set(f"Status: {msg}")