#필요한 모듈 import
import streamlit as st
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import re
import plotly.graph_objs as go
import plotly.express as px
from tkinter.tix import COLUMN
from pyparsing import empty

# 페이지 기본 설정
st.set_page_config(
    page_title='서울시 개인형이동장치(PM) 대시보드',
    page_icon=':scooter:',
    layout = 'wide',
    menu_items= {
        # 'Get Help' : 'https//www.naver.com',
        'About' : '서울시 개인형이동장치(PM) 사고율 및 '
                  '견인 현황을 알아 보기 위한 대시보드입니다.'
                    '(작성자: 최윤하)'
    },
    initial_sidebar_state= 'collapsed',#collapsed #expanded
    # bg_color="#f0f8ff"
)

#사용할 데이터를 read.csv()로 불러옴
month_total = pd.read_csv("./data/month_total.csv")
day_total = pd.read_csv("./data/day_total.csv")
year_total = pd.read_csv("./data/year_total.csv")
result = pd.read_csv("./data/result.csv")
PM_total = pd.read_csv("./data/PM_total.csv")

#서울시 사고 현황 페이지 타이틀 및 캡션 작성
st.title('서울시 개인형이동장치(PM) 사고 현황')
st.caption('2017년 ~ 2021년 년도별 서울시 개인형이동장치(PM)의 사고 현황을 나타내는 페이지입니다.')

#구분선 추가
st.markdown('***')


#####1. 월별 그래프 출력#####

#월별 그래프 헤더 설정
st.header('서울시 월별 사고 현황')
#헤더 하위에 캡션 입력
st.caption(' : 해당 그래프는 2017년 ~ 2021년 년도별 서울시 개인형이동장치(PM)의 월별 사고 건수를 나타내는 그래프입니다.')

# 불러온 데이터 프레임 컬럼명 수정
month_total.rename(columns = {'Unnamed: 0': '월별'}, inplace=True)

#년도에 따른 월별 라인 차트를 2017년 ~ 2021년까지 생성
fig = go.Figure()

fig.add_trace(go.Scatter(x=month_total['월별'], y=month_total['2017년'], name='2017년'))
fig.add_trace(go.Scatter(x=month_total['월별'], y=month_total['2018년'], name='2018년'))
fig.add_trace(go.Scatter(x=month_total['월별'], y=month_total['2019년'], name='2019년'))
fig.add_trace(go.Scatter(x=month_total['월별'], y=month_total['2020년'], name='2020년'))
fig.add_trace(go.Scatter(x=month_total['월별'], y=month_total['2021년'], name='2021년'))

#생성한 차트의 유형, x축 제목, y축 제목, 크기 설정
fig.update_layout(title='Line Chart', xaxis_title='월별', yaxis_title='사고건수',
                  width=800, height=600)

#차트 출력
st.plotly_chart(fig)

#####2. 요일별 그래프 출력#####

#요일별 그래프 헤더 설정
st.header('서울시 요일별 사고 현황')
#헤더 하위에 캡션 입력
st.caption(' : 해당 그래프는 2017년 ~ 2021년 년도별 서울시 개인형이동장치(PM)의 요일별 사고 건수를 나타내는 그래프입니다.')

# 불러온 데이터 프레임 컬럼명 수정
day_total.rename(columns = {'Unnamed: 0': '요일'}, inplace=True)

#년도에 따른 요일별 누적 막대 그래프 생성(x축 = 요일, y축 = 사고건수로 설정하고 막대 형식을 'stack(누적)'으로 설정)
fig = px.bar(day_total, x='요일', y=['2017년', '2018년', '2019년','2020년','2021년'], barmode='stack')
#생성한 차트의 유형, x축 제목, y축 제목, 크기 설정
fig.update_layout(title='Stacked Bar Chart', yaxis_title="사고건수", height=600, width=800)
#생성한 차트의 바깥쪽에 차트에 해당하는 값이 표시되도록 설정
fig.update_traces(texttemplate='%{y}', textposition='outside')

