# **Engeto Python Academy - Project 3**
### The third project for Engeto Python Academy
---
## **Project description**
This project is made for web scraping of the 2017 Parlament election results. [Here](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103) you can find a link to the Parlament election website.
## **Virtual enviroment and libraries installation**
You can find all libraries that I used in my code in the ```requirements.txt``` file. For installation I could recommend a new virtual environment and install with the manager as follows:
```Python
python3 -m venv tutorial-env         # Create a virtual environment

source tutorial-env/bin/activate     # Activate it in Linux

tutorial-env\Scripts\activate.bat    # Activate it in Windows

deactivate                           # Deactivate it

$ pip3 --version                     # checking the manager version
$ pip3 install -r requirements.txt   # insall all libraries
```
## **How to run the project**
You will run the `election-scraper.py` in terminal and use 2 required arguments
```
python3 election-scraper.py <link-uzemni-celek> <result-file-name>
```
You can find .csv file saved in your folder with the results.
## **Project preview**
Election results for okres Prostejov:
- 1 argument: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12xnumnuts=7103`
- 2 argument: `results-prostejov.csv`

### Run the program in terminal:
```
python3 election-scraper.py 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'results-prostejov.csv'
```
### Processing:
```
DOWNLOADING DATA FROM URL: 'https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'
SAVING TO FILE: results-prostejov.csv
ENDING election-scraper
```
### Result preview:
```
code,location,registred,envelopes,valid,Občanská demokratická strana,...
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
...
```
