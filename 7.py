import sys
import requests
import random

for modulename, module_path in sys.modules.items():
    print(modulename, module_path)