# 그래프 출력
st.plotly_chart(fig)


#####3. 히트맵 그래프 출력#####

#시간별 그래프 헤더 설정
st.header('서울시 시간별 사고 현황')
#헤더 하위에 캡션 입력
st.caption(' : 해당 그래프는 2017년 ~ 2021년 년도별 서울시 개인형이동장치(PM)의 시간별 사고 건수를 나타내는 그래프입니다.')

# 불러온 데이터 프레임 컬럼명 수정 및 인덱스를 특정 컬럼으로 설정
year_total.rename(columns = {'Unnamed: 0': '시간'}, inplace=True)
year_total = year_total.set_index('시간')

#년도에 따른 시간별 히트맵 생성
fig = px.imshow(year_total, text_auto=True)
#생성한 차트의 유형, x축 제목, y축 제목, 크기 설정
fig.update_layout(title='Heat Map', xaxis_title="년도", height=600, width=800)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)

#####4. 보호구 그래프 출력#####

#보호구 착용 여부에 따른 그래프 헤더 설정
st.header('서울시 보호구 착용 여부에 따른 사고 현황')
#헤더 하위에 캡션 입력
st.caption(' : 해당 그래프는 2017년 ~ 2021년간의 종합 데이터로,'
           '  보호구 착용 여부에 따른 서울시 개인형이동장치(PM)의 사망자/부상자의 수를 나타내는 그래프입니다.')

# 불러온 데이터 프레임 컬럼명 수정
result.rename(columns = {'Unnamed: 0': '사망/부상'}, inplace=True)
result1 = result.T
result1 = result1.rename(columns=result1.iloc[0])
result1 = result1.drop(result1.index[0])
result1.reset_index(inplace=True)

#하나의 그래프에 수직 막대그래프로로 나누어 그리기(보호구 착용/미착용 유형별)
fig = go.Figure()

# 보호구 착용에 따른 사망자/부상자 막대그래프 추가
fig.add_trace(go.Bar(
    x=['보호구 착용'],
    y=[result.iloc[0, 1]],
    name='사망자',
    marker_color='crimson'))
fig.add_trace(go.Bar(
    x=['보호구 착용'],
    y=[result.iloc[1, 1]],
    name='부상자',
    marker_color='lightsalmon'))
# 보호구 미착용에 따른 사망자/부상자 막대그래프 추가
fig.add_trace(go.Bar(
    x=['보호구 미착용'],
    y=[result.iloc[0, 2]],
    name='사망자',
    marker_color='royalblue'))
fig.add_trace(go.Bar(
    x=['보호구 미착용'],
    y=[result.iloc[1, 2]],
    name='부상자',
    marker_color='lightblue'))
# 그래프의 타이틀, x축, y축, barmode를 그룹, 그래프 사이즈 설정
fig.update_layout(
    title='Bar Chart',
    xaxis_title='보호구 착용 여부',
    yaxis_title='인원 수',
    barmode='group',
    width=800, height=600)

#생성한 차트의 바깥쪽에 차트에 해당하는 값이 표시되도록 설정
fig.update_traces(texttemplate='%{y}', textposition='outside')

#그래프 출력
st.plotly_chart(fig)

#####5. 구별 그래프 출력#####

#서울시 구별 사고현황 그래프 헤더 설정
st.header('서울시 구별 사고현황')
#헤더 하위에 캡션 입력
st.caption(' : 해당 그래프는 2017년 ~ 2021년간 종합한 서울시 자치구별 개인형이동장치(PM)의 사고율을 나타내는 그래프입니다.')

#종합 년도에 따른 자치구별 파이 차트 생성
PM = px.pie(PM_total, values='PM총합', names='자치구별')
#그래프의 타이틀, 그래프 사이즈 설정
PM.update_layout(title='Pie Chart', width=800, height=600)
#그래프 출력
st.plotly_chart(PM)

