package com.example.browserautomation

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.coroutines.*
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.IOException

class MainActivity : AppCompatActivity() {
    
    private lateinit var startButton: Button
    private lateinit var statusText: TextView
    private lateinit var statusButton: Button
    private lateinit var cleanupButton: Button
    
    private val client = OkHttpClient()
    private val serverUrl = "http://10.0.2.2:5000" // For Android emulator
    // Change to your actual server IP when testing on real device
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        startButton = findViewById(R.id.startButton)
        statusText = findViewById(R.id.statusText)
        statusButton = findViewById(R.id.statusButton)
        cleanupButton = findViewById(R.id.cleanupButton)
        
        setupButtons()
        checkServerHealth()
    }
    
    private fun setupButtons() {
        startButton.setOnClickListener {
            startAutomation()
        }
        
        statusButton.setOnClickListener {
            checkStatus()
        }
        
        cleanupButton.setOnClickListener {
            cleanupDriver()
        }
    }
    
    private fun startAutomation() {
        startButton.isEnabled = false
        statusText.text = "Starting automation..."
        
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val request = Request.Builder()
                    .url("$serverUrl/automate")
                    .post("".toRequestBody("application/json".toMediaType()))
                    .build()
                
                val response = client.newCall(request).execute()
                val responseBody = response.body?.string()
                
                withContext(Dispatchers.Main) {
                    if (response.isSuccessful && responseBody != null) {
                        val jsonResponse = JSONObject(responseBody)
                        val message = jsonResponse.optString("message", "Unknown response")
                        statusText.text = "Automation: $message"
                        Toast.makeText(this@MainActivity, message, Toast.LENGTH_SHORT).show()
                    } else {
                        statusText.text = "Failed to start automation"
                        Toast.makeText(this@MainActivity, "Failed to start automation", Toast.LENGTH_SHORT).show()
                    }
                    startButton.isEnabled = true
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    statusText.text = "Error: ${e.message}"
                    Toast.makeText(this@MainActivity, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
                    startButton.isEnabled = true
                }
            }
        }
    }
    
    private fun checkStatus() {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val request = Request.Builder()
                    .url("$serverUrl/status")
                    .get()
                    .build()
                
                val response = client.newCall(request).execute()
                val responseBody = response.body?.string()
                
                withContext(Dispatchers.Main) {
                    if (response.isSuccessful && responseBody != null) {
                        val jsonResponse = JSONObject(responseBody)
                        val isRunning = jsonResponse.optBoolean("is_running", false)
                        val driverActive = jsonResponse.optBoolean("driver_active", false)
                        
                        val status = "Running: $isRunning\nDriver Active: $driverActive"
                        statusText.text = status
                    } else {
                        statusText.text = "Failed to get status"
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    statusText.text = "Error getting status: ${e.message}"
                }
            }
        }
    }
    
    private fun cleanupDriver() {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val request = Request.Builder()
                    .url("$serverUrl/cleanup")
                    .post("".toRequestBody("application/json".toMediaType()))
                    .build()
                
                val response = client.newCall(request).execute()
                val responseBody = response.body?.string()
                
                withContext(Dispatchers.Main) {
                    if (response.isSuccessful && responseBody != null) {
                        val jsonResponse = JSONObject(responseBody)
                        val message = jsonResponse.optString("message", "Unknown response")
                        statusText.text = "Cleanup: $message"
                        Toast.makeText(this@MainActivity, message, Toast.LENGTH_SHORT).show()
                    } else {
                        statusText.text = "Failed to cleanup driver"
                        Toast.makeText(this@MainActivity, "Failed to cleanup driver", Toast.LENGTH_SHORT).show()
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    statusText.text = "Error during cleanup: ${e.message}"
                    Toast.makeText(this@MainActivity, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }
        }
    }
    
    private fun checkServerHealth() {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val request = Request.Builder()
                    .url("$serverUrl/health")
                    .get()
                    .build()
                
                val response = client.newCall(request).execute()
                
                withContext(Dispatchers.Main) {
                    if (response.isSuccessful) {
                        statusText.text = "Server is running"
                        startButton.isEnabled = true
                    } else {
                        statusText.text = "Server is not responding"
                        startButton.isEnabled = false
                    }
                }
            } catch (e: Exception) {
                withContext(Dispatchers.Main) {
                    statusText.text = "Cannot connect to server"
                    startButton.isEnabled = false
                }
            }
        }
    }
}