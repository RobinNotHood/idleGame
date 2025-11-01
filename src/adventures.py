"""
Adventure System
Manages the prestige/adventure mechanic and travel journal
"""


class AdventureManager:
    """Manages adventures and the travel journal"""

    ADVENTURES = [
        {
            'name': 'Camping Trip to Pine Valley',
            'description': 'A peaceful weekend in the woods with a crackling campfire and endless stars.',
            'journal_entry': "The pine trees swayed gently as I set up my tent. That night, sitting by the fire with my guitar, I felt truly at peace. The forest sounds were my backing band."
        },
        {
            'name': 'Ski Weekend in the Mountains',
            'description': 'Fresh powder, crisp air, and the thrill of carving down pristine slopes.',
            'journal_entry': "The mountain air was so crisp it made my nose tingle! After a day on the slopes, the lodge's fireplace felt earned. I made friends with other travelers over hot cocoa."
        },
        {
            'name': 'Road Trip Along the Coast',
            'description': 'Miles of scenic highway, ocean views, and spontaneous stops at cozy cafes.',
            'journal_entry': "The coastal road wound like a ribbon along the cliffs. I stopped at every lookout point, camera in hand. The sunset from that little beach cafe was perfect."
        },
        {
            'name': 'Book Festival in the City',
            'description': 'Browse independent bookstores, meet authors, and discover new favorite stories.',
            'journal_entry': "So many books! I came home with a backpack full of new stories and a head full of inspiration. Met an author who signed my copy of their book - they even liked my hoodie!"
        },
        {
            'name': 'Autumn Hike Through Golden Woods',
            'description': 'Crunching leaves underfoot and the smell of autumn in the air.',
            'journal_entry': "The leaves were at peak color - golds, reds, and oranges everywhere. Found a perfect log to sit on and read for an hour. No phone signal, just the forest."
        },
        {
            'name': 'Music Festival Under the Stars',
            'description': 'Live music, new friends, and the joy of singing along under an open sky.',
            'journal_entry': "The energy of the crowd, the bass you could feel in your chest, the stars above. I discovered three new favorite bands and learned some new guitar techniques!"
        },
        {
            'name': 'Cozy Cabin Retreat',
            'description': 'A week of solitude, books, and crackling fires in a remote mountain cabin.',
            'journal_entry': "Just me, a stack of books, and the sound of rain on the roof. I read five novels, wrote some songs, and learned that silence can be the best company."
        },
        {
            'name': 'Train Journey Across the Country',
            'description': 'Watch the landscape change from your window while reading and sketching.',
            'journal_entry': "The rhythmic clacking of the train was so soothing. Made friends in the dining car and spent hours just watching the world roll by. Every mile was a new scene."
        }
    ]

    def __init__(self):
        self.journal_entries = []
        self.current_adventure_index = 0

    def get_next_adventure(self):
        """Get the next adventure to embark on"""
        adventure = self.ADVENTURES[self.current_adventure_index % len(self.ADVENTURES)]
        return adventure

    def complete_adventure(self):
        """Complete an adventure and add to journal"""
        adventure = self.get_next_adventure()
        self.journal_entries.append({
            'name': adventure['name'],
            'entry': adventure['journal_entry'],
            'adventure_number': len(self.journal_entries) + 1
        })
        self.current_adventure_index += 1
        return adventure

    def get_journal_entries(self):
        """Get all journal entries"""
        return self.journal_entries

    def to_dict(self):
        """Serialize for saving"""
        return self.journal_entries

    def from_dict(self, data):
        """Load from saved data"""
        self.journal_entries = data
        self.current_adventure_index = len(data)


class ItemScrapbook:
    """Manages flavor text for purchased items"""

    ITEM_STORIES = {
        'plant': "This little succulent sits on the windowsill. It's hardy and cheerful - reminds me to stay resilient too.",
        'rug': "Found this at a local market. It's impossibly soft and makes padding to the kitchen for midnight snacks so much cozier.",
        'lamp': "Perfect for reading late into the night. Warm light that doesn't hurt the eyes. Already finished two books by its glow!",
        'bookshelf': "Built it myself! Well, mostly. Okay, I followed the instructions very carefully. But it holds all my favorites now!",
        'fireplace': "The centerpiece of the room. Nothing beats curling up with a book and a warm drink with the fire crackling nearby.",
        'window': "Let in so much more light! Now I can see the sunrise while having morning coffee. Makes the whole room feel bigger.",
        'guitar_basic': "Finally figured out that G chord! My fingers are sore but it's so worth it. Time to learn some real songs.",
        'guitar_songs': "Learned 'Wonderwall' today. Yes, I'm that person. But also learned some folk songs and a blues progression!",
        'reading_speed': "Turns out I was sub-vocalizing every word. Now I flow through pages so much faster! More stories, here I come.",
        'guitar_advanced': "Fingerpicking was tough at first, but now my guitar sounds like two instruments. It's like magic!",
        'hobby_focus': "Found my flow state. When I'm in it, hours pass like minutes. That's when the best creativity happens."
    }

    def __init__(self):
        self.unlocked_items = set()

    def unlock_item(self, item_id):
        """Unlock an item's story"""
        self.unlocked_items.add(item_id)

    def get_item_story(self, item_id):
        """Get the story for an item"""
        return self.ITEM_STORIES.get(item_id, "")

    def get_all_unlocked_stories(self):
        """Get all unlocked item stories"""
        return [(item_id, self.ITEM_STORIES.get(item_id, ""))
                for item_id in self.unlocked_items
                if item_id in self.ITEM_STORIES]
