"""
UI System
Handles all user interface rendering and interaction
"""

import pygame
from src.config import COLORS, UI_PADDING, BUTTON_HEIGHT, BUTTON_WIDTH, CORNER_RADIUS


class Button:
    """Modern, responsive button with smooth hover effects"""

    def __init__(self, x, y, width, height, text, callback, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.base_color = color or COLORS['button']
        self.hover_color = COLORS['button_hover']
        self.active_color = COLORS['button_active']
        self.disabled_color = COLORS['button_disabled']
        self.text_color = COLORS['text']
        self.is_hovered = False
        self.is_pressed = False
        self.enabled = True
        self.hover_animation = 0.0  # 0.0 to 1.0

    def update(self, dt):
        """Update button animations"""
        # Smooth hover animation
        target = 1.0 if self.is_hovered and self.enabled else 0.0
        if self.hover_animation < target:
            self.hover_animation = min(1.0, self.hover_animation + dt * 8)
        elif self.hover_animation > target:
            self.hover_animation = max(0.0, self.hover_animation - dt * 8)

    def draw(self, screen, font):
        """Draw the button with smooth hover effects"""
        # Determine color based on state
        if not self.enabled:
            color = self.disabled_color
        elif self.is_pressed:
            color = self.active_color
        else:
            # Interpolate between base and hover color
            t = self.hover_animation
            color = tuple(int(self.base_color[i] * (1 - t) + self.hover_color[i] * t) for i in range(3))

        # Draw shadow for depth (only when enabled)
        if self.enabled and self.hover_animation > 0:
            shadow_offset = 2
            shadow_rect = self.rect.copy()
            shadow_rect.x += shadow_offset
            shadow_rect.y += shadow_offset
            shadow_color = tuple(max(0, c - 50) for c in COLORS['bg'])
            pygame.draw.rect(screen, shadow_color, shadow_rect, border_radius=CORNER_RADIUS)

        # Draw main button
        pygame.draw.rect(screen, color, self.rect, border_radius=CORNER_RADIUS)

        # Draw border with glow effect when hovered
        border_width = 3 if self.hover_animation > 0.5 else 2
        pygame.draw.rect(screen, COLORS['border'], self.rect, width=border_width, border_radius=CORNER_RADIUS)

        # Draw text
        text_color = self.text_color if self.enabled else COLORS['text_secondary']
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.enabled:
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_pressed and self.rect.collidepoint(event.pos) and self.enabled:
                self.is_pressed = False
                self.callback()
                return True
            self.is_pressed = False
        return False

    def update_position(self, x, y):
        """Update button position"""
        self.rect.x = x
        self.rect.y = y

    def check_hover(self, mouse_pos):
        """Check if mouse is hovering (call every frame)"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)


class UpgradeButton(Button):
    """Modern upgrade button with cost display and effect preview"""

    def __init__(self, x, y, width, height, upgrade, callback, resources):
        self.upgrade = upgrade
        self.resources = resources
        super().__init__(x, y, width, height, upgrade.name, callback)

    def draw(self, screen, font, small_font):
        """Draw upgrade button with cost and effect info"""
        # Check if affordable
        self.enabled = self.upgrade.can_purchase(self.resources)

        # Create compact button text with level
        if self.upgrade.repeatable and self.upgrade.current_level > 0:
            self.text = f"{self.upgrade.name} [{self.upgrade.current_level}]"
        else:
            self.text = self.upgrade.name

        # Draw base button
        super().draw(screen, small_font)

        # Draw cost in a pill-shaped badge
        cost = self.upgrade.get_current_cost()
        cost_text = f"{self.format_number(cost)} {self.upgrade.cost_type.title()}"

        # Create badge background
        cost_surface = small_font.render(cost_text, True,
                                        COLORS['text_light'] if self.enabled else COLORS['text_secondary'])
        badge_padding = 8
        badge_width = cost_surface.get_width() + badge_padding * 2
        badge_height = 20
        badge_x = self.rect.right - badge_width - 8
        badge_y = self.rect.centery - badge_height // 2

        # Badge background
        badge_rect = pygame.Rect(badge_x, badge_y, badge_width, badge_height)
        badge_color = COLORS['success'] if self.enabled else COLORS['button_disabled']
        pygame.draw.rect(screen, badge_color, badge_rect, border_radius=10)

        # Badge text
        cost_rect = cost_surface.get_rect(center=badge_rect.center)
        screen.blit(cost_surface, cost_rect)

    @staticmethod
    def format_number(num):
        """Format numbers compactly"""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return f"{int(num)}"


class Panel:
    """Modern panel with subtle styling"""

    def __init__(self, x, y, width, height, title="", bg_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.bg_color = bg_color or COLORS['panel']
        self.border_color = COLORS['border']

    def draw(self, screen, font):
        """Draw the panel"""
        # Draw background with rounded corners
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=CORNER_RADIUS)

        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, width=2, border_radius=CORNER_RADIUS)

        # Draw title if present
        if self.title:
            title_surface = font.render(self.title, True, COLORS['text'])
            title_rect = title_surface.get_rect(left=self.rect.left + UI_PADDING, top=self.rect.top + 10)
            screen.blit(title_surface, title_rect)


class ResourceDisplay:
    """Modern, compact resource display optimized for numbers"""

    def __init__(self, x, y, resource_name, icon_text):
        self.x = x
        self.y = y
        self.resource_name = resource_name
        self.icon_text = icon_text

    def draw(self, screen, font, small_font, value, per_second=None):
        """Draw the resource display - compact and information-dense"""
        # Draw card-style background
        card_width = 220
        card_height = 60
        card_rect = pygame.Rect(self.x, self.y, card_width, card_height)

        # Card background
        pygame.draw.rect(screen, COLORS['panel'], card_rect, border_radius=8)
        pygame.draw.rect(screen, COLORS['border'], card_rect, width=2, border_radius=8)

        # Icon on the left
        icon_size = 40
        icon_x = self.x + 10
        icon_y = self.y + 10
        icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
        pygame.draw.rect(screen, COLORS['button'], icon_rect, border_radius=6)

        icon_surface = font.render(self.icon_text, True, COLORS['text_light'])
        icon_text_rect = icon_surface.get_rect(center=icon_rect.center)
        screen.blit(icon_surface, icon_text_rect)

        # Resource name (small, above value)
        name_x = icon_x + icon_size + 10
        name_surface = small_font.render(self.resource_name.upper(), True, COLORS['text_secondary'])
        name_rect = name_surface.get_rect(left=name_x, top=self.y + 8)
        screen.blit(name_surface, name_rect)

        # Value (large, prominent)
        value_text = self.format_number(value)
        value_surface = font.render(value_text, True, COLORS['text'])
        value_rect = value_surface.get_rect(left=name_x, top=name_rect.bottom + 2)
        screen.blit(value_surface, value_rect)

        # Per second (if provided)
        if per_second is not None:
            per_sec_text = f"+{self.format_number(per_second)}/s"
            per_sec_surface = small_font.render(per_sec_text, True, COLORS['accent'])
            per_sec_rect = per_sec_surface.get_rect(left=value_rect.right + 8, centery=value_rect.centery)
            screen.blit(per_sec_surface, per_sec_rect)

    @staticmethod
    def format_number(num):
        """Format numbers compactly"""
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.2f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.2f}K"
        else:
            return f"{num:.1f}"


class UI:
    """Main UI manager with dark mode and resizing support"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.panels = []
        self.dark_mode = False

        # Initialize fonts
        self.title_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)

        # Resource displays (will be repositioned on resize)
        self.update_resource_positions()

        # Current tab
        self.current_tab = "home"  # home, upgrades, memories, adventure

    def update_resource_positions(self):
        """Update resource display positions"""
        self.warmth_display = ResourceDisplay(UI_PADDING, UI_PADDING, "Warmth", "♨")
        self.inspiration_display = ResourceDisplay(UI_PADDING + 240, UI_PADDING, "Inspiration", "★")
        self.memories_display = ResourceDisplay(UI_PADDING + 480, UI_PADDING, "Memories", "♥")

    def toggle_dark_mode(self):
        """Toggle between light and dark themes"""
        self.dark_mode = not self.dark_mode
        from src import config
        if self.dark_mode:
            config.COLORS = config.COLORS_DARK.copy()
        else:
            config.COLORS = config.COLORS_LIGHT.copy()
        # Update COLORS reference
        global COLORS
        COLORS = config.COLORS

    def resize(self, width, height):
        """Handle window resize"""
        self.screen_width = width
        self.screen_height = height
        self.update_resource_positions()

    def draw_background(self, screen):
        """Draw the background"""
        screen.fill(COLORS['bg'])

    def draw_resources(self, screen, resources):
        """Draw all resource displays"""
        self.warmth_display.draw(screen, self.medium_font, self.small_font,
                                  resources.warmth,
                                  resources.warmth_per_second * resources.warmth_multiplier)

        self.inspiration_display.draw(screen, self.medium_font, self.small_font,
                                       resources.inspiration)

        self.memories_display.draw(screen, self.medium_font, self.small_font,
                                    resources.memories)

    def update(self, dt):
        """Update UI animations"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
            button.update(dt)

    def handle_event(self, event):
        """Handle UI events - improved click detection"""
        # Handle events in reverse order (top buttons first)
        for button in reversed(self.buttons):
            if button.handle_event(event):
                return True
        return False

    def clear_buttons(self):
        """Clear all buttons"""
        self.buttons = []

    def add_button(self, button):
        """Add a button to the UI"""
        self.buttons.append(button)

    def draw_text(self, screen, text, x, y, font=None, color=None):
        """Helper to draw text"""
        if font is None:
            font = self.medium_font
        if color is None:
            color = COLORS['text']

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        screen.blit(text_surface, text_rect)
        return text_rect

    def draw_multiline_text(self, screen, text, x, y, max_width, font=None, color=None):
        """Draw text with word wrapping"""
        if font is None:
            font = self.small_font
        if color is None:
            color = COLORS['text']

        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, color)

            if test_surface.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        y_offset = 0
        for line in lines:
            line_surface = font.render(line, True, color)
            screen.blit(line_surface, (x, y + y_offset))
            y_offset += font.get_height() + 5

        return y_offset
