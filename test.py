import json
from DDC_REGS import *


data = None

try:
    with open('conf.json', 'w') as file:
        json.dump(REGS_DEFAULT, file)
except FileNotFoundError:
    pass

print(data)
