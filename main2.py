"""
Tavily API Demo Script - Educational Version
============================================
This script demonstrates three AI agents using the Tavily API:
1. Search Agent - Searches the web for information
2. Extract Agent - Extracts content from specific URLs
3. Crawl Agent - Crawls websites to discover content

Perfect for teaching API integration, class design, and error handling in Python!

Author: Python Class Demo
Date: 2025
"""

# Import required libraries
import os          # For accessing environment variables
import json        # For handling JSON data (useful for debugging)
from tavily import TavilyClient  # Tavily's official Python SDK
from dotenv import load_dotenv   # For loading .env files

# Load environment variables from .env file
# This must be called before accessing any environment variables
load_dotenv()


class TavilyAgents:
    """
    A class that encapsulates three different AI agents using Tavily API.
    
    This demonstrates:
    - Object-oriented programming (OOP) principles
    - API integration
    - Error handling
    - Method organization
    """
    
    def __init__(self, api_key=None):
        """
        Constructor: Initializes the TavilyAgents class
        
        Args:
            api_key (str, optional): Your Tavily API key. 
                                     If not provided, will look for TAVILY_API_KEY 
                                     environment variable.
        
        Raises:
            ValueError: If no API key is found
        
        Teaching Notes:
        - __init__ is a special method called when creating a new instance
        - self refers to the instance of the class
        - We use 'or' operator for fallback logic
        """
        # Try to get API key from parameter, otherwise check environment variable
        self.api_key = api_key or os.environ.get('TAVILY_API_KEY')
        
        # Validate that we have an API key (defensive programming)
        if not self.api_key:
            raise ValueError(
                "Please provide TAVILY_API_KEY environment variable "
                "or pass it to the constructor"
            )
        
        # Create an instance of TavilyClient with our API key
        # This client will be used by all our agent methods
        self.client = TavilyClient(api_key=self.api_key)
    
    def search_agent(self, query, max_results=5):
        """
        Search Agent: Performs web search and returns relevant results
        
        This agent demonstrates:
        - Making API calls
        - Processing JSON responses
        - Iterating through results
        - String formatting and slicing
        
        Args:
            query (str): The search query (e.g., "Python programming tutorials")
            max_results (int): Maximum number of results to return (default: 5)
        
        Returns:
            dict: The full response from Tavily API, or None if error occurs
        
        Teaching Notes:
        - We use try-except for error handling (always important with APIs!)
        - enumerate() gives us both index and value when iterating
        - f-strings (f"...") are modern Python string formatting
        - include_raw_content=True gives us the full page content
        """
        # Print a header with emoji for user-friendly output
        print(f"\n🔍 SEARCH AGENT: Searching for '{query}'...\n")
        
        try:
            # Make the API call to Tavily's search endpoint
            # search_depth="advanced" gives us more comprehensive results
            # include_raw_content=True ensures we get full content, not summaries
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced",  # Can be "basic" or "advanced"
                include_raw_content=True  # Get full page content
            )
            
            # Extract the results list from the response dictionary
            # .get() is safer than [] - returns None if key doesn't exist
            results = response.get('results', [])
            
            # Display count of results found
            print(f"Found {len(results)} results:\n")
            
            # Iterate through results with enumerate
            # enumerate(list, 1) starts counting from 1 instead of 0
            for i, result in enumerate(results, 1):
                # Each result is a dictionary with keys like 'title', 'url', 'content'
                print(f"\n{'='*70}")
                print(f"Result #{i}")
                print(f"{'='*70}")
                print(f"📌 Title: {result['title']}")
                print(f"🔗 URL: {result['url']}")
                
                # Show relevance score (if available)
                print(f"⭐ Relevance Score: {result.get('score', 'N/A')}")
                
                # Display FULL content - try raw_content first, then content
                full_content = result.get('raw_content', '') or result.get('content', '')
                content_length = len(full_content)
                print(f"📊 Content Length: {content_length} characters")
                
                print(f"\n📄 Full Content:")
                print(f"{'-'*70}")
                # Print the complete content without truncation
                print(full_content)
                print(f"{'-'*70}")
                print()  # Extra blank line for readability
                
                # Debug: Show what keys are available in the result
                print(f"🔍 Available data fields: {', '.join(result.keys())}")
                print()
            
            # Return the full response for potential further processing
            return response
            
        except Exception as e:
            # Catch any errors (network issues, API errors, etc.)
            # Always good practice to handle exceptions with APIs
            print(f"❌ Error in search: {str(e)}")
            return None
    
    def extract_agent(self, urls):
        """
        Extract Agent: Extracts content from specific URLs
        
        This agent demonstrates:
        - Type checking and conversion
        - List operations
        - Working with API responses containing multiple items
        
        Args:
            urls (list or str): Single URL string or list of URLs to extract from
        
        Returns:
            dict: The extraction response, or None if error occurs
        
        Teaching Notes:
        - isinstance() checks if a variable is of a specific type
        - We normalize input to always work with a list
        - This makes the function more flexible and user-friendly
        """
        # Type checking: if urls is a string, convert it to a list
        # This allows users to pass either "url" or ["url1", "url2"]
        if isinstance(urls, str):
            urls = [urls]  # Wrap single URL in a list
        
        # Display what we're doing
        print(f"\n📄 EXTRACT AGENT: Extracting content from {len(urls)} URL(s)...\n")
        
        try:
            # Call Tavily's extract API to get content from the URLs
            response = self.client.extract(urls=urls)
            
            # Process each result
            for i, result in enumerate(response.get('results', []), 1):
                print(f"\n{'='*70}")
                print(f"Extraction #{i}")
                print(f"{'='*70}")
                print(f"🔗 URL: {result['url']}")
                print(f"📌 Title: {result.get('title', 'N/A')}")
                
                # Get the full raw content
                raw_content = result.get('raw_content', '')
                print(f"📊 Content Length: {len(raw_content)} characters")
                
                # Display FULL content instead of preview
                print(f"\n📄 Full Extracted Content:")
                print(f"{'-'*70}")
                print(raw_content)
                print(f"{'-'*70}")
                print()  # Empty line for readability
            
            return response
            
        except Exception as e:
            # Handle any errors that occur during extraction
            print(f"❌ Error in extraction: {str(e)}")
            return None
    
    def crawl_agent(self, url, max_depth=2):
        """
        Crawl Agent: Crawls a website and discovers linked pages
        
        This agent demonstrates:
        - Web crawling concepts
        - Working with nested data structures
        - Extracting and displaying structured information
        
        Args:
            url (str): Starting URL to begin crawling from
            max_depth (int): How many levels deep to crawl (not fully implemented 
                           in basic Tavily API, shown for educational purposes)
        
        Returns:
            dict: The crawl response, or None if error occurs
        
        Teaching Notes:
        - Web crawling means following links from page to page
        - max_depth prevents infinite crawling
        - Real crawlers need to respect robots.txt and rate limits
        """
        print(f"\n🕷️ CRAWL AGENT: Crawling '{url}' (depth: {max_depth})...\n")
        
        try:
            # Note: Tavily's basic API has limited crawling
            # We use extract with additional options as a demonstration
            response = self.client.extract(
                urls=[url],
                include_raw_content=True  # Get full page content
            )
            
            # Check if we got results back
            # 'and' short-circuits: if response is None, doesn't check .get()
            if response and response.get('results'):
                # Get the first result (main page)
                result = response['results'][0]
                
                # Display information about the crawled page
                print(f"\n{'='*70}")
                print(f"📍 Main Page: {result['url']}")
                print(f"{'='*70}")
                print(f"📌 Title: {result.get('title', 'N/A')}")
                
                # Get the full content
                full_content = result.get('raw_content', '')
                content_length = len(full_content)
                print(f"📊 Content extracted: {content_length} characters")
                
                # Display FULL content instead of preview
                print(f"\n📄 Full Crawled Content:")
                print(f"{'-'*70}")
                print(full_content)
                print(f"{'-'*70}")
            
            return response
            
        except Exception as e:
            # Error handling - always important with external APIs
            print(f"❌ Error in crawling: {str(e)}")
            return None


