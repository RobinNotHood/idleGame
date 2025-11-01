"""
UI System
Handles all user interface rendering and interaction
"""

import pygame
from src.config import COLORS, UI_PADDING, BUTTON_HEIGHT, BUTTON_WIDTH, CORNER_RADIUS


class Button:
    """A cozy, rounded button"""

    def __init__(self, x, y, width, height, text, callback, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color or COLORS['warm_orange']
        self.hover_color = COLORS['button_hover']
        self.text_color = COLORS['text_dark']
        self.is_hovered = False
        self.enabled = True

    def draw(self, screen, font):
        """Draw the button with rounded corners"""
        color = self.hover_color if self.is_hovered and self.enabled else self.color

        if not self.enabled:
            color = COLORS['tan']

        # Draw rounded rectangle
        pygame.draw.rect(screen, color, self.rect, border_radius=CORNER_RADIUS)

        # Draw border
        pygame.draw.rect(screen, COLORS['deep_brown'], self.rect, width=2, border_radius=CORNER_RADIUS)

        # Draw text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """Handle mouse events"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered and self.enabled:
                self.callback()
                return True
        return False

    def update_position(self, x, y):
        """Update button position"""
        self.rect.x = x
        self.rect.y = y


class UpgradeButton(Button):
    """Special button for upgrades with cost display"""

    def __init__(self, x, y, width, height, upgrade, callback, resources):
        self.upgrade = upgrade
        self.resources = resources
        super().__init__(x, y, width, height, upgrade.name, callback)

    def draw(self, screen, font, small_font):
        """Draw upgrade button with additional info"""
        # Check if affordable
        self.enabled = self.upgrade.can_purchase(self.resources)

        # Draw base button
        super().draw(screen, font)

        # Draw cost and level info
        cost = self.upgrade.get_current_cost()
        cost_text = f"{cost} {self.upgrade.cost_type.title()}"
        if self.upgrade.repeatable:
            cost_text += f" (Lv.{self.upgrade.current_level})"

        cost_surface = small_font.render(cost_text, True,
                                          COLORS['text_dark'] if self.enabled else COLORS['soft_brown'])
        cost_rect = cost_surface.get_rect(centerx=self.rect.centerx, top=self.rect.bottom + 5)
        screen.blit(cost_surface, cost_rect)


class Panel:
    """A cozy panel for UI organization"""

    def __init__(self, x, y, width, height, title="", bg_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.bg_color = bg_color or COLORS['soft_white']
        self.border_color = COLORS['deep_brown']

    def draw(self, screen, font):
        """Draw the panel"""
        # Draw background with rounded corners
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=CORNER_RADIUS)

        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, width=3, border_radius=CORNER_RADIUS)

        # Draw title if present
        if self.title:
            title_surface = font.render(self.title, True, COLORS['text_dark'])
            title_rect = title_surface.get_rect(centerx=self.rect.centerx, top=self.rect.top + UI_PADDING)
            screen.blit(title_surface, title_rect)


class ResourceDisplay:
    """Display for a single resource"""

    def __init__(self, x, y, resource_name, icon_text):
        self.x = x
        self.y = y
        self.resource_name = resource_name
        self.icon_text = icon_text

    def draw(self, screen, font, small_font, value, per_second=None):
        """Draw the resource display"""
        # Draw icon background (circular)
        icon_radius = 25
        pygame.draw.circle(screen, COLORS['warm_orange'], (self.x + icon_radius, self.y + icon_radius), icon_radius)
        pygame.draw.circle(screen, COLORS['deep_brown'], (self.x + icon_radius, self.y + icon_radius), icon_radius, 2)

        # Draw icon text (emoji-like)
        icon_surface = font.render(self.icon_text, True, COLORS['text_dark'])
        icon_rect = icon_surface.get_rect(center=(self.x + icon_radius, self.y + icon_radius))
        screen.blit(icon_surface, icon_rect)

        # Draw resource name
        name_surface = small_font.render(self.resource_name, True, COLORS['text_dark'])
        name_rect = name_surface.get_rect(left=self.x + icon_radius * 2 + 10, centery=self.y + 15)
        screen.blit(name_surface, name_rect)

        # Draw value
        value_text = self.format_number(value)
        value_surface = font.render(value_text, True, COLORS['deep_brown'])
        value_rect = value_surface.get_rect(left=self.x + icon_radius * 2 + 10, centery=self.y + 35)
        screen.blit(value_surface, value_rect)

        # Draw per second if provided
        if per_second is not None:
            per_sec_text = f"+{self.format_number(per_second)}/s"
            per_sec_surface = small_font.render(per_sec_text, True, COLORS['soft_brown'])
            per_sec_rect = per_sec_surface.get_rect(left=value_rect.right + 10, centery=self.y + 35)
            screen.blit(per_sec_surface, per_sec_rect)

    @staticmethod
    def format_number(num):
        """Format numbers for display"""
        if num >= 1_000_000:
            return f"{num / 1_000_000:.2f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.2f}K"
        else:
            return f"{num:.1f}"


class UI:
    """Main UI manager"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.panels = []

        # Initialize fonts
        self.title_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 20)

        # Resource displays
        self.warmth_display = ResourceDisplay(UI_PADDING, UI_PADDING, "Warmth", "♨")
        self.inspiration_display = ResourceDisplay(UI_PADDING + 250, UI_PADDING, "Inspiration", "★")
        self.memories_display = ResourceDisplay(UI_PADDING + 500, UI_PADDING, "Memories", "♥")

        # Current tab
        self.current_tab = "home"  # home, upgrades, memories, adventure

    def draw_background(self, screen):
        """Draw the warm, cozy background"""
        screen.fill(COLORS['warm_cream'])

    def draw_resources(self, screen, resources):
        """Draw all resource displays"""
        self.warmth_display.draw(screen, self.medium_font, self.small_font,
                                  resources.warmth,
                                  resources.warmth_per_second * resources.warmth_multiplier)

        self.inspiration_display.draw(screen, self.medium_font, self.small_font,
                                       resources.inspiration)

        self.memories_display.draw(screen, self.medium_font, self.small_font,
                                    resources.memories)

    def handle_event(self, event):
        """Handle UI events"""
        for button in self.buttons:
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
            color = COLORS['text_dark']

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(topleft=(x, y))
        screen.blit(text_surface, text_rect)
        return text_rect

    def draw_multiline_text(self, screen, text, x, y, max_width, font=None, color=None):
        """Draw text with word wrapping"""
        if font is None:
            font = self.small_font
        if color is None:
            color = COLORS['text_dark']

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
