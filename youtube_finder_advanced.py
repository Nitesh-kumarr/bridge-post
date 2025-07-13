#!/usr/bin/env python3
"""
Advanced YouTube Channel Video Finder
A Python application that runs a hidden browser to search YouTube for videos from specific channels.
Features:
- Multiple browser support (Chrome, Firefox, Edge)
- Better error handling and retry logic
- Configurable search parameters
- Video information extraction
- Screenshot capture
"""

import time
import sys
import os
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import urllib.parse

class AdvancedYouTubeFinder:
    def __init__(self, browser_type="chrome", headless=True, timeout=30):
        """
        Initialize the Advanced YouTube Finder
        
        Args:
            browser_type (str): Browser to use ('chrome', 'firefox', 'edge')
            headless (bool): Run browser in headless mode
            timeout (int): Timeout for element waits
        """
        self.browser_type = browser_type.lower()
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup WebDriver with appropriate options"""
        try:
            if self.browser_type == "chrome":
                self.driver = self._setup_chrome()
            elif self.browser_type == "firefox":
                self.driver = self._setup_firefox()
            elif self.browser_type == "edge":
                self.driver = self._setup_edge()
            else:
                raise ValueError(f"Unsupported browser type: {self.browser_type}")
            
            self.wait = WebDriverWait(self.driver, self.timeout)
            print(f"✅ {self.browser_type.capitalize()} browser initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing {self.browser_type} browser: {e}")
            print("Please make sure the browser is installed")
            sys.exit(1)
    
    def _setup_chrome(self):
        """Setup Chrome WebDriver"""
        options = ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        # Performance and stealth options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Disable images for faster loading
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)
        
        # Use webdriver-manager to automatically download and manage ChromeDriver
        service = webdriver.chrome.service.Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _setup_firefox(self):
        """Setup Firefox WebDriver"""
        options = FirefoxOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        # Performance options
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        # Use webdriver-manager to automatically download and manage GeckoDriver
        service = webdriver.firefox.service.Service(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def _setup_edge(self):
        """Setup Edge WebDriver"""
        options = EdgeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        # Performance options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        # Use webdriver-manager to automatically download and manage EdgeDriver
        service = webdriver.edge.service.Service(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    def search_youtube(self, topic, channel_name, max_videos=30, scroll_count=5):
        """
        Search YouTube for videos from a specific channel
        
        Args:
            topic (str): Search topic
            channel_name (str): Channel name to filter by
            max_videos (int): Maximum number of videos to check
            scroll_count (int): Number of times to scroll down
            
        Returns:
            dict: Search results with video information
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
            self.scroll_to_load_more(scroll_count)
            
            # Find videos from the specified channel
            return self.find_channel_videos(channel_name, max_videos)
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
            return {"success": False, "error": str(e)}
    
    def scroll_to_load_more(self, scroll_count=5):
        """Scroll down to load more search results"""
        print(f"📜 Scrolling {scroll_count} times to load more results...")
        
        for i in range(scroll_count):
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                print(f"   Scroll {i+1}/{scroll_count} completed")
            except Exception as e:
                print(f"   Error during scroll {i+1}: {e}")
    
    def find_channel_videos(self, channel_name, max_videos=30):
        """
        Find videos from the specified channel
        
        Args:
            channel_name (str): Name of the channel to look for
            max_videos (int): Maximum number of videos to check
            
        Returns:
            dict: Results with found videos and their information
        """
        try:
            print(f"🎯 Looking for videos from channel: {channel_name}")
            
            # Find all video elements
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, "a#video-title")
            
            if not video_elements:
                print("❌ No video elements found")
                return {"success": False, "videos": [], "message": "No video elements found"}
            
            print(f"📹 Found {len(video_elements)} videos")
            
            found_videos = []
            
            # Iterate through videos to find ones from the target channel
            for i, video in enumerate(video_elements[:max_videos]):
                try:
                    # Get video title and URL
                    video_title = video.get_attribute("title") or video.text
                    video_url = video.get_attribute("href")
                    
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
                            video_info = {
                                'title': video_title,
                                'channel': channel_text,
                                'url': video_url,
                                'index': i + 1
                            }
                            found_videos.append(video_info)
                            print(f"🎉 Found matching video: '{video_title}'")
                    
                except Exception as e:
                    print(f"   Error processing video {i+1}: {e}")
                    continue
            
            if found_videos:
                print(f"✅ Found {len(found_videos)} videos from channel '{channel_name}'")
                return {
                    "success": True,
                    "videos": found_videos,
                    "total_found": len(found_videos)
                }
            else:
                print(f"❌ No videos found from channel '{channel_name}'")
                return {
                    "success": False,
                    "videos": [],
                    "message": f"No videos found from channel '{channel_name}'"
                }
                
        except Exception as e:
            print(f"❌ Error finding channel videos: {e}")
            return {"success": False, "error": str(e)}
    
    def click_video(self, video_index=0):
        """
        Click on a specific video by index
        
        Args:
            video_index (int): Index of the video to click (0-based)
            
        Returns:
            bool: True if video was clicked successfully
        """
        try:
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, "a#video-title")
            
            if video_index >= len(video_elements):
                print(f"❌ Video index {video_index} is out of range")
                return False
            
            video = video_elements[video_index]
            video_title = video.get_attribute("title") or video.text
            
            print(f"🖱️ Clicking on video: {video_title}")
            video.click()
            
            # Wait for video page to load
            time.sleep(3)
            
            print("✅ Video clicked successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error clicking video: {e}")
            return False
    
    def get_current_video_info(self):
        """Get detailed information about the currently playing video"""
        try:
            # Wait for video page to load
            time.sleep(2)
            
            video_info = {}
            
            # Get video title
            try:
                title_element = self.driver.find_element(By.CSS_SELECTOR, "h1.ytd-video-primary-info-renderer")
                video_info['title'] = title_element.text
            except NoSuchElementException:
                video_info['title'] = "Title not found"
            
            # Get channel name
            try:
                channel_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-channel-name yt-formatted-string")
                video_info['channel'] = channel_element.text
            except NoSuchElementException:
                video_info['channel'] = "Channel not found"
            
            # Get video URL
            video_info['url'] = self.driver.current_url
            
            # Get view count (if available)
            try:
                view_element = self.driver.find_element(By.CSS_SELECTOR, "span.ytd-video-view-count-renderer")
                video_info['views'] = view_element.text
            except NoSuchElementException:
                video_info['views'] = "Views not available"
            
            # Get upload date (if available)
            try:
                date_element = self.driver.find_element(By.CSS_SELECTOR, "ytd-video-primary-info-renderer yt-formatted-string")
                video_info['upload_date'] = date_element.text
            except NoSuchElementException:
                video_info['upload_date'] = "Date not available"
            
            print(f"\n📺 Currently playing:")
            print(f"   Title: {video_info['title']}")
            print(f"   Channel: {video_info['channel']}")
            print(f"   Views: {video_info['views']}")
            print(f"   Upload Date: {video_info['upload_date']}")
            print(f"   URL: {video_info['url']}")
            
            return video_info
            
        except Exception as e:
            print(f"❌ Error getting video info: {e}")
            return None
    
    def take_screenshot(self, filename=None):
        """Take a screenshot of the current page"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"youtube_screenshot_{timestamp}.png"
            
            self.driver.save_screenshot(filename)
            print(f"📸 Screenshot saved as: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error taking screenshot: {e}")
            return None
    
    def save_results(self, results, filename=None):
        """Save search results to a JSON file"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"youtube_search_results_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Results saved to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error saving results: {e}")
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("🔒 Browser closed")

