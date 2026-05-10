import json # Used to load JSON data filed
import os  # Used to handle file paths reliably across different operating systems
import re

# 🔹 Load market data (Calabar)
def load_market_data():
    # 🔹 Get current file directory (engine folder)
    base_dir = os.path.dirname(__file__)

    # 🔹 Build correct path to market data
    data_path = os.path.join(base_dir, "../data/market/calabar_data.json")

    # 🔹 Normalize path (important for Windows)
    data_path = os.path.abspath(data_path)

    # 🔹 Open file
    with open(data_path, "r") as file:
        data = json.load(file)

    return data

# 🔹 Get average from range
def get_average(min_val, max_val):
    # Simple average calculation
    return (min_val + max_val) / 2



# 🔹 Calculate building cost            (🔹 COST METHOD)
def calculate_building_cost(data, property_input):
    construction_data = data["construction"] #Extract Construction data

    property_type = property_input["property_type"] 
    floor_area = property_input["floor_area_sqm"]
    finish = property_input["finish_level"]

     # 🔥 LAND CHECK
    if property_type == "land":
        return 0, 0

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
   if property_input.get("fence_length_m"):
       min_val = ext["fence_wall"]["min"]
       max_val = ext["fence_wall"]["max"]
       avg = get_average(min_val, max_val)
       total += property_input["fence_length_m"] * avg

   return total

# 🔹 Calculate services cost
def calculate_services(data, property_input):
    total = 0  # 🔹 Initialize total BEFORE using it

    # Soakaway
    if property_input.get("has_soakaway"):
        total += data["services"]["soakaway"]

    return total # 🔹 Always return the value



# 🔹            (💰 Investment Method)
def calculate_investment_value(raw_data):
    subject = raw_data["subject"]
    rental = subject.get("Rental Information", {})

    try:
        units = int(rental.get("Number of Units", 0))
        rent = int(str(rental.get("Annual Rent Per Unit", "0")).replace("₦", "").replace(",", ""))
        occupancy = float(str(rental.get("Estimated Occupancy Rate", "0")).replace("%", "")) / 100

        gross_income = units * rent
        effective_income = gross_income * occupancy

        cap_rate = 0.08

        return effective_income / cap_rate

    except:
        return None




# 🔹             (📊 Comparative Method)
def calculate_comparative_value(raw_data):
    subject = raw_data["subject"]
                
                # 🔹 Get surrounding property prices
    price_data = subject.get("Price of Surrounding properties", "")
    prices = re.findall(r"₦?\d[\d,]*", price_data) # 🔹 Extract prices properly


                # 🔹 No comparable data found
    if not prices:
        return None
    

                # 🔹 Clean extracted prices
    cleaned_prices = []

    for p in prices:
        
        # Convert to string first
        p = (
            str(p)
            # Remove commas, currency symbols, spaces
            .replace("₦", "")
            .replace(",", "")
            .strip()
        )

        # Convert to integer
        cleaned_prices.append(int(p))

    # 🔹 Calculate average comparable value
    average_price = (
        sum(cleaned_prices)
        / len(cleaned_prices)
    )

    return average_price



# 🔹                🏗️ Residual Method
def calculate_residual_value(cost_value):
    developer_margin = 0.25
    return cost_value * (1 - developer_margin)



# 🔹                🔧 Market Adjustment
def apply_market_adjustment(cost_value, comparative_value):
    if comparative_value:
        return (cost_value * 0.6) + (comparative_value * 0.4)
    return cost_value


# 🔹 5. METHOD SELECTOR
def select_valuation_method(raw_data):
    desc = raw_data["subject"]["Description of property"].lower()

                     # Investment-related properties
    if any(x in desc for x in[
        "flat",
        "tenement",
        "shop",
        "office",
        "commercial",
        "mixed-use",
        "retail"
    ]):
        return "investment"

                     # Land properties
                    # 🔹 Bare land 
    elif "bare land" in desc:
            return "comparative"
    
                    # 🔹 Developed land
    elif "developed land" in desc:
        return "residual"
    
                    # 🔹 Hotels / business operations
    elif any(x in desc for x in [
        "hotel",
        "school",
        "petrol station"
    ]):
        return "profit"

                    # 🔹 Default residential
    return "cost"



# 🔹 Main valuation function
def run_valuation(property_input, raw_data):
    data = load_market_data()   # Load market data

    method = select_valuation_method(raw_data)  # 🔹 Determine valuation method

            # 🔹 Base result structure
    result = {
        "method_used": method
    }

    # ==========================================
    # 🧱 COST METHOD
    # ==========================================
    if method == "cost":
        building_cost, rate = calculate_building_cost(data, property_input)
        external_cost = calculate_external_works(data, property_input)
        service_cost = calculate_services(data, property_input)

        cost_total = (
            building_cost +
            external_cost +
            service_cost
        )

        comparative_value = calculate_comparative_value(raw_data)

        # 🔥 Blend market reality with cost
        final_value = apply_market_adjustment(
            cost_total, 
            comparative_value
        )

        result.update({
            "building_cost": building_cost,
            "external_cost": external_cost,
            "service_cost": service_cost,
            "rate_per_sqm": rate,
            "cost_total": cost_total,
            "comparative_value": comparative_value,
            "final_value": final_value
        })

    # ==========================================
    # 💰 INVESTMENT METHOD
    # ==========================================
    elif method == "investment":

        investment_value = calculate_investment_value(raw_data)

        result.update({
            "investment_value": investment_value,
            "final_value": investment_value
        })


    # ==========================================
    # 🏗️ RESIDUAL METHOD
    # ==========================================
    elif method == "residual":
        building_cost, rate = calculate_building_cost(data, property_input)
        
        external_cost = calculate_external_works(data, property_input)
       
        service_cost = calculate_services(data, property_input)

        cost_total = (
            building_cost +
            external_cost +
            service_cost
        )

        residual_value = calculate_residual_value(cost_total)

        result.update({
            "cost_value": cost_total,
            "residual_value": residual_value,
            "final_value": residual_value
        })


    # ==========================================
    # ⚠️ FALLBACK
    # ==========================================
    else:

        result.update({
            "final_value": None
        })

    return result
            