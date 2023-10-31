#필요한 모듈 import
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# 페이지 기본 설정
st.set_page_config(
    page_title='서울시 개인형이동장치(PM) 대시보드',
    page_icon=':scooter:',
    layout = 'wide',
    menu_items= {
        # 'Get Help' : 'https//www.naver.com',
        'About' : '서울시 개인형이동장치(PM) 사고율 및 '
                  '견인 현황을 알아 보기 위한 대시보드입니다.'
                  '(작성자: 고민주)'
    },
    initial_sidebar_state= 'collapsed',#collapsed #expanded
    # bg_color="#f0f8ff"
)

#자치구별 사고 현황 헤더 설정
st.title('서울시 자치구별 개인형이동장치(PM) 사고 현황')
#헤더 하위에 캡션 입력
st.caption('2018년 ~ 2021년간 종합한 서울시 개인형이동장치(PM)의 자치구별 사고 현황을 나타내는 페이지입니다.')

##### 날씨 조회 함수 #####
now = datetime.datetime.now()
base_date = now.date().strftime("%Y%m%d")
base_time = now.time().strftime("%H%M")

#사용할 데이터를 read.csv()로 불러옴
xy = pd.read_csv("./data/기상청제공위경도.csv")
def weather_now(gu):
    key = 'POt4cCBFEG6ttsuSzsLdyQDtxAjMUVHZvy40cGESFGdxUv7ggP7qGYhXb8lpgM9epQZi8RZ7ZFgxWBDvulRAzA=='
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'

    x = xy[xy['구'] == gu].x
    y = xy[xy['구'] == gu].y
    now = datetime.datetime.now()
    base_date = now.date().strftime("%Y%m%d")
    base_time = (now - datetime.timedelta(hours=1)).strftime("%H%M")

    params = {'ServiceKey': key,
              'numOfRows': 1000,
              'pageNo': 1,
              'base_date': base_date,
              'base_time': base_time,
              'nx': x,
              'ny': y}

    res = requests.get(url, params=params)
    soup = BeautifulSoup(res.text, 'xml')
    items = soup.findAll('item')

    cols = ['baseDate', 'baseTime', 'category', 'fcstDate', 'fcstTime', 'fcstValue', 'nx', 'ny']
    dict_list = []
    for item in items:
        dict = {}
        for col in cols:
            dict[col] = item.find(col).text
        dict_list.append(dict)

    df = pd.DataFrame(dict_list, columns=cols)
    sky = df[df['category'] == 'SKY'].iloc[0].fcstValue
    pty = df[df['category'] == 'PTY'].iloc[0].fcstValue

    if (pty == '1') | (pty == '5'):
        weather = ['비', '']
    elif (pty == '3') | (pty == '7'):
        weather = ['눈', '']
    elif (pty == '2') | (pty == '6'):
        weather = ['눈', '비']
    elif (sky == '1') & (pty == '0'):
        weather = ['맑음', '']
    elif ((sky == '3') & (pty == '0')) | ((sky == '4') & (pty == '0')):
        weather = ['흐림', '']

    return weather

weather_data = pd.read_csv("./data/기상상태별 교통사고 전처리 데이터.csv", encoding='cp949')
def weather_acd(gu):
    weather = weather_now(gu)
    cnt = []
    for w in weather:
        cnt1 = 0
        for i in range(len(weather_data)):
            if (weather_data.iloc[i]['지자체'] == gu) & (weather_data.iloc[i]['기상상태'] == w):
                cnt.append(weather_data.iloc[i]['발생건수'])
            else:
                continue

    # 구별 사고건수 총합
    total_gu = weather_data[weather_data['지자체'] == gu].발생건수.sum()
    # 사고율
    acd_rate = cnt / total_gu * 100

    w_dic = {}
    if weather[1] == '':
        w_dic[weather[0]] = round(acd_rate[0], 2)
    else:
        w_dic[weather[0]] = round(acd_rate[0], 2)
        w_dic[weather[1]] = round(acd_rate[1], 2)

    return w_dic

##### 유형별 사고 데이터 불러오기 함수 #####
def sex_gu(gu):
    acd1 =  pd.read_csv('./data/성별 교통사고 전처리 데이터.csv', encoding = 'cp949')
    acd1=acd1.drop('Unnamed: 0', axis=1)
    acd1 = acd1[acd1['지자체'] == gu]
    acd1=acd1.drop('지자체', axis=1)
    acd1.reset_index(drop=True, inplace=True)
    acd1 = acd1.sort_values(by=['발생건수'], ascending=False)
    return acd1

def weather(gu):
    acd1 = pd.read_csv('./data/기상상태별 교통사고 전처리 데이터.csv',encoding = 'cp949')
    acd1=acd1.drop('Unnamed: 0', axis=1)
    acd1 = acd1[acd1['지자체'] == gu]
    acd1=acd1.drop('지자체', axis=1)
    acd1.reset_index(drop=True, inplace=True)
    return acd1

