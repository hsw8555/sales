import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# 한글 폰트 설정 (Colab에 설치된 나눔바른고딕 사용)
try:
    fm.fontManager.addfont('/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf')
    plt.rc('font', family='NanumBarunGothic')
except:
    pass
plt.rcParams['axes.unicode_minus'] = False

# 페이지 설정
st.set_page_config(page_title="지점별 매출 분석 대시보드", layout="wide")

# 데이터 로드 캐싱
@st.cache_data
def load_data():
    # 실제 환경에 맞게 경로를 조정하여 데이터를 로드합니다.
    df = pd.read_excel("https://github.com/hsw8555/sales/blob/main/Sales.xlsx?raw=true")
    df.dropna(inplace=True)
    return df

try:
    df = load_data()

    st.title("🏪 지점별 매출 분석 대시보드")
    st.markdown("---")

    # 사이드바 필터
    st.sidebar.header("필터 설정")
    selected_branch = st.sidebar.multiselect(
        "분석할 지점 선택",
        options=df['Branch'].unique(),
        default=df['Branch'].unique()
    )

    # 데이터 필터링
    filtered_df = df[df['Branch'].isin(selected_branch)]

    # 주요 지표 (KPIs)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("선택된 지점 총 매출액", f"${filtered_df['Total'].sum():,.2f}")
    with col2:
        st.metric("평균 매출액", f"${filtered_df['Total'].mean():,.2f}")
    with col3:
        st.metric("총 거래 건수", f"{len(filtered_df):,} 건")

    st.markdown("---")

    # 시각화 레이아웃
    plot_col1, plot_col2 = st.columns(2)

    with plot_col1:
        st.subheader("📍 지점별 평균 매출 비교")
        branch_mean = filtered_df.groupby('Branch')['Total'].mean().reset_index()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x='Branch', y='Total', data=branch_mean, palette='Set1', ax=ax)
        ax.set_ylabel("평균 매출 (Total)")
        st.pyplot(fig)

    with plot_col2:
        st.subheader("🕒 시간대별 매출 분포 (BoxPlot)")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(x='Time_cat', y='Total', hue='Branch', data=filtered_df, palette='Set2', ax=ax)
        ax.set_ylabel("매출액")
        st.pyplot(fig)

    st.subheader("🛍️ 카테고리(Product line)별 지점 매출 비교")
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.boxplot(x='Product line', y='Total', hue='Branch', data=filtered_df, palette='pastel', ax=ax)
    plt.xticks(rotation=15)
    st.pyplot(fig)

    # 데이터 테이블 보기
    if st.checkbox("상세 데이터 보기"):
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"데이터를 로드하는 중 오류가 발생했습니다: {e}")
