"""
Upgrade System
Manages all upgrades for warmth, inspiration, and prestige bonuses
"""


class Upgrade:
    """Represents a single upgrade"""

    def __init__(self, id, name, description, cost, cost_type, effect_type, effect_value, repeatable=False, max_level=1):
        self.id = id
        self.name = name
        self.description = description
        self.base_cost = cost
        self.cost_type = cost_type  # 'warmth', 'inspiration', or 'memories'
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.repeatable = repeatable
        self.max_level = max_level
        self.current_level = 0

    def get_current_cost(self):
        """Calculate cost based on current level"""
        if not self.repeatable:
            return self.base_cost
        # Exponential scaling: cost * (1.15 ^ level)
        return int(self.base_cost * (1.15 ** self.current_level))

    def can_purchase(self, resources):
        """Check if upgrade can be purchased"""
        if not self.repeatable and self.current_level >= self.max_level:
            return False

        cost = self.get_current_cost()
        return resources.can_afford(self.cost_type, cost)

    def purchase(self, resources):
        """Purchase the upgrade"""
        if not self.can_purchase(resources):
            return False

        cost = self.get_current_cost()
        if resources.spend_resource(self.cost_type, cost):
            self.current_level += 1
            self.apply_effect(resources)
            return True
        return False

    def apply_effect(self, resources):
        """Apply the upgrade effect to resources"""
        if self.effect_type == 'warmth_per_second':
            resources.warmth_per_second += self.effect_value
        elif self.effect_type == 'warmth_multiplier':
            resources.warmth_multiplier += self.effect_value
        elif self.effect_type == 'inspiration_per_click':
            resources.inspiration_per_click += self.effect_value
        elif self.effect_type == 'inspiration_multiplier':
            resources.inspiration_multiplier += self.effect_value

    def to_dict(self):
        """Serialize upgrade progress"""
        return {
            'id': self.id,
            'current_level': self.current_level
        }


