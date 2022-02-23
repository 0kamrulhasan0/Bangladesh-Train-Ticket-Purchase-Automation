Setup Geckodriver for Firefox
```
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz
$ tar -xvzf geckodriver-v0.30.0-linux32.tar.gz
$ rm geckodriver-v0.30.0-linux32.tar.gz
$ mv geckodriver /usr/bin/
OR $export PATH=$PATH:/path-to-extracted-file/.
OR put os.environ['PATH'] += r"/home/kamrul-hasan/Selenium_Automation/geckodriver"
```
