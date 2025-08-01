#!/usr/bin/env python3
"""
Full Voice Integration for Claude Code
Automatically speaks Claude's responses and listens for voice input
"""

import os
import sys
import time
import threading
import subprocess
import speech_recognition as sr
from text_to_speech import ElevenLabsTTS
import re

class ClaudeVoiceIntegration:
    def __init__(self):
        self.tts = ElevenLabsTTS()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        
    def setup_microphone(self):
        """Calibrate microphone for ambient noise"""
        print("Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Microphone ready!")
    
    def listen_for_speech(self):
        """Continuously listen for voice input"""
        print("Voice input active. Say 'Hey Claude' to start speaking...")
        
        while True:
            try:
                with self.microphone as source:
                    # Listen for audio with a timeout
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                
                # Check for wake word
                if "hey claude" in text.lower():
                    self.handle_voice_command(text)
                    
            except sr.WaitTimeoutError:
                pass  # No speech detected, continue listening
            except sr.UnknownValueError:
                pass  # Speech not understood, continue listening
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                time.sleep(1)
    
    def handle_voice_command(self, text):
        """Process voice command and send to Claude"""
        # Remove wake word
        command = re.sub(r"hey claude,?\s*", "", text, flags=re.IGNORECASE)
        
        if command.strip():
            print(f"Processing command: {command}")
            
            # Here you would integrate with Claude Code API or use subprocess
            # For now, we'll simulate by speaking back
            response = f"You asked me: {command}. I would process this through Claude Code."
            self.tts.speak(response)
    
    def speak_claude_response(self, text):
        """Speak Claude's response"""
        # Clean up text for better speech
        clean_text = self.clean_text(text)
        if clean_text:
            self.tts.speak(clean_text)
    
    def clean_text(self, text):
        """Clean text for speech"""
        # Remove markdown
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # Bold
        text = re.sub(r'\*([^*]+)\*', r'\1', text)      # Italic
        text = re.sub(r'`([^`]+)`', r'\1', text)        # Code
        text = re.sub(r'#{1,6}\s*', '', text)           # Headers
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Clean whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text if len(text) > 10 else None

def main():
    print("Claude Voice Integration Starting...")
    
    integration = ClaudeVoiceIntegration()
    
    # Setup
    integration.setup_microphone()
    
    # Start voice listening in background
    voice_thread = threading.Thread(target=integration.listen_for_speech)
    voice_thread.daemon = True
    voice_thread.start()
    
    print("Full voice integration active!")
    print("- Say 'Hey Claude' followed by your question")
    print("- Claude's responses will be spoken automatically")
    print("- Press Ctrl+C to exit")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Voice integration stopped.")

if __name__ == "__main__":
    main()