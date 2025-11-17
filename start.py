"""
Quick start script for AI Research Agent
"""

import subprocess
import sys
import os

def check_env_file():
    """Check if .env file exists and has required keys"""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("📝 Creating .env from .env.example...")
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ .env file created")
            print("\n⚠️  IMPORTANT: Edit .env and add your API keys:")
            print("   - GEMINI_API_KEY")
            print("   - TAVILY_API_KEY")
            return False
    
    # Check if keys are set
    with open('.env', 'r') as f:
        content = f.read()
        if 'GEMINI_API_KEY=' in content and 'GEMINI_API_KEY=your_gemini_api_key_here' not in content:
            if 'TAVILY_API_KEY=' in content:
                return True
    
    print("⚠️  API keys not configured in .env file")
    print("Please add your API keys to .env:")
    print("   - GEMINI_API_KEY=your_gemini_key")
    print("   - TAVILY_API_KEY=your_tavily_key")
    return False


def start_server():
    """Start the FastAPI server"""
    print("\n" + "=" * 60)
    print("🚀 Starting AI Research Agent Server")
    print("=" * 60)
    print()
    
    if not check_env_file():
        print("\n" + "=" * 60)
        print("Setup required before starting server")
        print("=" * 60)
        return
    
    print("✅ Configuration OK")
    print("\n📡 Server will be available at:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "backend.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")


if __name__ == "__main__":
    start_server()
