#!/usr/bin/env python3
"""
YouTube Channel Video Finder
A Python application that runs a hidden browser to search YouTube for videos from specific channels.
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import urllib.parse

class YouTubeChannelFinder:
    def __init__(self, headless=True):
        """
        Initialize the YouTube Channel Finder
        
        Args:
            headless (bool): Run browser in headless mode (hidden)
        """
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        # Additional options for better performance and stealth
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Disable images and CSS for faster loading
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Browser initialized successfully")
        except Exception as e:
            print(f"❌ Error initializing browser: {e}")
            print("Please make sure Chrome and ChromeDriver are installed")
            sys.exit(1)
    
    def search_youtube(self, topic, channel_name):
        """
        Search YouTube for videos from a specific channel
        
        Args:
            topic (str): Search topic
            channel_name (str): Channel name to filter by
            
        Returns:
            bool: True if video was found and clicked, False otherwise
        """
        try:
            # Construct search query
            search_query = f"{topic} {channel_name}"
            encoded_query = urllib.parse.quote(search_query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            
            print(f"🔍 Searching for: {search_query}")
            print(f"🌐 Navigating to: {search_url}")
            
            # Navigate to YouTube search results
            self.driver.get(search_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Scroll down to load more results
            self.scroll_to_load_more()
            
            # Find videos from the specified channel
            return self.find_and_click_channel_video(channel_name)
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            return False
    
    def scroll_to_load_more(self, scroll_count=3):
        """Scroll down to load more search results"""
        print("📜 Scrolling to load more results...")
        
        for i in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            print(f"   Scroll {i+1}/{scroll_count} completed")
    
    def find_and_click_channel_video(self, channel_name):
        """
        Find and click on a video from the specified channel
        
        Args:
            channel_name (str): Name of the channel to look for
            
        Returns:
            bool: True if video was found and clicked, False otherwise
        """
        try:
            print(f"🎯 Looking for videos from channel: {channel_name}")
            
            # Wait for videos to load
            wait = WebDriverWait(self.driver, 10)
            
            # Find all video elements
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, "a#video-title")
            
            if not video_elements:
                print("❌ No video elements found")
                return False
            
            print(f"📹 Found {len(video_elements)} videos")
            
            # Iterate through videos to find one from the target channel
            for i, video in enumerate(video_elements[:20]):  # Check first 20 videos
                try:
                    # Get video title
                    video_title = video.get_attribute("title") or video.text
                    
                    # Find the parent container to look for channel name
                    parent = video.find_element(By.XPATH, "./ancestor::ytd-video-renderer")
                    
                    # Look for channel name in various possible locations
                    channel_element = None
                    channel_selectors = [
                        "#channel-name a",
                        "#channel-name",
                        "ytd-channel-name a",
                        "ytd-channel-name"
                    ]
                    
                    for selector in channel_selectors:
                        try:
                            channel_element = parent.find_element(By.CSS_SELECTOR, selector)
                            break
                        except NoSuchElementException:
                            continue
                    
                    if channel_element:
                        channel_text = channel_element.text.strip()
                        print(f"   Video {i+1}: '{video_title[:50]}...' | Channel: '{channel_text}'")
                        
                        # Check if this video is from the target channel
                        if channel_name.lower() in channel_text.lower():
                            print(f"🎉 Found matching video: '{video_title}'")
                            print(f"   Channel: '{channel_text}'")
                            
                            # Click on the video
                            video.click()
                            print("✅ Video clicked successfully!")
                            
                            # Wait a moment to see the video page
                            time.sleep(3)
                            
                            return True
                    
                except Exception as e:
                    print(f"   Error processing video {i+1}: {e}")
                    continue
            
            print(f"❌ No videos found from channel '{channel_name}'")
            return False
            
        except Exception as e:
            print(f"❌ Error finding channel video: {e}")
            return False
    
    def get_current_video_info(self):
        """Get information about the currently playing video"""
        try:
            # Wait for video page to load
            time.sleep(2)
            
            # Get video title
            title_element = self.driver.find_element(By.CSS_SELECTOR, "h1.ytd-video-primary-info-renderer")
            title = title_element.text
            
            # Get channel name
            channel_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-channel-name yt-formatted-string")
            channel = channel_element.text
            
            print(f"\n📺 Currently playing:")
            print(f"   Title: {title}")
            print(f"   Channel: {channel}")
            print(f"   URL: {self.driver.current_url}")
            
            return {
                'title': title,
                'channel': channel,
                'url': self.driver.current_url
            }
            
        except Exception as e:
            print(f"❌ Error getting video info: {e}")
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def main():
    """Main function to run the YouTube Channel Finder"""
    print("🎬 YouTube Channel Video Finder")
    print("=" * 40)
    
    # Get user input
    topic = input("Enter search topic (e.g., 'Android development'): ").strip()
    channel_name = input("Enter channel name (e.g., 'Google Developers'): ").strip()
    
    if not topic or not channel_name:
        print("❌ Please provide both topic and channel name")
        return
    
    # Initialize the finder
    finder = YouTubeChannelFinder(headless=False)  # Set to True for hidden browser
    
    try:
        # Search for videos
        success = finder.search_youtube(topic, channel_name)
        
        if success:
            # Get video information
            video_info = finder.get_current_video_info()
            
            print("\n🎉 Success! Video found and opened.")
            print("Press Enter to close the browser...")
            input()
        else:
            print("\n❌ No matching video found.")
    
    except KeyboardInterrupt:
        print("\n⏹️ Operation cancelled by user")
    
    finally:
        finder.close()

if __name__ == "__main__":
    main()