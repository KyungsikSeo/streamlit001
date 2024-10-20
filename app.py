import plotly.graph_objects as go
import pandas as pd
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

def main():
    st.title("주식 데이터")
    st.sidebar.title("Stock Chart")
    ticker = st.sidebar.text_input("Enter a ticker (e. g. AAPL)", value = "AAPL")
    st.sidebar.markdown('Tickers Link : [All Stock Symbols](https://stockanalysis.com/stocks/)')
    start_date = st.sidebar.date_input("시작 날짜: ", value = pd.to_datetime("2023-01-01"))
    end_date = st.sidebar.date_input("종료 날짜: ", value = pd.to_datetime("2023-07-28"))

	#ticker 종목의 시작~종료 날짜 사이의 가격변화를 데이터로 보여줌
    data = yf.download(ticker, start= start_date, end= end_date)
    st.dataframe(data)

     #Line Chart, Candle Stick 선택형으로 만들기
    chart_type = st.sidebar.radio("Select Chart Type", ("Candle_Stick", "Line"))
    candlestick = go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'])
    line = go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close')

    if chart_type == "Candle_Stick":
        fig = go.Figure(candlestick)
    elif chart_type == "Line":
        fig = go.Figure(line)
    else:
        st.error("error")

    fig.update_layout(title=f"{ticker} Stock {chart_type} Chart", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig)
    st.markdown("<hr>", unsafe_allow_html=True)	#구분선 추가
   
   #숫자를 넣을 수 있는 영역 생성
    num_row = st.sidebar.number_input("Number of Rows", min_value= 1, max_value=len(data))
    
    #최근 날짜부터 결과값 보여줌
    st.dataframe(data[-num_row:].reset_index().sort_index(ascending = False).set_index("Date"))
        #방법1
    value1 = st.sidebar.slider('숫자 선택(1)', 0, 100)
    st.sidebar.write(value1)

    data = pd.DataFrame({
    'latitude': [37.7749, 34.0522, 40.7128],
    'longitude': [-122.4194, -118.2437, -74.0060]
    })
    st.map(data, zoom=10)

    
    
if __name__ == "__main__":
    main()