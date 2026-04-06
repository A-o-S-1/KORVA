import os
import json
from engine.valuation_engine import run_valuation

base_path = "../data/properties/"

# loop through all location folders
for location in os.listdir(base_path):
    location_path = os.path.join(base_path, location)

    if os.path.isdir(location_path):
        print(f"\n📍 LOCATION: {location.upper()}")

        # Loop through properties in each location
        for file in os.listdir(location_path):
            if file.endswith(".json"):
                file_path = os.path.join(location_path, file)

                with open(file_path, "r") as f:
                    property_input = json.load(f)

                result = run_valuation(property_input)

                print(f"\n--- {file} ---")
                print(f"Total Cost: ₦{result['total_estimated_cost']:,}")
