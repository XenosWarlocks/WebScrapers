import requests
from bs4 import BeautifulSoup
import csv


def scrape_names_and_emails(url):
    # Send a GET request to the website
    response = requests.get(url)


    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')


        # Find all content description blocks based on the provided structure
        content_descriptions = soup.find_all('div', class_='content-description')


        # Prepare the data for CSV
        data = []
       
        for content in content_descriptions:
            # Extract the name
            name_tag = content.find('div', class_='field--name-field-display-title')
            name = name_tag.find('a').get_text(strip=True) if name_tag else "No Name"


            # Extract the email
            email_tag = content.find('div', class_='field--name-field-faculty-email')
            email = email_tag.find('a').get_text(strip=True) if email_tag else "No Email"


            # Append the collected data to the list
            data.append([url, name, email])
            print(f'Name: {name}, Email: {email}')


        # Write data to CSV file
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write the header
            csvwriter.writerow(['URL', 'Name', 'Email'])
            # Write the data rows
            csvwriter.writerows(data)


        print("Data has been written to scraped_data.csv")


    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


# Example usage
url = input("Enter the URL of the website you want to scrape: ")
scrape_names_and_emails(url)



