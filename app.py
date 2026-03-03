import streamlit as st
import pandas as pd

st.set_page_config(page_title="NEPSE Live Market Dashboard", layout="wide")

st.title("🇳🇵 NEPSE Live Market Dashboard")


# AUTO PAGE REFRESH EVERY 60 SEC

st.markdown(
    """
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 60000);
    </script>
    """,
    unsafe_allow_html=True
)


# FETCH LIVE DATA (no permanent cache)

@st.cache_data(ttl=60)
def load_live_data():
    url = "https://www.merolagani.com/LatestMarket.aspx"
    tables = pd.read_html(url)
    df = tables[0]
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


try:
    df = load_live_data()
    st.success("Live market data loaded successfully ")
except:
    st.error("Failed to fetch live data ")
    st.stop()

# Convert LTP to numeric
df["LTP"] = pd.to_numeric(
    df["LTP"].astype(str).str.replace(",", ""),
    errors="coerce"
)


# MARKET SUMMARY

st.subheader(" Market Summary")

total_stocks = len(df)
highest_price = df["LTP"].max()
lowest_price = df["LTP"].min()

col1, col2, col3 = st.columns(3)
col1.metric("Stocks Traded Today", total_stocks)
col2.metric("Highest Price", round(highest_price, 2))
col3.metric("Lowest Price", round(lowest_price, 2))

st.divider()


# SEARCH SECTION

st.header(" Search Stock")

search = st.text_input("Enter Stock Symbol (Example: NABIL)").upper()

if search:
    result = df[df["Symbol"].str.upper() == search]

    if not result.empty:
        st.success("Stock Found ")
        st.dataframe(result, width="stretch")
    else:
        st.error("Stock Not Found ")

st.divider()


# FULL MARKET TABLE

st.header(" Full Market Overview")
st.dataframe(df, width="stretch")
