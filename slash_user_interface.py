"""
Copyright (c) 2021 Anshul Patel
This code is licensed under MIT license (see LICENSE.MD for details)

@author: slash
"""

# Import Libraries
import sys
import hyperlink

sys.path.append('../')
import streamlit as st
from src.main_streamlit import search_items_API
from src.url_shortener import shorten_url
import pandas as pd
import re
import os
# Add custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #fae0c3 /* Beige background color */
    }
    .navbar {
        background-color: white;
        padding: 10px;
    }
    .navbar a {
        color: #1DC5A9; /* Teal color for navbar links */
    }
    .search-button {
        background-color: #1DC5A9;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        cursor: pointer;
    }
    .search-button:hover {
        background-color: #121211 /* Darker teal color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add a navbar
st.markdown(
    """
    <div class="navbar">
        <h1>Splash - E-commerce Deal Finder</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Display Image
st.image("assets/slash.png")

st.write("Slash is a command line tool that scrapes the most popular e-commerce websites to get the best deals on the searched items across multiple websites")
product = st.text_input('Enter the product item name')

website = st.selectbox('Select the website', ('Amazon', 'Walmart', 'Ebay', 'BestBuy', 'Target', 'Costco', 'All'))

website_dict = {
    'Amazon': 'az',
    'Walmart': 'wm',
    'Ebay': 'eb',
    'BestBuy': 'bb',
    'Target': 'tg',
    'Costco': 'cc',
    'All': 'all'
}

# Pass product and website to method
if st.button('Search') and product and website:
    results = search_items_API(website_dict[website], product)
    # Use st.columns based on return values
    description = []
    url = []
    price = []
    site = []

    if results is not None and isinstance(results, list):
        for result in results:
            if result != {} and result['price'] != '':
                description.append(result['title'])
                url.append(result['link'])
                price_str = result['price']
                match = re.search(r'\d+(\.\d{1,2})?', price_str)
                if match:
                    price_str = match.group(0)
                    price_f = float(price_str)
                    price.append(price_f)
                else:
                    print("Unable to extract a valid price from the string")
                site.append(result['website'])

    if len(price):

        def highlight_row(dataframe):
            # copy df to new - original data are not changed
            df = dataframe.copy()
            minimumPrice = df['Price'].min()
            # set by condition
            mask = df['Price'] == minimumPrice
            df.loc[mask, :] = 'background-color: lightgreen'
            df.loc[~mask, :] = 'background-color: #DFFFFA'
            return df
        # url = hyperlink.parse(url)
        # Create the DataFrame with specified headings
        data = {'Description': description, 'Price': price, 'Link': url, 'Website': site}
        dataframe = pd.DataFrame(data)
        
        # Display the DataFrame
        # st.write(dataframe)
        dataframe_with_links = dataframe.copy()


        # Make all the links in the rows clickable
        for index, row in dataframe_with_links.iterrows():
            link = row['Link']
            if link:
                clickable_link = hyperlink.URL.from_text(row['Link'])
                if clickable_link.to_text().startswith(("http://", "https://")):
                    st.markdown(f"[{clickable_link.to_text()}]({clickable_link.to_text()})")
                else:
                    st.markdown(f"[{clickable_link.to_text()}](http://{clickable_link.to_text()})")
        st.table(dataframe_with_links)
       
        st.balloons()
        st.markdown("<h1 style='text-align: center; color: #1DC5A9;'>RESULT</h1>", unsafe_allow_html=True)
        st.dataframe(dataframe.style.apply(highlight_row, axis=None))
        st.markdown("<h1 style='text-align: center; color: #1DC5A9;'>Visit the Website</h1>", unsafe_allow_html=True)
        min_value = min(price)
        min_idx = [i for i, x in enumerate(price) if x == min_value]
        for minimum_i in min_idx:
            link_button_url = shorten_url(url[minimum_i].split('\\')[-1])
            st.write("Cheapest Product [link]("+link_button_url+")")
    else:
        st.error('Sorry!, there is no other website with the same product')
            

# Add footer to UI
footer="""<style>
a:link , a:visited{
color: #121211
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: white;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0%;
width: 100%;
background-color: #362017;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://github.com/anshulp2912/slash" target="_blank">slash</a></p>
<p><a style='display: block; text-align: center;' href="https://github.com/anshulp2912/slash/blob/main/LICENSE" target="_blank">MIT License Copyright (c) 2021 Rohan Shah</a></p>
<p>Contributors: Anshul, Bhavya, Darshan, Pragna, Rohan</p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
