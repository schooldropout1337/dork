import argparse
import requests
import bs4
import urllib.parse
import re


print('''\033[92m
     _            _
  __| | ___  _ __| | __
 / _` |/ _ \| '__| |/ /
| (_| | (_) | |  |   <
 \__,_|\___/|_|  |_|\_/

    \033[00m''')

# Create an argument parser
parser = argparse.ArgumentParser(description='Google Dork Script')

# Add the input argument
parser.add_argument('-d', '--dork', type=str, help='Specify the search dork.')

# Parse the command line arguments
args = parser.parse_args()

# Check if the dork argument is provided
if not args.dork:
    parser.error('The search query (-d/--dork) is required.')

# Retrieve the search query from the command line arguments
dork = args.dork

# Convert the search query to URL-encoded format
encoded_query = urllib.parse.quote(dork)
#print(encoded_query)
print("dork : " '\033[93m' + dork + '\033[00m\n')


# Define the parameters to remove
params_to_remove = ['sa', 'ved', 'usg']

# Iterate over the first three pages of search results
for page in range(2):
    # Calculate the start index for the current page
    start = page * 10

    # Construct the Google search URL for the current page
    #url = f'https://google.com/search?q={dork}&start={start}'
    url = f'https://google.com/search?q={dork}'

    # Send a GET request to the URL and store the response
    request_result = requests.get(url)

    # Create a BeautifulSoup object from the response HTML
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")

    # Find all anchor tags (links) within the search results
    link_tags = soup.find_all('a')

    # Iterate through the link tags and extract the URLs
    for link_tag in link_tags:
        href = link_tag.get('href')
        if href.startswith('/url?q='):  # Extract the URL from the href attribute
            url = href[7:]  # Remove the '/url?q=' prefix
            url = urllib.parse.unquote(url)  # Decode URL-encoded characters

            if not (url.startswith('https://www.google.com') or
                    url.startswith('https://support.google.com/web') or
                    url.startswith('https://accounts.google.com')):  # Exclude specified links
                # Remove the parameters along with their values
                cleaned_url = re.sub(r'&?(?:{})=.*?(?=&|$)'.format('|'.join(params_to_remove)), '', url)
                print(cleaned_url)

print()
