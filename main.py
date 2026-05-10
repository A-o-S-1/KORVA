import os
import json
from engine.valuation_engine import run_valuation
from engine.parser import parse_property # 🔥 new import

BASE_PATH = "data/properties/"

# 🔹 List all properties
def list_properties():
    properties = []

    for location in os.listdir(BASE_PATH):
        location_path = os.path.join(BASE_PATH, location)

        if os.path.isdir(location_path):
            for file in os.listdir(location_path):
                if file.endswith(".json"):
                    full_path = os.path.join(location_path, file)
                    properties.append((location, file, full_path))

    return properties

# 🔹 Display menu
def show_menu(properties):
    print("\n=== SELECT PROPERTY TO TEST ===\n")

    for i, (location, file, _) in enumerate(properties):
        print(f"{i + 1}. {location} → {file}")

    choice = int(input("\nEnter number:")) - 1
    return properties[choice][2]


# 🔹 MAIN FLOW
properties = list_properties()

if not properties:
    print("No property files found.")
    exit()

selected_file =  show_menu(properties)

# 🔹 Load selected property
with open(selected_file, "r") as file:
    raw_data = json.load(file)

# 🔹 Convert raw data → engine format
property_input = parse_property(raw_data)

# 🔹 Run valuation
result = run_valuation(property_input, raw_data)

# 🔹 Print results
print("\n=== SVIS VALUATION RESULT ===")

print(f"Method Used: {result['method_used']}")

if result.get("building_cost") is not None:
    print(f"Building Cost: ₦{int(result['building_cost']):,}")

if result.get("external_cost") is not None:
    print(f"External Works: ₦{int(result['external_cost']):,}")

if result.get("service_cost") is not None:
    print(f"Services Cost: ₦{int(result['service_cost']):,}")

if result.get("cost_value") is not None:
    print(f"Cost Value: ₦{int(result['cost_value']):,}")

if result.get("investment_value") is not None:
    print(f"Investment Value: ₦{int(result['investment_value']):,}")

if result.get("comparative_value") is not None:
    print(f"Comparative Value: ₦{int(result['comparative_value']):,}")

if result.get("residual_value") is not None:
    print(f"Residual Value: ₦{int(result['residual_value']):,}")

if result.get("final_value") is not None:
    print(f"Final Value: ₦{int(result['final_value']):,}")

# “Let’s integrate prompts” Prompt-based (manual testing first, no API)


