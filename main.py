import streamlit as st
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from urllib.request import urlopen as uReq
import pandas as pd
import time

# streamlit run C:/Users/patri/CSGOCasePrices/main.py

st.set_page_config(layout="wide")

st.title('CS:GO Case Price App')

st.markdown("""
This app retrieves CS:GO case prices and quantities from the **Steam Community Market**
""")

st.markdown("""
**About**
* **Python Libraries:** streamlit, BeautifulSoup, selenium.webdriver, time, urllib, pandas
* **Data Source:** Steam Community Market
""")

driver = webdriver.Chrome()

sidebar = st.sidebar
sidebar.header('Input Options')
selected_item = sidebar.selectbox('Select the item type you would like to see', ('Cases', 'Other'))


@st.cache
def load_item(pages, url):
    temp = pd.DataFrame(columns=['Item', 'Quantity', 'Price'])
    item_name = []
    quantity = []
    price = []
    for page_number in range(1, pages):
        full_url = url + str(page_number) + '_price_desc'
        driver.get(full_url)
        pagesource = driver.page_source

        uClient = uReq(full_url)
        page_html = uClient.read()
        uClient.close()

        soup = BeautifulSoup(pagesource, "html.parser")

        # finds each case
        items = soup.findAll("div", {"class": "market_listing_row"})

        for item in items:
            # case name
            item_name.append(list(item.find("span", {"market_listing_item_name"}))[0].strip())

            # number of cases
            quantity.append(int(item.find("span", "market_listing_num_listings_qty")["data-qty"]))

            # price of one case in dollars
            value = (item.find("span", {"class": "normal_price"}))
            full_price = float(value.span["data-price"]) / 100.0
            price.append(full_price)
            time.sleep(1)

    temp['Item'] = item_name
    temp['Quantity'] = quantity
    temp['Price'] = price
    return temp


if selected_item == 'Cases':
    url = 'https://steamcommunity.com/market/search?q=Case&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730#p'
    cases = load_item(6, url)

    sorted_cases = sorted(cases['Item'])
    selected_cases = sidebar.multiselect('Item', sorted_cases, sorted_cases)

    cases_selected_cases = cases[(cases['Item'].isin(selected_cases))]

    st.subheader('Price and Quantity Data of CS:GO cases')
    st.dataframe(cases_selected_cases)

