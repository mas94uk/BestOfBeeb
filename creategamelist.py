#!/usr/bin/env python3

""" Download BBC Micro games and screenshots from bbcmicro.co.uk, and create gamelist.xml for EmulationStation """

# Constants
WEBSITE_URL = "https://bbcmicro.co.uk"
OUTPUT_DIR = "output"

# Stage 0: Get the arguments.
# TODO: This would be nicer using a proper arg parser, but it will do for now
import sys
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} numberOfGames")
    exit(-1)
numGames = int(sys.argv[1])

print(f"Attempting to generate gamefile.xml with the top {numGames} games from {WEBSITE_URL}")

# Stage 1: Download the "top" list
import requests
from bs4 import BeautifulSoup

gameDetails = []
pageNum = 0
while len(gameDetails) < numGames:
    pageNum += 1

    # Get a page of games, sorted by "p" (popularity)
    print(f"Downloading popular games page {pageNum}")
    url = f"{WEBSITE_URL}/index.php?sort=p&page={pageNum}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Unable to download games list: code {response.status_code}")
        exit(-1)

    # Parse the HTML to get the games
    soup = BeautifulSoup(response.content, "html.parser")
    maingrid = soup.find("div", {"id": "maingrid"})
    games = maingrid.find_all("div", {"class": "thumb1"})

    # Get the details from each game
    for game in games:
        title = game.find("div", {"class": "row-title"}).text
        print(f" - Extracting details of {title}")
        img_path = game.find("img")["src"]
        publisher = game.find("div", {"class": "row-pub"}).text
        year = game.find("div", {"class": "row-dt"}).text
        link_element = game.find("a", string="Download")
        
        # Some games are not available to download
        if not link_element:
            print(f"No download exists for {title}")
            continue
        download_path = link_element["href"]

        gameDetail = {
              "title": title,
            "download_path": download_path,
            "img_path": img_path,
            "publisher": publisher,
            "year": year
            }
        gameDetails.append(gameDetail)
  
        if len(gameDetails) >= numGames:
            break
  
  
# Stage 2: Create gamelist.xml
print(f"Creating games list XML with {len(gameDetails)} games")

import os
if os.path.exists(OUTPUT_DIR):
    import shutil
    shutil.rmtree(OUTPUT_DIR)
os.mkdir(OUTPUT_DIR)

    # import code
    # import readline
    # import rlcompleter
            
    # vars = globals()
    # vars.update(locals())
                                                
    # readline.set_completer(rlcompleter.Completer(vars).complete)
    # readline.parse_and_bind("tab: complete")
    # code.InteractiveConsole(vars).interact()

import xml.etree.ElementTree as ET
games_elem = ET.Element("gameList")

for gameDetail in gameDetails:
    game_elem = ET.Element("game")

    # Different menus show different fields. Fill them in as best we can.
        
    path_elem = ET.Element("path")
    filename = os.path.basename(gameDetail["download_path"])
    path_elem.text = f"./{filename}"
    game_elem.append(path_elem)
    gameDetail["filename"] = filename
    
    name_elem = ET.Element("name")
    name_elem.text = gameDetail["title"]
    game_elem.append(name_elem)
    
    pub_elem = ET.Element("publisher")
    pub_elem.text = gameDetail["publisher"]
    game_elem.append(pub_elem)

    developer_elem = ET.Element("developer")
    developer_elem.text = gameDetail["publisher"]
    game_elem.append(developer_elem)
    
    try:
        year = int(gameDetail["year"])
        releasedate_elem = ET.Element("releasedate")
        releasedate_elem.text = f"{year:04}0101T000000" # Assusme 1st Jan, since we don't know
        game_elem.append(releasedate_elem)
    except ValueError:
        # Some games don't have a valid release date; skip it
        pass

    desc_elem = ET.Element("desc")
    desc_elem.text = f"Publisher: {gameDetail["publisher"]} ({gameDetail["year"]})"
    game_elem.append(desc_elem)
    
    image_elem = ET.Element("image")
    image_filename = os.path.basename(gameDetail["img_path"])
    image_elem.text = f"./{image_filename}"
    game_elem.append(image_elem)
    gameDetail["img_filename"] = image_filename

    # Don't have anything useful to put in genre    
    # genre_elem = ET.Element("genre")
    # genre_elem.text = ""
    # game_elem.append(genre_elem)
    
    games_elem.append(game_elem)

tree = ET.ElementTree(games_elem)
ET.indent(tree, space="\t", level=0)
output_filename = os.path.join(OUTPUT_DIR, "gamelist.xml")
tree.write(output_filename, xml_declaration=True, )


# Stage 3: Download the files
print(f"Downloading game files and images")

download_failures = 0
for gameDetail in gameDetails:
    for (urlpath, filepath) in ( ("download_path", "filename"), ("img_path", "img_filename")):
        url = f"{WEBSITE_URL}/{gameDetail[urlpath]}"
        print(f" - Downloading {url}")
        response = requests.get(url)
        if response.status_code == 200:
            output_filepath = os.path.join(OUTPUT_DIR, gameDetail[filepath])
            with open(output_filepath, "wb") as of:
                of.write(response.content)
        else:
            print(f"Unable to download {url} - skipping")
            download_failures += 1

print(f"Complete with {download_failures} download failues.")
print(f"Now you should move the contents of the `output` directory to your emulator.")
print(f"This might be at /userdata/roms/bbc (for Batocera and perhaps others)")
