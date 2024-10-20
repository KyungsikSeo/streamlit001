# icons = ["glyphicon-cloud", "glyphicon-star", "glyphicon-home", "glyphicon-tree-conifer",
#          "glyphicon-tree-deciduous", "glyphicon-fire", "glyphicon-flash", "glyphicon-road",
#          "glyphicon-cutlery", "glyphicon-plane", "glyphicon-phone", "glyphicon-globe",
#          "glyphicon-heart", "glyphicon-info-sign", "glyphicon-exclamation-sign", 
#          "glyphicon-thumbs-up", "glyphicon-thumbs-down", "glyphicon-fullscreen", 
#          "glyphicon-screenshot", "glyphicon-cloud-upload", "glyphicon-cloud-download"]
#colors = ‘red’, ‘blue’, ‘green’, ‘purple’, ‘orange’, ‘darkred’, ’lightred’, ‘beige’, ‘darkblue’, ‘darkgreen’, ‘cadetblue’, ‘darkpurple’, ‘white’, ‘pink’, ‘lightblue’, ‘lightgreen’, ‘gray’, ‘black’, ‘lightgray’

# marker = folium.Marker(
#     [49.61068, 6.13127],
#     popup="<a href=https://fr.wikipedia.org/wiki/Place_Guillaume_II>Place Guillaume II</a>",
#     tooltip=tooltip
# )

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import folium
import openpyxl
from pyxlsb import open_workbook as open_xlsb
# 권한주기
from io import BytesIO
from xlsxwriter import Workbook

st.title('🍰먹고, 😎놀고, ✈️여행하는')
st.title(' 팅이의 탐방 지도! 👍')
st.subheader("Tingi's World Map!")
#st.subheader('원하는 조건을 선택하여 보다 쉽게 검색해봐요! 😎', anchor=None, help=None, divider=False)

info=st.info('사이드 바에서 원하는 조건을 입력하세요!',  icon='🔍')
#if ((options is not None) or (state_name_options is not None) or (town_name_options is not None )):
#    info.info(f'{options} 포함 , 시군구명: {state_name_options} 읍면동명"{town_name_options} 에 일치하는 결과를 로딩합니다')


# csv 파일, 지도 업로드 부분
data = pd.read_csv('./BusanHotelFirst.csv')
#st.write(data)
filter_data=data
last_data=filter_data
down_data=last_data

# 다운 데이터 정제 함수
def process_down_data(filter_data):
    last_data=filter_data
    down_data=last_data
    #도로명주소
    adress_roadname=last_data['도로명']+last_data['도로명상세']
    adress_roadname.fillna('',inplace=True)
    #읍면동주소
    adress=last_data['시도명']+last_data['시군구명']+last_data['읍면동명']+last_data['번지']
    adress.fillna('',inplace=True)

    last_data['일반주소']=adress
    last_data['도로명주소']=adress_roadname
    down_data=last_data[['업체명','일반주소','도로명주소','전화번호','홈페이지주소']]
    down_data.fillna('',inplace=True)

    return down_data


# 사이드바, 검색조건 설정하기
# 일단 조건별로 


def filteringMap():
    st.write(st.checkbox.__name__)

st.sidebar.title("검색 조건 사이드바")

options = st.sidebar.multiselect(
    '편의시설',
    ['휠체어 이동 가능', '점자도로이용가능', '물품보관함 이용가능', '수유실 이용 가능'])
#st.write(options)


# 검색조건별로 컬럼 엮는 딕셔너리

options_value={
    '휠체어 이동 가능':'휠체어이동가능여부',
    '점자도로이용가능':'점자유도로유무',
    '물품보관함 이용가능':'물품보관함유무',
    '수유실 이용 가능':'수유실유무'

}


state_options=data['시군구명'].unique()
state_options=np.insert(state_options,0,'전체')
town_options=data['읍면동명'].unique()
#town_options=np.insert(town_options,0,'전체')
state_name_options=st.sidebar.selectbox(
    '시군구명',
    state_options

)




