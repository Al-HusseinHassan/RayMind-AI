import sys
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)