"""
Save/Load System
Handles game state persistence
"""

import json
import os
from src.config import SAVE_FILE


class SaveSystem:
    """Manages saving and loading game state"""

    @staticmethod
    def save_game(resources, upgrades, adventures_journal):
        """Save the current game state"""
        save_data = {
            'version': '1.0',
            'resources': resources.to_dict(),
            'upgrades': upgrades.to_dict(),
            'adventures_journal': adventures_journal
        }

        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    @staticmethod
    def load_game(resources, upgrades):
        """Load the game state"""
        if not os.path.exists(SAVE_FILE):
            return None

        try:
            with open(SAVE_FILE, 'r') as f:
                save_data = json.load(f)

            # Load resources
            resources.from_dict(save_data.get('resources', {}))

            # Load upgrades first
            upgrades.from_dict(save_data.get('upgrades', {}))

            # Re-apply all upgrade effects
            SaveSystem._reapply_upgrades(resources, upgrades)

            # Load adventures journal
            adventures_journal = save_data.get('adventures_journal', [])

            return adventures_journal

        except Exception as e:
            print(f"Error loading game: {e}")
            return None

    @staticmethod
    def _reapply_upgrades(resources, upgrades):
        """Reapply all upgrade effects after loading"""
        # Reset to base values
        from src.config import BASE_WARMTH_RATE, WARMTH_MULTIPLIER, INSPIRATION_MULTIPLIER

        resources.warmth_per_second = BASE_WARMTH_RATE
        resources.warmth_multiplier = WARMTH_MULTIPLIER
        resources.inspiration_per_click = 1.0
        resources.inspiration_multiplier = INSPIRATION_MULTIPLIER

        # Apply each upgrade's effect based on its current level
        for upgrade in upgrades.upgrades.values():
            for _ in range(upgrade.current_level):
                if upgrade.effect_type == 'warmth_per_second':
                    resources.warmth_per_second += upgrade.effect_value
                elif upgrade.effect_type == 'warmth_multiplier':
                    resources.warmth_multiplier += upgrade.effect_value
                elif upgrade.effect_type == 'inspiration_per_click':
                    resources.inspiration_per_click += upgrade.effect_value
                elif upgrade.effect_type == 'inspiration_multiplier':
                    resources.inspiration_multiplier += upgrade.effect_value

    @staticmethod
    def delete_save():
        """Delete the save file"""
        try:
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
                return True
        except Exception as e:
            print(f"Error deleting save: {e}")
        return False
