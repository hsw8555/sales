import streamlit as st
import pandas as pd
import numpy as np

# 웹 페이지 기본 설정
st.set_page_config(page_title="우리반 데이터 대시보드", layout="wide")

st.title('🚀 학생들과 함께하는 데이터 대시보드')
st.write('Colab에서 데이터를 분석하고 Streamlit으로 구현한 예제입니다.')

# 1. 가상의 데이터 생성 (실제 수업에서는 GitHub이나 Drive 데이터를 불러옵니다)
@st.cache_data
def load_data():
    df = pd.DataFrame({
        '학생이름': ['학생A', '학생B', '학생C', '학생D', '학생E'],
        '파이썬': np.random.randint(70, 100, 5),
        '데이터분석': np.random.randint(70, 100, 5),
    })
    return df

data = load_data()

# 2. 화면 분할 (좌측: 데이터표, 우측: 차트)
col1, col2 = st.columns(2)

with col1:
    st.subheader('📊 성적 데이터')
    st.dataframe(data, use_container_width=True)

with col2:
    st.subheader('📈 인터랙티브 차트')
    # 셀렉트박스로 과목 선택
    subject = st.selectbox('조회할 과목을 선택하세요', ['파이썬', '데이터분석'])
    # 선택된 과목으로 바 차트 그리기
    st.bar_chart(data.set_index('학생이름')[subject])
