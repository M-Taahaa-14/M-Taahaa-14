
import os
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

USERNAME = "M-Taahaa-14"
TOKEN = os.getenv("GH_TOKEN")

def fetch_contributions(username, token):
    query = {
        "query": f"""
        {{
          user(login: "{username}") {{
            contributionsCollection {{
              contributionCalendar {{
                weeks {{
                  contributionDays {{
                    date
                    contributionCount
                  }}
                }}
              }}
            }}
          }}
        }}
        """
    }
    headers = {"Authorization": f"bearer {token}"} if token else {}
    response = requests.post("https://api.github.com/graphql", json=query, headers=headers)
    data = response.json()
    contributions = []
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    for week in weeks:
        for day in week["contributionDays"]:
            date = day["date"]
            count = day["contributionCount"]
            contributions.append((date, count))
    return contributions[-90:]  # Use last 90 days for a shorter animation

def draw_frame(date, value, frame_index):
    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#002B36')  # Night mode green
    draw = ImageDraw.Draw(img)

    # Stadium lights
    for i in range(0, width, 100):
        draw.ellipse((i + 30, 10, i + 50, 30), fill="#FFFFFF")

    # Field lines
    draw.rectangle([20, 60, 480, 260], outline="white", width=4)
    draw.line((250, 60, 250, 260), fill="white", width=2)
    draw.ellipse((220, 130, 280, 190), outline="white", width=2)

    # Goalposts
    draw.rectangle((20, 120, 30, 200), fill="white")
    draw.rectangle((470, 120, 480, 200), fill="white")

    # Football (based on value)
    radius = 10
    x = 30 + (value * 10 % 440)
    y = 160 + int(20 * ((-1)**frame_index))  # Slight movement up/down
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill="white", outline="black")

    # Text
    draw.text((20, 270), f"Date: {date}", fill="white")
    draw.text((350, 270), f"Commits: {value}", fill="white")
    return img

def main():
    contributions = fetch_contributions(USERNAME, TOKEN)
    frames = []
    for i, (date, value) in enumerate(contributions):
        frames.append(draw_frame(date, value, i))

    os.makedirs("output", exist_ok=True)
    frames[0].save("output/github-contribution-football.gif",
                   save_all=True, append_images=frames[1:], duration=100, loop=0)
    print("GIF generated at output/github-contribution-football.gif")

if __name__ == "__main__":
    main()
