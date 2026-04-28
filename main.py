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

        # ── Step 2: Load Data ─────────────────────────────────────────────────────
        def _load_data(self):
            file_path = filedialog.askopenfilename(
                title="Select Healthcare Worker CSV File",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
            if not file_path:
                self._set_status("No file selected.")
                return
            try:
                # Step A: load with csv module (satisfies csv requirement)
                raw_rows = load_csv_with_csv_module(file_path)

                # Step B: load into Pandas DataFrame for processing
                self.df = pd.read_csv(file_path)

                # Enforce correct numeric types
                numeric_cols = [
                    "Age", "Education", "HourlyRate", "YearsAtCompany",
                    "YearsInCurrRole", "DistanceFromHome", "WorkLifeBalance",
                    "YearsLastPromotion", "YearsCurrManager"
                ]
                for col in numeric_cols:
                    if col in self.df.columns:
                        self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

                fname = os.path.basename(file_path)
                self._clear_output()
                self._print("=" * 60 + "\n", "heading")
                self._print("  📂  DATA LOADED SUCCESSFULLY\n", "heading")
                self._print("=" * 60 + "\n\n", "heading")
                self._print(f"  File            : ", "sub");
                self._print(f"{fname}\n", "value")
                self._print(f"  Records         : ", "sub");
                self._print(f"{len(self.df)} rows\n", "value")
                self._print(f"  Columns         : ", "sub");
                self._print(f"{len(self.df.columns)}\n", "value")
                self._print(f"  Missing values  : ", "sub");
                self._print(f"{self.df.isnull().sum().sum()}\n", "value")
                self._print(f"  csv module rows : ", "sub");
                self._print(f"{len(raw_rows)}\n\n", "value")

                self._print("  COLUMNS:\n", "heading")
                for col in self.df.columns:
                    self._print(f"    • {col:<25}", "sub")
                    self._print(f"({str(self.df[col].dtype)})\n", "value")

                self._print("\n  DATA PREVIEW (first 5 rows):\n", "heading")
                self._print("-" * 60 + "\n", "sub")
                self._print(f"  {'ID':<12}{'Age':<6}{'Gender':<10}{'Dept':<14}{'Role':<16}{'Left'}\n", "sub")
                self._print("  " + "-" * 58 + "\n", "sub")
                for _, row in self.df[["EmployeeID", "Age", "Gender",
                                       "Department", "JobRole", "Attrition"]].head().iterrows():
                    self._print(
                        f"  {str(row['EmployeeID']):<12}"
                        f"{str(int(row['Age'])):<6}"
                        f"{str(row['Gender']):<10}"
                        f"{str(row['Department']):<14}"
                        f"{str(row['JobRole']):<16}"
                        f"{str(row['Attrition'])}\n", "value")

                self._print("\n  ✅ Data ready. Click ⚙️ Process & Summarise next.\n", "success")
                self._set_status(f"✅ Loaded {len(self.df)} records from '{fname}'")

            except Exception as e:
                self._print(f"\n  ❌ Error loading file:\n  {e}\n", "error")
                self._set_status("❌ Failed to load data.")
                self.df = None

        # ── Step 3: Process & Summarise ───────────────────────────────────────────
        def _process_data(self):
            if self.df is None:
                messagebox.showwarning("No Data", "Please load the CSV data first!")
                return
            try:
                self.summary = build_summary(self.df)
                s = self.summary

                self._clear_output()
                self._print("=" * 60 + "\n", "heading")
                self._print("  ⚙️   DATA SUMMARY\n", "heading")
                self._print("=" * 60 + "\n\n", "heading")

                self._print("  ── GENERAL ──────────────────────────────────\n", "sub")
                self._print(f"  Total Employees      : ", "sub");
                self._print(f"{s['total_employees']}\n", "value")
                self._print(f"  Departments          : ", "sub");
                self._print(f"{', '.join(s['unique_departments'])}\n", "value")
                self._print(f"  Education Levels     : ", "sub");
                self._print(f"{s['education_levels']} levels\n", "value")

                self._print("\n  ── EDUCATION BREAKDOWN ──────────────────────\n", "sub")
                for code, count in s["education_counts"].items():
                    label = s["education_label_map"].get(int(code), str(code))
                    pct = math_round(count / s["total_employees"] * 100, 1)
                    self._print(f"  Level {code} ({label:<12}): ", "sub")
                    self._print(f"{count}  ({pct}%)\n", "value")

                self._print("\n  ── MARITAL STATUS ───────────────────────────\n", "sub")
                self._print(f"  Single               : ", "sub");
                self._print(f"{s['single_count']}  ({s['single_pct']}%)\n", "value")
                self._print(f"  Married              : ", "sub");
                self._print(f"{s['married_count']}  ({s['married_pct']}%)\n", "value")
                self._print(f"  Divorced             : ", "sub");
                self._print(f"{s['divorced_count']}  ({s['divorced_pct']}%)\n", "value")

                self._print("\n  ── YEARS AT COMPANY ─────────────────────────\n", "sub")
                self._print(f"  Min / Max / Avg      : ", "sub")
                self._print(f"{s['years_min']} / {s['years_max']} / {s['years_avg']} yrs\n", "value")

                self._print("\n  ── DISTANCE FROM HOME ───────────────────────\n", "sub")
                self._print(f"  Min / Max / Avg      : ", "sub")
                self._print(f"{s['distance_min']} / {s['distance_max']} / {s['distance_avg']} km\n", "value")

                self._print("\n  ── HOURLY RATE ──────────────────────────────\n", "sub")
                self._print(f"  Min / Max / Avg      : ", "sub")
                self._print(f"${s['hourly_min']} / ${s['hourly_max']} / ${s['hourly_avg']}\n", "value")

                self._print("\n  ── OVERTIME ─────────────────────────────────\n", "sub")
                self._print(f"  Works Overtime       : ", "sub");
                self._print(f"{s['overtime_yes']}  ({s['overtime_pct']}%)\n", "value")
                self._print(f"  No Overtime          : ", "sub");
                self._print(f"{s['overtime_no']}\n", "value")

                self._print("\n  ── WORK-LIFE BALANCE ────────────────────────\n", "sub")
                self._print(f"  Average Score        : ", "sub")
                self._print(f"{s['avg_work_life_balance']} / 3  ({s['wlb_label']})\n", "value")
                self._print(f"  Scale: ", "sub");
                self._print("0=Bad  1=Good  2=Better  3=Best\n", "value")

                self._print("\n  ── ATTRITION ────────────────────────────────\n", "sub")
                self._print(f"  Total Attritions     : ", "sub");
                self._print(f"{s['total_attritions']} employees left\n", "value")
                self._print(f"  Attrition Rate       : ", "sub");
                self._print(f"{s['attrition_rate_pct']}%\n", "value")

                self._print("\n  ── EMPLOYEES PER DEPARTMENT ─────────────────\n", "sub")
                for dept, count in s["dept_counts"].items():
                    pct = math_round(count / s["total_employees"] * 100, 1)
                    self._print(f"  {dept:<22}: ", "sub");
                    self._print(f"{count}  ({pct}%)\n", "value")

                self._print("\n  ── GENDER BREAKDOWN ─────────────────────────\n", "sub")
                for gender, count in s["gender_counts"].items():
                    pct = math_round(count / s["total_employees"] * 100, 1)
                    self._print(f"  {gender:<22}: ", "sub");
                    self._print(f"{count}  ({pct}%)\n", "value")

                self._print("\n  ── JOB ROLES ────────────────────────────────\n", "sub")
                for role, count in s["jobrole_counts"].items():
                    pct = math_round(count / s["total_employees"] * 100, 1)
                    self._print(f"  {role:<22}: ", "sub");
                    self._print(f"{count}  ({pct}%)\n", "value")

                self._print("\n  ✅ Summary complete. Click 📊 Visualise next.\n", "success")
                self._set_status(f"✅ Summary done — {s['total_employees']} employees | "
                                 f"{s['total_attritions']} attritions ({s['attrition_rate_pct']}%)")

            except Exception as e:
                self._print(f"\n  ❌ Error processing data:\n  {e}\n", "error")
                self._set_status("❌ Processing failed.")

# ── Step 4: Visualise Data ────────────────────────────────────────────────
    def _visualise_data(self):
        if self.df is None:
            messagebox.showwarning("No Data", "Please load the CSV data first!")
            return
        if not self.summary:
            messagebox.showwarning("No Summary", "Please process the data first!")
            return
        choice = self._ask_chart_choice()
        if choice == 1:
            self._show_pie_chart()
        elif choice == 2:
            self._show_bar_chart()
        elif choice == 3:
            self._show_dashboard()

    def _ask_chart_choice(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Visualisation")
        dialog.geometry("340x230")
        dialog.configure(bg=BG_DARK)
        dialog.resizable(False, False)
        dialog.grab_set()
        tk.Label(dialog, text="Choose a Visualisation",
                 font=("Courier New", 12, "bold"),
                 bg=BG_DARK, fg=ACCENT_TEAL).pack(pady=(18, 10))
        choice = tk.IntVar(value=0)

        def make_btn(txt, val, color):
            b = tk.Button(dialog, text=txt,
                          bg=BG_CARD, fg=color,
                          activebackground=color, activeforeground=BG_DARK,
                          font=FONT_BTN, relief="flat", bd=0,
                          padx=10, pady=8, cursor="hand2", width=28,
                          command=lambda: [choice.set(val), dialog.destroy()])
            b.pack(pady=3)
            b.bind("<Enter>", lambda e: b.configure(bg=color, fg=BG_DARK))
            b.bind("<Leave>", lambda e: b.configure(bg=BG_CARD, fg=color))

        make_btn("🥧  Pie Chart  — Department",   1, ACCENT_TEAL)
        make_btn("📊  Bar Chart  — Gender",        2, ACCENT_BLUE)
        make_btn("📋  Dashboard  — Full Overview", 3, "#F4A261")
        dialog.wait_window()
        return choice.get()

    def _show_pie_chart(self):
        dept_counts = self.summary["dept_counts"]
        labels  = list(dept_counts.keys())
        sizes   = list(dept_counts.values())
        colors  = ["#00C9A7", "#4FC3F7", "#F4A261"]
        explode = [0.05] * len(labels)
        fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG_DARK)
        ax.set_facecolor(BG_DARK)
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, autopct="%1.1f%%",
            colors=colors, explode=explode, startangle=140, pctdistance=0.82,
            wedgeprops=dict(edgecolor=BG_DARK, linewidth=2))
        for t in texts:
            t.set_color(TEXT_LIGHT); t.set_fontsize(11)
        for at in autotexts:
            at.set_color(BG_DARK); at.set_fontweight("bold"); at.set_fontsize(10)
        ax.set_title("Employees by Department",
                     color=ACCENT_TEAL, fontsize=14, fontweight="bold", pad=16)
        patches = [mpatches.Patch(color=colors[i], label=f"{labels[i]}: {sizes[i]}")
                   for i in range(len(labels))]
        ax.legend(handles=patches, loc="lower center",
                  bbox_to_anchor=(0.5, -0.08), ncol=3,
                  facecolor=BG_MID, edgecolor=BORDER_COL,
                  labelcolor=TEXT_LIGHT, fontsize=9)
        plt.tight_layout()
        self._open_chart_window("Pie Chart — Department Distribution", fig)
        self._print("\n  🥧 Pie chart displayed.\n", "success")
        self._set_status("Pie chart shown.")

    def _show_bar_chart(self):
        gender_counts = self.summary["gender_counts"]
        genders = list(gender_counts.keys())
        counts  = list(gender_counts.values())
        colors  = [ACCENT_TEAL if g == "Female" else ACCENT_BLUE for g in genders]
        total   = sum(counts)
        fig, ax = plt.subplots(figsize=(7, 5), facecolor=BG_DARK)
        ax.set_facecolor(BG_MID)
        bars = ax.bar(genders, counts, color=colors, width=0.45,
                      edgecolor=BG_DARK, linewidth=1.5)
        for bar, count in zip(bars, counts):
            pct = math_round(count / total * 100, 1)
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 3,
                    f"{count}\n({pct}%)",
                    ha="center", va="bottom",
                    color=TEXT_LIGHT, fontsize=11, fontweight="bold")
        ax.set_title("Employees by Gender",
                     color=ACCENT_TEAL, fontsize=14, fontweight="bold", pad=14)
        ax.set_xlabel("Gender", color=TEXT_DIM, fontsize=11)
        ax.set_ylabel("Number of Employees", color=TEXT_DIM, fontsize=11)
        ax.tick_params(colors=TEXT_LIGHT, labelsize=11)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color(BORDER_COL)
        ax.set_ylim(0, max(counts) + 50)
        fig.patch.set_facecolor(BG_DARK)
        plt.tight_layout()
        self._open_chart_window("Bar Chart — Gender Distribution", fig)
        self._print("\n  📊 Bar chart displayed.\n", "success")
        self._set_status("Bar chart shown.")

    def _show_dashboard(self):
        s  = self.summary
        df = self.df
        fig = plt.figure(figsize=(13, 8), facecolor=BG_DARK)
        fig.suptitle("Healthcare Worker Engagement — Dashboard",
                     color=ACCENT_TEAL, fontsize=15, fontweight="bold", y=0.98)

        # 1) Dept pie
        ax1 = fig.add_subplot(2, 3, 1)
        ax1.set_facecolor(BG_MID)
        dept = s["dept_counts"]
        ax1.pie(dept.values(), labels=dept.keys(), autopct="%1.0f%%",
                colors=["#00C9A7", "#4FC3F7", "#F4A261"], startangle=140,
                textprops={"color": TEXT_LIGHT, "fontsize": 8},
                wedgeprops=dict(edgecolor=BG_DARK, linewidth=1.2))
        ax1.set_title("By Department", color=ACCENT_BLUE, fontsize=10, fontweight="bold")

        # 2) Gender bar
        ax2 = fig.add_subplot(2, 3, 2)
        ax2.set_facecolor(BG_MID)
        genders = s["gender_counts"]
        bars = ax2.bar(genders.keys(), genders.values(),
                       color=[ACCENT_TEAL, ACCENT_BLUE],
                       edgecolor=BG_DARK, linewidth=1)
        for bar in bars:
            ax2.text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 2, str(int(bar.get_height())),
                     ha="center", color=TEXT_LIGHT, fontsize=9, fontweight="bold")
        ax2.set_title("By Gender", color=ACCENT_BLUE, fontsize=10, fontweight="bold")
        ax2.tick_params(colors=TEXT_LIGHT, labelsize=9)
        ax2.spines[["top", "right"]].set_visible(False)
        ax2.spines[["left", "bottom"]].set_color(BORDER_COL)

        # 3) Attrition pie
        ax3 = fig.add_subplot(2, 3, 3)
        att_yes = s["total_attritions"]
        att_no  = s["total_employees"] - att_yes
        ax3.pie([att_no, att_yes], labels=["Stayed", "Left"],
                autopct="%1.1f%%", colors=["#00C9A7", "#E76F51"],
                startangle=90,
                textprops={"color": TEXT_LIGHT, "fontsize": 9},
                wedgeprops=dict(edgecolor=BG_DARK, linewidth=1.2))
        ax3.set_title("Attrition Rate", color=ACCENT_BLUE, fontsize=10, fontweight="bold")

        # 4) Attrition by dept
        ax4 = fig.add_subplot(2, 3, 4)
        ax4.set_facecolor(BG_MID)
        dept_att = df[df["Attrition"] == AttritionStatus.YES.value]["Department"].value_counts()
        ax4.bar(dept_att.index, dept_att.values,
                color=["#F4A261", "#E76F51", "#E9C46A"],
                edgecolor=BG_DARK, linewidth=1)
        for i, (idx, val) in enumerate(dept_att.items()):
            ax4.text(i, val + 0.3, str(val),
                     ha="center", color=TEXT_LIGHT, fontsize=9, fontweight="bold")
        ax4.set_title("Attritions by Dept", color=ACCENT_BLUE, fontsize=10, fontweight="bold")
        ax4.tick_params(colors=TEXT_LIGHT, labelsize=8)
        ax4.spines[["top", "right"]].set_visible(False)
        ax4.spines[["left", "bottom"]].set_color(BORDER_COL)

        # 5) Work-life balance bar
        ax5 = fig.add_subplot(2, 3, 5)
        ax5.set_facecolor(BG_MID)
        wlb_map    = {e.value: e.name.capitalize() for e in WorkLifeBalanceLevel}
        wlb_counts = df["WorkLifeBalance"].value_counts().sort_index()
        wlb_names  = [wlb_map.get(int(k), str(k)) for k in wlb_counts.index]
        ax5.bar(wlb_names, wlb_counts.values,
                color=["#E76F51", "#F4A261", "#4FC3F7", "#00C9A7"],
                edgecolor=BG_DARK, linewidth=1)
        for i, val in enumerate(wlb_counts.values):
            ax5.text(i, val + 1, str(val),
                     ha="center", color=TEXT_LIGHT, fontsize=9, fontweight="bold")
        ax5.set_title("Work-Life Balance", color=ACCENT_BLUE, fontsize=10, fontweight="bold")
        ax5.tick_params(colors=TEXT_LIGHT, labelsize=9)
        ax5.spines[["top", "right"]].set_visible(False)
        ax5.spines[["left", "bottom"]].set_color(BORDER_COL)

        # 6) Key metrics panel
        ax6 = fig.add_subplot(2, 3, 6)
        ax6.set_facecolor(BG_CARD)
        ax6.axis("off")
        ax6.set_title("Key Metrics", color=ACCENT_BLUE, fontsize=10, fontweight="bold")
        metrics = [
            ("Total Employees",  str(s["total_employees"])),
            ("Total Attritions", str(s["total_attritions"])),
            ("Attrition Rate",   f"{s['attrition_rate_pct']}%"),
            ("Avg WLB Score",    f"{s['avg_work_life_balance']} / 3"),
            ("Avg Years at Co.", f"{s['years_avg']} yrs"),
            ("Avg Hourly Rate",  f"${s['hourly_avg']}"),
            ("Overtime Workers", f"{s['overtime_yes']}  ({s['overtime_pct']}%)"),
        ]
        for i, (label, value) in enumerate(metrics):
            y_pos = 0.90 - i * 0.13
            ax6.text(0.05, y_pos, label + ":",
                     transform=ax6.transAxes, color=TEXT_DIM, fontsize=9)
            ax6.text(0.95, y_pos, value,
                     transform=ax6.transAxes, color=ACCENT_TEAL,
                     fontsize=10, fontweight="bold", ha="right")

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        self._open_chart_window("Dashboard — Full Overview", fig)
        self._print("\n  📋 Dashboard displayed.\n", "success")
        self._set_status("Dashboard shown.")

    def _open_chart_window(self, title: str, fig):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.configure(bg=BG_DARK)
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        tk.Button(win, text="✖  Close",
                  command=lambda: [plt.close(fig), win.destroy()],
                  font=FONT_BTN, bg=BG_CARD, fg="#E76F51",
                  activebackground="#E76F51", activeforeground=BG_DARK,
                  relief="flat", padx=10, pady=6, cursor="hand2").pack(pady=(0, 10))

        