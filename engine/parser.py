# 🔹 This file converts raw property JSON into engine-ready format
def parse_property(raw_data):
    subject = raw_data["subject"]

    description = subject["Description of property"].lower()

     # 🔸 Detect property type from description
    if "bungalow" in description:
        property_type = "bungalow"
    elif "duplex" in description:
        property_type = "duplex"
    else:
        property_type = "bungalow" # default fallback

    # 🔸 Detect bedroom type
    if "2-bedroom" in description:
        bedroom_type = "2_bedroom"
    elif "3-bedroom" in description:
        bedroom_type = "3_bedroom"
    elif "4-bedroom" in description:
        bedroom_type = "4_bedroom"
    else:
        bedroom_type = "3_bedroom" # default fallback

    # 🔸 Extract sqm (convert string to int)
    floor_area = int(subject["Sqm"]) # (Total Square meters that is plus the building if any)"

    # 🔸 Default finish (can improve later)
    finish = "standard"

    # 🔸 External works detection
    amemities = subject["Amenities in that property"].lower()

    has_fence = "fence" in amemities
    has_borehole = "borehole" in amemities
    
     # 🔹 Return clean structure for engine
    return {
        "property_type": property_type,
        "bedroom_type": bedroom_type,
        "floor_area_sqm": floor_area,
        "finish_level": finish,

        # extras (optional for now)
        "paved_courtyard_sqm": 0, # Placeholder, can extract from description if needed
        "fence_lenght_m": 0, # Placeholder, can extract from description if needed
        "has_soakaway": True # assume true for now
    } 
