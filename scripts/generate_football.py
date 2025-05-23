
import requests
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import json

# Configuration
USERNAME = os.getenv('USERNAME', 'M-Taahaa-14')
TOKEN = os.getenv('GH_TOKEN')
OUTPUT_DIR = 'assets'
IMAGE_NAME = 'football-commits.png'

# Visual constants
FIELD_WIDTH = 1000
FIELD_HEIGHT = 300
CELL_SIZE = 8
GRID_COLS = 53
GRID_ROWS = 7

# Colors
FIELD_GREEN = (34, 139, 34)
COMMIT_GREEN = (0, 255, 65)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
PLAYER_RED = (255, 68, 68)

def fetch_commit_data():
    """Fetch commit data from GitHub API"""
    headers = {'Authorization': f'Bearer {TOKEN}'}
    
    # Get all repositories
    repos_url = f'https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner'
    repos_response = requests.get(repos_url, headers=headers)
    
    if repos_response.status_code != 200:
        print(f"Error fetching repos: {repos_response.status_code}")
        return {}
    
    repos = repos_response.json()
    commit_data = {}
    
    # Get commits from each repo
    one_year_ago = (datetime.now() - timedelta(days=365)).isoformat()
    
    for repo in repos:
        commits_url = f'https://api.github.com/repos/{USERNAME}/{repo["name"]}/commits'
        params = {
            'author': USERNAME,
            'since': one_year_ago,
            'per_page': 100
        }
        
        commits_response = requests.get(commits_url, headers=headers, params=params)
        
        if commits_response.status_code == 200:
            commits = commits_response.json()
            
            for commit in commits:
                commit_date = commit['commit']['author']['date'][:10]
                commit_data[commit_date] = commit_data.get(commit_date, 0) + 1
    
    return commit_data

def draw_football_field(draw, width, height):
    """Draw a realistic football field"""
    # Main field
    draw.rectangle([0, 0, width, height], fill=FIELD_GREEN)
    
    # Field lines
    # Center line
    draw.line([(width//2, 20), (width//2, height-20)], fill=WHITE, width=3)
    
    # Center circle
    center_x, center_y = width//2, height//2
    draw.ellipse([
        center_x - 30, center_y - 30,
        center_x + 30, center_y + 30
    ], outline=WHITE, width=2)
    
    # Goals
    goal_width = 15
    goal_height = 80
    # Left goal
    draw.rectangle([
        5, center_y - goal_height//2,
        5 + goal_width, center_y + goal_height//2
    ], outline=WHITE, width=2)
    
    # Right goal
    draw.rectangle([
        width - 5 - goal_width, center_y - goal_height//2,
        width - 5, center_y + goal_height//2
    ], outline=WHITE, width=2)
    
    # Penalty areas
    penalty_width = 50
    penalty_height = 120
    # Left penalty area
    draw.rectangle([
        0, center_y - penalty_height//2,
        penalty_width, center_y + penalty_height//2
    ], outline=WHITE, width=1)
    
    # Right penalty area
    draw.rectangle([
        width - penalty_width, center_y - penalty_height//2,
        width, center_y + penalty_height//2
    ], outline=WHITE, width=1)

def generate_football_image(commit_data):
    """Generate the football field with commit visualization"""
    # Create image
    img = Image.new('RGB', (FIELD_WIDTH, FIELD_HEIGHT), FIELD_GREEN)
    draw = ImageDraw.Draw(img)
    
    # Draw field
    draw_football_field(draw, FIELD_WIDTH, FIELD_HEIGHT)
    
    # Calculate commit grid positioning
    grid_width = GRID_COLS * CELL_SIZE
    grid_height = GRID_ROWS * CELL_SIZE
    start_x = (FIELD_WIDTH - grid_width) // 2
    start_y = (FIELD_HEIGHT - grid_height) // 2
    
    # Draw commit grid with transparency effect
    today = datetime.now().date()
    total_commits = 0
    
    for i in range(365):
        date = today - timedelta(days=364-i)
        date_str = date.strftime('%Y-%m-%d')
        commits = commit_data.get(date_str, 0)
        total_commits += commits
        
        # Calculate grid position
        week = i // 7
        day = i % 7
        
        if week < GRID_COLS and day < GRID_ROWS:
            x = start_x + week * CELL_SIZE
            y = start_y + day * CELL_SIZE
            
            if commits > 0:
                # Intensity based on commit count
                intensity = min(commits / 5.0, 1.0)
                green_val = int(255 * intensity)
                commit_color = (0, green_val, 0)
                
                # Draw commit square
                draw.rectangle([
                    x, y, x + CELL_SIZE - 1, y + CELL_SIZE - 1
                ], fill=commit_color)
                
                # Add glow effect for high activity
                if commits > 3:
                    draw.rectangle([
                        x-1, y-1, x + CELL_SIZE, y + CELL_SIZE
                    ], outline=COMMIT_GREEN, width=1)
    
    # Add player (football) at a position based on recent activity
    recent_commits = sum(commit_data.get(
        (today - timedelta(days=i)).strftime('%Y-%m-%d'), 0
    ) for i in range(7))
    
    player_x = min(50 + recent_commits * 10, FIELD_WIDTH - 50)
    player_y = FIELD_HEIGHT // 2
    
    # Draw player as a football
    draw.ellipse([
        player_x - 8, player_y - 8,
        player_x + 8, player_y + 8
    ], fill=PLAYER_RED)
    
    # Add stats overlay
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    stats_text = f"⚽ Total Goals (Commits): {total_commits}"
    draw.text((20, 20), stats_text, fill=WHITE, font=font)
    
    return img

def main():
    """Main function"""
    print("🏈 Generating football commits visualization...")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Fetch commit data
    commit_data = fetch_commit_data()
    
    if not commit_data:
        print("⚠️ No commit data found, using sample data")
        # Generate sample data for testing
        today = datetime.now().date()
        commit_data = {
            (today - timedelta(days=i)).strftime('%Y-%m-%d'): 
            (i % 5) if i % 3 == 0 else 0
            for i in range(365)
        }
    
    # Generate image
    img = generate_football_image(commit_data)
    
    # Save image
    output_path = os.path.join(OUTPUT_DIR, IMAGE_NAME)
    img.save(output_path, 'PNG')
    
    print(f"✅ Football visualization saved to: {output_path}")
    print(f"📊 Total commits visualized: {sum(commit_data.values())}")

if __name__ == "__main__":
    main()
