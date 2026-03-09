import os
import json
from jinja2 import Environment, FileSystemLoader

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
team_template = env.get_template('TeamPageTemplate.html')
home_template = env.get_template('HomePageTemplate.html')

# Create output folder
os.makedirs("TeamHTMLFiles", exist_ok=True)

# Folder with JSON data
data_folder = "TeamInformation"

# Store data for homepage
homepage_teams = []

# Generate individual team pages
for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".json"):
        team_num = filename.replace("team", "").replace(".json", "")
        team_path = os.path.join(data_folder, filename)

        with open(team_path, "r", encoding="utf-8") as f:
            team_data = json.load(f)

        #Determine if a Team Logo file exists
        team_logo_path = f"./TeamLogo/{team_data['Team_Number']}.png"
        team_data["Has_Logo"] = os.path.exists(team_logo_path)

        # Determine if MP4 video file exists
        video_path = f"TeamPrototypes/{team_data['Team_Number']}.mp4"
        team_data["Video_File"] = os.path.exists(video_path)

        # Render individual team HTML
        rendered_html = team_template.render(**team_data)

        output_filename = f"TeamHTMLFiles/team{int(team_num):02}.html"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        # print(f"Generated {output_filename}")

        # Determine paths for homepage
        poster_image_path = f"./TeamPosters/{team_data['Team_Number']}.jpg"
        if not os.path.exists(poster_image_path):
            poster_image_path = "TeamLogo/goose2.png"

        prototype_image_path = f"./TeamPrototypes/{team_data['Team_Number']}.png"
        if not os.path.exists(prototype_image_path):
            prototype_image_path = "TeamLogo/smugwhale.png"

        homepage_teams.append({
            "Team_Name": team_data["Team_Name"],
            "Team_Number": team_data["Team_Number"],
            "Prototype_Image": prototype_image_path,
            "Poster": poster_image_path,
            "Page_Link": f"./TeamHTMLFiles/team{int(team_num):02}.html"
        })
print("Generated All Team HTML Files.")

# Render homepage
homepage_html = home_template.render(teams=homepage_teams)
with open("BME2026CapstoneShowcase.html", "w", encoding="utf-8") as f:
    f.write(homepage_html)

print("Generated BME2026CapstoneShowcase.html file.")
