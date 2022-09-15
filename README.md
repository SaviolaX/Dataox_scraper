### Simple website scraper on Selenium
It collects information from "kijiji.ca" and save one to database

#### Tech stack:
- Python3
- PostgreSQL
- Selenium


#### To use:
1. Clone files on your pc<br>
  `git clone https://github.com/SaviolaX/Dataox_scraper.git`
2. Create environment<br>
  `python -m venv env`
3. Install requirements<br>
  `pip install requirements.txt`
4. Add your db credentials in `settings.py`
5. Change table name in `db.py`
6. Change url to parse in `main.py`
7. Download driver and put in cloned folder<br>
  chromedrive - for chrome browser<br>
  geckodriver - for firefox browser
8. Run `main.py` to start process<br>
  `python main.py`
