# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL setup and HTML request
url = 'https://www.amazon.ca/Sony-WF-1000XM3-Industry-Canceling-Wireless/product-reviews/B07T81554H/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
r = requests.get('http://localhost:8050/render.html', params = {'url': url, 'wait' : 2})
#print(r)

# Parsing the HTML content
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup)

# Getting desired data from our parsed soup
reviews = soup.find_all('div', {'data-hook': 'review'})
#print(reviews)

# Initialize list
data = []

# For every item in review, scrape the following data points and store as a list called review
for item in reviews:
    review = {
    # scrape product name
    'product': soup.title.text.replace('Amazon.ca:Customer reviews: ', '').strip(), 
    # scrape the review title
    'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
    # scrape the date (includes the syntax: Reviewed in Canada on...)
    'date': item.find('span', {'data-hook': 'review-date'}).text.strip(),
    # scrape the star rating, leave as a decimal
    'rating': float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
    # scrape the actual review text
    'text': item.find('span', {'data-hook': 'review-body'}).text.strip(),
    }
    data.append(review)  
#print(len(data))

# Save results to a dataframe, then export as CSV
df = pd.DataFrame(data)
df.to_csv(r'sony-headphones.csv', index=False)

