"""
Example script to test the AI Research Agent API
Run this after starting the server with: python backend/main.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test if API is running"""
    print("🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ API is healthy!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Health check failed: {response.status_code}")
    print()


def test_root_endpoint():
    """Test root endpoint"""
    print("🔍 Testing root endpoint...")
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        print("✅ Root endpoint working!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Root endpoint failed: {response.status_code}")
    print()


def conduct_research(topic, depth=3, max_results=5):
    """Conduct research on a topic"""
    print(f"🔍 Conducting research on: {topic}")
    
    payload = {
        "topic": topic,
        "depth": depth,
        "max_results": max_results
    }
    
    response = requests.post(f"{BASE_URL}/research", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Research completed!")
        print(f"Research ID: {data['research_id']}")
        print(f"Status: {data['status']}")
        print(f"\nSummary:\n{data.get('summary', 'N/A')}")
        print(f"\nKey Findings:")
        for i, finding in enumerate(data.get('key_findings', []), 1):
            print(f"  {i}. {finding}")
        print(f"\nSources found: {len(data.get('sources', []))}")
        return data['research_id']
    else:
        print(f"❌ Research failed: {response.status_code}")
        print(response.text)
        return None


def generate_report(research_id):
    """Generate PDF report"""
    print(f"\n📄 Generating report for research: {research_id}")
    
    payload = {
        "research_id": research_id,
        "format": "pdf",
        "include_sources": True
    }
    
    response = requests.post(f"{BASE_URL}/report", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Report generated!")
        print(f"Report ID: {data['report_id']}")
        print(f"File path: {data['file_path']}")
        print(f"Download URL: {BASE_URL}{data['download_url']}")
        return data
    else:
        print(f"❌ Report generation failed: {response.status_code}")
        print(response.text)
        return None


def get_history(limit=5):
    """Get research history"""
    print(f"\n📜 Retrieving research history (limit: {limit})...")
    response = requests.get(f"{BASE_URL}/history?limit={limit}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['count']} research entries")
        for entry in data['research']:
            print(f"  - {entry['research_id']}: {entry['metadata'].get('topic', 'N/A')}")
    else:
        print(f"❌ History retrieval failed: {response.status_code}")


def main():
    """Main test function"""
    print("=" * 60)
    print("🧠 AI Research Agent - API Test Script")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    test_health_check()
    
    # Test 2: Root endpoint
    test_root_endpoint()
    
    # Test 3: Conduct research (REQUIRES API KEYS!)
    # Uncomment to test with real API keys
    """
    research_id = conduct_research(
        topic="Recent advances in artificial intelligence and machine learning",
        depth=3,
        max_results=5
    )
    
    if research_id:
        time.sleep(2)  # Wait a bit
        
        # Test 4: Generate report
        generate_report(research_id)
        
        time.sleep(1)
        
        # Test 5: Get history
        get_history(limit=5)
    """
    
    print("\n" + "=" * 60)
    print("⚠️  To test research and report generation, you need to:")
    print("1. Add your API keys to .env file:")
    print("   - OPENAI_API_KEY")
    print("   - TAVILY_API_KEY")
    print("2. Uncomment the research test code above")
    print("3. Run this script again")
    print("=" * 60)


if __name__ == "__main__":
    main()
