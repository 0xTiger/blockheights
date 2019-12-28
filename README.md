# blockheights
A collection of Python scripts for scraping and visualising the minecraft world

## dataset
The dataset provided has been scraped from about 1 billion blocks, over 15 regions. 
The region files were generated using minecraft version 1.15.1

## scraper
The majority of the work here is done by the [anvil library](https://pypi.org/project/anvil-parser/), written by matt44 so massive thanks to them. It can be found on PyPi or installed by pip using `pip install anvil-parser`

The blockheights_scraper is written for Python 2.7 however one of it's dependencies: anvil library is written for Python 3. This may cause issues.

## reader
The first related visualisation I posted on reddit was made using oreheights_reader.py, the latter (animation) was made using blockheights_reader.py. 
The icons I used for each block can be found by extracting the minecraft jarfile. I will not redistribute these on github.
