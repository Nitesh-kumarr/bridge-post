#!/usr/bin/env python3
"""
YouTube Channel Video Finder - GUI Version
A Python GUI application that runs a hidden browser to search YouTube for videos from specific channels.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime
from youtube_finder_advanced import AdvancedYouTubeFinder

class YouTubeFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Channel Video Finder")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize finder
        self.finder = None
        self.search_thread = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="YouTube Channel Video Finder", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Search topic
        ttk.Label(main_frame, text="Search Topic:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.topic_var = tk.StringVar()
        self.topic_entry = ttk.Entry(main_frame, textvariable=self.topic_var, width=50)
        self.topic_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Channel name
        ttk.Label(main_frame, text="Channel Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.channel_var = tk.StringVar()
        self.channel_entry = ttk.Entry(main_frame, textvariable=self.channel_var, width=50)
        self.channel_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Browser options frame
        options_frame = ttk.LabelFrame(main_frame, text="Browser Options", padding="10")
        options_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Browser type
        ttk.Label(options_frame, text="Browser:").grid(row=0, column=0, sticky=tk.W)
        self.browser_var = tk.StringVar(value="chrome")
        browser_combo = ttk.Combobox(options_frame, textvariable=self.browser_var, 
                                    values=["chrome", "firefox", "edge"], state="readonly", width=15)
        browser_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Headless mode
        self.headless_var = tk.BooleanVar(value=True)
        headless_check = ttk.Checkbutton(options_frame, text="Headless Mode (Hidden Browser)", 
                                       variable=self.headless_var)
        headless_check.grid(row=0, column=2, sticky=tk.W, padx=(20, 0))
        
        # Search button
        self.search_button = ttk.Button(main_frame, text="Search YouTube", command=self.start_search)
        self.search_button.grid(row=4, column=0, columnspan=3, pady=10)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var)
        progress_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # Results text area
        results_frame = ttk.LabelFrame(main_frame, text="Search Results", padding="10")
        results_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=80)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Action buttons frame
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        self.click_button = ttk.Button(action_frame, text="Click First Video", 
                                      command=self.click_first_video, state="disabled")
        self.click_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.screenshot_button = ttk.Button(action_frame, text="Take Screenshot", 
                                          command=self.take_screenshot, state="disabled")
        self.screenshot_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.save_button = ttk.Button(action_frame, text="Save Results", 
                                     command=self.save_results, state="disabled")
        self.save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.close_button = ttk.Button(action_frame, text="Close Browser", 
                                      command=self.close_browser)
        self.close_button.pack(side=tk.LEFT)
        
        # Store search results
        self.search_results = None
        self.found_videos = []
    
    def log_message(self, message):
        """Add message to results text area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_search(self):
        """Start the search process in a separate thread"""
        topic = self.topic_var.get().strip()
        channel = self.channel_var.get().strip()
        
        if not topic or not channel:
            messagebox.showerror("Error", "Please provide both topic and channel name")
            return
        
        # Disable search button and enable action buttons
        self.search_button.config(state="disabled")
        self.click_button.config(state="normal")
        self.screenshot_button.config(state="normal")
        self.save_button.config(state="normal")
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.found_videos = []
        
        # Start search in separate thread
        self.search_thread = threading.Thread(target=self.perform_search, args=(topic, channel))
        self.search_thread.daemon = True
        self.search_thread.start()
    
    def perform_search(self, topic, channel):
        """Perform the actual search"""
        try:
            self.log_message("🎬 Starting YouTube search...")
            self.progress_var.set("Initializing browser...")
            
            # Initialize finder
            self.finder = AdvancedYouTubeFinder(
                browser_type=self.browser_var.get(),
                headless=self.headless_var.get()
            )
            
            self.progress_var.set("Searching YouTube...")
            self.log_message(f"🔍 Searching for: {topic} {channel}")
            
            # Perform search
            self.search_results = self.finder.search_youtube(topic, channel)
            
            if self.search_results["success"] and self.search_results["videos"]:
                self.found_videos = self.search_results["videos"]
                self.log_message(f"✅ Found {len(self.found_videos)} videos from '{channel}'")
                
                # Display found videos
                for i, video in enumerate(self.found_videos):
                    self.log_message(f"{i+1}. {video['title']}")
                    self.log_message(f"   Channel: {video['channel']}")
                    self.log_message(f"   URL: {video['url']}")
                    self.log_message("")
                
                self.progress_var.set(f"Found {len(self.found_videos)} videos")
                
            else:
                self.log_message(f"❌ {self.search_results.get('message', 'No matching videos found')}")
                self.progress_var.set("No videos found")
                
        except Exception as e:
            self.log_message(f"❌ Error during search: {e}")
            self.progress_var.set("Search failed")
            messagebox.showerror("Error", f"Search failed: {e}")
        
        finally:
            # Re-enable search button
            self.search_button.config(state="normal")
    
    def click_first_video(self):
        """Click on the first found video"""
        if not self.finder or not self.found_videos:
            messagebox.showwarning("Warning", "No videos found to click")
            return
        
        try:
            self.log_message("🖱️ Clicking on first video...")
            self.progress_var.set("Clicking video...")
            
            # Click on the first video
            if self.finder.click_video(0):
                self.log_message("✅ Video clicked successfully!")
                
                # Get video information
                video_info = self.finder.get_current_video_info()
                if video_info:
                    self.log_message(f"📺 Now playing: {video_info['title']}")
                    self.log_message(f"   Channel: {video_info['channel']}")
                    self.log_message(f"   Views: {video_info['views']}")
                    self.log_message(f"   URL: {video_info['url']}")
                
                self.progress_var.set("Video opened successfully")
                
            else:
                self.log_message("❌ Failed to click on video")
                self.progress_var.set("Failed to click video")
                
        except Exception as e:
            self.log_message(f"❌ Error clicking video: {e}")
            self.progress_var.set("Error clicking video")
    
    def take_screenshot(self):
        """Take a screenshot of the current page"""
        if not self.finder:
            messagebox.showwarning("Warning", "No browser session active")
            return
        
        try:
            self.log_message("📸 Taking screenshot...")
            filename = self.finder.take_screenshot()
            if filename:
                self.log_message(f"✅ Screenshot saved: {filename}")
                self.progress_var.set("Screenshot taken")
            else:
                self.log_message("❌ Failed to take screenshot")
                self.progress_var.set("Screenshot failed")
                
        except Exception as e:
            self.log_message(f"❌ Error taking screenshot: {e}")
            self.progress_var.set("Screenshot error")
    
    def save_results(self):
        """Save search results to file"""
        if not self.search_results:
            messagebox.showwarning("Warning", "No search results to save")
            return
        
        try:
            self.log_message("💾 Saving results...")
            filename = self.finder.save_results(self.search_results)
            if filename:
                self.log_message(f"✅ Results saved: {filename}")
                self.progress_var.set("Results saved")
            else:
                self.log_message("❌ Failed to save results")
                self.progress_var.set("Save failed")
                
        except Exception as e:
            self.log_message(f"❌ Error saving results: {e}")
            self.progress_var.set("Save error")
    
    def close_browser(self):
        """Close the browser"""
        if self.finder:
            try:
                self.finder.close()
                self.finder = None
                self.log_message("🔒 Browser closed")
                self.progress_var.set("Browser closed")
                
                # Disable action buttons
                self.click_button.config(state="disabled")
                self.screenshot_button.config(state="disabled")
                self.save_button.config(state="disabled")
                
            except Exception as e:
                self.log_message(f"❌ Error closing browser: {e}")
        else:
            self.log_message("ℹ️ No browser session to close")
    
    def on_closing(self):
        """Handle window closing"""
        if self.finder:
            self.finder.close()
        self.root.destroy()

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = YouTubeFinderGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main()