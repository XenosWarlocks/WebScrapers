#main.py
########################################################################
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager




# def main():
#     # Prompt the user to enter a website URL
#     url = input("Please enter the website URL you want to visit: ")




#     # Set up Chrome options
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("detach", True)  # Keeps the browser open after the script finishes
#     options.add_argument('--no-sandbox')  # Disables the sandbox for Chrome
#     options.add_argument('--disable-dev-shm-usage')  # Disables shared memory use for Chrome
#     options.add_argument('--start-maximized')  # Maximizes the browser window




#     # Set up the Chrome driver using WebDriver Manager
#     service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(options=options, service=service)




#     try:
#         # Navigate to the provided URL
#         print(f"Visiting {url}...")
#         driver.get(url)




#         # Wait for the page to load
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#         print("Page loaded successfully.")




#         # Get the page title
#         title = driver.title
#         print(f"Page Title: {title}")




#         # Example: Extract all links from the page
#         links = driver.find_elements(By.TAG_NAME, "a")
#         print(f"Found {len(links)} links on the page.")
#         for link in links[:10]:  # Print the first 10 links as an example
#             href = link.get_attribute('href')
#             if href:
#                 print(href)




#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         # The browser will stay open due to the detach option, so no need to close it here.
#         pass




# if __name__ == "__main__":
#     main()




######################################################################




# import requests
# from bs4 import BeautifulSoup
# import csv
# import re




# def extract_phone_number(text):
#     """Extract phone number from text using regular expressions."""
#     phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
#     match = phone_pattern.search(text)
#     return match.group() if match else None




# def main():
#     # Prompt the user for a URL
#     url = input("Enter the website URL to scrape: ")




#     try:
#         # Send a GET request to the URL
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for bad responses




#         # Parse the page content with BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')




#         # Prepare to write data to CSV
#         csv_file = 'scraped_data.csv'
#         csv_columns = ['Name', 'Phone Number', 'Email']
       
#         with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.DictWriter(file, fieldnames=csv_columns)
#             writer.writeheader()




#             # Extract <h3> and <p> tags within the "title-description" class
#             print("\nDetails from <div class='title-description'>:")
#             for div in soup.find_all('div', class_='title-description'):
#                 # Extract the <h3> tag text
#                 name = None
#                 h3 = div.find('h3')
#                 if h3:
#                     name = h3.get_text(strip=True)




#                 # Initialize phone and email
#                 phone = None
#                 email = None




#                 # Extract <p> tags
#                 for p in div.find_all('p'):
#                     p_text = p.get_text(strip=True)
#                     # Extract phone number using regex
#                     phone = extract_phone_number(p_text) or phone
#                     # Extract email if available
#                     if '@' in p_text:
#                         email = p.find('a').get_text(strip=True) if p.find('a') else None




#                 # Print extracted data
#                 print(f"Name: {name}")
#                 print(f"Phone Number: {phone}")
#                 print(f"Email: {email}")




#                 # Write data to CSV
#                 writer.writerow({
#                     'Name': name,
#                     'Phone Number': phone,
#                     'Email': email
#                 })
       
#         print(f"\nData has been saved to {csv_file}.")




#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")




# if __name__ == "__main__":
#     main()
######################################################################




import requests
from bs4 import BeautifulSoup
import csv
import re
from urllib.parse import urljoin




def extract_email_from_profile(profile_url):
    """Extract email from the profile page."""
    try:
        response = requests.get(profile_url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')




        # Find email addresses in <span> tags containing <a> tags with href="mailto:"
        email = None
        for span in soup.find_all('span'):
            a_tag = span.find('a', href=True)
            if a_tag and a_tag['href'].startswith('mailto:'):
                email = a_tag.get_text(strip=True)
                break
        return email
    except requests.exceptions.RequestException as e:
        print(f"Error fetching profile page: {e}")
        return None




def scrape_page(url, writer):
    """Scrape data from a single page."""
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses




        # Parse the page content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')




        # Extract data from elements with class "person-card"
        print(f"\nScraping data from {url}:")
        for card in soup.find_all('div', class_='person-card'):
            # Extract aria-label from <a> tag
            aria_label = None
            a_tag = card.find('a', {'aria-label': True})
            if a_tag:
                aria_label = a_tag['aria-label']
           
            # Extract src from <img> tag
            img_src = None
            img_tag = card.find('img', src=True)
            if img_tag:
                img_src = img_tag['src']
           
            # Follow the URL in <a> tag to find the email
            profile_url = a_tag['href'] if a_tag else None
            email = None
            if profile_url:
                profile_url = urljoin(url, profile_url)  # Handle relative URLs
                email = extract_email_from_profile(profile_url)




            # Print extracted data
            print(f"Aria Label: {aria_label}")
            # print(f"Image Source: {img_src}")
            print(f"Email: {email}")




            # Write data to CSV
            writer.writerow({
                'Aria Label': aria_label,
                # 'Image Source': img_src,
                'Email': email
            })
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")




def main():
    base_url = "https://dornsife.usc.edu/our-staff/"
    start_page = 1
    end_page = 91




    # Prepare to write data to CSV
    csv_file = 'scraped_data.csv'
    csv_columns = ['Aria Label', 'Email']
   
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=csv_columns)
        writer.writeheader()




        # Loop through pages
        for page_number in range(start_page, end_page + 1):
            page_url = f"{base_url}{page_number}/"
            scrape_page(page_url, writer)




    print(f"\nData has been saved to {csv_file}.")




if __name__ == "__main__":
    main()







