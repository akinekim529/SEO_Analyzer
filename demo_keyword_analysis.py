#!/usr/bin/env python3
"""
Demo script for Comprehensive Keyword Analysis Tool
Shows how to use the keyword analysis functionality
"""

import os
import sys
from comprehensive_keyword_tool import ComprehensiveKeywordTool

def demo_text_analysis():
    """Demo text analysis functionality"""
    print("🔍 Demo: Text Analysis")
    print("=" * 50)
    
    # Sample text for analysis
    sample_text = """
    Artificial Intelligence and Machine Learning are revolutionizing the way businesses operate. 
    AI technology has become essential for modern companies looking to improve efficiency and productivity. 
    Machine learning algorithms can analyze vast amounts of data to provide valuable insights. 
    Deep learning, a subset of machine learning, uses neural networks to solve complex problems. 
    Natural language processing enables computers to understand and interpret human language. 
    Computer vision allows machines to analyze and understand visual information. 
    The future of AI looks promising with advancements in robotics and automation. 
    Businesses are investing heavily in AI solutions to stay competitive in the market. 
    Data science and analytics play a crucial role in AI development. 
    The integration of AI in various industries is creating new opportunities and challenges.
    """
    
    title = "Artificial Intelligence and Machine Learning in Business"
    description = "An overview of how AI and ML technologies are transforming modern businesses"
    
    tool = ComprehensiveKeywordTool()
    result = tool.analyze_text_comprehensive(sample_text, title, description)
    tool.print_analysis_summary(result)

def demo_url_analysis():
    """Demo URL analysis functionality"""
    print("\n🌐 Demo: URL Analysis")
    print("=" * 50)
    
    # Example URL (you can change this to any URL you want to test)
    test_url = "https://example.com"
    
    print(f"Note: This demo will attempt to analyze {test_url}")
    print("You can modify the test_url variable to analyze any website.")
    
    tool = ComprehensiveKeywordTool()
    result = tool.analyze_url_comprehensive(test_url)
    tool.print_analysis_summary(result)

def demo_competitive_analysis():
    """Demo competitive analysis functionality"""
    print("\n🏆 Demo: Competitive Analysis")
    print("=" * 50)
    
    # Example URLs for competitive analysis
    main_url = "https://example.com"
    competitor_urls = [
        "https://competitor1.com",
        "https://competitor2.com"
    ]
    
    print(f"Note: This demo will analyze {main_url} against competitors")
    print("You can modify the URLs to analyze real websites.")
    
    tool = ComprehensiveKeywordTool()
    result = tool.analyze_url_comprehensive(main_url, True, competitor_urls)
    tool.print_analysis_summary(result)

def main():
    """Main demo function"""
    print("🚀 Comprehensive Keyword Analysis Tool - Demo")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        print("\nFor demo purposes, you can create a .env file with:")
        print("echo 'OPENAI_API_KEY=your_actual_api_key_here' > .env")
        return
    
    print("Choose a demo to run:")
    print("1. Text Analysis Demo (recommended for testing)")
    print("2. URL Analysis Demo")
    print("3. Competitive Analysis Demo")
    print("4. Run all demos")
    
    try:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            demo_text_analysis()
        elif choice == '2':
            demo_url_analysis()
        elif choice == '3':
            demo_competitive_analysis()
        elif choice == '4':
            demo_text_analysis()
            demo_url_analysis()
            demo_competitive_analysis()
        else:
            print("❌ Invalid choice. Please run the script again.")
            return
        
        print("\n🎉 Demo completed!")
        print("Check your desktop for the generated analysis folder with all reports.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")
        print("Make sure you have a valid OpenAI API key in your .env file.")

if __name__ == "__main__":
    main()