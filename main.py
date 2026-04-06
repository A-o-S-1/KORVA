import json
from engine.valuation_engine import run_valuation
from engine.parser import parse_property # 🔥 new import

# 🔹 Load property file
with open("data/properties/state_housing_estate/property_1_residential_duplex.json", "r") as file:
    raw_data = json.load(file)

# 🔹 Convert raw data → engine format
property_input = parse_property(raw_data)

# 🔹 Run valuation
result = run_valuation(property_input)

# 🔹 Print results
print("=== SVIS VALUATION RESULT ===")
print(f"Building Cost: ₦{int(result['building_cost']):,}")
print(f"External Works: ₦{int(result['external_cost']):,}")
print(f"Services Cost: ₦{int(result['service_cost']):,}")
print(f"Rate per sqm: ₦{int(result['rate_per_sqm']):,}")
print(f"Total Cost: ₦{int(result['total_estimated_cost']):,}")

# “Let’s integrate prompts” Prompt-based (manual testing first, no API)


