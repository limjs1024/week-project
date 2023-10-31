#필요한 모듈 import
import pandas as pd
import streamlit as st
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import plotly.express as px
from PIL import Image
import streamlit.components.v1 as components
st.set_page_config(
    page_title='서울시 개인형이동장치(PM) 대시보드',
    page_icon=':scooter:',
    layout = 'wide',
    menu_items= {
        # 'Get Help' : 'https//www.naver.com',
        'About' : '서울시 개인형이동장치(PM) 사고율 및 '
                  '견인 현황을 알아 보기 위한 대시보드입니다.'
                   '(작성자: 임준성)'
    },
    initial_sidebar_state= 'collapsed',#collapsed #expanded
    # bg_color="#f0f8ff"
)
two = pd.read_csv('./data/tow1.csv')
#사용할 이미지를 저장 및 사이즈 재설정
three = Image.open("./data/three.png").resize((20,20))
ban = Image.open("./data/ban.png").resize((20,20))
bus = Image.open("./data/bus.png").resize((20,20))
eye = Image.open("./data/eye.png").resize((20,20))
road = Image.open("./data/road.png").resize((20,20))
train = Image.open("./data/train.png").resize((20,20))
#견인 현황 페이지 타이틀 및 캡션 추가
st.title('서울시 개인형이동장치(PM) 견인 현황')
st.caption('서울시에서 개인형이동장치(PM)가 견인된 시점부터의 견인 장소를 제공하는 페이지입니다.')
#구분선 추가
st.markdown('***')
st.header('서울시 견인구역 시각화')
st.caption('(개인형이동장치(PM) 실제 견인 구역만 표시되었으니, 사용시 참고 부탁드립니다.)')
imog = st.checkbox('아이콘 설명')
cols = st.columns([1,1.7,1])
if imog:
    cols[0].markdown(':red[그 외 주차 금지 구역](주정차 금지구역)')
    cols[0].image(ban)
    cols[0].markdown(':orange[버스정류소 전면 5M]')
    cols[0].image(bus)
    cols[1].markdown(':green[보행자와 차량이 분리된 차도 및 자전거도로]')
    cols[1].image(road)
    cols[1].markdown(':black[점자블럭 및 교통섬 위]')
    cols[1].image(eye)
    cols[2].markdown(':blue[지하철역 출구 전면 5M]')
    cols[2].image(train)
    cols[2].markdown(':puple[횡단보도 전후 3m]')
    cols[2].image(three)
    cols[0].markdown(
        '[견인제도 자세히보기](https://mediahub.seoul.go.kr/archives/2004079)')
HtmlFile = open("./data/견인구역 시각화.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
print(source_code)
components.html(source_code,height = 600)
st.header('종합 서울시 유형별 사고 현황 그래프')
tow2 = two[['번호','유형']]
two3 = pd.pivot_table(tow2, values='번호', index=['유형'],
                    aggfunc={'유형':'count'})
two4 = px.bar(two3,x = two3.index,y='유형',title =  '서울시 견인 구역에 따른 개인형 이동장치 견인 건수',
              labels={'index':'사고 유형','유형':'사고 건수'})
st.plotly_chart(two4)