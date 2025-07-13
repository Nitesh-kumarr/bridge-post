package com.example.hiddenbrowser;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private WebView webView;
    private EditText searchTopicEditText;
    private EditText channelNameEditText;
    private Button searchButton;
    private boolean isSearchPage = false;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize views
        webView = findViewById(R.id.webView);
        searchTopicEditText = findViewById(R.id.searchTopicEditText);
        channelNameEditText = findViewById(R.id.channelNameEditText);
        searchButton = findViewById(R.id.searchButton);

        // Configure WebView
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setUseWideViewPort(true);
        webSettings.setBuiltInZoomControls(true);
        webSettings.setDisplayZoomControls(false);
        webSettings.setSupportZoom(true);
        webSettings.setDefaultTextEncodingName("utf-8");
        webSettings.setUserAgentString("Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36");

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                
                // Only inject script on search results pages
                if (isSearchPage && url.contains("youtube.com/results")) {
                    // Wait a bit for dynamic content to load
                    view.postDelayed(() -> injectYouTubeSearchScript(), 2000);
                }
            }
        });

        webView.setWebChromeClient(new WebChromeClient());

        // Set up search button
        searchButton.setOnClickListener(v -> {
            String searchTopic = searchTopicEditText.getText().toString().trim();
            String channelName = channelNameEditText.getText().toString().trim();
            
            if (searchTopic.isEmpty() || channelName.isEmpty()) {
                Toast.makeText(this, "Please enter both topic and channel name", Toast.LENGTH_SHORT).show();
                return;
            }

            // Navigate to YouTube search
            String searchQuery = searchTopic + " " + channelName;
            String encodedQuery = java.net.URLEncoder.encode(searchQuery, "UTF-8");
            String youtubeSearchUrl = "https://www.youtube.com/results?search_query=" + encodedQuery;
            
            isSearchPage = true;
            webView.loadUrl(youtubeSearchUrl);
        });

        // Load YouTube homepage initially
        webView.loadUrl("https://www.youtube.com");
    }

    private void injectYouTubeSearchScript() {
        String script = "javascript:" +
                "(function() {" +
                "   var channelName = '" + channelNameEditText.getText().toString().trim() + "';" +
                "   var maxAttempts = 5;" +
                "   var attemptCount = 0;" +
                "   " +
                "   function findChannelVideo() {" +
                "       attemptCount++;" +
                "       console.log('Attempt ' + attemptCount + ' to find channel video');" +
                "       " +
                "       // Try multiple selectors for YouTube's dynamic content" +
                "       var selectors = [" +
                "           'a#video-title'," +
                "           'a[href*=\"/watch?v=\"]'," +
                "           'ytd-video-renderer a#video-title'," +
                "           'ytd-compact-video-renderer a#video-title'" +
                "       ];" +
                "       " +
                "       for (var s = 0; s < selectors.length; s++) {" +
                "           var videos = document.querySelectorAll(selectors[s]);" +
                "           console.log('Found ' + videos.length + ' videos with selector: ' + selectors[s]);" +
                "           " +
                "           for (var i = 0; i < videos.length; i++) {" +
                "               var video = videos[i];" +
                "               var title = video.getAttribute('title') || video.textContent;" +
                "               " +
                "               // Try to find channel name in various ways" +
                "               var channelElement = null;" +
                "               var parent = video.closest('ytd-video-renderer') || video.closest('ytd-compact-video-renderer');" +
                "               " +
                "               if (parent) {" +
                "                   channelElement = parent.querySelector('#channel-name a') || " +
                "                                parent.querySelector('#channel-name') || " +
                "                                parent.querySelector('ytd-channel-name a') || " +
                "                                parent.querySelector('ytd-channel-name');" +
                "               }" +
                "               " +
                "               if (channelElement) {" +
                "                   var channelText = channelElement.textContent.trim();" +
                "                   console.log('Video: ' + title + ', Channel: ' + channelText);" +
                "                   " +
                "                   if (channelText.toLowerCase().includes(channelName.toLowerCase())) {" +
                "                       console.log('Found matching channel video: ' + title);" +
                "                       video.click();" +
                "                       return true;" +
                "                   }" +
                "               }" +
                "           }" +
                "       }" +
                "       " +
                "       // If no video found and we haven't exceeded max attempts, scroll and try again" +
                "       if (attemptCount < maxAttempts) {" +
                "           console.log('No video found, scrolling down...');" +
                "           window.scrollTo(0, document.body.scrollHeight);" +
                "           setTimeout(findChannelVideo, 2000);" +
                "       } else {" +
                "           console.log('No video found from target channel after ' + maxAttempts + ' attempts');" +
                "       }" +
                "       return false;" +
                "   }" +
                "   " +
                "   // Start the search process" +
                "   setTimeout(findChannelVideo, 1000);" +
                "})();";

        webView.evaluateJavascript(script, null);
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}