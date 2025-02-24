import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    options = Options()
    # Remove headless mode for debugging
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def linkedin_login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)
    
    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    login_button.click()
    time.sleep(5)

def scrape_linkedin_profile(driver, profile_url):
    driver.get(profile_url)
    time.sleep(5)
    
    try:
        name = driver.find_element(By.XPATH, "//h1[contains(@class, 'inline t-24 v-align-middle break-words')]").text
    except:
        name = "Not Found"
    
    try:
        bio = driver.find_element(By.XPATH, "//div[contains(@class, 'text-body-medium break-words')]").text
    except:
        bio = "Not Found"
    
    experience, education, socials, certifications, projects = [], [], [], [], []
    
    try:
        exp_elements = driver.find_elements(By.XPATH, "//section[@id='experience-section']//li")
        for exp in exp_elements:
            try:
                company = exp.find_element(By.XPATH, ".//span[contains(@class, 't-14 t-normal')]").text
                role = exp.find_element(By.XPATH, ".//span[contains(@class, 'visually-hidden')]//span").text
                experience.append({company: role})
            except:
                continue
    except:
        experience = "Not Found"
    
    try:
        edu_elements = driver.find_elements(By.XPATH, "//section[@id='education-section']//li")
        for edu in edu_elements:
            try:
                university = edu.find_element(By.XPATH, ".//span[contains(@class, 'visually-hidden')]//span").text
                degree = edu.find_element(By.XPATH, ".//span[contains(@class, 't-14 t-normal')]//span").text
                education.append({university: degree})
            except:
                continue
    except:
        education = "Not Found"
    
    try:
        cert_elements = driver.find_elements(By.XPATH, "//section[contains(@id, 'certifications-section')]//li")
        for cert in cert_elements:
            try:
                certification = cert.find_element(By.XPATH, ".//span[contains(@class, 'visually-hidden')]//span").text
                certifications.append(certification)
            except:
                continue
    except:
        certifications = "Not Found"
    
    try:
        project_elements = driver.find_elements(By.XPATH, "//section[contains(@id, 'projects-section')]//li")
        for proj in project_elements:
            try:
                project = proj.find_element(By.XPATH, ".//span[contains(@class, 'mr1 t-bold')]//span").text
                projects.append(project)
            except:
                continue
    except:
        projects = "Not Found"
    
    return {
        "LinkedIn URL": profile_url,
        "Name": name,
        "Bio": bio,
        "Socials": socials,
        "Experience": experience,
        "Education": education,
        "Certifications": certifications,
        "Projects": projects
    }

def main():
    input_file = "Assignment.xlsx"
    df = pd.read_excel(input_file)
    
    if "LinkedIn URLs" not in df.columns:
        raise KeyError("The column 'LinkedIn URLs' was not found in the Excel file. Please check the column name.")
    
    driver = setup_driver()
    
    email = "youremail@gmail.com"  # Replace with your LinkedIn email
    password = "yourpassword"  # Replace with your LinkedIn password
    linkedin_login(driver, email, password)
    
    scraped_data = []
    for url in df["LinkedIn URLs"]:
        scraped_data.append(scrape_linkedin_profile(driver, url))
    
    driver.quit()
    
    output_df = pd.DataFrame(scraped_data)
    output_df.to_csv("scraped_output.csv", index=False)
    print("Scraping completed! Output saved as 'scraped_output.csv'")

if __name__ == "__main__":
    main()
