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

    property_type = property_input["property_type"] 
    floor_area = property_input["floor_area_sqm"]
    finish = property_input["finish_level"]

    cost_per_sqm = 0 # Initialize cost per sqm

    # 🔸 Duplex
    if property_type == "duplex":
       min_val = construction_data["duplex"]["min"]
       max_val = construction_data["duplex"]["max"]
       cost_per_sqm = get_average(min_val, max_val)

    # 🔸 Bungalow
    elif property_type == "bungalow":
        subtype = property_input["bedroom_type"] # e.g. 3_bedroom
        min_val = construction_data["bungalow"][subtype]["min"]
        max_val = construction_data["bungalow"][subtype]["max"]
        cost_per_sqm = get_average(min_val, max_val)

    # 🔸 Storey building
    elif property_type == "storey":
        min_val = construction_data["storey_building"][finish]["min"]
        max_val = construction_data["storey_building"][finish]["max"]
        cost_per_sqm = get_average(min_val, max_val)

    # 🔹 Total building cost
    total_cost = cost_per_sqm * floor_area

    return total_cost, cost_per_sqm

# 🔹 Calculate external works
def calculate_external_works(data, property_input):
   ext = data["external_works"]

   total = 0  # Initialize total cost

   # Pavement
   if property_input.get("paved_courtyard_sqm"):
       total += property_input["paved_courtyard_sqm"] * ext["paved_courtyard"]

   # Fence
   if property_input.get("fence_lenght_m"):
       min_val = ext["fence_wall"]["min"]
       max_val = ext["fence_wall"]["max"]
       avg = get_average(min_val, max_val)
       total += property_input["fence_lenght_m"] * avg

   return total

# 🔹 Calculate services cost
def calculate_services(data, property_input):

    # Soakaway
    if property_input.get("has_soakaway"):
        total += data["services"]["soakaway"]

    return total

# 🔹 Main valuation function
def run_valuation(property_input):
    data = load_market_data()   # Load market data

    # Calculate different components
    building_cost, rate = calculate_building_cost(data, property_input)
    external_cost = calculate_external_works(data, property_input)
    service_cost = calculate_services(data, property_input)

    # Total cost
    total_cost = building_cost + external_cost + service_cost

    # Return structured result
    return {
        "building_cost": building_cost,
        "external_cost": external_cost,
        "service_cost": service_cost,
        "rate_per_sqm": rate,
        "total_estimated_cost": total_cost
    }
