import csv
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
from webdriver_manager.chrome import ChromeDriverManager


# List of User-Agents to cycle through
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/92.0.902.62 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
]


def close_overlay(driver):
    """Close any overlay such as cookie consent that might block interactions."""
    try:
        # Attempt to close the overlay by finding and clicking the close button
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))  # Example ID for cookie consent
        )
        close_button.click()
        print("Overlay closed.")
    except (TimeoutException, NoSuchElementException):
        print("No overlay found or unable to close overlay.")


def scrape_names_emails_and_phones(url):
    # Select a random User-Agent from the list
    user_agent = random.choice(user_agents)


    # Set up the Chrome WebDriver with options
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')  # Disable GPU acceleration
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument('start-maximized')  # Open the browser in maximized mode
    options.add_argument('disable-infobars')  # Disable info bars
    options.add_argument('--disable-extensions')  # Disable extensions
    options.add_argument("--incognito")  # Open in incognito mode


    # Set custom User-Agent to mimic a real browser
    options.add_argument(f'user-agent={user_agent}')


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)


    # Wait for the page to load and the elements to be available
    wait = WebDriverWait(driver, 10)


    # Close any overlay that might block interactions
    close_overlay(driver)


    # Prepare CSV writing
    with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(['URL', 'Name', 'Phone', 'Email'])


        try:
            # Find all rows with class 'person'
            people = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.person")))


            for person in people:
                try:
                    # Extract the name
                    name_elements = person.find_elements(By.CSS_SELECTOR, "td.name strong")
                    if name_elements:
                        full_name = name_elements[0].text.strip()


                    # Extract the phone number
                    contact_info = person.find_element(By.ID, "contact")
                    phone_number = contact_info.text.strip().split("\n")[-1]


                    # Click the "Show Email" link to reveal the email
                    show_email_link = contact_info.find_element(By.CLASS_NAME, "show-email")


                    # Introduce random delay
                    time.sleep(random.uniform(1.5, 3.5))


                    # Ensure the "Show Email" button is clickable
                    driver.execute_script("arguments[0].scrollIntoView();", show_email_link)


                    # Handle click interception by retrying
                    attempts = 3
                    for attempt in range(attempts):
                        try:
                            show_email_link.click()
                            break
                        except (ElementClickInterceptedException, ElementNotInteractableException):
                            print(f"Element click intercepted or not interactable, retrying... (Attempt {attempt + 1})")
                            time.sleep(1)


                    # Wait for the email to be revealed
                    time.sleep(2)  # Wait 2 seconds to ensure the email is visible


                    try:
                        # Extract the email
                        email_element = contact_info.find_element(By.CSS_SELECTOR, "a[href^='mailto:']")
                        email = email_element.get_attribute("href").replace("mailto:", "").strip()


                    except NoSuchElementException:
                        email = "No Email"
                        print("Email not found, using placeholder.")


                    # Append the collected data to the CSV file
                    csvwriter.writerow([url, full_name, phone_number, email])
                    print(f'Name: {full_name}, Phone: {phone_number}, Email: {email}')
                except Exception as e:
                    print(f"An error occurred for one of the entries: {str(e)}")
                    continue
        except TimeoutException:
            print("Timeout occurred while waiting for people elements.")


    print("Data has been written to scraped_data.csv")


    # Close the browser
    driver.quit()


# Example usage
urls = [
    "",
]


for url in urls:
    scrape_names_emails_and_phones(url)


