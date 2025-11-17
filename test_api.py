"""
Test API with Gemini Integration
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_root():
    """Test root endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Root Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def test_research():
    """Test research endpoint with Gemini"""
    print("\n" + "="*60)
    print("TEST 3: Research with Gemini AI")
    print("="*60)
    
    try:
        payload = {
            "topic": "Python programming best practices",
            "max_results": 3
        }
        
        print(f"Sending request: {json.dumps(payload, indent=2)}")
        print("This may take 10-30 seconds...")
        
        response = requests.post(
            f"{BASE_URL}/research",
            json=payload,
            timeout=60
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nResearch ID: {data.get('research_id')}")
            print(f"Topic: {data.get('topic')}")
            print(f"Status: {data.get('status')}")
            print(f"\nSummary:\n{data.get('summary')}")
            print(f"\nKey Findings ({len(data.get('key_findings', []))}):")
            for i, finding in enumerate(data.get('key_findings', []), 1):
                print(f"  {i}. {finding}")
            print(f"\nSources ({len(data.get('sources', []))}):")
            for source in data.get('sources', []):
                print(f"  - {source}")
            return True
        else:
            print(f"ERROR Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI RESEARCH AGENT - GEMINI INTEGRATION TEST")
    print("="*60)
    
    results = []
    
    # Test 1: Health
    results.append(("Health Check", test_health()))
    
    # Test 2: Root
    results.append(("Root Endpoint", test_root()))
    
    # Test 3: Research with Gemini
    results.append(("Research with Gemini", test_research()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    total = len(results)
    passed_count = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed_count}/{total} tests passed")
    print("="*60 + "\n")
    
    return all(p for _, p in results)


if __name__ == "__main__":
    # Wait for server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        exit(1)
