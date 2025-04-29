import streamlit as st
import pandas as pd
import requests
import time

st.set_page_config(page_title="Nifty Option Chain Viewer", layout="wide")

@st.cache_data(ttl=300)  # Cache the data for 5 minutes
def fetch_nifty_data():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    session = requests.Session()
    session.headers.update(headers)
    try:
        response = session.get(url, timeout=10)
        data = response.json()
        return data
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def process_data(data):
    records = data['records']
    spot_price = float(records['underlyingValue'])

    options = records['data']
    df = pd.DataFrame([{
        'strikePrice': item['strikePrice'],
        'callVolume': item.get('CE', {}).get('totalTradedVolume', 0),
        'putVolume': item.get('PE', {}).get('totalTradedVolume', 0),
        'callChangeOI': item.get('CE', {}).get('changeinOpenInterest', 0),
        'putChangeOI': item.get('PE', {}).get('changeinOpenInterest', 0)
    } for item in options])

    df = df.sort_values('strikePrice').reset_index(drop=True)

    # Find the nearest strikes
    nearest_strike = df.iloc[(df['strikePrice']-spot_price).abs().argsort()[:1]]['strikePrice'].values[0]
    nearest_index = df.index[df['strikePrice'] == nearest_strike][0]

    lower_bound = max(nearest_index - 10, 0)
    upper_bound = min(nearest_index + 10, len(df) - 1)

    df_filtered = df.iloc[lower_bound:upper_bound+1].reset_index(drop=True)

    return spot_price, df_filtered

def main():
    st.title("Nifty Option Chain (Nearest 10 Up & Down Strikes)")
    st.caption("Auto-refreshes every 5 minutes.")

    data = fetch_nifty_data()
    if data:
        spot_price, df_filtered = process_data(data)
        
        st.subheader(f"Nifty Spot Price: {spot_price:.2f}")

        st.dataframe(df_filtered.rename(columns={
            'strikePrice': 'Strike Price',
            'callVolume': 'Call Volume',
            'putVolume': 'Put Volume',
            'callChangeOI': 'Call Change OI',
            'putChangeOI': 'Put Change OI'
        }), use_container_width=True)

    # Auto-refresh mechanism
    count = st.empty()
    for i in range(300, 0, -1):
        count.metric(label="Refreshing in", value=f"{i} seconds")
        time.sleep(1)
    st.experimental_rerun()

if __name__ == "__main__":
    main()
