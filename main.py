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
This app retrieves CS:GO prices and quantities from the **Steam Community Market**
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
        print(page_number)
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

        time.sleep(2)

    temp['Item'] = item_name
    temp['Quantity'] = quantity
    temp['Price'] = price
    return temp


sidebar = st.sidebar
sidebar.header('Input Options')
selected_type = sidebar.selectbox('Select the item type you would like to see',
                                  ('Cases', 'Knives', 'Souvenirs', 'Stickers', 'Weapons'))

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

elif selected_type == 'Knives':
    selected_weapon = sidebar.selectbox('Select the weapon you would like to see here', ('Bayonet', 'Bowie Knife', 'Butterfly Knife', 'Classic Knife', 'Falchion Knife',
                                                                                         'Flip Knife', 'Gut Knife', 'Huntsman Knife', 'Karambit', 'M9 Bayonet',
                                                                                         'Navaja Knife', 'Nomad Knife', 'Paracord Knife', 'Shadow Daggers', 'Skeleton Knife',
                                                                                         'Stiletto Knife', 'Survival Knife', 'Talon Knife', 'Ursus Knife'))
    knives = pd.DataFrame()
    if selected_weapon == 'Bayonet':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_bayonet&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(5, url)

    elif selected_weapon == 'Bowie Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_survival_bowie&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'Butterfly Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_butterfly&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'Classic Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_css&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'Falchion Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_falchion&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'Flip Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_flip&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'Gut Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_gut&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(5, url)

    elif selected_weapon == 'Huntsman Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_tactical&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'Karambit':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_karambit&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'M9 Bayonet':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_m9_bayonet&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(5, url)

    elif selected_weapon == 'Navaja Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_gypsy_jackknife&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'Nomad Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_outdoor&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(2, url)

    elif selected_weapon == 'Paracord Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_cord&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(2, url)

    elif selected_weapon == 'Shadow Daggers':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_push&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'Skeleton Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_skeleton&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(2, url)

    elif selected_weapon == 'Stiletto Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_stiletto&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(5, url)

    elif selected_weapon == 'Survival Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_canis&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(2, url)

    elif selected_weapon == 'Talon Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_widowmaker&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    elif selected_weapon == 'Ursus Knife':
        url = 'https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_knife_ursus&category_730_Exterior%5B%5D=tag_WearCategory0&appid=730#p'
        knives = load_item(4, url)

    sorted_knives = sorted(knives['Item'])
    selected_knife = sidebar.multiselect('Item', sorted_knives, sorted_knives)

    selected_knives = knives[(knives['Item'].isin(selected_knife))]

    st.subheader('Price and Quantity Data of Selected Knife in Factory New Condition')
    st.dataframe(selected_knives)

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