def main():
    """
    Main function: Entry point of the program
    
    This demonstrates:
    - Program structure and flow control
    - User input handling
    - Menu-driven interfaces
    - While loops for continuous operation
    
    Teaching Notes:
    - main() is a common convention for the program's entry point
    - We use while True for an infinite loop that runs until user chooses to exit
    - The menu pattern is common in CLI applications
    """
    # Print a nice header using string multiplication for the line
    print("=" * 60)
    print("🤖 TAVILY API DEMO - Three Agent System")
    print("=" * 60)
    
    # Debug: Check if API key is loaded
    api_key = os.environ.get('TAVILY_API_KEY')
    if api_key:
        print(f"✅ API Key loaded: {api_key[:10]}..." if len(api_key) > 10 else "✅ API Key loaded")
    else:
        print("❌ No API key found in environment variables")
        print("\n🔍 Debugging Info:")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   .env file exists: {os.path.exists('.env')}")
        if os.path.exists('.env'):
            print("\n   Contents of .env file:")
            with open('.env', 'r') as f:
                for line in f:
                    if 'TAVILY' in line:
                        print(f"   {line.strip()}")
    
    # Try to initialize our agents
    try:
        agents = TavilyAgents()
    except ValueError as e:
        # If initialization fails (no API key), show helpful error message
        print(f"\n❌ {str(e)}")
        print("\nTo use this script:")
        print("1. Get an API key from https://tavily.com")
        print("2. Create a .env file in the same directory as this script")
        print("3. Add this line to .env (NO SPACES around =):")
        print("   TAVILY_API_KEY=tvly-your-key-here")
        print("\n4. Make sure python-dotenv is installed:")
        print("   pip install python-dotenv")
        return  # Exit the function early
    
    # Main program loop - runs until user chooses to exit
    while True:
        # Display menu options
        print("\n" + "=" * 60)
        print("Select an agent:")
        print("1. 🔍 Search Agent - Search the web")
        print("2. 📄 Extract Agent - Extract content from URL(s)")
        print("3. 🕷️ Crawl Agent - Crawl a website")
        print("4. 🚪 Exit")
        print("=" * 60)
        
        # Get user input and remove any extra whitespace
        choice = input("\nEnter your choice (1-4): ").strip()
        
        # Process user's choice using if-elif-else structure
        if choice == '1':
            # SEARCH AGENT
            query = input("\nEnter search query: ").strip()
            if query:  # Only proceed if user entered something
                agents.search_agent(query)
            else:
                print("❌ Search query cannot be empty!")
        
        elif choice == '2':
            # EXTRACT AGENT
            url_input = input("\nEnter URL(s) (comma-separated for multiple): ").strip()
            if url_input:
                # Split input by commas and strip whitespace from each URL
                # List comprehension: [expression for item in iterable]
                urls = [u.strip() for u in url_input.split(',')]
                agents.extract_agent(urls)
            else:
                print("❌ URL cannot be empty!")
        
        elif choice == '3':
            # CRAWL AGENT
            url = input("\nEnter URL to crawl: ").strip()
            if url:
                agents.crawl_agent(url)
            else:
                print("❌ URL cannot be empty!")
        
        elif choice == '4':
            # EXIT
            print("\n👋 Goodbye!")
            break  # Exit the while loop
        
        else:
            # Invalid input handling
            print("\n❌ Invalid choice. Please select 1-4.")
        
        # Pause before showing menu again
        # This gives user time to read the output
        input("\nPress Enter to continue...")


# This is a Python idiom that checks if this file is being run directly
# (as opposed to being imported as a module)
if __name__ == "__main__":
    # If running directly, call the main function
    main()


    """Notes: Steps to Increase Terminal Buffer in VS Code
Open Settings:
Press Ctrl + , (or Cmd + , on macOS), or go to File > Preferences > Settings.
Search for Terminal Scrollback:
In the search bar at the top, type: terminal scrollback.
Adjust the Value:

Look for Terminal › Integrated: Scrollback.
The default is usually 1000 lines. You can increase it to a higher number like 10000 
or more depending on your needs"""