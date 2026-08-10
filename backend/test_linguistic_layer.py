import sys
import os

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from linguistic_engine.pipeline import process_somali_medical_response

def test_pipeline():
    test_cases = [
        "wahid jooji dhiigga",
        "dhaawac culus ayaa jira",
        "dhakhtar degdeg ah u wac",
        "Bukaanku wuxuu qabaa hypertension iyo fracture."
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"--- Test Case {i} ---")
        print(f"Input: {case}")
        output = process_somali_medical_response(case)
        # Use encode/decode to avoid console cp1252 errors on Windows
        print(f"Output SSML:\n{output.encode('utf-8', 'replace').decode('utf-8')}\n")

if __name__ == "__main__":
    test_pipeline()
