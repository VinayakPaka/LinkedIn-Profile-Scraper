# LinkedIn Profile Scraper

This script is designed to scrape LinkedIn profiles for specific information such as name, bio, experience, and education details. The data is extracted from LinkedIn URLs provided in an Excel file and saved into a CSV file.

## Prerequisites

- Python 3.x
- Google Chrome browser

## Required Libraries

The script requires the following Python libraries:

- `undetected-chromedriver`
- `selenium`
- `pandas`
- `openpyxl` (for reading Excel files)

## Installation

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

- On Windows:
  ```bash
  .\venv\Scripts\activate
  ```

- On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```

3. Install the required libraries:

```bash
pip install undetected-chromedriver selenium pandas openpyxl
```

## How to Use

1. Prepare an Excel file named `Assignment.xlsx` with a column named "LinkedIn URLs" containing the profile URLs you want to scrape.

2. Open `main.py` and update your LinkedIn credentials:
   ```python
   email = "youremail@.com"
   password = "password"
   ```

3. Run the script:
   ```bash
   python main.py
   ```

4. The script will:
   - Open Chrome browser
   - Log into LinkedIn
   - Scrape each profile from the Excel file
   - Save the results in `scraped_output.csv`

## Features

The script extracts the following information from each profile:
- Name
- Bio
- Experience details:
  - Role
  - Company
  - Date Range
  - Location
  - Description
- Education details:
  - Institute
  - Degree
  - Date Range
  - Location
  - Description

## Important Notes

- The script includes CAPTCHA detection and will pause for manual intervention if needed
- A delay is implemented between profile scrapes to avoid rate limiting
- This script is for educational purposes only. Please ensure you comply with LinkedIn's terms of service and have permission to scrape the data
- The script uses undetected-chromedriver to help avoid detection, but LinkedIn may still detect automated access

## Deactivating Virtual Environment

When you're done, you can deactivate the virtual environment:

```bash
deactivate
```




