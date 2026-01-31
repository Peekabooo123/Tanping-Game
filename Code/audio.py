import pygame
from pygame import mixer
from CONFIG import SOUND_FILES

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        for name, file in SOUND_FILES.items():
            try:
                self.sounds[name] = mixer.Sound(file)
            except:
                print(f"Warning: Could not load sound file {file}")
                # Create dummy sound object
                self.sounds[name] = type('DummySound', (), {'play': lambda: None})()

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
