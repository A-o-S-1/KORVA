import json
from engine.valuation_engine import run_valuation

# 🔹 Load property file
with open("data/properties/State Housing Estate/Property 1 (Residential Duplex).json", "r") as file:
    property_input = json.load(file)

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


