"""
Game Configuration
Defines all game constants, colors, and settings
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GAME_TITLE = "Milo's Cozy Adventures"

# Warm color palette inspired by Milo
COLORS = {
    'warm_cream': (255, 250, 235),
    'soft_brown': (139, 103, 78),
    'tan': (210, 180, 140),
    'warm_orange': (255, 160, 100),
    'golden_yellow': (255, 215, 120),
    'deep_brown': (101, 67, 33),
    'soft_white': (250, 245, 240),
    'text_dark': (80, 60, 50),
    'text_light': (255, 250, 235),
    'button_hover': (255, 180, 120),
    'progress_fill': (255, 200, 100),
}

# Resource generation rates (per second)
BASE_WARMTH_RATE = 1.0
BASE_INSPIRATION_CLICK = 1.0

# Game balance
WARMTH_MULTIPLIER = 1.0
INSPIRATION_MULTIPLIER = 1.0

# Save file
SAVE_FILE = "milo_save.json"

# UI Settings
UI_PADDING = 20
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 200
CORNER_RADIUS = 15

# Animation speeds
IDLE_ANIMATION_SPEED = 0.1
INTERACTION_ANIMATION_SPEED = 0.15
