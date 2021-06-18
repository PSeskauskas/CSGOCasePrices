import streamlit as st
from bs4 import BeautifulSoup
import selenium.webdriver as webdriver
from urllib.request import urlopen as uReq
import pandas as pd
import time

# streamlit run C:/Users/patri/CSGOCasePrices/main.py

st.set_page_config(layout="wide")

st.title('CS:GO Item Data App')

st.markdown("""
This app retrieves CS:GO case prices and quantities from the **Steam Community Market**
""")

st.markdown("""
**About**
* **Python Libraries:** streamlit, BeautifulSoup, selenium.webdriver, time, urllib, pandas
* **Data Source:** Steam Community Market
""")


@st.cache
def load_item(pages, item_url):
    driver = webdriver.Chrome()
    temp = pd.DataFrame(columns=['Item', 'Quantity', 'Price'])
    item_name = []
    quantity = []
    price = []
    for page_number in range(1, pages):
        full_url = item_url + str(page_number) + '_price_desc'
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


sidebar = st.sidebar
sidebar.header('Input Options')
selected_type = sidebar.selectbox('Select the item type you would like to see',
                                  ('Stickers', 'Weapons', 'Cases', 'Souvenirs'))

if selected_type == 'Stickers':

    selected_item = sidebar.selectbox('Select the Stickers you would like to see', ('Team Capsules', 'Autograph Capsules'))

    if selected_item == 'Autograph Capsules':
        url = 'https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730&q=Legends+Autograph+Capsule#p'
        legends_autographs = load_item(3, url)

        url = 'https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730&q=Challengers+Autograph+Capsule#p'
        challengers_autographs = load_item(4, url)

        datasets = [legends_autographs, challengers_autographs]

        autographs = pd.concat(datasets)

        sorted_autographs = sorted(autographs['Item'])
        selected_autographs = sidebar.multiselect('Item', sorted_autographs, sorted_autographs)

        autographs_sorted_autographs = autographs[(autographs['Item'].isin(selected_autographs))]

        st.subheader('Price and Quantity Data of CS:GO Legends and Challengers Autograph Capsules')
        st.dataframe(autographs_sorted_autographs)

    elif selected_item == 'Team Capsules':
        url = 'https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730&q=Legends#p'
        legends_stickers = load_item(5, url)

        url = 'https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730&q=Challengers#p'
        challengers_stickers = load_item(6, url)

        url = 'https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730&q=Contenders#p'
        contenders_stickers = load_item(3, url)

        datasets = [legends_stickers, challengers_stickers, contenders_stickers]
        capsules = pd.concat(datasets)

        sorted_capsules = sorted(capsules['Item'])
        selected_capsules = sidebar.multiselect('Item', sorted_capsules, sorted_capsules)

        capsules_sorted_capsules = capsules[(capsules['Item'].isin(selected_capsules))]

        st.subheader("Price and Quantity Data for CS:GO Team Capsules")
        st.dataframe(capsules_sorted_capsules)

elif selected_type == 'Cases':
    url = 'https://steamcommunity.com/market/search?q=Case&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730#p'
    cases = load_item(6, url)

    sorted_cases = sorted(cases['Item'])
    selected_cases = sidebar.multiselect('Item', sorted_cases, sorted_cases)

    cases_selected_cases = cases[(cases['Item'].isin(selected_cases))]

    st.subheader('Price and Quantity Data of CS:GO cases')
    st.dataframe(cases_selected_cases)

elif selected_type == 'Weapons':
    st.subheader('Work in progress')

elif selected_type == 'Souvenirs':
    url = 'https://steamcommunity.com/market/search?category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any&category_730_Type%5B%5D=tag_CSGO_Type_WeaponCase&appid=730&q=Souvenir#p'
    souvenirs = load_item(12, url)

    sorted_souvenirs = sorted(souvenirs['Item'])
    selected_souvenirs = sidebar.multiselect('Item', sorted_souvenirs, sorted_souvenirs)

    souvenirs_selected_souvenirs = souvenirs[(souvenirs['Item'].isin(selected_souvenirs))]

    st.subheader('Price and Quantity Data of CS:GO Souvenir Packages')
    st.dataframe(souvenirs_selected_souvenirs)
