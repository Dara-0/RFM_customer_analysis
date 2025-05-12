import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# --- Page Config ---
st.set_page_config(
    page_title="RFM Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("data/rfm_segments.csv")

df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("🎯 Customer Segment Filter")
segment_options = df['ClusterLabel'].unique().tolist()
selected_segment = st.sidebar.selectbox("Choose a Segment", segment_options)

# --- Title ---
st.title("📊 RFM Customer Segmentation Dashboard")
st.markdown("""
Use this dashboard to explore customer behavior using **Recency, Frequency, and Monetary** value analysis.
""")

# --- SECTION 1: General Insights ---
with st.expander("📌 General Customer Insights", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Gender Distribution")
        gender_dist = df['CustGender'].value_counts()
        st.bar_chart(gender_dist)

    with col2:
        st.subheader("Top 10 Customer Locations")
        top_locations = df['CustLocation'].value_counts().head(10)
        st.bar_chart(top_locations)

    if 'AgeGroup' in df.columns:
        st.subheader("🎂 Age Group Distribution")
        age_counts = df['AgeGroup'].value_counts().sort_index()
        st.bar_chart(age_counts)

# --- SECTION 2: Transaction Trends ---
with st.expander("📆 Transaction Trends Over Time", expanded=True):
    st.subheader("Daily Transaction Volume")
    txn_trend = df.groupby('TransactionDate')['TransactionID'].count().reset_index()
    txn_trend.columns = ['Date', 'Transactions']
    st.line_chart(txn_trend.set_index('Date'))

    st.subheader("💳 Account Balance Distribution")
    fig_bal, ax_bal = plt.subplots(figsize=(6, 3))
    sns.histplot(df['CustAccountBalance'], bins=30, kde=True, ax=ax_bal, color="teal")
    st.pyplot(fig_bal)

# --- SECTION 3: Segment Distribution by Demographics ---
with st.expander("🔎 Segment Distribution by Demographics", expanded=False):
    st.subheader("Segment Count by Age Group or Location")
    group_by_option = st.radio("Group by:", ['AgeGroup', 'CustLocation'])

    grouped = df.groupby([group_by_option, 'ClusterLabel']).size().reset_index(name='Count')
    pivot_table = grouped.pivot(index=group_by_option, columns='ClusterLabel', values='Count').fillna(0)

    st.dataframe(pivot_table)
    st.bar_chart(pivot_table)

# --- SECTION 4: Segment-Level Analysis ---
with st.expander("📂 Segment-Level RFM Analysis", expanded=True):
    segment_df = df[df['ClusterLabel'] == selected_segment].copy()

    st.subheader(f"Segment: {selected_segment} ({len(segment_df)} customers)")
    st.dataframe(segment_df[['CustomerID', 'Recency', 'Frequency', 'Monetary']].head(10))

    st.download_button(
        label="📥 Download Segment as CSV",
        data=segment_df.to_csv(index=False),
        file_name=f"{selected_segment}_segment.csv",
        mime='text/csv'
    )

    st.subheader("📊 RFM Distributions")
    col1, col2, col3 = st.columns(3)

    with col1:
        fig_r = plt.figure(figsize=(4, 3))
        sns.histplot(segment_df['Recency'], bins=20, color="skyblue")
        plt.title("Recency")
        st.pyplot(fig_r)

    with col2:
        fig_f = plt.figure(figsize=(4, 3))
        sns.histplot(segment_df['Frequency'], bins=20, color="salmon")
        plt.title("Frequency")
        st.pyplot(fig_f)

    with col3:
        fig_m = plt.figure(figsize=(4, 3))
        sns.histplot(segment_df['Monetary'], bins=20, color="seagreen")
        plt.title("Monetary")
        st.pyplot(fig_m)

        # --- Optional: Export plot as PNG ---
        buf = BytesIO()
        fig_m.savefig(buf, format="png")
        st.download_button(
            label="Download Monetary Plot",
            data=buf.getvalue(),
            file_name="monetary_histogram.png",
            mime="image/png"
        )

# --- SECTION 5: Segment Comparison ---
with st.expander("📊 Compare All Segments (RFM Averages)", expanded=False):
    avg_rfm_by_cluster = df.groupby('ClusterLabel')[['Recency', 'Frequency', 'Monetary']].mean().round(2)
    st.dataframe(avg_rfm_by_cluster)
    st.line_chart(avg_rfm_by_cluster)

# --- SECTION 6: Simulation ---
with st.expander("🔬 What-if Simulation: Frequency Boost", expanded=False):
    st.subheader("Simulate Frequency Increase")
    boost = st.slider("Increase Frequency by", 0, 5, 1)
    segment_df['Simulated Frequency'] = segment_df['Frequency'] + boost

    st.line_chart(
        segment_df[['Frequency', 'Simulated Frequency']].reset_index(drop=True),
        use_container_width=True
    )
