import json # Used to load JSON data filed

# 🔹 Load market data (Calabar)
def load_market_data():
    # Open the JSOn file containing market data
    with open("../data/calabar_data.json", "r") as file:
        data = json.load(file) # Convert Json to python dictionary
    return data

# 🔹 Get average from range
def get_average(min_val, max_val):
    # Simple average calculation
    return (min_val + max_val) / 2

# 🔹 Calculate building cost
def calculate_building_cost(data, property_input):
    construction_data = data["construction"] #Extract Construction data
    
