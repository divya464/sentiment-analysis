import streamlit as st
import pandas as pd
import plotly.express as px

# App title
st.set_page_config(page_title="Financial Sentiment Dashboard", layout="wide")
st.title("💹 Financial Sentiment Analysis Dashboard")

# File upload section
uploaded_file = st.file_uploader("📤 Upload Financial Sentiment CSV", type=["csv"])

if uploaded_file is not None:
    # Read the dataset
    df = pd.read_csv(uploaded_file)
    
    # Display data preview
    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # Dataset summary
    st.subheader("📊 Dataset Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    col2.metric("Unique Dates", df['date'].nunique() if 'date' in df.columns else "N/A")
    col3.metric("Unique Sentiments", df['sentiment'].nunique() if 'sentiment' in df.columns else "N/A")

    # Sentiment distribution chart
    st.subheader("📈 Sentiment Distribution")
    sentiment_count = df['sentiment'].value_counts().reset_index()
    sentiment_count.columns = ['Sentiment', 'Count']
    fig = px.pie(sentiment_count, names='Sentiment', values='Count', color='Sentiment',
                 color_discrete_map={'Positive':'green', 'Negative':'red', 'Neutral':'gray'},
                 title="Overall Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Sentiment trend over time
    if 'date' in df.columns:
        st.subheader("📅 Sentiment Trend Over Time")
        trend_df = df.groupby(['date', 'sentiment']).size().reset_index(name='Count')
        fig2 = px.line(trend_df, x='date', y='Count', color='sentiment', markers=True,
                       title="Daily Sentiment Trend")
        st.plotly_chart(fig2, use_container_width=True)

    # Filter by sentiment
    st.subheader("🔍 Filter Headlines by Sentiment")
    selected_sentiment = st.selectbox("Choose sentiment:", df['sentiment'].unique())
    filtered_df = df[df['sentiment'] == selected_sentiment]
    st.dataframe(filtered_df[['date', 'headline']].reset_index(drop=True))

    # Download filtered results
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Headlines as CSV",
        data=csv,
        file_name=f"{selected_sentiment.lower()}_headlines.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Upload a CSV file to start analyzing financial sentiment.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & Plotly | © 2025 Financial Sentiment Dashboard")