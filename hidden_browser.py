import os
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs

class HiddenBrowser:
    def __init__(self):
        self.driver = None
        self.is_initialized = False
        
    def initialize_browser(self):
        """Initialize the hidden browser with Chrome options"""
        try:
            chrome_options = Options()
            
            # Make browser hidden/headless
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            # Disable images and other media to speed up loading
            chrome_options.add_argument("--disable-images")
            chrome_options.add_argument("--disable-javascript")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-extensions")
            
            # Additional options for better performance
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            
            # Initialize the driver
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Set page load timeout
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            self.is_initialized = True
            print("Hidden browser initialized successfully")
            
        except Exception as e:
            print(f"Error initializing browser: {str(e)}")
            raise
    
    def open_video(self, video_url):
        """
        Open a YouTube video in the hidden browser
        
        Args:
            video_url (str): The YouTube video URL to open
        """
        try:
            if not self.is_initialized:
                self.initialize_browser()
            
            print(f"Opening video: {video_url}")
            
            # Navigate to the video
            self.driver.get(video_url)
            
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Extract video information
            video_info = self._extract_video_info()
            
            # Simulate video interaction (optional)
            self._interact_with_video()
            
            print(f"Video opened successfully: {video_info.get('title', 'Unknown')}")
            return video_info
            
        except TimeoutException:
            print("Timeout while loading video")
            raise
        except Exception as e:
            print(f"Error opening video: {str(e)}")
            raise
    
    def _extract_video_info(self):
        """Extract video information from the current page"""
        try:
            # Get page title
            title = self.driver.title
            
            # Try to get video title from meta tags
            try:
                title_elem = self.driver.find_element(By.CSS_SELECTOR, 'meta[property="og:title"]')
                title = title_elem.get_attribute('content')
            except:
                pass
            
            # Get current URL
            current_url = self.driver.current_url
            
            # Extract video ID from URL
            video_id = None
            if 'youtube.com/watch' in current_url:
                parsed_url = urlparse(current_url)
                query_params = parse_qs(parsed_url.query)
                video_id = query_params.get('v', [None])[0]
            
            return {
                'title': title,
                'url': current_url,
                'video_id': video_id
            }
            
        except Exception as e:
            print(f"Error extracting video info: {str(e)}")
            return {'title': 'Unknown', 'url': self.driver.current_url, 'video_id': None}
    
    def _interact_with_video(self):
        """Simulate basic interaction with the video (optional)"""
        try:
            # Wait a moment for the page to fully load
            time.sleep(2)
            
            # Try to find and click the play button if video is not auto-playing
            try:
                play_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '.ytp-play-button'))
                )
                play_button.click()
                print("Clicked play button")
            except:
                print("Play button not found or already playing")
            
            # Wait a bit more to let the video start
            time.sleep(3)
            
        except Exception as e:
            print(f"Error interacting with video: {str(e)}")
    
    def search_and_click_video(self, search_topic, channel_name=None):
        """
        Search YouTube for a topic and click on a video from a specific channel
        
        Args:
            search_topic (str): The topic to search for
            channel_name (str): Optional channel name to filter by
            
        Returns:
            dict: Information about the clicked video
        """
        try:
            if not self.is_initialized:
                self.initialize_browser()
            
            # Navigate to YouTube search
            search_url = f"https://www.youtube.com/results?search_query={search_topic.replace(' ', '+')}"
            self.driver.get(search_url)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer"))
            )
            
            # Find video links
            video_elements = self.driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer")
            
            target_video = None
            
            for video_elem in video_elements:
                try:
                    # Get video title
                    title_elem = video_elem.find_element(By.CSS_SELECTOR, "#video-title")
                    title = title_elem.get_attribute("title")
                    
                    # Get channel name
                    channel_elem = video_elem.find_element(By.CSS_SELECTOR, "#channel-name a")
                    channel = channel_elem.text
                    
                    print(f"Found video: {title} by {channel}")
                    
                    # Check if this video matches our criteria
                    if not channel_name or channel_name.lower() in channel.lower():
                        target_video = video_elem
                        print(f"Selected video: {title}")
                        break
                        
                except Exception as e:
                    continue
            
            if target_video:
                # Click on the video
                title_link = target_video.find_element(By.CSS_SELECTOR, "#video-title")
                title_link.click()
                
                # Wait for video page to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#player"))
                )
                
                # Extract video information
                video_info = self._extract_video_info()
                
                # Interact with the video
                self._interact_with_video()
                
                return video_info
            else:
                print(f"No video found matching criteria: topic='{search_topic}', channel='{channel_name}'")
                return None
                
        except Exception as e:
            print(f"Error searching and clicking video: {str(e)}")
            raise
    
    def close_browser(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                self.is_initialized = False
                print("Browser closed")
        except Exception as e:
            print(f"Error closing browser: {str(e)}")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.close_browser()
    
    def run_in_background(self, video_url):
        """
        Run video opening in a background thread
        
        Args:
            video_url (str): The YouTube video URL to open
        """
        def _open_video_thread():
            try:
                self.open_video(video_url)
            except Exception as e:
                print(f"Background video opening failed: {str(e)}")
        
        thread = threading.Thread(target=_open_video_thread)
        thread.daemon = True
        thread.start()
        return thread