# 로컬 다운시
def save_data():
    st.write('여기로옴..')

    file_name=state_name_options+'_'
    for i in town_name_options:
        file_name+=i
    st.write(file_name)
    filter_data.to_excel(
        excel_writer='C:\\'
         f'{file_name}.xlsx')


# 시군구별 읍면동명 데이터


town_groupby_state_data=data.groupby('시군구명')['읍면동명'].unique()

#st.write(town_groupby_state_data)

if(state_name_options is not None):
    if(state_name_options=='전체'):
        town_options=data['읍면동명'].unique()
    else:town_options=town_groupby_state_data[state_name_options]
    town_name_options=st.sidebar.multiselect(
     '읍면동명',
     town_options
     )



show_data_count_bar=st.sidebar.slider('추출개수',min_value=5)




# 검색조건이 있으면 그에 대응하는 칼럼으로 조건식 졸려서 map에 적용
# data->원본  filter_data -> data에 조건식 들어간거 filter data를 집어 넣기

#st.write(filter_data)
if (options is not None):

    for i in options:
        col=options_value[i]
        filter_data=filter_data[filter_data[col]=='Y']

# 시군구별 지도 필터링

if(state_name_options is not None):
    if state_name_options=='전체':
        filter_data=filter_data

    else:filter_data=filter_data[filter_data['시군구명']==state_name_options]


# 읍면동별 지도 필터링
if (len(town_name_options)!=0):
    filter_data=filter_data[filter_data['읍면동명'].isin(town_name_options)]

#df[df['country'].isin(country_list)]


# 엑셀파일로 다운받는 
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)
    writer.close()
    processed_data = output.getvalue()
    return processed_data
#df_xlsx = to_excel(process_down_data(filter_data))

if(len(filter_data)==0):
    filter_data=data

map=folium.Map(location=[filter_data['위도'].mean(),filter_data['경도'].mean()], zoom_start=10)

for n in filter_data.index:
    name=filter_data.loc[n,'업체명'] # n번 행의 상호명
    address=filter_data.loc[n,'도로명'] # n번 행의 도로명주소
    address_spc=filter_data.loc[n,'도로명상세']
   
    
    popup=folium.Popup(f'<i>{name}-{address}{address_spc}</i>', max_width=600, max_height=600) # 상호명과 도로명주소 이어붙이기
    location=[filter_data.loc[n,'위도'],filter_data.loc[n,'경도']] # n번 행의 위도, 경도
    folium.Marker(
        location=location, # 위도 경도 위치에
        popup=popup, # 상호명과 도로명 주소 popup 띄우기
        icon=folium.Icon(color='red', icon='plus', prefix='fa')
    ).add_to(map) # 마커를 지도에 추가하기
st.components.v1.html(map._repr_html_(), width=800, height=600)



#






# 필터링 끝난뒤에 현재 위경도 거리에서 거리순으로 나열하는거 필터링

data_count=len(filter_data)



    


on=st.sidebar.toggle('전체보기')
if on:
    show_data_count_bar=data_count
else:
    if show_data_count_bar>data_count:
        show_data_count_bar=data_count

# 정보 포매팅
if len(options)==0:
   options=''
   options_str=''
else:
    options_str=f'{options}'+'포함,'
if len(state_name_options)==0:
    state_name_options=''
if len(town_name_options)==0:
    town_name_options=''


options_str=f'{options}'+'포함,'
st.info(f'📜 {options_str} {state_name_options} {town_name_options} 위치의 숙박업소  {show_data_count_bar}개 의 정보를 로딩합니다.!')
st.write(filter_data.head(show_data_count_bar))

df_xlsx = to_excel(process_down_data(filter_data.head(show_data_count_bar)))

st.sidebar.download_button(label='📥 Download Current Result',
                                data=df_xlsx ,
                                file_name= 'df_test.xlsx')

# last_execl_save_data


# 마지막 사이드바
st.sidebar.header('🏖️ Naver Blog Home ↓')
st.sidebar.subheader('https://blog.naver.com/tingi40')
st.sidebar.header('✉️ Tingi e-mail')
st.sidebar.subheader('jlovemelove@naver.com')
#st.sidebar.subheader('👩🏻‍💻 GitHub : sunk-dev')