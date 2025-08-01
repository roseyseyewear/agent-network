#!/usr/bin/env python3
"""
ElevenLabs Text-to-Speech Integration for Claude Responses
Usage: python text_to_speech.py "Your text here"
"""

import os
import sys
import requests
import json
from pathlib import Path
import pygame
import io
from load_env import load_env

# Load environment variables from .env file
load_env()

class ElevenLabsTTS:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Default voice ID (Rachel - professional female voice)
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID', 'AZnzlk1XvdvUeBnXmlld')
        
        if not self.api_key:
            print("Error: ELEVENLABS_API_KEY environment variable not set")
            print("Set it with: set ELEVENLABS_API_KEY=your_api_key_here")
            sys.exit(1)
    
    def text_to_speech(self, text, voice_id=None):
        """Convert text to speech using ElevenLabs API"""
        if not voice_id:
            voice_id = self.voice_id
            
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            print(f"Error calling ElevenLabs API: {e}")
            return None
    
    def play_audio(self, audio_data):
        """Play audio data using pygame"""
        try:
            pygame.mixer.init()
            audio_file = io.BytesIO(audio_data)
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
                
        except Exception as e:
            print(f"Error playing audio: {e}")
        finally:
            pygame.mixer.quit()
    
    def speak(self, text):
        """Convert text to speech and play it"""
        print(f"Speaking: {text[:50]}...")
        
        audio_data = self.text_to_speech(text)
        if audio_data:
            self.play_audio(audio_data)
            print("Audio playback complete.")
        else:
            print("Failed to generate speech.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python text_to_speech.py \"Your text here\"")
        print("Or pipe text: echo \"Hello world\" | python text_to_speech.py")
        sys.exit(1)
    
    # Check if text is being piped
    if not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        text = " ".join(sys.argv[1:])
    
    if not text:
        print("No text provided")
        sys.exit(1)
    
    tts = ElevenLabsTTS()
    tts.speak(text)

if __name__ == "__main__":
    main()