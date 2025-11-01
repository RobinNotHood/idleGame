"""
Main Game Class
Orchestrates all game systems and manages the game loop
"""

import pygame
import sys
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, MIN_SCREEN_WIDTH, MIN_SCREEN_HEIGHT, FPS, GAME_TITLE, COLORS, UI_PADDING, BUTTON_HEIGHT, BUTTON_WIDTH
from src.resources import ResourceManager
from src.upgrades import UpgradeManager
from src.ui import UI, Button, UpgradeButton, Panel
from src.save_system import SaveSystem
from src.adventures import AdventureManager, ItemScrapbook


class Game:
    """Main game class with resizable window and dark mode"""

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game systems
        self.resources = ResourceManager()
        self.upgrades = UpgradeManager()
        self.adventures = AdventureManager()
        self.scrapbook = ItemScrapbook()
        self.ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Game state
        self.current_screen = "home"  # home, upgrades, memories, adventure, journal
        self.show_offline_popup = False
        self.offline_warmth_gained = 0

        # Load saved game
        self.load_game()

        # Milo state
        self.milo_animation_timer = 0
        self.milo_is_interacting = False
        self.interaction_timer = 0

    def load_game(self):
        """Load saved game data"""
        journal_data = SaveSystem.load_game(self.resources, self.upgrades)
        if journal_data:
            self.adventures.from_dict(journal_data)

            # Check for offline progress
            if self.resources.offline_time > 60:
                self.show_offline_popup = True
                self.offline_warmth_gained = self.resources.warmth - self.resources.total_warmth_earned + self.resources.offline_time * self.resources.warmth_per_second

    def save_game(self):
        """Save the game"""
        SaveSystem.save_game(self.resources, self.upgrades, self.adventures.to_dict())

    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.draw()

        # Save on exit
        self.save_game()

    def handle_events(self):
        """Handle all input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.VIDEORESIZE:
                # Handle window resize
                new_width = max(event.w, MIN_SCREEN_WIDTH)
                new_height = max(event.h, MIN_SCREEN_HEIGHT)
                self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                self.ui.resize(new_width, new_height)

            elif event.type == pygame.KEYDOWN:
                # Toggle dark mode with D key
                if event.key == pygame.K_d:
                    self.ui.toggle_dark_mode()

            # Let UI handle events first
            if self.ui.handle_event(event):
                continue

            # Handle screen-specific events
            if self.current_screen == "home":
                self.handle_home_events(event)

    def handle_home_events(self, event):
        """Handle events on the home screen (Milo interaction)"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if clicking on Milo area (responsive to window size)
            milo_rect = pygame.Rect(
                self.ui.screen_width // 2 - 150,
                self.ui.screen_height // 2 - 150,
                300, 300
            )
            if milo_rect.collidepoint(event.pos):
                # Generate inspiration
                inspiration = self.resources.click_hobby()
                self.milo_is_interacting = True
                self.interaction_timer = 0.5  # Half second interaction

    def update(self, dt):
        """Update game state"""
        # Update resources
        self.resources.update(dt)

        # Update UI (for button animations)
        self.ui.update(dt)

        # Update Milo animation
        self.milo_animation_timer += dt
        if self.milo_is_interacting:
            self.interaction_timer -= dt
            if self.interaction_timer <= 0:
                self.milo_is_interacting = False

        # Auto-save every 30 seconds
        if int(self.milo_animation_timer) % 30 == 0 and self.milo_animation_timer % 30 < dt:
            self.save_game()

    def draw(self):
        """Draw everything"""
        self.ui.draw_background(self.screen)

        # Draw current screen
        if self.current_screen == "home":
            self.draw_home_screen()
        elif self.current_screen == "upgrades":
            self.draw_upgrades_screen()
        elif self.current_screen == "memories":
            self.draw_memories_screen()
        elif self.current_screen == "adventure":
            self.draw_adventure_screen()
        elif self.current_screen == "journal":
            self.draw_journal_screen()
        elif self.current_screen == "scrapbook":
            self.draw_scrapbook_screen()

        # Draw resource bar at top (always visible)
        self.ui.draw_resources(self.screen, self.resources)

        # Draw navigation
        self.draw_navigation()

        # Draw offline popup if needed
        if self.show_offline_popup:
            self.draw_offline_popup()

        pygame.display.flip()

    def draw_navigation(self):
        """Draw navigation buttons"""
        nav_y = self.ui.screen_height - BUTTON_HEIGHT - UI_PADDING
        nav_buttons = [
            ("Home", "home"),
            ("Upgrades", "upgrades"),
            ("Memories", "memories"),
            ("Adventure", "adventure"),
            ("Journal", "journal"),
            ("Scrapbook", "scrapbook")
        ]

        button_width = 130
        total_width = button_width * len(nav_buttons) + UI_PADDING * (len(nav_buttons) - 1)
        start_x = (self.ui.screen_width - total_width) // 2

        # Clear old nav buttons
        self.ui.buttons = [b for b in self.ui.buttons if not hasattr(b, 'is_nav')]

        for i, (label, screen) in enumerate(nav_buttons):
            x = start_x + i * (button_width + UI_PADDING)

            # Highlight current screen
            color = COLORS['accent'] if screen == self.current_screen else COLORS['button']

            btn = Button(x, nav_y, button_width, BUTTON_HEIGHT - 10,
                         label,
                         lambda s=screen: self.switch_screen(s),
                         color=color)
            btn.is_nav = True
            self.ui.add_button(btn)
            btn.draw(self.screen, self.ui.small_font)

    def switch_screen(self, screen):
        """Switch to a different screen"""
        self.current_screen = screen
        self.ui.clear_buttons()

    def draw_home_screen(self):
        """Draw the main home screen with Milo"""
        # Title
        title = self.ui.title_font.render("Milo's Cozy Adventures", True, COLORS['text'])
        title_rect = title.get_rect(centerx=self.ui.screen_width // 2, top=100)
        self.screen.blit(title, title_rect)

        # Subtitle (dark mode hint)
        subtitle = "Press 'D' to toggle dark mode"
        subtitle_surface = self.ui.small_font.render(subtitle, True, COLORS['text_secondary'])
        subtitle_rect = subtitle_surface.get_rect(centerx=self.ui.screen_width // 2, top=title_rect.bottom + 5)
        self.screen.blit(subtitle_surface, subtitle_rect)

        # Milo area (clickable)
        milo_center_x = self.ui.screen_width // 2
        milo_center_y = self.ui.screen_height // 2

        # Draw Milo (simple representation - a cozy circle with features)
        self.draw_milo(milo_center_x, milo_center_y)

        # Instruction text
        instruction = "Click on Milo to gain Inspiration!"
        inst_surface = self.ui.medium_font.render(instruction, True, COLORS['text'])
        inst_rect = inst_surface.get_rect(centerx=self.ui.screen_width // 2, top=milo_center_y + 180)
        self.screen.blit(inst_surface, inst_rect)

        # Stats panel
        stats_panel = Panel(UI_PADDING, self.ui.screen_height - 250, 350, 150, "Progress")
        stats_panel.draw(self.screen, self.ui.medium_font)

        stats_y = self.ui.screen_height - 210
        self.ui.draw_text(self.screen, f"Adventures: {self.resources.adventures_completed}",
                          UI_PADDING + 20, stats_y, self.ui.small_font)
        self.ui.draw_text(self.screen, f"Total Warmth: {int(self.resources.total_warmth_earned)}",
                          UI_PADDING + 20, stats_y + 30, self.ui.small_font)
        self.ui.draw_text(self.screen, f"Total Inspiration: {int(self.resources.total_inspiration_earned)}",
                          UI_PADDING + 20, stats_y + 60, self.ui.small_font)

    def draw_milo(self, x, y):
        """Draw Milo character (simplified) - works in both light and dark mode"""
        # Base color - brown for Milo's fur (always consistent)
        base_color = COLORS['milo_base']
        accent_color = COLORS['milo_accent']

        # Body (large circle)
        body_radius = 80
        pygame.draw.circle(self.screen, base_color, (x, y), body_radius)
        pygame.draw.circle(self.screen, COLORS['border'], (x, y), body_radius, 3)

        # Face patch (lighter)
        face_radius = 50
        pygame.draw.circle(self.screen, accent_color, (x, y + 10), face_radius)

        # Eyes
        eye_color = COLORS['accent']
        left_eye = (x - 25, y - 10)
        right_eye = (x + 25, y - 10)
        pygame.draw.circle(self.screen, eye_color, left_eye, 12)
        pygame.draw.circle(self.screen, eye_color, right_eye, 12)
        pygame.draw.circle(self.screen, COLORS['border'], left_eye, 6)
        pygame.draw.circle(self.screen, COLORS['border'], right_eye, 6)

        # Nose
        nose_points = [(x, y + 15), (x - 8, y + 5), (x + 8, y + 5)]
        pygame.draw.polygon(self.screen, COLORS['border'], nose_points)

        # Ears
        left_ear = (x - 60, y - 60)
        right_ear = (x + 60, y - 60)
        pygame.draw.circle(self.screen, base_color, left_ear, 25)
        pygame.draw.circle(self.screen, base_color, right_ear, 25)
        pygame.draw.circle(self.screen, COLORS['border'], left_ear, 25, 2)
        pygame.draw.circle(self.screen, COLORS['border'], right_ear, 25, 2)

        # Interaction effect
        if self.milo_is_interacting:
            # Draw sparkles around Milo
            sparkle_color = COLORS['accent']
            for i in range(6):
                angle = (self.milo_animation_timer * 3 + i * 60) % 360
                import math
                sparkle_x = x + int(math.cos(math.radians(angle)) * 100)
                sparkle_y = y + int(math.sin(math.radians(angle)) * 100)
                pygame.draw.circle(self.screen, sparkle_color, (sparkle_x, sparkle_y), 5)

    def draw_upgrades_screen(self):
        """Draw the upgrades screen - compact for easy scanning"""
        # Title
        self.ui.draw_text(self.screen, "Upgrades", self.ui.screen_width // 2 - 50, 100,
                          self.ui.large_font, COLORS['text'])

        # Get warmth and inspiration upgrades
        warmth_upgrades = self.upgrades.get_available_upgrades(self.resources, 'warmth')
        inspiration_upgrades = self.upgrades.get_available_upgrades(self.resources, 'inspiration')

        # Draw warmth upgrades (left column)
        self.draw_upgrade_column("Cozy Home", warmth_upgrades, UI_PADDING, 160, self.ui.screen_width // 2 - UI_PADDING - 20)

        # Draw inspiration upgrades (right column)
        self.draw_upgrade_column("Skills & Hobbies", inspiration_upgrades,
                                  self.ui.screen_width // 2 + 20, 160, self.ui.screen_width // 2 - UI_PADDING - 20)

    def draw_upgrade_column(self, title, upgrades, x, y, width):
        """Draw a column of upgrades - compact list"""
        panel = Panel(x, y - 40, width, 30, title, COLORS['button'])
        panel.draw(self.screen, self.ui.medium_font)

        current_y = y + 10
        button_height = 40  # Compact buttons

        for upgrade in upgrades:
            if not upgrade.can_purchase(self.resources) and upgrade.current_level >= upgrade.max_level:
                continue  # Don't show maxed upgrades that can't be repeated

            btn = UpgradeButton(x + 10, current_y, width - 20, button_height,
                                upgrade,
                                lambda u=upgrade: self.purchase_upgrade(u),
                                self.resources)

            btn.draw(self.screen, self.ui.small_font, self.ui.small_font)
            self.ui.add_button(btn)

            # Draw effect description next to button (compact)
            desc_text = upgrade.description[:50] + "..." if len(upgrade.description) > 50 else upgrade.description
            desc_surface = self.ui.small_font.render(desc_text, True, COLORS['text_secondary'])
            desc_rect = desc_surface.get_rect(left=x + 15, top=current_y + button_height + 3)
            self.screen.blit(desc_surface, desc_rect)

            current_y += button_height + 30  # Compact spacing

    def purchase_upgrade(self, upgrade):
        """Purchase an upgrade"""
        if self.upgrades.purchase_upgrade(upgrade.id, self.resources):
            # Add to scrapbook if it's a special item
            if upgrade.id in ['plant', 'rug', 'lamp', 'bookshelf', 'fireplace', 'window',
                              'guitar_basic', 'guitar_songs', 'reading_speed', 'guitar_advanced', 'hobby_focus']:
                self.scrapbook.unlock_item(upgrade.id)
            self.save_game()

    def draw_memories_screen(self):
        """Draw the Scrapbook of Memories screen"""
        # Title
        self.ui.draw_text(self.screen, "Scrapbook of Memories", SCREEN_WIDTH // 2 - 180, 100,
                          self.ui.large_font, COLORS['deep_brown'])

        # Subtitle
        subtitle = "Permanent upgrades from your adventures"
        self.ui.draw_text(self.screen, subtitle, SCREEN_WIDTH // 2 - 200, 150,
                          self.ui.small_font, COLORS['soft_brown'])

        # Get memory upgrades
        memory_upgrades = self.upgrades.get_available_upgrades(self.resources, 'memories')

        current_y = 200
        for upgrade in memory_upgrades:
            btn = UpgradeButton(SCREEN_WIDTH // 2 - 200, current_y, 400, BUTTON_HEIGHT,
                                upgrade,
                                lambda u=upgrade: self.purchase_upgrade(u),
                                self.resources)

            btn.draw(self.screen, self.ui.small_font, self.ui.small_font)
            self.ui.add_button(btn)

            # Draw description
            desc_y = current_y + BUTTON_HEIGHT + 25
            self.ui.draw_multiline_text(self.screen, upgrade.description,
                                         SCREEN_WIDTH // 2 - 190, desc_y, 380,
                                         self.ui.small_font, COLORS['soft_brown'])

            current_y += BUTTON_HEIGHT + 80

    def draw_adventure_screen(self):
        """Draw the adventure planning screen"""
        # Title
        self.ui.draw_text(self.screen, "Plan Your Next Adventure", SCREEN_WIDTH // 2 - 200, 100,
                          self.ui.large_font, COLORS['deep_brown'])

        # Get next adventure
        next_adventure = self.adventures.get_next_adventure()

        # Adventure panel
        panel = Panel(SCREEN_WIDTH // 2 - 300, 200, 600, 300)
        panel.draw(self.screen, self.ui.medium_font)

        # Adventure name
        self.ui.draw_text(self.screen, next_adventure['name'],
                          SCREEN_WIDTH // 2 - 280, 230,
                          self.ui.large_font, COLORS['deep_brown'])

        # Description
        self.ui.draw_multiline_text(self.screen, next_adventure['description'],
                                     SCREEN_WIDTH // 2 - 280, 280, 560,
                                     self.ui.medium_font, COLORS['text_dark'])

        # Info about what happens
        info_text = "Starting an adventure will reset your Warmth and Inspiration, but you'll earn Memories based on your progress!"
        self.ui.draw_multiline_text(self.screen, info_text,
                                     SCREEN_WIDTH // 2 - 280, 360, 560,
                                     self.ui.small_font, COLORS['soft_brown'])

        # Potential memories
        potential_memories = int((self.resources.total_warmth_earned / 1000) +
                                 (self.resources.total_inspiration_earned / 500))
        potential_memories = max(1, potential_memories)

        memories_text = f"Potential Memories to earn: {potential_memories}"
        self.ui.draw_text(self.screen, memories_text,
                          SCREEN_WIDTH // 2 - 280, 430,
                          self.ui.medium_font, COLORS['golden_yellow'])

        # Start adventure button
        btn = Button(SCREEN_WIDTH // 2 - 150, 470, 300, BUTTON_HEIGHT + 10,
                     "Begin Adventure!",
                     self.start_adventure,
                     COLORS['golden_yellow'])
        btn.draw(self.screen, self.ui.medium_font)
        self.ui.add_button(btn)

    def start_adventure(self):
        """Start an adventure (prestige)"""
        # Complete the adventure
        adventure = self.adventures.complete_adventure()
        memories_earned = self.resources.start_adventure()

        # Save the game
        self.save_game()

        # Switch to journal to see the new entry
        self.switch_screen("journal")

    def draw_journal_screen(self):
        """Draw the travel journal"""
        # Title
        self.ui.draw_text(self.screen, "Travel Journal", SCREEN_WIDTH // 2 - 120, 100,
                          self.ui.large_font, COLORS['deep_brown'])

        # Get journal entries
        entries = self.adventures.get_journal_entries()

        if not entries:
            no_entries = "No adventures yet! Start your first adventure to begin writing your story."
            self.ui.draw_multiline_text(self.screen, no_entries,
                                         SCREEN_WIDTH // 2 - 300, 200, 600,
                                         self.ui.medium_font, COLORS['soft_brown'])
            return

        # Draw entries (most recent first)
        current_y = 180
        for entry in reversed(entries[-5:]):  # Show last 5 entries
            panel = Panel(UI_PADDING + 50, current_y, SCREEN_WIDTH - 2 * UI_PADDING - 100, 100)
            panel.draw(self.screen, self.ui.small_font)

            # Adventure number and name
            header = f"Adventure #{entry['adventure_number']}: {entry['name']}"
            self.ui.draw_text(self.screen, header,
                              UI_PADDING + 70, current_y + 15,
                              self.ui.medium_font, COLORS['deep_brown'])

            # Journal entry
            self.ui.draw_multiline_text(self.screen, entry['entry'],
                                         UI_PADDING + 70, current_y + 50,
                                         SCREEN_WIDTH - 2 * UI_PADDING - 140,
                                         self.ui.small_font, COLORS['text_dark'])

            current_y += 120

    def draw_scrapbook_screen(self):
        """Draw the item scrapbook"""
        # Title
        self.ui.draw_text(self.screen, "Item Scrapbook", SCREEN_WIDTH // 2 - 120, 100,
                          self.ui.large_font, COLORS['deep_brown'])

        # Get unlocked stories
        stories = self.scrapbook.get_all_unlocked_stories()

        if not stories:
            no_items = "Purchase upgrades to unlock their stories!"
            self.ui.draw_multiline_text(self.screen, no_items,
                                         SCREEN_WIDTH // 2 - 250, 200, 500,
                                         self.ui.medium_font, COLORS['soft_brown'])
            return

        # Draw stories
        current_y = 180
        for item_id, story in stories:
            # Get the upgrade to show its name
            upgrade = self.upgrades.get_upgrade(item_id)
            if not upgrade:
                continue

            panel = Panel(UI_PADDING + 50, current_y, SCREEN_WIDTH - 2 * UI_PADDING - 100, 90)
            panel.draw(self.screen, self.ui.small_font)

            # Item name
            self.ui.draw_text(self.screen, upgrade.name,
                              UI_PADDING + 70, current_y + 15,
                              self.ui.medium_font, COLORS['deep_brown'])

            # Story
            self.ui.draw_multiline_text(self.screen, story,
                                         UI_PADDING + 70, current_y + 45,
                                         SCREEN_WIDTH - 2 * UI_PADDING - 140,
                                         self.ui.small_font, COLORS['text_dark'])

            current_y += 110

            if current_y > SCREEN_HEIGHT - 200:
                break  # Don't overflow screen

    def draw_offline_popup(self):
        """Draw popup showing offline progress"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(COLORS['deep_brown'])
        self.screen.blit(overlay, (0, 0))

        # Popup panel
        panel = Panel(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 150, 500, 300,
                      "Welcome Back!", COLORS['warm_cream'])
        panel.draw(self.screen, self.ui.large_font)

        # Time away
        hours = int(self.resources.offline_time // 3600)
        minutes = int((self.resources.offline_time % 3600) // 60)
        time_text = f"You were away for {hours}h {minutes}m"

        self.ui.draw_text(self.screen, time_text,
                          SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 80,
                          self.ui.medium_font)

        # Warmth gained
        warmth_text = f"Warmth earned while away: {int(self.offline_warmth_gained)}"
        self.ui.draw_text(self.screen, warmth_text,
                          SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 30,
                          self.ui.medium_font, COLORS['golden_yellow'])

        # Close button
        close_btn = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, BUTTON_HEIGHT,
                           "Continue",
                           self.close_offline_popup,
                           COLORS['warm_orange'])
        close_btn.draw(self.screen, self.ui.medium_font)
        self.ui.add_button(close_btn)

    def close_offline_popup(self):
        """Close the offline popup"""
        self.show_offline_popup = False
