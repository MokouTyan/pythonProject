#%%

import re
import json
import requests
#%%
with open('config.json', 'r', encoding='utf-8') as f:
    JsonFile = json.load(f)
base_url=JsonFile['base_url']

#%%

content = requests.get(base_url)

print(content.json())
