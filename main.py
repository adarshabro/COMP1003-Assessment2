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