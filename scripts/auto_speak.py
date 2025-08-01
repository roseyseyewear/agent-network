#!/usr/bin/env python3
"""
Auto Text-to-Speech for Claude Responses
Monitors clipboard for new text and automatically speaks it
"""

import os
import sys
import time
import threading
import pyperclip
from text_to_speech import ElevenLabsTTS

class AutoSpeaker:
    def __init__(self):
        self.tts = ElevenLabsTTS()
        self.last_clipboard = ""
        self.running = False
        self.speaking = False
        
    def start_monitoring(self):
        """Start monitoring clipboard for new text"""
        self.running = True
        print("Auto-speak started. Copy Claude's responses to hear them!")
        print("Press Ctrl+C to stop.")
        
        try:
            while self.running:
                current_clipboard = pyperclip.paste()
                
                # Check if clipboard has new text
                if (current_clipboard != self.last_clipboard and 
                    current_clipboard.strip() and 
                    len(current_clipboard) > 10 and
                    not self.speaking):
                    
                    self.last_clipboard = current_clipboard
                    
                    # Start speaking in a separate thread
                    speak_thread = threading.Thread(
                        target=self._speak_text,
                        args=(current_clipboard,)
                    )
                    speak_thread.start()
                
                time.sleep(1)  # Check every second
                
        except KeyboardInterrupt:
            print("\nAuto-speak stopped.")
            self.running = False
    
    def _speak_text(self, text):
        """Speak text in a separate thread"""
        self.speaking = True
        try:
            # Clean up text (remove markdown, excessive whitespace)
            clean_text = self._clean_text(text)
            if clean_text:
                print(f"Speaking: {clean_text[:100]}...")
                self.tts.speak(clean_text)
        except Exception as e:
            print(f"Error speaking text: {e}")
        finally:
            self.speaking = False
    
    def _clean_text(self, text):
        """Clean text for better speech"""
        # Remove markdown formatting
        text = text.replace('**', '').replace('*', '')
        text = text.replace('##', '').replace('#', '')
        text = text.replace('```', '')
        text = text.replace('`', '')
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Skip if too short or looks like code
        if len(text) < 20 or text.startswith('cd ') or text.startswith('./'):
            return None
            
        return text

def main():
    speaker = AutoSpeaker()
    speaker.start_monitoring()

if __name__ == "__main__":
    main()