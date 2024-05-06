import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL" : "https://facerecognitionmems-default-rtdb.firebaseio.com/"
})

ref = db.reference("Students")

import json

# Input data
data = {
   "Num 1 uy": {
       "Name": "Pham Khac Uy",
       "ID": "10423122",
       "Major": "Computer Science",
       "Intake": 2023,
       "Year": 1
   },
   "Num 1 dung": {
       "Name": "Le Tri Dung",
       "ID": "10423022",
       "Major": "Computer Science",
       "Intake": 2023,
       "Year": 1
   },
   "Num 1 an": {
       "Name": "Nguyen Thanh An",
       "ID": "10423003",
       "Major": "Computer Science",
       "Intake": 2023,
       "Year": 1
   },
   "Num 1 phu": {
       "Name": "Nguyen Minh Phu",
       "ID": "10423090",
       "Major": "Computer Science",
       "Intake": 2023,
       "Year": 1
   },
   "Num 1 khoa": {
       "Name": "Tran Nguyen Khoa",
       "ID": "10423060",
       "Major": "Computer Science",
       "Intake": 2023,
       "Year": 1
   },
   "Num 1 hung": {
       "Name": "Tran Tan Hung",
       "ID": "10423052",
       "Major": "Computer Science",
       "Intake": 2023,
       "Year": 1
   },
   "Num 1 minh": {
       "Name": "Phan Anh Minh",
       "ID": "10423191",
       "Major": "Computer Science",
       "Intake": 2023,
       "Year": 1
   }
}

# Function to replace keys with sequential numbers
def replace_num(data):
    for i in range(1, 26):
        key = f"Num {i} uy"
        value = data["Num 1 uy"].copy()  # Create a copy to avoid modifying original data
        data[key] = value
    for i in range(1, 26):
        key = f"Num {i} dung"
        value = data["Num 1 dung"].copy()  # Create a copy to avoid modifying original data
        data[key] = value
    for i in range(1, 26):
        key = f"Num {i} an"
        value = data["Num 1 an"].copy()  # Create a copy to avoid modifying original data
        data[key] = value
    for i in range(1, 26):
        key = f"Num {i} phu"
        value = data["Num 1 phu"].copy()  # Create a copy to avoid modifying original data
        data[key] = value
    for i in range(1, 26):
        key = f"Num {i} khoa"
        value = data["Num 1 khoa"].copy()  # Create a copy to avoid modifying original data
        data[key] = value
    for i in range(1, 26):
        key = f"Num {i} hung"
        value = data["Num 1 hung"].copy()  # Create a copy to avoid modifying original data
        data[key] = value
    for i in range(1, 26):
        key = f"Num {i} minh"
        value = data["Num 1 minh"].copy()  # Create a copy to avoid modifying original data
        data[key] = value

# Replace numbers
replace_num(data)

# Print modified data
print(json.dumps(data, indent=4))

for key, value in data.items():
    ref.child(key).set(value)