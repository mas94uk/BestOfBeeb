# Best of Beeb

Generate a curated collection of the best BBC Micro games.

Downloads the top (most played) games and their screenshots from [The Complete BBC Micro Games Archive](https://bbcmicro.co.uk/), and creates a `gamelist.xml` for EmulationStation (used in Batocera, RetroPie, Recalbox and other distributions).

The result is a curated collection of the most popular BBC Micro games, which display nicely in EmulationStaton.

## How to use

Clone this repository:

    git clone https://github.com/mas94uk/BestOfBeeb.git    
    cd BestOfBeeb

Create a virtual environment with the dependencies:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Run the script to download the top 50 (or however many) games:

    ./creategamelist.py 50

Copy the contents of the `output` directory to your EmulationStation `roms/bbc` directory.
