# -*- coding: utf-8 -*-
"""
Created on Sat May 28 06:45:25 2022

@author: Nayeem Badshah
"""

import cv2
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
from sqlite_db import MedDB
import tensorflow as tf
import pandas as pd
import plotly.express as px



model = tf.keras.models.load_model("med_classifier_v0.1.h5")


def matchMed1(image):
    med_classes = {0:'Calpol 650',
                1:'Cetzine',
                2:'Combiflam',
                3:'Nasivion Adult',
                4:'Pan 40'}
   
    resized = cv2.resize(image, (128, 128),
                interpolation = cv2.INTER_AREA)
    resized = resized/255.0
    resized = np.array([resized])
    i = model.predict(resized).argmax(axis=1)
    return(med_classes[i[0]])





# Using object notation
st.set_page_config(
     page_title="Self-Med Self-Help",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",     
 )

hide_streamlit_style = """
            <style>
            #MainMenu {display: none;}
            footer {display: none;}
            </style>
            """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# # Remove whitespace from the top of the page and sidebar
# st.markdown("""
#         <style>
#                .css-18e3th9 {
#                     padding-top: 0rem;
#                     padding-bottom: 10rem;
#                     padding-left: 5rem;
#                     padding-right: 5rem;
#                 }
#                .css-1d391kg {
#                     padding-top: 3.5rem;
#                     padding-right: 1rem;
#                     padding-bottom: 3.5rem;
#                     padding-left: 1rem;
#                 }
#         </style>
#         """, unsafe_allow_html=True)

st.title('Self-Med Self-Help')

side_bar_options = ["Get Medicine Info", "Your Self-Med Practices","Self-Med Analysis", "About"]

# with st.sidebar:
selected = option_menu(
    menu_title = "Main Menu",
    options = side_bar_options,
    orientation='horizontal'
)





if selected == side_bar_options[0]:
    img = st.file_uploader(
    'Select Medicine Image To Get Information about medicine.', type=['jpg', 'png'])

    if img is not None:
        file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        # med_name = matchMed(opencv_image)
        med_name = matchMed1(opencv_image)
        med_info = MedDB().findOneMed(med_name)[0]
        # print(med_info)
        st.image(opencv_image, channels="BGR", width=200)
        st.subheader('Medicine Name:')
        st.markdown(med_info[1])

        st.subheader('Medicine Manufacturer:')
        st.markdown("""
        <div style='width: 100%;text-align: justify'>
        {}
        </div>
        """.format(med_info[2]), unsafe_allow_html=True)


        st.subheader('Medicine Composition:')
        st.markdown("""
        <div style='width: 100%;text-align: justify'>
        {}
        </div>
        """.format(med_info[3]), unsafe_allow_html=True)

        st.subheader('Medicine Description:')
        st.markdown("""
        <div style='width: 100%;text-align: justify'>
        {}
        </div>
        """.format(med_info[4]), unsafe_allow_html=True)
        st.subheader('Use:')
        st.markdown("""
        <div style='width: 100%;text-align: justify'>
        {}
        </div>
        """.format(med_info[5]), unsafe_allow_html=True)
        st.subheader('Sideffects:')
        st.markdown("""
        <div style='width: 100%;text-align: justify'>
        {}
        </div>
        """.format(med_info[6]), unsafe_allow_html=True)

elif selected == side_bar_options[1]:
    st.components.v1.html(
        '<iframe width="100%" height="700px" src="https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAO__cJ569hUMTA4MlZZUzdBRDRRVDdGRkNHOUtTTFVGMi4u&embed=true" frameborder="0" marginwidth="0" marginheight="0" style="border: none; max-width:100%; max-height:100vh" allowfullscreen webkitallowfullscreen mozallowfullscreen msallowfullscreen> </iframe>',
        height=1200, scrolling=True)


