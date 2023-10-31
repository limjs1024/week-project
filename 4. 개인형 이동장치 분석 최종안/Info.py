import streamlit as st
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import base64
from PIL import Image
import textwrap

# 페이지 기본 설정
st.set_page_config(
    page_title='서울시 개인형이동장치(PM) 대시보드',
    page_icon=':scooter:',
    layout = 'wide',
    menu_items= {
        # 'Get Help' : 'https//www.naver.com',
        'About' : '서울시 개인형이동장치(PM) 사고율 및 견인 현황을 알아 보기 위한 대시보드입니다. (작성자: 고민주, 임준성, 최윤하)'
    },
    initial_sidebar_state= 'collapsed',#collapsed #expanded
    # bg_color="#f0f8ff"
)

##### 1. 대시보드 이미지(Images) 삽입
bg_image = Image.open("./data/PM2.jpg")
bg_image.putalpha(alpha= 150)#alpha는 0(완전 투명)부터 255(완전 불투명) 사이의 값
# resized_image = bg_image.resize((500, 700))# 이미지 크기 조절
st.image(bg_image , use_column_width=True) #caption="이미지 설명"

##### 2. 대시보드 헤더(Header) 설정
st.title("About Dashboard")

# 대시보드 헤더(Header)에 내용 입력
st.write("""
안녕하세요, 서울시 개인형이동장치(PM) 대시보드에 방문하신 것을 환영합니다.

개인형이동장치(PM)는 전동킥보드 등 전기를 동력으로 하는 1인용 교통수단으로,

단거리 통행 시 짧은 시간 내 이동이 가능하고 크기가 작아 휴대하기 용이하며

친환경성, 경제성, 편리성 등 다양한 장점을 내세워 최근들어 꾸준히 수요가 늘어나고 있습니다.

그러나, 개인형이동장치(PM)의 보급이 증가함에 따라 사고율 또한 나날이 증가하는 상황입니다.

**따라서, 다음의 대시보드에서는 서울시 내 개인형이동장치(PM)의 사고 현황 및 견인 현황을**

**제공하여 서울 시민들이 보다 안전하게 교통수단을 이용함에 도움이 되고자 합니다.**

""")

#페이지 빈줄 추가
st.write("")
st.write("")

##### 3. 체크 박스를 이용하여 서울시 선정 이유 선택할 수 있도록 설정
why = st.checkbox('서울시 선정 이유가 궁금하신가요?')
if why:
    st.markdown("""
    <div style='border: 0.5px solid #aaaaaa; background-color: #F5F5F5; padding:10px; border-radius: 3px'>
        <p style="text-align: left; "font-size: 8px;"><br>
        개인형이동수단(PM)으로 인한 교통사고 건수와 사망자가 최근 5년새 크게 증가한 것으로 나타났으며,<br>
        개인형이동수단(PM) 교통사고는 2017년 117건에서 2021년 1735건으로 10배 이상 늘어나는 추이를 보이고 있습니다.<br><br>
        특히, 전국에서 가장 사고가 빈번한 지역 8곳 확인 시<br>
        : 강남역사거리, 신사역사거리, 선릉역, 강남구청역 남쪽, 언주역 동쪽 등 서울시가 주를 이루었습니다.<br><br>
        따라서, 해당 대시보드에서는 지역을 서울시로 한정하여 정보를 제공하고 있습니다.</p>
        <p style="text-align: right; "font-size: 5px;"> <a href="https://www.sedaily.com/NewsView/26B75ZUAC6">출처: 서울경제</p>
    </div>
    """, unsafe_allow_html=True)  # <p>태그를 이용하여 문단을 나누어 작성하고, text 위치, size 및 하이퍼링크를 설정

#페이지 구분선 추가
st.markdown('***')

##### 4. Dashboar 소개 타이틀 작성
st.markdown('## Dashboard 소개')
# 접기/펼치기 가능한 상자 생성
#상자1. 서울시 개인형이동장치 사고 현황 소개
with st.expander("서울시 개인형이동장치(PM) 사고 현황"):
    st.write("해당 대시보드에서는 **서울시 전체 개인형이동장치(PM)의 사고 현황**을 확인할 수 있습니다.")
    st.markdown("현재는 다음과 같은 <span style='color:red'>항목별 사고 현황</span>을 제공하고 있습니다.", unsafe_allow_html=True)
    st.markdown("- 서울시 요일별 사고현황\n- 서울시 시간별 사고현황\n- 서울시 보호구 착용 여부에 따른 사고현황\n- 서울시 구별 사고현황")
#상자2. 서울시 구별 개인형이동장치 사고 현황 소개
with st.expander("서울시 구별 개인형이동장치(PM) 사고 현황"):
    st.write("해당 대시보드에서는 **서울시 자치구별 개인형이동장치(PM)의 사고 현황**을 확인할 수 있습니다.")
    st.markdown("현재는 다음과 같은 <span style='color:red'>항목별 사고 현황</span>을 제공하고 있습니다.", unsafe_allow_html=True)
    st.markdown("- 실시간 날씨 현황 \n- 자치구별 날씨별 사고현황 \n- 자치구별 성별 사고 현황\n- 자치구별 위반유형에 따른 사고현황\n- 자치구별 연령별 사고현황")
#상자3. 서울시 개인형이동장치 견인 현황 소개
with st.expander("서울시 개인형이동장치(PM) 견인 현황"):
    st.write("해당 대시보드에서는 **서울시 전체 개인형이동장치(PM)의 견인 현황**을 확인할 수 있습니다.")
    st.markdown("현재는 다음과 같은 <span style='color:red'>항목별 견인 현황</span>을 제공하고 있습니다.", unsafe_allow_html=True)
    st.markdown("- 서울시 전체 견인 구역\n- 서울시 개인형이동장치(PM) 견인 유형")
#상자4. 서울시 구별 개인형이동장치 견인 현황 소개
with st.expander("서울시 구별 개인형이동장치(PM) 견인 현황"):
    st.write("해당 대시보드에서는 **서울시 자치구별 개인형이동장치(PM)의 견인 현황**을 확인할 수 있습니다.")
    st.markdown("현재는 다음과 같은 <span style='color:red'>항목별 견인 현황</span>을 제공하고 있습니다.", unsafe_allow_html=True)
    st.markdown("- 서울시 자치구별 견인 구역\n- 서울시 자치구별 개인형이동장치(PM) 견인 유형")


