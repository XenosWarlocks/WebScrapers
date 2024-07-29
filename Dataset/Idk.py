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


        # Find all person items based on the provided structure
        people = soup.find_all('div', class_='row person-item')


        # Prepare the data for CSV
        data = []
       
        for person in people:
            # Extract the name
            first_name = person.find('span', class_='first-name').get_text(strip=True)
            middle_initial = person.find('span', class_='middle-initial').get_text(strip=True) if person.find('span', class_='middle-initial') else ""
            last_name = person.find('span', class_='last-name').get_text(strip=True)
            full_name = f"{first_name} {middle_initial} {last_name}".strip()


            # Extract the email
            email_tag = person.find('a', class_='email')
            email = email_tag.find('span', class_='content').get_text(strip=True) if email_tag else "No Email"


            # Extract the phone number
            phone_tag = person.find('a', class_='phone')
            phone = phone_tag.find('span', class_='content').get_text(strip=True) if phone_tag else "No Phone"


            # Append the collected data to the list
            data.append([url, full_name, phone, email])
            print(f'Name: {full_name}, Phone: {phone}, Email: {email}')


        # Write data to CSV file
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write the header
            csvwriter.writerow(['URL', 'Name', 'Phone', 'Email'])
            # Write the data rows
            csvwriter.writerows(data)


        print("Data has been written to scraped_data.csv")


    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


# Example usage
url = input("Enter the URL of the website you want to scrape: ")
scrape_names_and_emails(url)



