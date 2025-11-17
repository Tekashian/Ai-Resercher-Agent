"""
Test Google Gemini Integration
Verifies that Gemini API is properly configured and working
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 70)
print("🧪 Google Gemini 2.0 Flash - Integration Test")
print("=" * 70)
print()

# Test 1: Import Gemini SDK
print("1️⃣ Testing Gemini SDK import...")
try:
    import google.generativeai as genai
    print("   ✅ google-generativeai imported successfully")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    sys.exit(1)

print()

# Test 2: Load configuration
print("2️⃣ Testing configuration...")
try:
    from config.settings import settings
    
    print(f"   Model: {settings.GEMINI_MODEL}")
    
    if settings.GEMINI_API_KEY:
        masked = settings.GEMINI_API_KEY[:12] + "..." + settings.GEMINI_API_KEY[-4:]
        print(f"   ✅ API Key: {masked}")
    else:
        print("   ❌ API Key not configured")
        sys.exit(1)
        
except Exception as e:
    print(f"   ❌ Configuration error: {e}")
    sys.exit(1)

print()

# Test 3: Initialize AIAgent
print("3️⃣ Testing AIAgent initialization...")
try:
    from backend.src.services.agent import AIAgent
    
    agent = AIAgent()
    print("   ✅ AIAgent initialized successfully")
    
except Exception as e:
    print(f"   ❌ AIAgent initialization failed: {e}")
    sys.exit(1)

print()

# Test 4: Test simple Gemini API call
print("4️⃣ Testing Gemini API connection...")
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    response = model.generate_content("Say 'Hello from Gemini!' in JSON format with a 'message' field.")
    
    print(f"   ✅ API Response received")
    print(f"   Response preview: {response.text[:100]}...")
    
except Exception as e:
    print(f"   ❌ API call failed: {e}")
    sys.exit(1)

print()

# Test 5: Test analyze_topic method
print("5️⃣ Testing analyze_topic method...")
try:
    import asyncio
    
    async def test_analysis():
        result = await agent.analyze_topic(
            topic="Test topic: Benefits of AI",
            context="AI has many benefits including automation and efficiency.",
            depth=1
        )
        return result
    
    result = asyncio.run(test_analysis())
    
    print("   ✅ analyze_topic executed successfully")
    print(f"   Summary: {result.get('summary', 'N/A')[:80]}...")
    print(f"   Key findings count: {len(result.get('key_findings', []))}")
    print(f"   Metadata: {result.get('metadata', {})}")
    
except Exception as e:
    print(f"   ❌ Analysis failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 70)
print("🎉 All Gemini Integration Tests Passed!")
print("=" * 70)
print()
print("Summary:")
print("  ✅ Gemini SDK imported")
print("  ✅ Configuration loaded")
print("  ✅ AIAgent initialized")
print("  ✅ API connection verified")
print("  ✅ Analysis method working")
print()
print(f"🤖 Model: {settings.GEMINI_MODEL}")
print("🚀 Ready to use Google Gemini 2.0 Flash!")
print()
