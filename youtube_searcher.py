import requests
import re
import json
import time
from urllib.parse import quote_plus, urlparse, parse_qs
from bs4 import BeautifulSoup

class YouTubeSearcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_url = "https://www.youtube.com"
    
    def search_videos(self, topic, channel=None, max_results=10):
        """
        Search YouTube for videos on a specific topic, optionally filtering by channel
        
        Args:
            topic (str): The search topic
            channel (str): Optional channel name to filter by
            max_results (int): Maximum number of results to return
            
        Returns:
            list: List of video dictionaries with metadata
        """
        try:
            # Construct search URL
            search_query = quote_plus(topic)
            search_url = f"{self.base_url}/results?search_query={search_query}"
            
            print(f"Searching YouTube for: {topic}")
            if channel:
                print(f"Filtering by channel: {channel}")
            
            # Get search results page
            response = self.session.get(search_url)
            response.raise_for_status()
            
            # Parse the page
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract video data from the page
            videos = self._extract_videos_from_page(soup, channel)
            
            # Limit results
            videos = videos[:max_results]
            
            print(f"Found {len(videos)} videos")
            return videos
            
        except Exception as e:
            print(f"Error searching YouTube: {str(e)}")
            return []
    
    def _extract_videos_from_page(self, soup, channel_filter=None):
        """Extract video information from YouTube search results page"""
        videos = []
        
        try:
            # Look for the initial data script tag
            scripts = soup.find_all('script')
            initial_data = None
            
            for script in scripts:
                if script.string and 'var ytInitialData = ' in script.string:
                    # Extract the JSON data
                    json_str = script.string.split('var ytInitialData = ')[1].split(';</script>')[0]
                    initial_data = json.loads(json_str)
                    break
            
            if initial_data:
                videos = self._parse_initial_data(initial_data, channel_filter)
            else:
                # Fallback to parsing HTML directly
                videos = self._parse_html_results(soup, channel_filter)
                
        except Exception as e:
            print(f"Error extracting videos: {str(e)}")
            # Fallback to simple HTML parsing
            videos = self._parse_html_results(soup, channel_filter)
        
        return videos
    
    def _parse_initial_data(self, data, channel_filter=None):
        """Parse YouTube's initial data JSON to extract video information"""
        videos = []
        
        try:
            # Navigate through the JSON structure to find video results
            contents = data.get('contents', {})
            tab_contents = contents.get('tabbedSearchResultsRenderer', {}).get('tabs', [])
            
            for tab in tab_contents:
                if 'tabRenderer' in tab and tab['tabRenderer'].get('selected'):
                    tab_content = tab['tabRenderer'].get('content', {})
                    section_list = tab_content.get('sectionListRenderer', {}).get('contents', [])
                    
                    for section in section_list:
                        if 'itemSectionRenderer' in section:
                            items = section['itemSectionRenderer'].get('contents', [])
                            
                            for item in items:
                                if 'videoRenderer' in item:
                                    video_data = item['videoRenderer']
                                    video_info = self._extract_video_info(video_data)
                                    
                                    if video_info and self._matches_channel_filter(video_info, channel_filter):
                                        videos.append(video_info)
                                        
        except Exception as e:
            print(f"Error parsing initial data: {str(e)}")
        
        return videos
    
    def _extract_video_info(self, video_data):
        """Extract video information from video renderer data"""
        try:
            video_id = video_data.get('videoId', '')
            title = video_data.get('title', {}).get('runs', [{}])[0].get('text', 'Unknown Title')
            
            # Extract channel info
            owner_text = video_data.get('ownerText', {}).get('runs', [{}])
            channel_name = owner_text[0].get('text', 'Unknown Channel') if owner_text else 'Unknown Channel'
            
            # Extract duration
            length_text = video_data.get('lengthText', {}).get('simpleText', 'Unknown')
            
            # Extract view count
            view_count_text = video_data.get('viewCountText', {}).get('simpleText', 'Unknown views')
            
            # Extract thumbnail
            thumbnails = video_data.get('thumbnail', {}).get('thumbnails', [])
            thumbnail_url = thumbnails[-1].get('url', '') if thumbnails else ''
            
            return {
                'title': title,
                'channel': channel_name,
                'duration': length_text,
                'views': view_count_text,
                'url': f"https://www.youtube.com/watch?v={video_id}",
                'thumbnail': thumbnail_url,
                'video_id': video_id
            }
            
        except Exception as e:
            print(f"Error extracting video info: {str(e)}")
            return None
    
    def _parse_html_results(self, soup, channel_filter=None):
        """Fallback method to parse HTML directly"""
        videos = []
        
        try:
            # Look for video links
            video_links = soup.find_all('a', href=re.compile(r'/watch\?v='))
            
            for link in video_links:
                try:
                    video_id = parse_qs(urlparse(link['href']).query).get('v', [''])[0]
                    if not video_id:
                        continue
                    
                    # Get video title
                    title_elem = link.find('h3')
                    title = title_elem.get_text(strip=True) if title_elem else 'Unknown Title'
                    
                    # Try to find channel info
                    channel_elem = link.find_parent().find('a', href=re.compile(r'/channel/|/user/|/c/'))
                    channel_name = channel_elem.get_text(strip=True) if channel_elem else 'Unknown Channel'
                    
                    video_info = {
                        'title': title,
                        'channel': channel_name,
                        'duration': 'Unknown',
                        'views': 'Unknown views',
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'thumbnail': '',
                        'video_id': video_id
                    }
                    
                    if self._matches_channel_filter(video_info, channel_filter):
                        videos.append(video_info)
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error parsing HTML results: {str(e)}")
        
        return videos
    
    def _matches_channel_filter(self, video_info, channel_filter):
        """Check if video matches the channel filter"""
        if not channel_filter:
            return True
        
        channel_name = video_info.get('channel', '').lower()
        filter_name = channel_filter.lower()
        
        return filter_name in channel_name or channel_name in filter_name
    
    def get_video_details(self, video_id):
        """Get detailed information about a specific video"""
        try:
            url = f"{self.base_url}/watch?v={video_id}"
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract video title
            title_elem = soup.find('meta', property='og:title')
            title = title_elem['content'] if title_elem else 'Unknown Title'
            
            # Extract channel name
            channel_elem = soup.find('link', itemprop='name')
            channel = channel_elem['content'] if channel_elem else 'Unknown Channel'
            
            # Extract description
            desc_elem = soup.find('meta', property='og:description')
            description = desc_elem['content'] if desc_elem else ''
            
            return {
                'title': title,
                'channel': channel,
                'description': description,
                'url': url,
                'video_id': video_id
            }
            
        except Exception as e:
            print(f"Error getting video details: {str(e)}")
            return None