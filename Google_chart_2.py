import streamlit as st
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def main():
    st.title('Google Trends')

    # 메뉴 선택
    menu = st.sidebar.selectbox('메뉴', ['인기 검색어', '키워드 검색'])

    if menu == '인기 검색어':
        st.title('나라별 인기 검색어')

        # Google Trends API 객체 생성
        pytrends = TrendReq(hl='ko-KR', tz=540)

        # 지역 선택 기능 추가
        locations = ['south_korea', 'united_states', 'japan']
        selected_location = st.selectbox("Choose a region", locations)

        try:
            # 선택한 지역과 날짜 범위의 인기 검색어 데이터 가져오기
            kw_list = []
            pytrends.build_payload(kw_list, geo=selected_location)
            df = pytrends.trending_searches()

            # Streamlit 앱 화면 구성
            st.title(f"{selected_location.replace('_', ' ').title()} Trending Searches")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error occurred while fetching trending searches: {str(e)}")

    elif menu == '키워드 검색':
        st.title('키워드 검색')

        # 국가 선택
        countries = ['South Korea', 'United States', 'Japan', 'China']
        selected_country = st.selectbox('Select Country', countries)

        # 키워드 입력
        keyword = st.text_input('Enter Keyword', 'chatgpt')

        # 날짜 범위 선택 기능 추가
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
        end_date = st.date_input("End Date", datetime.now())

        try:
            # Google Trends 데이터 가져오기
            pytrends = TrendReq(hl='ko-KR', tz=540)
            kw_list = [keyword]
            if selected_country == 'South Korea':
                pytrends.build_payload(kw_list, geo='KR', timeframe=f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}")
            elif selected_country == 'United States':
                pytrends.build_payload(kw_list, geo='US', timeframe=f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}")
            elif selected_country == 'Japan':
                pytrends.build_payload(kw_list, geo='JP', timeframe=f"{start_date.strftime('%Y-%m-%d')} {end_date.strftime('%Y-%m-%d')}")
            df = pytrends.interest_over_time()

            # 그래프 출력
            st.line_chart(df)
        except Exception as e:
            st.error(f"Error occurred while fetching keyword data: {str(e)}")

if __name__ == '__main__':
    main()
