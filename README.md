# LinkedIn Profile Scraper

This script is designed to scrape LinkedIn profiles for specific information such as name, bio, experience, education, certifications, and projects. The data is extracted from LinkedIn URLs provided in an Excel file and saved into a CSV file.

## Prerequisites

- Python 3.x
- Google Chrome browser
- ChromeDriver

## Necessary Libraries

The script requires the following Python libraries:

- `selenium`
- `pandas`
- `webdriver-manager`
- `openpyxl` (for reading Excel files)

## Installing Libraries

You can install the required libraries using the `requirements.txt` file. First, ensure your virtual environment is activated, then run the following command:

```bash
pip install -r requirements.txt
```

## How to Run the Script

1. Ensure that you have the necessary libraries installed and the virtual environment activated.
2. Open the `linkedin_scraper.py` file and replace the placeholder email and password with your LinkedIn credentials.
3. Ensure that the input Excel file (`Assignment.xlsx`) is in the same directory as the script and contains a column named `LinkedIn URLs`.
4. Run the script using the following command:

   ```bash
   python linkedin_scraper.py
   ```

5. The script will log into LinkedIn, scrape the profiles listed in the Excel file, and save the output to `scraped_output.csv`.

## Virtual Environment

It is recommended to use a virtual environment to manage dependencies. Here are the steps to create and use a virtual environment:

### Create a Virtual Environment

1. Navigate to the project directory.
2. Run the following command to create a virtual environment:

   ```bash
   python -m venv venv
   ```

### Activate the Virtual Environment

- On Windows:

  ```bash
  .\venv\Scripts\activate
  ```

- On macOS and Linux:

  ```bash
  source venv/bin/activate
  ```

### Deactivate the Virtual Environment

Once you have finished running the script and generating the output file, you can deactivate the virtual environment by simply running:

```bash
deactivate
```

## Important Notes

- This script is for educational purposes only. Scraping LinkedIn profiles may violate LinkedIn's terms of service.
- Ensure that you have permission to scrape the data and that you comply with all applicable laws and regulations.




