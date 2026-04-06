from engine.valuation_engine import run_valuation

# 🔹 Sample property input
property_input = {
    "property_type": "duplex",
    "floor_area_sqm": 300,
    "finish_level": "standard",

    "paved_courtyard_sqm": 120,
    "fence_length_m": 80,
    "has_soakaway": True
}
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


