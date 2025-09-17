# src/visualizer.py

import pygame
import random
import time
import sys

class SortingVisualizer:
    def __init__(self):
        # Screen Setup
        pygame.init()
        self.SCREEN_WIDTH = 1200
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Sorting Visualizer")

        # Colors
        self.COLORS = {
            'BACKGROUND': (240, 248, 255),
            'BAR_COLORS': [
                (255, 105, 180),
                (30, 144, 255),
                (50, 205, 50),
                (255, 165, 0),
                (138, 43, 226)
            ],
            'TEXT': (0, 0, 0),
            'HIGHLIGHT': (255, 69, 0)
        }

        # Sorting Parameters
        self.NUM_BARS = 30
        self.BAR_WIDTH = 25
        self.BAR_MARGIN = 5
        self.MAX_BAR_HEIGHT = 500

        # Sorting Speed
        self.SORTING_SPEED = 0.05

        # Generate Initial Bars
        self.bars = self.generate_bars()

    def generate_bars(self):
        return [
            random.randint(50, self.MAX_BAR_HEIGHT) 
            for _ in range(self.NUM_BARS)
        ]

    def draw_menu(self):
        self.screen.fill(self.COLORS['BACKGROUND'])
        font = pygame.font.SysFont('Comic Sans MS', 50)
        title = font.render("Sorting Adventure!", True, self.COLORS['TEXT'])
        title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        buttons = [
            "Bubble Sort", 
            "Insertion Sort", 
            "Quick Sort", 
            "Shuffle", 
            "Exit"
        ]
        
        button_font = pygame.font.SysFont('Comic Sans MS', 30)
        for i, button in enumerate(buttons):
            button_surface = button_font.render(button, True, self.COLORS['TEXT'])
            button_rect = pygame.Rect(
                self.SCREEN_WIDTH // 2 - 100, 
                150 + i * 70, 
                200, 
                50
            )
            pygame.draw.rect(
                self.screen, 
                self.COLORS['BAR_COLORS'][i % len(self.COLORS['BAR_COLORS'])], 
                button_rect
            )
            button_text_rect = button_surface.get_rect(center=button_rect.center)
            self.screen.blit(button_surface, button_text_rect)

        pygame.display.update()

    def draw_bars(self, comparison_indices=None):
        self.screen.fill(self.COLORS['BACKGROUND'])
        total_width = (self.BAR_WIDTH + self.BAR_MARGIN) * self.NUM_BARS
        start_x = (self.SCREEN_WIDTH - total_width) // 2

        for i, height in enumerate(self.bars):
            x = start_x + i * (self.BAR_WIDTH + self.BAR_MARGIN)
            if comparison_indices and i in comparison_indices:
                color = self.COLORS['HIGHLIGHT']
            else:
                color = self.COLORS['BAR_COLORS'][i % len(self.COLORS['BAR_COLORS'])]
            pygame.draw.rect(
                self.screen, 
                color, 
                (x, self.SCREEN_HEIGHT - height, self.BAR_WIDTH, height)
            )

        pygame.display.update()

    def bubble_sort(self):
        for i in range(len(self.bars)):
            for j in range(0, len(self.bars) - i - 1):
                self.draw_bars([j, j+1])
                time.sleep(self.SORTING_SPEED)
                if self.bars[j] > self.bars[j + 1]:
                    self.bars[j], self.bars[j + 1] = self.bars[j + 1], self.bars[j]

    def insertion_sort(self):
        for i in range(1, len(self.bars)):
            key = self.bars[i]
            j = i - 1
            while j >= 0 and key < self.bars[j]:
                self.bars[j + 1] = self.bars[j]
                self.draw_bars([j, j+1])
                time.sleep(self.SORTING_SPEED)
                j -= 1
            self.bars[j + 1] = key

    def quick_sort(self, low=0, high=None):
        if high is None:
            high = len(self.bars) - 1

        def partition(low, high):
            pivot = self.bars[high]
            i = low - 1
            for j in range(low, high):
                self.draw_bars([j, high])
                time.sleep(self.SORTING_SPEED)
                if self.bars[j] < pivot:
                    i += 1
                    self.bars[i], self.bars[j] = self.bars[j], self.bars[i]
            self.bars[i + 1], self.bars[high] = self.bars[high], self.bars[i + 1]
            return i + 1

        def quick_sort_recursive(low, high):
            if low < high:
                pi = partition(low, high)
                quick_sort_recursive(low, pi - 1)
                quick_sort_recursive(pi + 1, high)

        quick_sort_recursive(low, high)

    def main(self):
        running = True
        while running:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 450 <= x <= 650:
                        if 150 <= y <= 200:
                            self.bubble_sort()
                        elif 220 <= y <= 270:
                            self.insertion_sort()
                        elif 290 <= y <= 340:
                            self.quick_sort()
                        elif 360 <= y <= 410:
                            self.bars = self.generate_bars()
                        elif 430 <= y <= 480:
                            running = False

        pygame.quit()