elif selected == side_bar_options[2]:
    st.subheader('Survey Data Analysis')
    df = pd.read_excel('SurveyData.xlsx')

    ###############
    therapy_ana = df.therapy.str.get_dummies('|').sum()
    therapy_ana = pd.DataFrame({'Therapy': therapy_ana.index, 'Count': therapy_ana.values})
    therapy_ana['Percentage of used Therapy'] = 100 * (therapy_ana['Count'] / therapy_ana['Count'].sum()).round(2)
    therapy_ana = therapy_ana.sort_values(by=['Percentage of used Therapy'], ascending=False).head(6)

    fig = px.bar(therapy_ana, x="Therapy", y="Percentage of used Therapy", title="Therapy Practiced by Population",
                 text=therapy_ana['Percentage of used Therapy'].apply(lambda x: '{}%'.format(x)), width=700)

    fig.update_layout(
        title={
            'text': "Therapy Practiced by Population",
            'y': 0.839,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    st.plotly_chart(fig, use_container_width=True)
    ###############
    often_used_med_ana = df.often_used_med.str.get_dummies('|').sum()
    often_used_med_ana = pd.DataFrame(
        {'Often Used Medicine': often_used_med_ana.index, 'Count': often_used_med_ana.values})
    often_used_med_ana['Percentage of Used Medicine'] = 100 * (
                often_used_med_ana['Count'] / often_used_med_ana['Count'].sum())
    often_used_med_ana = often_used_med_ana.sort_values(by=['Percentage of Used Medicine'], ascending=False).head(
        6).round(2)
    fig = px.bar(often_used_med_ana, x="Often Used Medicine", y="Percentage of Used Medicine",
                 title="Often Used Medicines",
                 text=often_used_med_ana['Percentage of Used Medicine'].apply(lambda x: '{0:1.2f}%'.format(x)),
                 width=700)
    # fig.update_traces(marker_color='black')
    fig.update_layout(
        title={
            'text': "Often Used Medicines",
            'y': 0.839,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    st.plotly_chart(fig, use_container_width=True)
    ###############
    allergy = df.allergy.str.strip()
    allergy_ana = allergy.str.get_dummies('|').sum()
    allergy_ana = pd.DataFrame({'Type of Allergy': allergy_ana.index, 'Count': allergy_ana.values})
    allergy_ana['Allergy Type Percentage'] = 100 * (allergy_ana['Count'] / allergy_ana['Count'].sum())
    allergy_ana = allergy_ana[allergy_ana['Type of Allergy'] != 'No']
    allergy_ana1 = allergy_ana.sort_values(by=['Allergy Type Percentage'], ascending=False).head(8).round(2)
    fig = px.bar(allergy_ana1, x="Type of Allergy", y="Allergy Type Percentage",
                 text=allergy_ana1['Allergy Type Percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), width=700)
    # fig.update_traces(marker_color='black')
    fig.update_layout(
        title={
            'text': "Allergy From Substances",
            'y': 0.93,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    st.plotly_chart(fig, use_container_width=True)
    #################
    self_med_info_ana = df.self_med_info.str.get_dummies('|').sum()
    self_med_info_ana = pd.DataFrame({'Medicine Info': self_med_info_ana.index, 'Count': self_med_info_ana.values})
    self_med_info_ana['Info Type Percentage'] = 100 * (self_med_info_ana['Count'] / self_med_info_ana['Count'].sum())
    self_med_info_ana = self_med_info_ana.sort_values(by=['Info Type Percentage'], ascending=False).head(8).round(2)

    fig = px.bar(self_med_info_ana, x="Medicine Info", y="Info Type Percentage", title="Medicine Info Analysis",
                 text=self_med_info_ana['Info Type Percentage'].apply(lambda x: '{0:1.2f}%'.format(x)), width=800)
    # fig.update_traces(marker_color='black')
    fig.update_layout(
        title={
            'text': "Medicine Information Sources",
            'y': 0.837,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    st.plotly_chart(fig, use_container_width=True)


elif selected == side_bar_options[3]:
    st.subheader("About:")
    st.markdown("""
    <div style="text-align: justify;width: 500px;">
    People nowadays often and very often medicate themselves with or without prior knowledge of medicine. They only try to treat the symptoms without treating the actual cause and of course we are not trained to do so. But to reach out to an immediate satisfaction and cure we do it so rapidly. And thus it became sometime a hazardous thing for us. Who take some medicine during a long time once after a doctor prescribed for him, suffers a long term side effect even develop chronic disease. Without proper diagnosis they often take medicine and suffer for long time.
    </div>
    """,unsafe_allow_html=True)

    st.subheader("Aim of This Project:")
    st.markdown("""
    <div style="text-align: justify;width: 500px;">
        So, to analyze, classify the people who use self-medication very often and to aware people, we come up with an idea which can help us reach the goal.
        <ul>
            <li>Analyze the self-medication practices among Teachers and Students in the University</li>
            <li>Classification of types of chronic diseases among the people</li>
            <li>Health Statistic Assessment of the overall university</li>
            <li>Use Computer Vision to classify medicine</li>
            <li>Show classified medicine name, medicine description, usecases, sideffects to the user</li>
            <li>That information will help people to know more about the medicine</li>
        </ul>
    </div>
    """,unsafe_allow_html=True)



# with st.spinner('Wait for it...'):
#     time.sleep(5)
# st.success('Done!')





    


