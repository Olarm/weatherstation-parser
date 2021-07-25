
Install virtual environment

    sudo apt-get install python3-venv

Navigate to project root and create virtual environment

    python3 -m venv .weather_parser

Active the virtual environment from the project root

    source .weather_parser/bin/activate

Install requirements

    pip3 install -r requirements.txt

Setup crontab to run every 5 minutes (or something else)

    */5 * * * * /opt/weatherstation-parser/.weather_parser/bin/python3 /opt/weatherstation-parser/parser.py

The python path is probably redundant due to the shebang in the file itself.
