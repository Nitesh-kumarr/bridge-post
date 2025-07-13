import os
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup

# Import our custom modules
from youtube_searcher import YouTubeSearcher
from hidden_browser import HiddenBrowser

class YouTubeSearchApp(App):
    search_results = StringProperty("")
    is_searching = BooleanProperty(False)
    
    def build(self):
        # Set window size for desktop testing
        if platform == 'android':
            Window.fullscreen = 'auto'
        else:
            Window.size = (400, 600)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text="YouTube Hidden Browser Search",
            size_hint_y=None,
            height=50,
            font_size='20sp',
            bold=True
        )
        main_layout.add_widget(title)
        
        # Search topic input
        self.topic_input = TextInput(
            hint_text="Enter search topic...",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(self.topic_input)
        
        # Channel name input
        self.channel_input = TextInput(
            hint_text="Enter channel name (optional)...",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(self.channel_input)
        
        # Search button
        self.search_button = Button(
            text="Search YouTube",
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.search_button.bind(on_press=self.start_search)
        main_layout.add_widget(self.search_button)
        
        # Progress bar
        self.progress_bar = ProgressBar(
            size_hint_y=None,
            height=20
        )
        self.progress_bar.opacity = 0
        main_layout.add_widget(self.progress_bar)
        
        # Results area
        results_label = Label(
            text="Search Results:",
            size_hint_y=None,
            height=30,
            bold=True
        )
        main_layout.add_widget(results_label)
        
        # Scrollable results
        self.results_layout = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.results_layout)
        main_layout.add_widget(scroll_view)
        
        return main_layout
    
    def start_search(self, instance):
        topic = self.topic_input.text.strip()
        channel = self.channel_input.text.strip()
        
        if not topic:
            self.show_popup("Error", "Please enter a search topic!")
            return
        
        self.is_searching = True
        self.search_button.text = "Searching..."
        self.search_button.disabled = True
        self.progress_bar.opacity = 1
        
        # Clear previous results
        self.results_layout.clear_widgets()
        
        # Start search in background thread
        threading.Thread(target=self.perform_search, args=(topic, channel)).start()
    
    def perform_search(self, topic, channel):
        try:
            # Initialize the YouTube searcher
            searcher = YouTubeSearcher()
            
            # Perform the search
            results = searcher.search_videos(topic, channel)
            
            # Update UI on main thread
            Clock.schedule_once(lambda dt: self.update_results(results), 0)
            
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            Clock.schedule_once(lambda dt: self.show_popup("Error", error_msg), 0)
        finally:
            Clock.schedule_once(lambda dt: self.search_complete(), 0)
    
    def update_results(self, results):
        if not results:
            no_results = Label(
                text="No videos found matching your criteria.",
                size_hint_y=None,
                height=40,
                color=(0.7, 0.7, 0.7, 1)
            )
            self.results_layout.add_widget(no_results)
            return
        
        for result in results:
            # Create result item
            result_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=120)
            
            # Title
            title_label = Label(
                text=result['title'][:50] + "..." if len(result['title']) > 50 else result['title'],
                size_hint_y=None,
                height=30,
                bold=True,
                text_size=(Window.width - 20, None),
                halign='left'
            )
            result_layout.add_widget(title_label)
            
            # Channel
            channel_label = Label(
                text=f"Channel: {result['channel']}",
                size_hint_y=None,
                height=25,
                color=(0.6, 0.6, 0.6, 1)
            )
            result_layout.add_widget(channel_label)
            
            # Duration and views
            info_label = Label(
                text=f"Duration: {result['duration']} | Views: {result['views']}",
                size_hint_y=None,
                height=25,
                color=(0.5, 0.5, 0.5, 1)
            )
            result_layout.add_widget(info_label)
            
            # Watch button
            watch_button = Button(
                text="Watch Video",
                size_hint_y=None,
                height=30,
                background_color=(0.2, 0.8, 0.2, 1)
            )
            watch_button.bind(on_press=lambda btn, url=result['url']: self.watch_video(url))
            result_layout.add_widget(watch_button)
            
            # Add separator
            separator = Label(
                text="",
                size_hint_y=None,
                height=1,
                background_color=(0.8, 0.8, 0.8, 1)
            )
            
            self.results_layout.add_widget(result_layout)
            self.results_layout.add_widget(separator)
    
    def watch_video(self, url):
        try:
            # Initialize hidden browser
            browser = HiddenBrowser()
            browser.open_video(url)
            self.show_popup("Success", "Video opened in hidden browser!")
        except Exception as e:
            self.show_popup("Error", f"Failed to open video: {str(e)}")
    
    def search_complete(self):
        self.is_searching = False
        self.search_button.text = "Search YouTube"
        self.search_button.disabled = False
        self.progress_bar.opacity = 0
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

if __name__ == '__main__':
    YouTubeSearchApp().run()