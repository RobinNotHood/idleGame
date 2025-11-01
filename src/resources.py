"""
Resource Management System
Handles Warmth, Inspiration, and Memories
"""

import time
from src.config import BASE_WARMTH_RATE, WARMTH_MULTIPLIER, INSPIRATION_MULTIPLIER


class ResourceManager:
    """Manages all game resources and their generation"""

    def __init__(self):
        self.warmth = 0.0
        self.inspiration = 0.0
        self.memories = 0

        # Generation rates
        self.warmth_per_second = BASE_WARMTH_RATE
        self.inspiration_per_click = 1.0

        # Multipliers from upgrades
        self.warmth_multiplier = WARMTH_MULTIPLIER
        self.inspiration_multiplier = INSPIRATION_MULTIPLIER

        # Lifetime stats
        self.total_warmth_earned = 0.0
        self.total_inspiration_earned = 0.0
        self.adventures_completed = 0

        # Time tracking
        self.last_update_time = time.time()
        self.offline_time = 0

    def update(self, dt):
        """Update passive resource generation"""
        # Generate warmth passively
        warmth_gain = self.warmth_per_second * self.warmth_multiplier * dt
        self.warmth += warmth_gain
        self.total_warmth_earned += warmth_gain

    def click_hobby(self, hobby_type="guitar"):
        """Generate inspiration from active clicking"""
        inspiration_gain = self.inspiration_per_click * self.inspiration_multiplier
        self.inspiration += inspiration_gain
        self.total_inspiration_earned += inspiration_gain
        return inspiration_gain

    def can_afford(self, resource_type, amount):
        """Check if player can afford a cost"""
        if resource_type == "warmth":
            return self.warmth >= amount
        elif resource_type == "inspiration":
            return self.inspiration >= amount
        elif resource_type == "memories":
            return self.memories >= amount
        return False

    def spend_resource(self, resource_type, amount):
        """Spend a resource if affordable"""
        if not self.can_afford(resource_type, amount):
            return False

        if resource_type == "warmth":
            self.warmth -= amount
        elif resource_type == "inspiration":
            self.inspiration -= amount
        elif resource_type == "memories":
            self.memories -= amount

        return True

    def start_adventure(self):
        """Begin an adventure (prestige reset)"""
        # Calculate memories earned based on progress
        memories_earned = int((self.total_warmth_earned / 1000) + (self.total_inspiration_earned / 500))
        memories_earned = max(1, memories_earned)  # At least 1 memory

        self.memories += memories_earned
        self.adventures_completed += 1

        # Reset current run resources
        self.warmth = 0
        self.inspiration = 0
        self.total_warmth_earned = 0
        self.total_inspiration_earned = 0

        return memories_earned

    def calculate_offline_progress(self, offline_seconds):
        """Calculate progress made while offline"""
        # Only warmth generates offline, capped at 24 hours
        max_offline = 24 * 3600  # 24 hours
        offline_seconds = min(offline_seconds, max_offline)

        offline_warmth = self.warmth_per_second * self.warmth_multiplier * offline_seconds
        self.warmth += offline_warmth
        self.total_warmth_earned += offline_warmth
        self.offline_time = offline_seconds

        return offline_warmth

    def to_dict(self):
        """Serialize to dictionary for saving"""
        return {
            'warmth': self.warmth,
            'inspiration': self.inspiration,
            'memories': self.memories,
            'warmth_per_second': self.warmth_per_second,
            'inspiration_per_click': self.inspiration_per_click,
            'warmth_multiplier': self.warmth_multiplier,
            'inspiration_multiplier': self.inspiration_multiplier,
            'total_warmth_earned': self.total_warmth_earned,
            'total_inspiration_earned': self.total_inspiration_earned,
            'adventures_completed': self.adventures_completed,
            'last_update_time': time.time()
        }

    def from_dict(self, data):
        """Load from dictionary"""
        self.warmth = data.get('warmth', 0)
        self.inspiration = data.get('inspiration', 0)
        self.memories = data.get('memories', 0)
        self.warmth_per_second = data.get('warmth_per_second', BASE_WARMTH_RATE)
        self.inspiration_per_click = data.get('inspiration_per_click', 1.0)
        self.warmth_multiplier = data.get('warmth_multiplier', WARMTH_MULTIPLIER)
        self.inspiration_multiplier = data.get('inspiration_multiplier', INSPIRATION_MULTIPLIER)
        self.total_warmth_earned = data.get('total_warmth_earned', 0)
        self.total_inspiration_earned = data.get('total_inspiration_earned', 0)
        self.adventures_completed = data.get('adventures_completed', 0)

        # Calculate offline progress
        last_time = data.get('last_update_time', time.time())
        offline_seconds = time.time() - last_time
        if offline_seconds > 60:  # Only if offline for more than 1 minute
            self.calculate_offline_progress(offline_seconds)

        self.last_update_time = time.time()
