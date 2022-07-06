import streamlit as st
import requests
import json
from PIL import Image
import pandas as pd
import numpy as np
import pydeck as pdk
from bokeh.models.widgets import Div

st.set_page_config(layout="centered", page_icon="✈️", page_title="Travelry - Never Get Lost!")

def set_bg_hack_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(https://i.pinimg.com/originals/e3/f1/d9/e3f1d969e39cba1c5fe76166263821cc.jpg);
             background-repeat: no-repeat;
             background-size: 1250px 1120px;
             background-position: center;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
set_bg_hack_url()

image = Image.open('badge.png')
st.image(image, use_column_width = True, caption='Never Get Lost!')


# input user
st.header("Traveler's Information")

with st.form(key='my_form'):
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Fill your Name")
        age = st.number_input("Fill your Age", step = 1, min_value=17)
        monthly_income = st.number_input("Fill your Monthly Income (Rupiah)", step = 100, min_value=0)
    with col2:
        person = st.number_input("Number of Person", step = 1, min_value=1)
        children = st.number_input("Number of Children", step = 1, min_value=0)
        trip = st.number_input("Average Number of Trip per year", step = 1, min_value=0)
    
    # filter hotel
    st.subheader("Hotel Facilities")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        pool = st.checkbox("Pool")
    with col2:
        wifi = st.checkbox("Free Wifi")
    with col3:
        breakfast = st.checkbox("Free Breakfast")
    with col4:
        beach = st.checkbox("Access to the Beach")
    with col5:
        spa = st.checkbox("Spa")
    
    hasil = [pool, wifi, breakfast, beach, spa]
    akumulasi = sum(hasil)
    encode = []
    encode2 = []

    for i in hasil:
        encode.append(i)

    for z in encode:
        if z == True:
            encode2.append('Yes')
        else :
            encode2.append('No')
    
    # filter resto
    st.subheader("Restaurant Type")

    filter_resto = st.selectbox("Food Type", ['All Category', 'Vegetarian Food', 'Italian Food', 'Western Food', 'Seafood',
        'Indonesian Food', 'Chinese Food', 'Japanese Food', 'Cafe', 'Fast Food'])

    # Inference Set
    data = {'age':age,
            'person':person,
            'trip':trip,
            'children':children,
            'monthly_income':monthly_income}
    
    # URL backend
    URL = "http://127.0.0.1:5000/predict"    
    
    # komunikasi
    class_prediction = st.form_submit_button(label='Submit')
    r = requests.post(URL, json=data)
    res = r.json()
    
# Recommendation System
st.header(f"Itinerary Recommendation for {name} in Labuan Bajo!")

# load dataset
hotel = pd.read_csv('hotel_final.csv')
resto = pd.read_csv('resto_final.csv', encoding='latin-1')
wisata = pd.read_csv('wisata_final.csv')

# logic recommendation
if res['result']['class_name'] == 'Basic':
    # logic filter hotel
    if akumulasi <= 1:    
        hasil_hotel_or = hotel[(hotel['cluster_hotel']== 'Basic') | 
        (hotel['facility_pool']== encode2[0]) |
        (hotel['facility_wifi'] == encode2[1]) |
        (hotel['facility_breakfast'] == encode2[2]) |
        (hotel['facility_beach_access'] == encode2[3]) |
        (hotel['facility_spa'] == encode2[4])]
        data_show = hasil_hotel_or
    else:
        hasil_hotel_dan = hotel[(hotel['cluster_hotel']== 'Basic') & 
        (hotel['facility_pool']== encode2[0]) &
        (hotel['facility_wifi'] == encode2[1]) &
        (hotel['facility_breakfast'] == encode2[2]) &
        (hotel['facility_beach_access'] == encode2[3]) &
        (hotel['facility_spa'] == encode2[4])]
        data_show = hasil_hotel_dan
        
    # logic filter resto
    if filter_resto == 'All Category':
        hasil_resto = resto[resto['cluster_resto'] == 'Basic']
    else:
        hasil_resto = resto[(resto['cluster_resto'] == 'Basic') & (resto['kategori'] == str(filter_resto))]

    # Define a layer to display on a map
    layer1 = pdk.Layer(
            "ScatterplotLayer",
            data = data_show,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=6,
            get_position='[lon, lat]',
            get_radius=15,
            get_fill_color=[0,0,255]
        )
    layer2 = pdk.Layer(
            "ScatterplotLayer",
            data = hasil_resto,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=6,
            get_position='[lon, lat]',
            get_radius=15,
            get_fill_color=[255.0,0]
        )
    layer3 = pdk.Layer(
            "ScatterplotLayer",
            data = wisata,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=6,
            get_position='[lon, lat]',
            get_radius=15,
            get_fill_color=[0,128,0]
        )
    
    # Set the viewport location
    view_state = pdk.ViewState(latitude=-8.460834, longitude=119.8631577, zoom=12)

    # Render
    st.pydeck_chart(pdk.Deck(layers=[layer1, layer2, layer3], initial_view_state=view_state, 
                             tooltip={"text": "{name}\nIDR {price}\n{kategori}"},
                             map_style='mapbox://styles/mapbox/navigation-day-v1'))

elif res['result']['class_name'] == 'Deluxe':
    # logic filter hotel
    if akumulasi <= 1:    
        hasil_hotel_or = hotel[(hotel['cluster_hotel']== 'Deluxe') | 
        (hotel['facility_pool']== encode2[0]) |
        (hotel['facility_wifi'] == encode2[1]) |
        (hotel['facility_breakfast'] == encode2[2]) |
        (hotel['facility_beach_access'] == encode2[3]) |
        (hotel['facility_spa'] == encode2[4])]
        data_show = hasil_hotel_or
    else:
        hasil_hotel_dan = hotel[(hotel['cluster_hotel']== 'Deluxe') & 
        (hotel['facility_pool']== encode2[0]) &
        (hotel['facility_wifi'] == encode2[1]) &
        (hotel['facility_breakfast'] == encode2[2]) &
        (hotel['facility_beach_access'] == encode2[3]) &
        (hotel['facility_spa'] == encode2[4])]
        data_show = hasil_hotel_dan
    
    # logic filter resto
    if filter_resto == 'All Category':
        hasil_resto = resto[resto['cluster_resto'] == 'Deluxe']
    else:
        hasil_resto = resto[(resto['cluster_resto'] == 'Deluxe') & (resto['kategori'] == str(filter_resto))]

    # Define a layer to display on a map
    layer1 = pdk.Layer(
            "ScatterplotLayer",
            data = data_show,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=6,
            get_position='[lon, lat]',
            get_radius=15,
            get_fill_color=[0,0,255],
        )
    layer2 = pdk.Layer(
            "ScatterplotLayer",
            data = hasil_resto,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=6,
            get_position='[lon, lat]',
            get_radius=15,
            get_fill_color=[255.0,0],
        )
    layer3 = pdk.Layer(
            "ScatterplotLayer",
            data = wisata,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=6,
            get_position='[lon, lat]',
            get_radius=15,
            get_fill_color=[0,128,0],
        )
    
    # Set the viewport location
    view_state = pdk.ViewState(latitude=-8.460834, longitude=119.8631577, zoom=12)

    # Render
    st.pydeck_chart(pdk.Deck(layers=[layer1, layer2, layer3], initial_view_state=view_state, 
                             tooltip={"text": "{name}\nIDR {price}\n{kategori}"},
                             map_style='mapbox://styles/mapbox/navigation-day-v1'))
    
else :
    # logic filter hotel
    if akumulasi <= 1:    
        hasil_hotel_or = hotel[(hotel['cluster_hotel']== 'King') | 
        (hotel['facility_pool']== encode2[0]) |
        (hotel['facility_wifi'] == encode2[1]) |
        (hotel['facility_breakfast'] == encode2[2]) |
        (hotel['facility_beach_access'] == encode2[3]) |
        (hotel['facility_spa'] == encode2[4])]
        data_show = hasil_hotel_or
    else:
        hasil_hotel_dan = hotel[(hotel['cluster_hotel']== 'King') & 
        (hotel['facility_pool']== encode2[0]) &
        (hotel['facility_wifi'] == encode2[1]) &
        (hotel['facility_breakfast'] == encode2[2]) &
        (hotel['facility_beach_access'] == encode2[3]) &
        (hotel['facility_spa'] == encode2[4])]
        data_show = hasil_hotel_dan
    
    # logic filter resto
    if filter_resto == 'All Category':
        hasil_resto = resto[resto['cluster_resto'] == 'King']
    else:
        hasil_resto = resto[(resto['cluster_resto'] == 'King') & (resto['kategori'] == str(filter_resto))]

    # Define a layer to display on a map
    layer1 = pdk.Layer(
            "ScatterplotLayer",
            data = data_show,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=6,
            get_position='[lon, lat]',
            get_radius=15,
            get_fill_color=[0,0,255],
        )
    layer2 = pdk.Layer(
            "ScatterplotLayer",
            data = hasil_resto,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=6,
            get_position='[lon, lat]',
            get_radius=15,
            get_fill_color=[255.0,0],
        )
    layer3 = pdk.Layer(
            "ScatterplotLayer",
            data = wisata,
            pickable=True,
            opacity=0.5,
            stroked=True,
            filled=True,
            auto_highlight=True,
            radius_scale=6,
            get_position='[lon, lat]',
            get_radius=15,
            get_fill_color=[0,128,0],
        )
    
    # Set the viewport location
    view_state = pdk.ViewState(latitude=-8.460834, longitude=119.8631577, zoom=12)

    # Render
    st.pydeck_chart(pdk.Deck(layers=[layer1, layer2, layer3], initial_view_state=view_state, 
                             tooltip={"text": "{name}\nIDR {price}\n{kategori}"},
                             map_style='mapbox://styles/mapbox/navigation-day-v1'))

# legend map
col1, col2, col3 = st.columns(3)
with col1:
    st.write("🔵 : Hotel")
with col2:
    st.write("🔴 : Restaurant")
with col3:
    st.write("🟢 : Tourist Attraction")
   
st.markdown("---")

# show image hotel
st.subheader("Top Recommendation Hotel")
show_hotel = data_show.sort_values('overall_score', ascending = False).head(3)
show_hotel = show_hotel.reset_index(drop = True)

col1, col2, col3 = st.columns(3)
if show_hotel.shape[0] == 0:
    st.write('Sorry there is no recommendation Hotel with your preferences 😥')
elif show_hotel.shape[0] == 1:
    with col1:
        st.image(show_hotel['image'][0])
        st.write( show_hotel['name'][0])
        st.write("IDR", str(show_hotel['price'][0]))
        st.write(show_hotel['kategori'][0])
elif show_hotel.shape[0] == 2:
    with col1:
        st.image(show_hotel['image'][0])
        st.write( show_hotel['name'][0])
        st.write("IDR", str(show_hotel['price'][0]))
        st.write(show_hotel['kategori'][0])
    with col2:
        st.image(show_hotel['image'][1])
        st.write(show_hotel['name'][1])
        st.write("IDR", str(show_hotel['price'][1]))
        st.write(show_hotel['kategori'][1])
elif show_hotel.shape[0] == 3:
    with col1:
        st.image(show_hotel['image'][0])
        st.write( show_hotel['name'][0])
        st.write("IDR", str(show_hotel['price'][0]))
        st.write(show_hotel['kategori'][0])
    with col2:
        st.image(show_hotel['image'][1])
        st.write(show_hotel['name'][1])
        st.write("IDR", str(show_hotel['price'][1]))
        st.write(show_hotel['kategori'][1])
    with col3:
        st.image(show_hotel['image'][2])
        st.write(show_hotel['name'][2])
        st.write("IDR", str(show_hotel['price'][2]))
        st.write(show_hotel['kategori'][2])

st.markdown("---")

# show image resto
st.subheader("Top Recommendation Restaurant")
show_resto = hasil_resto.sort_values('overall_score', ascending = False).head(3)
show_resto = show_resto.reset_index(drop = True)

col1, col2, col3 = st.columns(3)
if show_resto.shape[0] == 0:
    st.write('Sorry there is no recommendation Restaurant with your preferences 😥')
elif show_resto.shape[0] == 1:
    with col1:
        st.image(show_resto['image'][0])
        st.write( show_resto['name'][0])
        st.write("IDR", str(show_resto['price'][0]))
        st.write(show_resto['kategori'][0])
elif show_resto.shape[0] == 2:
    with col1:
        st.image(show_resto['image'][0])
        st.write( show_resto['name'][0])
        st.write("IDR", str(show_resto['price'][0]))
        st.write(show_resto['kategori'][0])
    with col2:
        st.image(show_resto['image'][1])
        st.write(show_resto['name'][1])
        st.write("IDR", str(show_resto['price'][1]))
        st.write(show_resto['kategori'][1])
elif show_resto.shape[0] == 3:
    with col1:
        st.image(show_resto['image'][0])
        st.write( show_resto['name'][0])
        st.write("IDR", str(show_resto['price'][0]))
        st.write(show_resto['kategori'][0])
    with col2:
        st.image(show_resto['image'][1])
        st.write(show_resto['name'][1])
        st.write("IDR", str(show_resto['price'][1]))
        st.write(show_resto['kategori'][1])
    with col3:
        st.image(show_resto['image'][2])
        st.write(show_resto['name'][2])
        st.write("IDR", str(show_resto['price'][2]))
        st.write(show_resto['kategori'][2])
        
st.markdown("---")
 
# show image wisata
st.subheader("Top Recommendation Tourist Attrraction")
show_wisata = wisata.sort_values('review',ascending = False).head(3)
show_wisata = show_wisata.reset_index(drop = True)

col1, col2, col3 = st.columns(3)
with col1:
    st.image(show_wisata['image'][0])
    st.write(show_wisata['name'][0])
    st.write(show_wisata['kategori'][0])
    with st.expander("See Comment"):
        st.write(show_wisata['review_comment'][0])
with col2:
    st.image(show_wisata['image'][1])
    st.write(show_wisata['name'][1])
    st.write(show_wisata['kategori'][1])
    with st.expander("See Comment"):
        st.write(show_wisata['review_comment'][1])
with col3:
    st.image(show_wisata['image'][2])
    st.write(show_wisata['name'][2])
    st.write(show_wisata['kategori'][2])
    with st.expander("See Comment"):
        st.write(show_wisata['review_comment'][2])
        
# chatbot help
col1, col2, col3 = st.columns(3)
with col1:
    st.write("")
with col2:
    st.write("")
with col3:
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    st.markdown("##")
    st.subheader("Need more help?")
    if st.button('🤖 Customer help with GoBot!'):
        js = "window.open('https://t.me/Lost_GoBot')"
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)