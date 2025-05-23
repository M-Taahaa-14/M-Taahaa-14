from PIL import Image, ImageDraw
import requests
import os
from datetime import datetime, timedelta

# Constants for visuals
WIDTH = 800
HEIGHT = 200
CELL_SIZE = 12
PADDING = 20
LUSH_GREEN = (34, 139, 34)  # vivid grass green
COMMIT_COLOR = (50, 205, 50)  # lime green
BG_COLOR = (12, 20, 30)  # night sky
GOAL_COLOR = (255, 255, 255)  # white

# GitHub username
USERNAME = "M-Taahaa-14"

# OPTIONAL: Direct token for local use (DO NOT PUSH THIS)
TOKEN = "your token here"

# --- Dummy data generator (replace with GitHub API if needed) ---
def dummy_contributions():
    today = datetime.now().date()
    return {
        today - timedelta(days=i): (i % 5) + 1
        for i in range(365)
    }

# Draw football pitch
def draw_field(draw, width, height):
    draw.rectangle([0, 0, width, height], fill=LUSH_GREEN)
    draw.rectangle([5, height // 2 - 25, 15, height // 2 + 25], fill=GOAL_COLOR)  # Left goal
    draw.rectangle([width - 15, height // 2 - 25, width - 5, height // 2 + 25], fill=GOAL_COLOR)  # Right goal
    draw.line([(width//2, 0), (width//2, height)], fill=GOAL_COLOR, width=1)  # Center line
    draw.ellipse([(width//2 - 10, height//2 - 10), (width//2 + 10, height//2 + 10)], outline=GOAL_COLOR, width=1)

# Generate football-style contribution GIF
def generate_football_gif(contributions):
    cols = 52
    rows = 7
    width = cols * CELL_SIZE + PADDING * 2
    height = rows * CELL_SIZE + PADDING * 2

    frames = []
    sorted_days = sorted(contributions.keys())
    total_frames = min(100, len(sorted_days))

    for i in range(total_frames):
        img = Image.new("RGB", (width, height), BG_COLOR)
        draw = ImageDraw.Draw(img)
        draw_field(draw, width, height)

        for j in range(i + 1):
            day = sorted_days[j]
            val = contributions[day]
            col = j // rows
            row = j % rows
            x = PADDING + col * CELL_SIZE
            y = PADDING + row * CELL_SIZE
            draw.ellipse([x, y, x + 10, y + 10], fill=COMMIT_COLOR)

        frames.append(img)

    output_path = "output/github-contribution-football.gif"
    os.makedirs("output", exist_ok=True)
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=120, loop=0)
    return output_path

# Run the generator
if __name__ == "__main__":
    contributions = dummy_contributions()
    gif_path = generate_football_gif(contributions)
    print(f"✅ Football GIF saved to: {gif_path}")