class UpgradeManager:
    """Manages all game upgrades"""

    def __init__(self):
        self.upgrades = {}
        self.initialize_upgrades()

    def initialize_upgrades(self):
        """Create all available upgrades"""

        # Warmth upgrades (Living Space improvements)
        warmth_upgrades = [
            Upgrade('plant', 'Potted Plant', 'A cheerful succulent for the windowsill. +0.5 Warmth/s',
                    cost=10, cost_type='warmth', effect_type='warmth_per_second', effect_value=0.5,
                    repeatable=False, max_level=1),

            Upgrade('rug', 'Soft Rug', 'A cozy rug to pad around on. +1.0 Warmth/s',
                    cost=50, cost_type='warmth', effect_type='warmth_per_second', effect_value=1.0,
                    repeatable=False, max_level=1),

            Upgrade('lamp', 'Reading Lamp', 'Perfect for late-night reading sessions. +2.0 Warmth/s',
                    cost=150, cost_type='warmth', effect_type='warmth_per_second', effect_value=2.0,
                    repeatable=False, max_level=1),

            Upgrade('bookshelf', 'Bookshelf', 'A place for all your favorite stories. +4.0 Warmth/s',
                    cost=400, cost_type='warmth', effect_type='warmth_per_second', effect_value=4.0,
                    repeatable=False, max_level=1),

            Upgrade('fireplace', 'Cozy Fireplace', 'The heart of any warm home. +8.0 Warmth/s',
                    cost=1000, cost_type='warmth', effect_type='warmth_per_second', effect_value=8.0,
                    repeatable=False, max_level=1),

            Upgrade('window', 'Bay Window', 'Let the sunshine in! +15.0 Warmth/s',
                    cost=2500, cost_type='warmth', effect_type='warmth_per_second', effect_value=15.0,
                    repeatable=False, max_level=1),
        ]

        # Inspiration upgrades (Skill improvements)
        inspiration_upgrades = [
            Upgrade('guitar_basic', 'Learn Basic Chords', 'Master the fundamentals. +0.5 Inspiration/click',
                    cost=20, cost_type='inspiration', effect_type='inspiration_per_click', effect_value=0.5,
                    repeatable=False, max_level=1),

            Upgrade('guitar_songs', 'Learn New Songs', 'Expand your repertoire. +1.0 Inspiration/click',
                    cost=75, cost_type='inspiration', effect_type='inspiration_per_click', effect_value=1.0,
                    repeatable=False, max_level=1),

            Upgrade('reading_speed', 'Speed Reading', 'Devour books faster! +1.5 Inspiration/click',
                    cost=100, cost_type='inspiration', effect_type='inspiration_per_click', effect_value=1.5,
                    repeatable=False, max_level=1),

            Upgrade('guitar_advanced', 'Advanced Techniques', 'Fingerpicking mastery. +2.5 Inspiration/click',
                    cost=300, cost_type='inspiration', effect_type='inspiration_per_click', effect_value=2.5,
                    repeatable=False, max_level=1),

            Upgrade('hobby_focus', 'Deep Focus', 'Find your flow state. +5.0 Inspiration/click',
                    cost=750, cost_type='inspiration', effect_type='inspiration_per_click', effect_value=5.0,
                    repeatable=False, max_level=1),
        ]

        # Memory upgrades (Prestige bonuses - Scrapbook of Memories)
        memory_upgrades = [
            Upgrade('memory_warmth1', 'Expert Camper', 'Start each adventure with more comfort. +10% Warmth generation',
                    cost=1, cost_type='memories', effect_type='warmth_multiplier', effect_value=0.1,
                    repeatable=True, max_level=999),

            Upgrade('memory_inspiration1', 'Seasoned Traveller', 'Your experiences fuel creativity. +10% Inspiration gain',
                    cost=1, cost_type='memories', effect_type='inspiration_multiplier', effect_value=0.1,
                    repeatable=True, max_level=999),

            Upgrade('memory_warmth2', 'Cozy Master', 'You know all the best spots. +1.0 Warmth/s',
                    cost=2, cost_type='memories', effect_type='warmth_per_second', effect_value=1.0,
                    repeatable=True, max_level=999),

            Upgrade('memory_inspiration2', 'Creative Soul', 'Ideas flow naturally. +1.0 Inspiration/click',
                    cost=2, cost_type='memories', effect_type='inspiration_per_click', effect_value=1.0,
                    repeatable=True, max_level=999),
        ]

        # Add all upgrades to the manager
        for upgrade in warmth_upgrades + inspiration_upgrades + memory_upgrades:
            self.upgrades[upgrade.id] = upgrade

    def get_available_upgrades(self, resources, filter_type=None):
        """Get list of available upgrades, optionally filtered by cost type"""
        available = []
        for upgrade in self.upgrades.values():
            if filter_type and upgrade.cost_type != filter_type:
                continue
            if upgrade.current_level < upgrade.max_level or upgrade.repeatable:
                available.append(upgrade)
        return available

    def get_upgrade(self, upgrade_id):
        """Get a specific upgrade by ID"""
        return self.upgrades.get(upgrade_id)

    def purchase_upgrade(self, upgrade_id, resources):
        """Attempt to purchase an upgrade"""
        upgrade = self.get_upgrade(upgrade_id)
        if upgrade:
            return upgrade.purchase(resources)
        return False

    def to_dict(self):
        """Serialize all upgrade progress"""
        return {
            'upgrades': [upgrade.to_dict() for upgrade in self.upgrades.values()]
        }

    def from_dict(self, data):
        """Load upgrade progress"""
        upgrade_data = data.get('upgrades', [])
        for saved_upgrade in upgrade_data:
            upgrade_id = saved_upgrade.get('id')
            if upgrade_id in self.upgrades:
                self.upgrades[upgrade_id].current_level = saved_upgrade.get('current_level', 0)
