#!/usr/bin/env python3
"""
Test script to verify all dependencies are installed correctly
"""

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import requests
        print("✅ requests - OK")
        
        import bs4
        print("✅ beautifulsoup4 - OK")
        
        import openai
        print("✅ openai - OK")
        
        from dotenv import load_dotenv
        print("✅ python-dotenv - OK")
        
        from urllib.parse import urljoin, urlparse
        print("✅ urllib - OK")
        
        print("\n🎉 All dependencies are installed correctly!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_env_file():
    """Test if .env file exists and has the required structure"""
    import os
    
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            if api_key == 'your_openai_api_key_here':
                print("⚠️  Please update your OpenAI API key in .env file")
            else:
                print("✅ OpenAI API key configured")
        else:
            print("❌ OPENAI_API_KEY not found in .env file")
    else:
        print("❌ .env file not found")
        print("Please create .env file from .env.example and add your OpenAI API key")

if __name__ == "__main__":
    print("🧪 Testing SEO Analyzer Setup")
    print("=" * 40)
    
    test_imports()
    print()
    test_env_file()
    
    print("\n📋 Next steps:")
    print("1. Make sure you have created .env file with your OpenAI API key")
    print("2. Run: python seo_analyzer.py")
    print("3. Enter a website URL when prompted")