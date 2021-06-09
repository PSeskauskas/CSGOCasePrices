import streamlit as st
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from urllib.request import urlopen as uReq
import pandas as pd

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


def load_cases():
    temp = pd.DataFrame(columns=['Case', 'Quantity', 'Price'])
    case_name = []
    quantity = []
    price = []
    for page_number in range(1, 6):
        url = 'https://steamcommunity.com/market/search?q=Case&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730#p' + str(
            page_number) + '_price_desc'
        driver.get(url)
        pagesource = driver.page_source

        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()

        soup = BeautifulSoup(pagesource, "html.parser")

        # finds each case
        containers = soup.findAll("div", {"class": "market_listing_row"})

        for container in containers:
            # case name
            case_name.append(list(container.find("span", {"market_listing_item_name"}))[0].strip())

            # number of cases
            quantity.append(int(container.find("span", "market_listing_num_listings_qty")["data-qty"]))

            # price of one case in dollars
            value = (container.find("span", {"class": "normal_price"}))
            full_price = float(value.span["data-price"]) / 100.0
            price.append(full_price)

    temp['Case'] = case_name
    temp['Quantity'] = quantity
    temp['Price'] = price
    return temp


cases = load_cases()
print(cases)

st.subheader('Price and Quantity Data of CS:GO cases')
st.dataframe(cases)
