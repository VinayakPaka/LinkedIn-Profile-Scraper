import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def setup_driver():
    driver = uc.Chrome()
    driver.maximize_window()
    return driver

def linkedin_login(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(3)
    
    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    
    time.sleep(10)
    
    if "captcha" in driver.page_source.lower() or "security verification" in driver.page_source.lower():
        print("CAPTCHA detected! Manual intervention required.")
        input("Press Enter after solving the CAPTCHA manually...")
        time.sleep(5)
    
    return True

def scrape_linkedin_profile(driver, profile_url):
    driver.get(profile_url)
    time.sleep(5)

    try:
        name = driver.find_element(By.XPATH, "//h1[contains(@class, 'inline t-24 v-align-middle break-words')]").text
    except NoSuchElementException:
        name = "Not Found"

    try:
        bio = driver.find_element(By.XPATH, "//div[contains(@class, 'text-body-medium') and contains(@class, 'break-words')]").text
    except NoSuchElementException:
        bio = "Not Found"

    # Scrape Experience Section
    experience = scrape_experience_section(driver)
    
    # Scrape Education Section
    education = scrape_education_section(driver)

    return {
        "LinkedIn URL": profile_url,
        "Name": name,
        "Bio": bio,
        "Experience": experience,
        "Education": education
    }

def scrape_experience_section(driver):
    experience = []

    experience_section_xpaths = [
        "//section[.//div[@id='experience']]",
        "//section[contains(@class, 'experience-section')]",
        "//section[@class='artdeco-card ember-view relative break-words pb3 mt2']",
        "//section[.//span[text()='Experience']]"
    ]

    experience_section = None
    for xpath in experience_section_xpaths:
        try:
            experience_section = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            if experience_section:
                break
        except (TimeoutException, NoSuchElementException):
            continue

    if experience_section:
        exp_items = experience_section.find_elements(By.XPATH, ".//li[contains(@class, 'artdeco-list__item')]")

        for item in exp_items:
            try:
                role = item.find_element(By.XPATH, ".//span[@aria-hidden='true']").text.strip()
            except NoSuchElementException:
                role = "Role Not Found"

            try:
                company = item.find_element(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal')]/span").text.strip()
            except NoSuchElementException:
                company = "Company Not Found"

            try:
                date_range = item.find_element(By.XPATH, ".//span[contains(@class, 'pvs-entity__caption-wrapper')]").text.strip()
            except NoSuchElementException:
                date_range = "Date Range Not Found"

            try:
                location_elements = item.find_elements(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal') and contains(@class, 't-black--light')]/span")
                location = "Location Not Found"
                for loc in location_elements:
                    loc_text = loc.text.strip()
                    if loc_text and not any(char.isdigit() for char in loc_text):
                        location = loc_text
                        break
                    
            except NoSuchElementException:
                location = "Location Not Found"

            try:
                description = ""
                description_xpaths = [
                    ".//div[contains(@class, 'description')]//span[@aria-hidden='true']",
                    ".//div[contains(@class, 'show-more-less-text')]//span[@aria-hidden='true']",
                    ".//div[contains(@class, 'inline-show-more-text')]//span[@aria-hidden='true']",
                    ".//div[contains(@class, 'pv-shared-text-with-see-more')]//span[@aria-hidden='true']"
                ]

                for xpath in description_xpaths:
                    try:
                        desc_element = item.find_element(By.XPATH, xpath)
                        potential_desc = desc_element.text.strip()
                        if potential_desc and len(potential_desc) > 20:
                            description = potential_desc
                            break
                    except NoSuchElementException:
                        continue

                if not description:
                    description = "No Description"
            except Exception as e:
                print(f"Error extracting description: {str(e)}")
                description = "Error extracting description"

            experience.append({
                "Role": role,
                "Company": company,
                "Date Range": date_range,
                "Location": location,
                "Description": description
            })

    return experience

def scrape_education_section(driver):
    education = []

    education_section_xpaths = [
        "//section[.//div[@id='education']]",
        "//section[contains(@class, 'education-section')]",
        "//section[@class='artdeco-card ember-view relative break-words pb3 mt2' and .//span[text()='Education']]",
        "//section[.//span[text()='Education']]"
    ]

    education_section = None
    for xpath in education_section_xpaths:
        try:
            education_section = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            if education_section:
                break
        except (TimeoutException, NoSuchElementException):
            continue

    if education_section:
        edu_items = education_section.find_elements(By.XPATH, ".//li[contains(@class, 'artdeco-list__item')]")

        for item in edu_items:
            try:
                institute = item.find_element(By.XPATH, ".//span[@aria-hidden='true']").text.strip()
            except NoSuchElementException:
                institute = "Institute Not Found"

            try:
                degree = item.find_element(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal')]/span").text.strip()
            except NoSuchElementException:
                degree = "Degree Not Found"

            try:
                date_range = item.find_element(By.XPATH, ".//span[contains(@class, 'pvs-entity__caption-wrapper')]").text.strip()
            except NoSuchElementException:
                date_range = "Date Range Not Found"

            try:
                location_elements = item.find_elements(By.XPATH, ".//span[contains(@class, 't-14') and contains(@class, 't-normal') and contains(@class, 't-black--light')]/span")
                location = "Location Not Found"
                for loc in location_elements:
                    loc_text = loc.text.strip()
                    if loc_text and not any(char.isdigit() for char in loc_text):
                        location = loc_text
                        break
            except NoSuchElementException:
                location = "Location Not Found"

            try:
                description = ""
                description_xpaths = [
                    ".//div[contains(@class, 'description')]//span[@aria-hidden='true']",
                    ".//div[contains(@class, 'show-more-less-text')]//span[@aria-hidden='true']",
                    ".//div[contains(@class, 'inline-show-more-text')]//span[@aria-hidden='true']",
                    ".//div[contains(@class, 'pv-shared-text-with-see-more')]//span[@aria-hidden='true']"
                ]

                for xpath in description_xpaths:
                    try:
                        desc_element = item.find_element(By.XPATH, xpath)
                        potential_desc = desc_element.text.strip()
                        if potential_desc and len(potential_desc) > 20:
                            description = potential_desc
                            break
                    except NoSuchElementException:
                        continue

                if not description:
                    description = "No Description"
            except Exception as e:
                print(f"Error extracting description: {str(e)}")
                description = "Error extracting description"

            education.append({
                "Institute": institute,
                "Degree": degree,
                "Date Range": date_range,
                "Location": location,
                "Description": description
            })

    return education

def main():
    input_file = "Assignment.xlsx"
    df = pd.read_excel(input_file)
    
    if "LinkedIn URLs" not in df.columns:
        raise KeyError("The column 'LinkedIn URLs' was not found in the Excel file. Please check the column name.")
    
    driver = setup_driver()
    
    email = "youremail@.com"
    password = "password"
    linkedin_login(driver, email, password)
    
    scraped_data = []
    for url in df["LinkedIn URLs"]:
        profile_data = scrape_linkedin_profile(driver, url)
        scraped_data.append(profile_data)
        print(f"Scraped: {profile_data['Name']}")
        time.sleep(3)
    
    driver.quit()
    
    # Format experience data for CSV output
    for data in scraped_data:
        if isinstance(data["Experience"], list) and data["Experience"]:
            formatted_exp = []
            for exp in data["Experience"]:
                exp_str = (
                    f"Role: {exp['Role']}\n"
                    f"Company: {exp['Company']}\n"
                    f"Date: {exp['Date Range']}\n"
                    f"Location: {exp['Location']}\n"
                    f"Description: {exp['Description']}"
                )
                formatted_exp.append(exp_str)
            data["Experience"] = "\n\n".join(formatted_exp)
            
        # Format education data for CSV output
        if isinstance(data["Education"], list) and data["Education"]:
            formatted_edu = []
            for edu in data["Education"]:
                edu_str = (
                    f"Institute: {edu['Institute']}\n"
                    f"Degree: {edu['Degree']}\n"
                    f"Date: {edu['Date Range']}\n"
                    f"Location: {edu['Location']}\n"
                    f"Description: {edu['Description']}"
                )
                formatted_edu.append(edu_str)
            data["Education"] = "\n\n".join(formatted_edu)
    
    output_df = pd.DataFrame(scraped_data)
    output_df.to_csv("scraped_output.csv", index=False)
    print("Scraping completed! Output saved as 'scraped_output.csv'")

if __name__ == "__main__":
    main()