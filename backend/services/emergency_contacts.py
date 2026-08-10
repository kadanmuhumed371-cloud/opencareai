from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class EmergencyContactService(ABC):
    @abstractmethod
    def lookup_contact(self, location: str, facility_type: Optional[str] = None) -> List[Dict]:
        pass

class MockEmergencyContactService(EmergencyContactService):
    def __init__(self):
        # Mock structured database
        self.db = [
            {
                "id": "1",
                "region": "Somali",
                "zone": "Fafan",
                "woreda": "Jigjiga",
                "town": "Jigjiga",
                "kebele": "01",
                "facility_name": "Jigjiga University Referral Hospital",
                "facility_type": "Hospital",
                "emergency_phone": "+251257755555",
                "alternate_phone": "+251911123456",
                "ambulance_available": True,
                "latitude": 9.35,
                "longitude": 42.8,
                "operating_hours": "24/7",
                "notes": "Main referral hospital",
                "language_support": ["Somali", "Amharic", "English"]
            },
            {
                "id": "2",
                "region": "Oromia",
                "zone": "East Shewa",
                "woreda": "Adama",
                "town": "Adama",
                "kebele": "14",
                "facility_name": "Adama General Hospital",
                "facility_type": "Hospital",
                "emergency_phone": "+251221111111",
                "alternate_phone": "+251922222222",
                "ambulance_available": True,
                "latitude": 8.54,
                "longitude": 39.27,
                "operating_hours": "24/7",
                "notes": "Regional hospital",
                "language_support": ["Afaan Oromo", "Amharic", "English"]
            }
        ]
        
    def lookup_contact(self, location: str, facility_type: Optional[str] = None) -> List[Dict]:
        results = []
        loc_lower = location.lower()
        for record in self.db:
            # Simple text search across location fields
            if (loc_lower in record["region"].lower() or 
                loc_lower in record["zone"].lower() or 
                loc_lower in record["town"].lower() or
                loc_lower in record["woreda"].lower()):
                
                if facility_type:
                    if facility_type.lower() in record["facility_type"].lower():
                        results.append(record)
                else:
                    results.append(record)
                    
        return results

# Factory method to return the active implementation
def get_emergency_service() -> EmergencyContactService:
    # Later, this can return FirebaseEmergencyContactService() or SQLiteEmergencyContactService()
    return MockEmergencyContactService()
