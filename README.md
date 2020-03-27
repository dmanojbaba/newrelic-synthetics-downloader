# New Relic Synthetics Downloader

### Download New Relic Synthetics Monitor Scripts on a Local Machine using Python

---

[New Relic Synthetics](https://newrelic.com/products/synthetics) is a suite of automated, scriptable tools to monitor websites, critical business transactions, and API endpoints. New Relic Synthetics ensures the website is not only available but fully functional.

New Relic Synthetics Scripted Browsers emulate and run complex test cases against a website with real, Selenium-powered Google Chrome browsers to ensure critical processes like checkout and login are always running smoothly.

Depending on the number of monitors, versioning and tracking changes to New Relic Synthetics Monitors and Monitor Scripts becomes apparent.

This repository enable Synthetics managers to download New Relic Synthetics Monitor Scripts on a local machine using Python.

---

## Prerequisites:
* Python3
* pip (Python Package Installer)
* New Relic Admin API Key
  * Login to New Relic as Admin user
  * Go to "Account settings" > "API keys"
  * Note the `account-id` [*e.g.: Your account ID is: `1234567`*]
  * Generate a new "Admin API key" or Click "(Show key)" for the admin user
  * Note the `admin-api-key` [*e.g.: Admin's API key: `NRAA-c0pypast3th3adm1nap1k3yh3r3`*]

## Run:
* Clone or download this repository
* Change current working directory to the cloned location
  * Example `cd newrelic-synthetics-downloader`
* Install required python packages 
  * `pip install -r requirements.txt`
* As required, add `account-id` and `admin-api-key` for each  New Relic account/sub-accounts in `config.json`
* For advanced configurations like API Endpoint, API Version, Proxy, etc., edit the appropriate value in `config.json` 
* Run `./main.py` or `python3 main.py`
* View the downloaded artifacts in the `accounts/<account-id>/monitors/` directory
  * For Ping and Simple Browser monitors, view `<monitor-id>.json` files
  * For Scripted Browser monitors and API tests, view `<monitor-id>.script` files
* Use `cron` to run `main.py` and download artifacts at scheduled intervals
* Use `git` to version control and track changes to the monitors and scripts

#### For bugs, enhancements, or other requests create an issue in this repository

---

*Note: This repository is purely aimed to download New Relic Synthetics Advanced Monitor Scripts under [New Relic License](https://docs.newrelic.com/docs/licenses) and [Acceptable Use Policy](https://docs.newrelic.com/docs/licenses/license-information/general-usage-licenses/acceptable-use-policy)*

---