def select_gu(gu):
    acd1 =  pd.read_csv('./data/위반유형별 교통사고 전처리 데이터.csv',encoding = 'cp949')
    acd1=acd1.drop('Unnamed: 0', axis=1)
    acd1 = acd1[acd1['지자체'] == gu]
    acd1=acd1.drop('지자체', axis=1)
    acd1.reset_index(drop=True, inplace=True)
    return acd1

def age_gu(gu):
    acd1 =pd.read_csv('./data/연령별 교통사고 전처리 데이터.csv',encoding = 'cp949')
    acd1=acd1.drop('Unnamed: 0', axis=1)
    acd1 = acd1[acd1['지자체'] == gu]
    acd1=acd1.drop('지자체', axis=1)
    acd1.reset_index(drop=True, inplace=True)
    return acd1

############
## 시각화 ##
############

st.markdown('***')
### 구 선택
input_gu = st.selectbox(
    '구를 선택하세요',
    (sorted(xy.구)))
# st.markdown('***')

#빈줄 추가
st.write("")
st.write("")
st.write("")



### 그래프 및 사고율
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

sunny = Image.open("./data/sun.png").resize((50, 50))
cloudy = Image.open("./data/cloudy.png").resize((50, 50))
rainy = Image.open("./data/rain.png").resize((50, 50))
snowy = Image.open("./data/snowflakes.png").resize((50, 50))

## 첫번째 행 (성별, 기상상태별)
col1, col2 = st.columns([2,2])
with col1.container():
    st.markdown(':scooter:**성별 사고발생 비중**')
    colors = {}
    colors[sex_gu('강남구').loc[0]['성별']] = '#F24472'
    colors[sex_gu('강남구').loc[1]['성별']] = '#03588C'
    colors[sex_gu('강남구').loc[2]['성별']] = '#868e96'
    fig1 = px.pie(names=sex_gu(input_gu).성별, values=sex_gu(input_gu).발생건수, color=sex_gu(input_gu).성별,
                  color_discrete_map=colors)
    fig1.update_traces(hole=.3, textposition='inside', textinfo='percent+label')
    fig1.update_layout(margin_t=10, width=300, height=300)
    st.plotly_chart(fig1)

with col2.container():
    st.markdown(':scooter:**기상상황별 사고발생 현황**')
    
    col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])
    # 사고율
    col1.markdown('###### 현재날씨 사고율')
    if '맑음' in weather_acd(input_gu):
        col2.image(sunny)
        col3.subheader(f' {weather_acd(input_gu)["맑음"]}%')
    elif '흐림' in weather_acd(input_gu):
        col2.image(cloudy)
        col3.subheader(f' {weather_acd(input_gu)["흐림"]}%')
    elif len(weather_acd(input_gu)) == 2:
        col2.image(snowy)
        col3.subheader(f' {weather_acd(input_gu)["눈"]}%')
        col4.image(rainy)
        col5.subheader(f' {weather_acd(input_gu)["비"]}%')
    elif '비' in weather_acd(input_gu):
        col2.image(rainy)
        col3.subheader(f' {weather_acd(input_gu)["비"]}%')
    elif '눈' in weather_acd(input_gu):
        col2.image(snowy)
        col3.subheader(f' {weather_acd(input_gu)["눈"]}%')
    
    # 그래프
    colors = ['#03588C',] * len(weather(input_gu))
    colors[weather(input_gu).발생건수.idxmax()] = '#F24472'
    data2 = go.Bar(x = weather(input_gu).기상상태, y=weather(input_gu).발생건수,
            text=weather(input_gu).발생건수,
            marker={'color':colors}
    )
    layout2 = go.Layout(autosize=False, width=300, height=250, margin=dict(t=10))
    fig2 = go.Figure(data=data2, layout=layout2)
    st.plotly_chart(fig2)

## 두번째 행 (위반유형별, 연령대별)
col1, col2 = st.columns([2,2])
with col1.container():
    st.markdown(':scooter:**위반유형별 사고발생 건수**')
    colors = ['#03588C',] * len(select_gu(input_gu))
    colors[select_gu(input_gu).발생건수.idxmax()] = '#F24472'
    data3 = go.Bar(x = select_gu(input_gu).위반유형, y=select_gu(input_gu).발생건수,
            text=select_gu(input_gu).발생건수,
            width=[0.7,] * len(age_gu(input_gu)),
            marker={'color':colors}
    )
    layout3 = go.Layout(autosize=False, width=300, height=300, margin=dict(t=10))
    fig3 = go.Figure(data=data3, layout=layout3)
    fig3.update_xaxes(
        tickangle=50)
    st.plotly_chart(fig3)

with col2.container():
    st.markdown(':scooter:**연령별 사고발생 건수**')
    colors = ['#03588C',] * len(age_gu(input_gu))
    colors[age_gu(input_gu).발생건수.idxmax()] = '#F24472'
    data4 = go.Bar(x = age_gu(input_gu).연령대, y=age_gu(input_gu).발생건수,
            text=age_gu(input_gu).발생건수,
            width=[0.7,]*len(age_gu(input_gu)),
            marker={'color':colors},
    )
    layout4 = go.Layout(autosize=False, width=300, height=300, margin=dict(t=10))
    fig4 = go.Figure(data=data4, layout=layout4)
    st.plotly_chart(fig4)