def main():
    """Main function to run the Advanced YouTube Finder"""
    print("🎬 Advanced YouTube Channel Video Finder")
    print("=" * 50)
    
    # Configuration
    browser_type = input("Choose browser (chrome/firefox/edge) [chrome]: ").strip().lower() or "chrome"
    headless = input("Run in headless mode? (y/n) [y]: ").strip().lower() != "n"
    
    # Get user input
    topic = input("Enter search topic (e.g., 'Android development'): ").strip()
    channel_name = input("Enter channel name (e.g., 'Google Developers'): ").strip()
    
    if not topic or not channel_name:
        print("❌ Please provide both topic and channel name")
        return
    
    # Initialize the finder
    finder = AdvancedYouTubeFinder(browser_type=browser_type, headless=headless)
    
    try:
        # Search for videos
        results = finder.search_youtube(topic, channel_name)
        
        if results["success"] and results["videos"]:
            print(f"\n🎉 Found {len(results['videos'])} videos from '{channel_name}'")
            
            # Display found videos
            for i, video in enumerate(results["videos"]):
                print(f"{i+1}. {video['title']}")
                print(f"   Channel: {video['channel']}")
                print(f"   URL: {video['url']}")
                print()
            
            # Ask user which video to click
            if len(results["videos"]) > 1:
                choice = input(f"Which video to click? (1-{len(results['videos'])}) [1]: ").strip()
                video_index = int(choice) - 1 if choice.isdigit() else 0
            else:
                video_index = 0
            
            # Click on the selected video
            if finder.click_video(video_index):
                # Get video information
                video_info = finder.get_current_video_info()
                
                # Take screenshot
                finder.take_screenshot()
                
                # Save results
                finder.save_results(results)
                
                print("\n🎉 Success! Video opened and information captured.")
                print("Press Enter to close the browser...")
                input()
            else:
                print("\n❌ Failed to click on video.")
        else:
            print(f"\n❌ {results.get('message', 'No matching videos found')}")
    
    except KeyboardInterrupt:
        print("\n⏹️ Operation cancelled by user")
    
    finally:
        finder.close()

if __name__ == "__main__":
    main()