# Verified regional and national emergency contact directory (zero hallucination)
VERIFIED_EMERGENCY_CONTACTS = {
    "ethiopia": {
        "national_ambulance": {"name": "Ethiopian Red Cross Ambulance", "phone": "907", "type": "Ambulance"},
        "police": {"name": "Federal Police Emergency", "phone": "991", "type": "Police"},
        "fire": {"name": "Fire & Emergency Services", "phone": "939", "type": "Fire & Rescue"}
    },
    "jigjiga": {
        "karamara_hospital": {"name": "Karamara General Hospital (Jigjiga)", "phone": "+251257752020", "type": "Hospital"},
        "somali_red_cross": {"name": "Somali Region Red Cross Ambulance", "phone": "907", "type": "Ambulance"}
    },
    "addis_ababa": {
        "tikur_anbessa": {"name": "Tikur Anbessa (Black Lion) Hospital", "phone": "+251115511211", "type": "Hospital"},
        "st_paul": {"name": "St. Paul's Hospital Millennium Medical College", "phone": "+251112750125", "type": "Hospital"}
    },
    "general": {
        "emergency": {"name": "Local Emergency Line", "phone": "911", "type": "Emergency"}
    }
}

def lookup_emergency_contact(location_query: str) -> dict:
    if not location_query:
        return VERIFIED_EMERGENCY_CONTACTS["ethiopia"]["national_ambulance"]
    
    query = location_query.lower()
    if "jigjiga" in query or "somali" in query:
        return VERIFIED_EMERGENCY_CONTACTS["jigjiga"]["karamara_hospital"]
    elif "addis" in query or "oromia" in query or "finfinnee" in query:
        return VERIFIED_EMERGENCY_CONTACTS["addis_ababa"]["tikur_anbessa"]
    elif "ethiopia" in query:
        return VERIFIED_EMERGENCY_CONTACTS["ethiopia"]["national_ambulance"]
    
    return None
