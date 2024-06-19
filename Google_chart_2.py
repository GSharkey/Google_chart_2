import streamlit as st
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def main():
    st.title('Google Trends')

    # 메뉴 선택
    menu = st.sidebar.selectbox('메뉴', ['키워드 검색', '나라별 트렌드'])

    if menu == '키워드 검색':
        st.title('키워드 검색')

        # 국가 선택
        countries = ['South Korea', 'United States', 'Japan']
        selected_country = st.selectbox('Select Country', countries)

        # 키워드 입력
        keywords = st.text_input('Enter Keywords (separated by commas)', 'chatgpt, openai, dall-e')
        keyword_list = [x.strip() for x in keywords.split(',')]

        # 날짜 범위 선택 기능 추가
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
        end_date = st.date_input("End Date", datetime.now())

        try:
            # Google Trends 데이터 가져오기
            pytrends = TrendReq(hl='ko-KR', tz=540)
            if selected_country == 'South Korea':
                pytrends.build_payload(keyword_list, geo='KR', timeframe=f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}")
            elif selected_country == 'United States':
                pytrends.build_payload(keyword_list, geo='US', timeframe=f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}")
            elif selected_country == 'Japan':
                pytrends.build_payload(keyword_list, geo='JP', timeframe=f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}")
            df = pytrends.interest_over_time()

            # 그래프 출력
            st.line_chart(df)
        except Exception as e:
            st.error(f"Error occurred while fetching keyword data: {str(e)}")

    elif menu == '나라별 트렌드':
        st.title('나라별 트렌드')

        # 키워드 입력
        keyword = st.text_input('Enter Keyword', 'chatgpt')

        try:
            # Google Trends 데이터 가져오기
            pytrends = TrendReq(hl='ko-KR', tz=540)
            kw_list = [keyword]
            pytrends.build_payload(kw_list)

            # 지역별 트렌드 지수 가져오기
            df = pytrends.interest_by_region(
                resolution='COUNTRY',
                inc_low_vol=True,
                inc_geo_code=True
            )

            # Streamlit 앱 화면 구성
            st.title(f"{keyword} Trends by Region")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error occurred while fetching regional trend data: {str(e)}")

if __name__ == '__main__':
    main()
