"""
Game Configuration
Defines all game constants, colors, and settings
"""

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MIN_SCREEN_WIDTH = 800
MIN_SCREEN_HEIGHT = 600
FPS = 60
GAME_TITLE = "Milo's Cozy Adventures"

# Light theme - Warm color palette inspired by Milo
COLORS_LIGHT = {
    'bg': (255, 250, 235),
    'bg_secondary': (250, 245, 240),
    'panel': (250, 245, 240),
    'button': (255, 160, 100),
    'button_hover': (255, 180, 120),
    'button_active': (255, 140, 80),
    'button_disabled': (210, 180, 140),
    'border': (101, 67, 33),
    'text': (80, 60, 50),
    'text_secondary': (139, 103, 78),
    'text_light': (255, 250, 235),
    'accent': (255, 215, 120),
    'success': (100, 200, 100),
    'milo_base': (139, 103, 78),
    'milo_accent': (210, 180, 140),
}

# Dark theme - Modern dark palette with warm accents
COLORS_DARK = {
    'bg': (25, 25, 30),
    'bg_secondary': (35, 35, 42),
    'panel': (40, 40, 48),
    'button': (255, 160, 100),
    'button_hover': (255, 180, 120),
    'button_active': (255, 140, 80),
    'button_disabled': (80, 80, 90),
    'border': (60, 60, 70),
    'text': (230, 230, 235),
    'text_secondary': (160, 160, 170),
    'text_light': (255, 250, 235),
    'accent': (255, 215, 120),
    'success': (100, 200, 100),
    'milo_base': (139, 103, 78),
    'milo_accent': (210, 180, 140),
}

# Default to light theme
COLORS = COLORS_LIGHT

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
