import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.linear_model import LinearRegression
import requests
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up Hugging Face API key from .env
HF_API_KEY = os.getenv("HF_API_KEY")
API_URL_SUMMARY = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_URL_QA = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

# Headers for Hugging Face API
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# Title and Introduction
st.title("AI-Powered Interactive Storytelling: The Climate Change Narrative")
st.write("""
Welcome to an AI-powered journey through climate change data. 
Explore temperature anomalies, CO2 levels, and sea-level rise globally and regionally.
Ask questions, get predictions, and uncover insights generated by AI.
""")

# Load sample datasets (replace with your actual data)
@st.cache_data
def load_data():
    years = np.arange(1900, 2023)
    temp_anomalies = np.random.normal(loc=0.8, scale=0.2, size=len(years)).cumsum()
    co2_levels = np.random.normal(loc=300, scale=5, size=len(years)).cumsum()
    sea_level_rise = np.random.normal(loc=0.1, scale=0.05, size=len(years)).cumsum()
    
    df = pd.DataFrame({
        "Year": years,
        "Temperature Anomaly (°C)": temp_anomalies,
        "CO2 Levels (ppm)": co2_levels,
        "Sea Level Rise (mm)": sea_level_rise
    })
    return df

@st.cache_data
def load_geospatial_data():
    data_path = os.path.join("data", "ne_110m_admin_0_countries.shp")
    world = gpd.read_file(data_path)
    
    # Print column names for debugging
    st.write("Columns in the dataset:", list(world.columns))
    
    # Simulate regional temperature anomalies
    np.random.seed(42)
    world['Temp Anomaly'] = np.random.normal(loc=0.8, scale=0.2, size=len(world))
    return world

df = load_data()
world = load_geospatial_data()

# Section 1: Global Temperature Anomalies
st.header("1. Rising Temperatures Over Time")
st.write("""
Global temperatures have been rising steadily since the industrial revolution. 
This section explores temperature anomalies relative to pre-industrial levels.
""")

with st.expander("Learn More About Temperature Anomalies"):
    st.write("""
    Temperature anomalies are deviations from the long-term average. 
    Positive anomalies indicate warmer-than-average conditions.
    """)

# Interactive widget for selecting time period
start_year, end_year = st.slider(
    "Select a time range:", 
    min_value=int(df["Year"].min()), 
    max_value=int(df["Year"].max()), 
    value=(1900, 2023)
)

filtered_df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

# Plot temperature anomalies
fig_temp = px.line(
    filtered_df, 
    x="Year", 
    y="Temperature Anomaly (°C)", 
    title="Temperature Anomalies Over Time",
    labels={"Temperature Anomaly (°C)": "Anomaly (°C)"}
)
st.plotly_chart(fig_temp, use_container_width=True)

# AI-Powered Narrative Generation
if st.button("Generate AI Summary for Selected Period"):
    summary_prompt = f"""
    Summarize the temperature anomalies between {start_year} and {end_year}. 
    Highlight any significant trends or anomalies.
    """
    response = requests.post(API_URL_SUMMARY, headers=headers, json={"inputs": summary_prompt})
    if response.status_code == 200:
        ai_summary = response.json()[0]["summary_text"]
        st.write(f"**AI-Generated Summary:** {ai_summary}")
    else:
        st.error(f"Error generating summary: {response.text}")

# Section 2: Regional Analysis with Geospatial Data
st.header("2. Regional Temperature Anomalies")
st.write("""
Explore how temperature anomalies vary across different regions of the world.
""")

# Create a choropleth map
m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
folium.Choropleth(
    geo_data=world,
    name="choropleth",
    data=world,
    columns=["NAME", "Temp Anomaly"],  # Replace 'name' with the correct column name
    key_on="feature.properties.NAME",  # Ensure this matches the column name
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Temperature Anomaly (°C)",
).add_to(m)

# Add tooltips for interactivity
tooltip = folium.features.GeoJsonTooltip(fields=['NAME', 'Temp Anomaly'], aliases=['Country', 'Temp Anomaly'])
folium.GeoJson(world, tooltip=tooltip).add_to(m)

# Display the map in Streamlit
folium_static(m)

# Section 3: Predictive Analytics for CO2 Levels
st.header("3. Predicting Future CO2 Levels")
st.write("""
Using AI, we can predict future CO2 levels based on historical trends. 
Let's train a simple model and forecast CO2 levels for the next decade.
""")

# Train a linear regression model
X = df["Year"].values.reshape(-1, 1)
y = df["CO2 Levels (ppm)"].values
model = LinearRegression()
model.fit(X, y)

# Predict future CO2 levels
future_years = np.arange(2023, 2033).reshape(-1, 1)
predicted_co2 = model.predict(future_years)

# Plot predictions
future_df = pd.DataFrame({"Year": future_years.flatten(), "Predicted CO2 Levels (ppm)": predicted_co2})
fig_co2_pred = px.line(
    future_df, 
    x="Year", 
    y="Predicted CO2 Levels (ppm)", 
    title="Predicted CO2 Levels (2023-2033)",
    labels={"Predicted CO2 Levels (ppm)": "CO2 (ppm)"}
)
st.plotly_chart(fig_co2_pred, use_container_width=True)

# Section 4: Natural Language Queries
st.header("4. Ask Questions About the Data")
st.write("""
Ask a question about the dataset in plain English. 
Our AI will interpret your query and provide an answer.
""")

query = st.text_input("Enter your question:")
if query:
    try:
        # Generate AI response
        qa_payload = {
            "question": query,
            "context": """
            This dataset contains information about global climate change. 
            It includes temperature anomalies, CO2 levels, and sea-level rise from 1900 to 2023.
            """
        }
        response = requests.post(API_URL_QA, headers=headers, json=qa_payload)
        if response.status_code == 200:
            ai_response = response.json()["answer"]
            st.write(f"**AI Response:** {ai_response}")
        else:
            st.error(f"Error answering question: {response.text}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Conclusion
st.header("Conclusion")
st.write("""
The data tells a clear story: human activities are driving climate change. 
By exploring temperature anomalies, CO2 levels, and sea-level rise, we can better 
understand the urgency of addressing this global challenge.
""")

st.markdown("""
**What Can You Do?**
- Reduce your carbon footprint.
- Support policies aimed at combating climate change.
- Spread awareness about the science behind climate change.
""")

# Footer
st.write("Made with ❤️ using Streamlit, Hugging Face, and Geospatial Data")
