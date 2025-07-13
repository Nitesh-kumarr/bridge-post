from flask import Flask, jsonify, request
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import threading
import time
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrowserAutomation:
    def __init__(self):
        self.driver = None
        self.is_running = False
    
    def setup_driver(self):
        """Setup headless Chrome driver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Chrome driver setup successful")
            return True
        except Exception as e:
            logger.error(f"Failed to setup driver: {e}")
            return False
    
    def youtube_automation(self):
        """Automate YouTube video clicking"""
        try:
            self.is_running = True
            logger.info("Starting YouTube automation")
            
            # Navigate to YouTube
            self.driver.get("https://www.youtube.com")
            logger.info("Navigated to YouTube")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Find and click on the first video
            # Look for video elements (multiple selectors to be safe)
            video_selectors = [
                "ytd-rich-grid-media",
                "ytd-video-renderer",
                "ytd-compact-video-renderer",
                "a#video-title"
            ]
            
            video_found = False
            for selector in video_selectors:
                try:
                    videos = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if videos:
                        # Click on the first video
                        videos[0].click()
                        logger.info(f"Clicked on video using selector: {selector}")
                        video_found = True
                        break
                except Exception as e:
                    logger.warning(f"Selector {selector} failed: {e}")
                    continue
            
            if not video_found:
                # Fallback: try to find any clickable video link
                try:
                    video_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/watch?v=']")
                    if video_links:
                        video_links[0].click()
                        logger.info("Clicked on video using fallback method")
                        video_found = True
                except Exception as e:
                    logger.error(f"Fallback method failed: {e}")
            
            if video_found:
                # Wait a bit to see the video page
                time.sleep(3)
                logger.info("YouTube automation completed successfully")
                return {"success": True, "message": "Video clicked successfully"}
            else:
                logger.error("No video found to click")
                return {"success": False, "message": "No video found to click"}
                
        except Exception as e:
            logger.error(f"YouTube automation failed: {e}")
            return {"success": False, "message": f"Automation failed: {str(e)}"}
        finally:
            self.is_running = False
    
    def cleanup(self):
        """Clean up the driver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Driver cleaned up successfully")
            except Exception as e:
                logger.error(f"Failed to cleanup driver: {e}")
            finally:
                self.driver = None

# Global automation instance
automation = BrowserAutomation()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Server is running"})

@app.route('/automate', methods=['POST'])
def start_automation():
    """Start the YouTube automation"""
    try:
        # Check if automation is already running
        if automation.is_running:
            return jsonify({"success": False, "message": "Automation already running"}), 400
        
        # Setup driver if not already done
        if not automation.driver:
            if not automation.setup_driver():
                return jsonify({"success": False, "message": "Failed to setup browser driver"}), 500
        
        # Start automation in a separate thread
        thread = threading.Thread(target=automation.youtube_automation)
        thread.daemon = True
        thread.start()
        
        return jsonify({"success": True, "message": "Automation started"})
        
    except Exception as e:
        logger.error(f"Failed to start automation: {e}")
        return jsonify({"success": False, "message": f"Failed to start automation: {str(e)}"}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get automation status"""
    return jsonify({
        "is_running": automation.is_running,
        "driver_active": automation.driver is not None
    })

@app.route('/cleanup', methods=['POST'])
def cleanup_driver():
    """Clean up the browser driver"""
    try:
        automation.cleanup()
        return jsonify({"success": True, "message": "Driver cleaned up successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Cleanup failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)