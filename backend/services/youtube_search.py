from abc import ABC, abstractmethod
from typing import List, Dict

class YouTubeSearchService(ABC):
    @abstractmethod
    def search_videos(self, topic: str, language: str) -> List[Dict]:
        pass

class MockYouTubeSearchService(YouTubeSearchService):
    def __init__(self):
        # Mock database of educational videos
        self.mock_videos = {
            "cpr": [
                {
                    "title": "How to perform CPR - Step by Step",
                    "url": "https://www.youtube.com/watch?v=-NodDryGZI",
                    "channel": "Red Cross",
                    "language": "English"
                },
                {
                    "title": "Sida Loo Sameeyo CPR (Af-Soomaali)",
                    "url": "https://www.youtube.com/watch?v=mock_cpr_somali",
                    "channel": "Somali Health Education",
                    "language": "Somali"
                }
            ],
            "breastfeeding": [
                {
                    "title": "Breastfeeding positions and attachment",
                    "url": "https://www.youtube.com/watch?v=mock_breastfeeding",
                    "channel": "UNICEF",
                    "language": "English"
                }
            ],
            "blood pressure": [
                {
                    "title": "How to Measure Blood Pressure Correctly",
                    "url": "https://www.youtube.com/watch?v=UGoOj_506-o",
                    "channel": "Mayo Clinic",
                    "language": "English"
                },
                {
                    "title": "Sida Loo Cabbiro Cadaadiska Dhiigga (Dhiigkarka)",
                    "url": "https://www.youtube.com/watch?v=mock_bp_somali",
                    "channel": "Somali Medical Association",
                    "language": "Somali"
                }
            ],
            "diabetes": [
                {
                    "title": "Understanding and Managing Diabetes Daily",
                    "url": "https://www.youtube.com/watch?v=mock_diabetes_english",
                    "channel": "Diabetes UK",
                    "language": "English"
                },
                {
                    "title": "Sida Loo Maareeyo Cudurka Macaanka",
                    "url": "https://www.youtube.com/watch?v=mock_diabetes_somali",
                    "channel": "Caafimaadka Bulshada",
                    "language": "Somali"
                }
            ],
            "wound": [
                {
                    "title": "First Aid: Cleaning and Dressing a Wound",
                    "url": "https://www.youtube.com/watch?v=mock_wound_english",
                    "channel": "St John Ambulance",
                    "language": "English"
                },
                {
                    "title": "Sida loo nadiifiyo dhaawaca loona duubo",
                    "url": "https://www.youtube.com/watch?v=mock_wound_somali",
                    "channel": "Gurmadka Degdegga ah",
                    "language": "Somali"
                }
            ]
        }
        
    def search_videos(self, topic: str, language: str) -> List[Dict]:
        results = []
        topic_lower = topic.lower()
        
        # Simple mock search logic
        for key, videos in self.mock_videos.items():
            if key in topic_lower:
                for video in videos:
                    results.append(video)
        
        # Filter/Sort by language preference: 1. User language, 2. Somali, 3. Afaan Oromo, 4. Amharic, 5. English
        def get_lang_score(vid_lang):
            vl = vid_lang.lower()
            ul = language.lower()
            if vl == ul: return 1
            if vl == "somali": return 2
            if vl == "afaan oromo": return 3
            if vl == "amharic": return 4
            if vl == "english": return 5
            return 6
            
        results.sort(key=lambda x: get_lang_score(x["language"]))
        
        return results[:2] # Return max 2 videos as requested

def get_youtube_service() -> YouTubeSearchService:
    return MockYouTubeSearchService()
