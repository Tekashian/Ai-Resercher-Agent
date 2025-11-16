"""
Diagnostic script to check if all dependencies are installed correctly
"""

import sys

def check_import(module_name, display_name=None):
    """Check if a module can be imported"""
    if display_name is None:
        display_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {display_name}")
        return True
    except ImportError as e:
        print(f"❌ {display_name} - {str(e)}")
        return False


def main():
    """Run diagnostic checks"""
    print("=" * 60)
    print("🔍 AI Research Agent - Dependency Check")
    print("=" * 60)
    print()
    
    print(f"Python Version: {sys.version}")
    print()
    
    print("Checking dependencies...")
    print("-" * 60)
    
    checks = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("pydantic_settings", "Pydantic Settings"),
        ("openai", "OpenAI"),
        ("tavily", "Tavily"),
        ("chromadb", "ChromaDB"),
        ("sentence_transformers", "Sentence Transformers"),
        ("reportlab", "ReportLab"),
        ("PIL", "Pillow"),
        ("dotenv", "Python-dotenv"),
        ("httpx", "HTTPX"),
        ("pytest", "Pytest"),
    ]
    
    passed = 0
    failed = 0
    
    for module, name in checks:
        if check_import(module, name):
            passed += 1
        else:
            failed += 1
    
    print("-" * 60)
    print()
    
    # Check project structure
    print("Checking project structure...")
    print("-" * 60)
    
    import os
    
    paths_to_check = [
        ("backend/main.py", "Main FastAPI app"),
        ("backend/src/services/agent.py", "AI Agent"),
        ("backend/src/services/search.py", "Web Search"),
        ("backend/src/services/vector_store.py", "Vector Store"),
        ("backend/src/services/pdf_generator.py", "PDF Generator"),
        ("backend/src/models/schemas.py", "Data Models"),
        ("config/settings.py", "Settings"),
        (".env", "Environment file"),
        ("requirements.txt", "Requirements"),
    ]
    
    for path, name in paths_to_check:
        if os.path.exists(path):
            print(f"✅ {name} ({path})")
        else:
            print(f"❌ {name} ({path}) - NOT FOUND")
    
    print("-" * 60)
    print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"Dependencies: {passed} passed, {failed} failed")
    print()
    
    if failed == 0:
        print("✅ All checks passed! You're ready to start the server.")
        print()
        print("Next steps:")
        print("1. Add your API keys to .env file")
        print("2. Run: python start.py")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print("❌ Some checks failed. Please run:")
        print("   pip install -r requirements.txt")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
