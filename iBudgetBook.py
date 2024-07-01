import os
import sys
from pathlib import Path

fName = "aFile.txt"
path = "C:/Users/janbo/OneDrive/Documents/GitHub/BudgetBook"
os.chdir(path)
with open(fName, 'r') as f:
    line = f.read()
    print(line)

