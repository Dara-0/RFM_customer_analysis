import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Config ---
st.set_page_config(page_title="RFM Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("data/rfm_segments.csv")

df = load_data()



# --- Sidebar Filters ---
st.sidebar.title("Customer Segment Filter")
segment_options = df['ClusterLabel'].unique().tolist()
selected_segment = st.sidebar.selectbox("Choose a Segment", segment_options)

# --- Title ---
st.title("📊 RFM Customer Segmentation Dashboard")
st.markdown("""
Visualize customer behavior based on Recency, Frequency, and Monetary value.
Use the sidebar to filter by customer segment.
""")

# --- Filtered Data ---
segment_df = df[df['ClusterLabel'] == selected_segment]
st.subheader(f"Segment: {selected_segment} ({len(segment_df)} customers)")
st.dataframe(segment_df[['CustomerID', 'Recency', 'Frequency', 'Monetary']].head(10))

# --- RFM Distributions ---
st.subheader("Distribution of RFM Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    fig_r = plt.figure(figsize=(4,3))
    sns.histplot(segment_df['Recency'], bins=20)
    plt.title("Recency")
    st.pyplot(fig_r)

with col2:
    fig_f = plt.figure(figsize=(4,3))
    sns.histplot(segment_df['Frequency'], bins=20)
    plt.title("Frequency")
    st.pyplot(fig_f)

with col3:
    fig_m = plt.figure(figsize=(4,3))
    sns.histplot(segment_df['Monetary'], bins=20)
    plt.title("Monetary")
    st.pyplot(fig_m)

# --- Simulation Option ---
st.subheader("🔬 What-if: Simulate Increased Engagement")
simulated_freq = st.slider("Increase Frequency by", 0, 5, 1)
segment_df['Simulated Frequency'] = segment_df['Frequency'] + simulated_freq

st.line_chart(segment_df[['Frequency', 'Simulated Frequency']].reset_index(drop=True))
