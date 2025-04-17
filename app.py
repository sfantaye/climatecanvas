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

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="ClimateCanvas", page_icon="🌍")

# --- Load Environment Variables ---
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")
API_URL_SUMMARY = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_URL_QA = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# --- Tailwind CSS Injection ---
# Include Tailwind CSS via CDN
st.markdown('<script src="https://cdn.tailwindcss.com"></script>', unsafe_allow_html=True)
st.markdown("""
<style>
/* You can add custom CSS here if needed, but Tailwind classes should cover most */
/* For example, to ensure full width */
.main .block-container {
    padding-top: 2rem; /* Add padding below the fixed navbar */
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%; /* Override default max-width if needed */
}
/* Style Streamlit generated elements if necessary (use browser inspector to find classes) */
.stButton>button {
    /* Example: Style Streamlit buttons with Tailwind-like appearance */
    /* Note: Direct styling of complex Streamlit widgets can be tricky */
    /* background-color: #3b82f6; /* blue-500 */ */
    /* color: white; */
    /* padding: 0.5rem 1rem; */
    /* border-radius: 0.375rem; /* rounded-md */ */
    /* font-weight: 600; /* font-semibold */ */
    /* transition: background-color 0.2s ease-in-out; */
}
/* .stButton>button:hover { */
    /* background-color: #2563eb; /* blue-600 */ */
/* } */

/* Ensure Plotly charts resize correctly */
.stPlotlyChart {
    width: 100% !important;
}

/* Ensure Folium maps resize correctly */
.stFoliumMap {
    width: 100% !important;
    height: 500px !important; /* Adjust height as needed */
    border-radius: 0.5rem; /* rounded-lg */
    overflow: hidden;
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1); /* shadow-md */
}

/* Style Streamlit expanders */
.st-expander {
    border: 1px solid #e5e7eb; /* border-gray-200 */
    border-radius: 0.5rem; /* rounded-lg */
    margin-bottom: 1rem; /* mb-4 */
    background-color: #f9fafb; /* bg-gray-50 */
    box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); /* shadow-sm */
}
.st-expander header {
    font-weight: 600; /* font-semibold */
    color: #1f2937; /* text-gray-800 */
}
</style>
""", unsafe_allow_html=True)


# --- Fancy Navbar ---
st.markdown("""
<nav class="fixed top-0 left-0 w-full bg-gradient-to-r from-sky-500 via-cyan-500 to-teal-400 p-4 shadow-lg z-50">
    <div class="container mx-auto flex justify-between items-center px-4">
        <div class="text-white text-3xl font-extrabold tracking-tight" style="font-family: 'Poppins', sans-serif; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);">
            Climate<span class="text-yellow-300">Canvas</span> 🌍
        </div>
        <!-- Add other nav items here if needed -->
    </div>
</nav>
<div class="h-20"></div> <!-- Add space to push content below fixed navbar -->
""", unsafe_allow_html=True)

# --- Main App Content ---
st.markdown("<div class='container mx-auto px-4 py-8'>", unsafe_allow_html=True)

# Title and Introduction - Using Markdown with Tailwind
st.markdown("""
<h1 class='text-4xl font-bold text-gray-800 mb-4 text-center'>
    AI-Powered Interactive Storytelling: The Climate Change Narrative
</h1>
<p class='text-lg text-gray-600 mb-8 text-center leading-relaxed'>
    Welcome to an AI-powered journey through climate change data.
    Explore temperature anomalies, CO₂ levels, and sea-level rise globally and regionally.
    Ask questions, get predictions, and uncover insights generated by cutting-edge AI.
</p>
<hr class='my-6 border-gray-300'>
""", unsafe_allow_html=True)


# Load sample datasets
@st.cache_data
def load_data():
    years = np.arange(1900, 2024) # Extended to 2024 for consistency
    base_temp_anomaly = 0.0005 * (years - 1900)**2 + np.random.normal(0, 0.15, len(years)) - 0.5
    base_co2 = 280 + 1.8 * (years - 1900) + np.random.normal(0, 5, len(years))
    base_sea_level = 0.08 * (years - 1900) + np.random.normal(0, 5, len(years))

    df = pd.DataFrame({
        "Year": years,
        "Temperature Anomaly (°C)": base_temp_anomaly,
        "CO2 Levels (ppm)": base_co2,
        "Sea Level Rise (mm)": base_sea_level
    })
    df['CO2 Levels (ppm)'] = df['CO2 Levels (ppm)'].astype(int) # More realistic CO2 levels
    df['Sea Level Rise (mm)'] = df['Sea Level Rise (mm)'].clip(lower=0) # Sea level shouldn't decrease drastically
    return df

@st.cache_data
def load_geospatial_data():
    # Attempt to load from local path first
    local_data_path = os.path.join("data", "ne_110m_admin_0_countries.shp")
    if os.path.exists(local_data_path):
         data_path = local_data_path
    else:
        # Fallback to geopandas dataset (requires internet)
        st.warning("Local shapefile not found. Using default geopandas dataset (requires internet). Place 'ne_110m_admin_0_countries' files in a 'data' folder for offline use.")
        data_path = gpd.datasets.get_path('naturalearth_lowres')

    world = gpd.read_file(data_path)

    # Simulate regional temperature anomalies based on latitude (crude simulation)
    np.random.seed(42)
    # Higher anomaly near poles, lower near equator (example logic)
    world['centroid_lat'] = world.geometry.centroid.y
    world['Temp Anomaly'] = 0.5 + 0.01 * np.abs(world['centroid_lat']) + np.random.normal(loc=0.0, scale=0.2, size=len(world))
    world['Temp Anomaly'] = world['Temp Anomaly'].round(2) # Round for display

    # Ensure the column used in Choropleth exists and has the correct name
    if 'name' not in world.columns and 'NAME' in world.columns:
        world = world.rename(columns={'NAME': 'name'})
    elif 'name' not in world.columns and 'ADMIN' in world.columns:
         world = world.rename(columns={'ADMIN': 'name'})
    # Add more fallbacks if necessary based on the shapefile structure

    # Handle potential missing names (fill with a placeholder)
    if 'name' in world.columns:
        world['name'] = world['name'].fillna('Unknown Country')
    else:
        st.error("Could not find a suitable country name column in the shapefile ('name', 'NAME', 'ADMIN'). Please check your shapefile attributes.")
        # Add a dummy name column if it's missing entirely to prevent errors, though the map might not work well
        world['name'] = [f"Region {i}" for i in range(len(world))]


    return world

try:
    df = load_data()
    world = load_geospatial_data()
    geodata_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.markdown("<p class='text-red-600 font-semibold'>Could not load necessary data. Some features might be unavailable.</p>", unsafe_allow_html=True)
    df = pd.DataFrame() # Create empty dataframe to avoid errors later
    world = None
    geodata_loaded = False


# --- Section Styling Function ---
def render_section_header(title, subtitle):
    st.markdown(f"""
    <div class='my-8 p-6 bg-white rounded-xl shadow-md border border-gray-200'>
        <h2 class='text-3xl font-bold text-cyan-700 mb-2'>{title}</h2>
        <p class='text-gray-600 leading-relaxed'>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

# --- Section 1: Global Temperature Anomalies ---
render_section_header(
    "1. Rising Temperatures: A Global View",
    "Global average temperatures have shown a significant upward trend, particularly since the mid-20th century. Explore the historical temperature anomalies relative to a baseline period (typically pre-industrial)."
)

with st.expander("What are Temperature Anomalies?"):
    st.markdown("""
    <div class='p-4 text-gray-700 bg-cyan-50 rounded-md'>
        Temperature anomalies represent the deviation (difference) of the temperature at a given time from a long-term average or baseline period.
        <ul>
            <li class='ml-4 list-disc'><strong>Positive anomalies</strong> indicate that the observed temperature was warmer than the baseline.</li>
            <li class='ml-4 list-disc'><strong>Negative anomalies</strong> indicate that the observed temperature was cooler than the baseline.</li>
        </ul>
        They are useful for identifying trends because they minimize the influence of geographical location and seasonal variations.
    </div>
    """, unsafe_allow_html=True)

# Interactive widget container with styling
st.markdown("<div class='my-6 p-4 bg-gray-50 rounded-lg shadow-inner border border-gray-200'>", unsafe_allow_html=True)
if not df.empty:
    min_year_data = int(df["Year"].min())
    max_year_data = int(df["Year"].max())
    default_start = max(min_year_data, 1950) # Default start year

    start_year, end_year = st.slider(
        "Select Time Range:",
        min_value=min_year_data,
        max_value=max_year_data,
        value=(default_start, max_year_data),
        help="Drag the sliders to select the start and end years for the analysis."
    )
    filtered_df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

    # Plot temperature anomalies
    st.markdown("<h3 class='text-xl font-semibold text-gray-700 mb-3'>Temperature Anomalies Over Selected Period</h3>", unsafe_allow_html=True)
    fig_temp = px.line(
        filtered_df,
        x="Year",
        y="Temperature Anomaly (°C)",
        title=f"Global Temperature Anomaly ({start_year}-{end_year})",
        labels={"Temperature Anomaly (°C)": "Anomaly (°C)"},
        template="plotly_white" # Use a clean template
    )
    fig_temp.update_layout(
        xaxis_title="Year",
        yaxis_title="Temperature Anomaly (°C)",
        font=dict(family="Arial, sans-serif", size=12, color="black"),
        title_font_size=18,
        hovermode="x unified"
    )
    fig_temp.update_traces(line=dict(color='#06b6d4', width=2.5)) # Teal color line
    st.plotly_chart(fig_temp, use_container_width=True)

    # AI-Powered Narrative Generation
    st.markdown("<div class='mt-5'>", unsafe_allow_html=True)
    if st.button("✨ Generate AI Summary for Selected Period", key="summary_temp"):
        if HF_API_KEY:
            summary_prompt = f"""
            Provide a concise summary of the global temperature anomaly trend shown in the data between the years {start_year} and {end_year}.
            Focus on the overall pattern (e.g., increasing, decreasing, stable), any notable acceleration or deceleration, and mention the approximate anomaly values at the start and end of the period based on the general trend.
            Context: The data represents global average temperature deviations from a baseline.
            Example data points (if available): Start year {start_year} anomaly might be around {filtered_df.iloc[0]['Temperature Anomaly (°C)']:.2f}°C, end year {end_year} anomaly might be around {filtered_df.iloc[-1]['Temperature Anomaly (°C)']:.2f}°C.
            """
            payload = {"inputs": summary_prompt, "parameters": {"max_length": 150, "min_length": 30}}
            try:
                response = requests.post(API_URL_SUMMARY, headers=headers, json=payload, timeout=30)
                response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
                ai_summary = response.json()[0]["summary_text"]
                st.markdown(f"""
                <div class='p-4 my-4 bg-teal-50 border border-teal-200 rounded-lg shadow-sm'>
                    <strong class='text-teal-800'>🤖 AI-Generated Summary:</strong>
                    <p class='mt-2 text-gray-800'>{ai_summary}</p>
                </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.RequestException as e:
                 st.error(f"😥 Network error generating summary: {e}")
            except Exception as e:
                 st.error(f"😥 Error generating summary: {e}")
        else:
            st.warning("Hugging Face API Key not configured. Cannot generate AI summary.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
     st.warning("Temperature data not loaded. Cannot display chart or generate summary.")

st.markdown("</div>", unsafe_allow_html=True) # Close widget container


# --- Section 2: Regional Analysis with Geospatial Data ---
render_section_header(
    "2. A World of Difference: Regional Anomalies",
    "Climate change impacts are not uniform. Explore how simulated temperature anomalies vary across different countries and regions using the interactive map below."
)

if geodata_loaded and world is not None and 'name' in world.columns:
    st.markdown("<div class='my-6 p-4 bg-gray-50 rounded-lg shadow-inner border border-gray-200'>", unsafe_allow_html=True)
    st.markdown("<h3 class='text-xl font-semibold text-gray-700 mb-3'>Interactive Map of Regional Temperature Anomalies</h3>", unsafe_allow_html=True)

    # Create a choropleth map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron', attr='CartoDB Positron')

    choropleth = folium.Choropleth(
        geo_data=world,
        name="choropleth",
        data=world,
        columns=["name", "Temp Anomaly"], # Use the standardized 'name' column
        key_on="feature.properties.name", # Use the standardized 'name' column
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Simulated Temperature Anomaly (°C)",
        highlight=True, # Highlight country on hover
        nan_fill_color="lightgrey" # Color for countries with no data
    ).add_to(m)

    # Add tooltips for interactivity
    tooltip = folium.features.GeoJsonTooltip(
        fields=['name', 'Temp Anomaly'],
        aliases=['Country:', 'Simulated Anomaly (°C):'],
        sticky=False, # Tooltip follows mouse
        style=("background-color: white; color: black; font-family: Arial; "
               "font-size: 12px; padding: 5px; border-radius: 3px; box-shadow: 1px 1px 3px grey;")
    )
    folium.GeoJson(
        world,
        style_function=lambda x: {'fillColor': 'transparent', 'color': 'transparent'}, # Make GeoJson layer invisible
        tooltip=tooltip
    ).add_to(m)

    # Add layer control
    folium.LayerControl().add_to(m)

    # Display the map in Streamlit using the styled container
    st.markdown("<div class='my-4 border rounded-lg shadow-md overflow-hidden'>", unsafe_allow_html=True)
    folium_static(m, width=None, height=500) # Let container control width
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<p class='text-sm text-gray-500 mt-2'>Hover over a country to see its name and simulated temperature anomaly. Note: Anomalies are simulated for illustrative purposes.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) # Close widget container
else:
    st.markdown("<div class='my-6 p-4 bg-yellow-50 rounded-lg border border-yellow-200'><p class='text-yellow-800'>Geospatial data could not be loaded or processed correctly. The regional map cannot be displayed.</p></div>", unsafe_allow_html=True)


# --- Section 3: Predictive Analytics for CO2 Levels ---
render_section_header(
    "3. Peering into the Future: CO₂ Predictions",
    "Using historical data, we can train a simple predictive model (Linear Regression) to forecast potential future CO₂ levels. This provides a glimpse into possible scenarios based on past trends."
)

st.markdown("<div class='my-6 p-4 bg-gray-50 rounded-lg shadow-inner border border-gray-200'>", unsafe_allow_html=True)
if not df.empty:
    st.markdown("<h3 class='text-xl font-semibold text-gray-700 mb-3'>Forecasting CO₂ Levels (2024-2034)</h3>", unsafe_allow_html=True)
    try:
        # Train a linear regression model
        X = df["Year"].values.reshape(-1, 1)
        y = df["CO2 Levels (ppm)"].values
        model = LinearRegression()
        model.fit(X, y)

        # Predict future CO2 levels
        last_year = int(df["Year"].max())
        future_years = np.arange(last_year + 1, last_year + 11).reshape(-1, 1)
        predicted_co2 = model.predict(future_years)

        # Combine historical and predicted data for plotting
        hist_df_plot = df[['Year', 'CO2 Levels (ppm)']].copy()
        hist_df_plot['Type'] = 'Historical'

        future_df_plot = pd.DataFrame({
            "Year": future_years.flatten(),
            "CO2 Levels (ppm)": predicted_co2,
            "Type": "Predicted"
        })

        combined_df = pd.concat([hist_df_plot[hist_df_plot['Year'] >= 2000], future_df_plot], ignore_index=True) # Show some recent history

        # Plot predictions
        fig_co2_pred = px.line(
            combined_df,
            x="Year",
            y="CO2 Levels (ppm)",
            color="Type",
            title="Historical and Predicted CO₂ Levels",
            labels={"CO2 Levels (ppm)": "CO₂ (ppm)"},
            template="plotly_white",
            color_discrete_map={'Historical': '#0ea5e9', 'Predicted': '#f97316'} # Sky blue and Orange
        )
        fig_co2_pred.update_layout(
             xaxis_title="Year",
             yaxis_title="CO₂ Levels (ppm)",
             font=dict(family="Arial, sans-serif", size=12, color="black"),
             title_font_size=18,
             legend_title_text='Data Type',
             hovermode="x unified"
        )
        fig_co2_pred.update_traces(mode='lines+markers', line=dict(width=2.5))
        st.plotly_chart(fig_co2_pred, use_container_width=True)

        st.markdown("<p class='text-sm text-gray-500 mt-2'>Note: This is a simple linear projection based solely on past trends and does not account for future policy changes, technological advancements, or complex climate feedback loops.</p>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"😥 Error during prediction: {e}")

else:
    st.warning("CO₂ data not loaded. Cannot display predictions.")

st.markdown("</div>", unsafe_allow_html=True) # Close widget container


# --- Section 4: Natural Language Queries ---
render_section_header(
    "4. Ask the AI",
    "Have specific questions about the climate data presented? Ask our AI assistant in plain English. It will attempt to answer based on the context of the dataset (temperature, CO₂, sea level trends from 1900-2023)."
)

st.markdown("<div class='my-6 p-4 bg-gray-50 rounded-lg shadow-inner border border-gray-200'>", unsafe_allow_html=True)
st.markdown("<h3 class='text-xl font-semibold text-gray-700 mb-3'>Query the Climate Data</h3>", unsafe_allow_html=True)

query = st.text_input("Enter your question about the trends (e.g., 'What was the approximate CO2 level in 2010?', 'Did sea level rise faster after 1980?'):", key="qa_input")

if query:
    if HF_API_KEY:
        try:
            # Provide more specific context based on the loaded data
            context_parts = []
            if not df.empty:
                 min_yr, max_yr = df['Year'].min(), df['Year'].max()
                 context_parts.append(f"The dataset covers the years {min_yr} to {max_yr}.")
                 if 'Temperature Anomaly (°C)' in df.columns:
                      min_temp, max_temp = df['Temperature Anomaly (°C)'].min(), df['Temperature Anomaly (°C)'].max()
                      context_parts.append(f"Global temperature anomalies range roughly from {min_temp:.2f}°C to {max_temp:.2f}°C, showing a general increasing trend.")
                 if 'CO2 Levels (ppm)' in df.columns:
                      min_co2, max_co2 = df['CO2 Levels (ppm)'].min(), df['CO2 Levels (ppm)'].max()
                      context_parts.append(f"Atmospheric CO2 levels range from approximately {min_co2} ppm to {max_co2} ppm, with a clear upward trend.")
                 if 'Sea Level Rise (mm)' in df.columns:
                      min_slr, max_slr = df['Sea Level Rise (mm)'].min(), df['Sea Level Rise (mm)'].max()
                      context_parts.append(f"Cumulative sea level rise ranges from {min_slr:.1f} mm to {max_slr:.1f} mm, also increasing over time.")
            else:
                 context_parts.append("Basic climate indicators like temperature anomaly, CO2 levels, and sea level rise are tracked over time.")

            full_context = " ".join(context_parts) + " The data generally shows warming temperatures, rising CO2, and rising sea levels throughout the period, especially accelerating in recent decades."

            qa_payload = {
                "question": query,
                "context": full_context
            }
            response = requests.post(API_URL_QA, headers=headers, json=qa_payload, timeout=30)
            response.raise_for_status() # Check for HTTP errors

            result = response.json()
            ai_response = result.get("answer", "The AI could not find a specific answer in the provided context.")
            score = result.get("score", 0) # Confidence score

            # Display response with confidence indication
            confidence_color = "green" if score > 0.5 else ("orange" if score > 0.1 else "red")
            st.markdown(f"""
            <div class='p-4 my-4 bg-blue-50 border border-blue-200 rounded-lg shadow-sm'>
                <strong class='text-blue-800'>🤖 AI Response:</strong>
                <p class='mt-2 text-gray-800'>{ai_response}</p>
                <p class='text-xs text-gray-500 mt-2'>(Confidence: <span class='font-semibold' style='color:{confidence_color};'>{score:.2f}</span>)</p>
            </div>
            """, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"😥 Network error processing question: {e}")
        except Exception as e:
            st.error(f"😥 Error processing question: {e}")
            st.error(f"Response content: {response.text if 'response' in locals() else 'No response object'}") # Log response content for debugging
    else:
        st.warning("Hugging Face API Key not configured. Cannot answer questions.")

st.markdown("</div>", unsafe_allow_html=True) # Close widget container


# --- Conclusion ---
st.markdown("""
<hr class='my-8 border-gray-300'>
<div class='my-8 p-6 bg-gradient-to-r from-emerald-50 to-lime-50 rounded-xl shadow-md border border-emerald-200'>
    <h2 class='text-3xl font-bold text-emerald-800 mb-3'>Conclusion: The Narrative Unfolds</h2>
    <p class='text-gray-700 leading-relaxed mb-4'>
        The visualizations and AI insights presented here paint a compelling picture: our climate is changing at an unprecedented rate. Rising temperatures, accumulating CO₂, and swelling oceans are interconnected parts of a global phenomenon driven significantly by human activities. Understanding these trends through data is the first step towards informed action.
    </p>
    <h3 class='text-xl font-semibold text-emerald-700 mb-2'>What Can You Do?</h3>
    <ul class='list-disc list-inside text-gray-700 space-y-1'>
        <li><strong>Reduce Your Footprint:</strong> Conserve energy, choose sustainable transport, reduce consumption, and adopt plant-rich diets.</li>
        <li><strong>Advocate for Change:</strong> Support policies and initiatives aimed at large-scale emissions reductions and renewable energy transition.</li>
        <li><strong>Stay Informed & Spread Awareness:</strong> Continue learning about climate science and share reliable information within your community.</li>
        <li><strong>Support Sustainable Businesses:</strong> Choose products and services from companies committed to environmental responsibility.</li>
    </ul>
</div>
""", unsafe_allow_html=True)


# --- Footer ---
st.markdown("""
<footer class='text-center text-sm text-gray-500 mt-12 py-6 border-t border-gray-200'>
    Made with <span style='color: #e25555;'>♥</span> using Streamlit by Sintayehu Fantaye
    <br>
    Data simulated for illustrative purposes. Climate science is complex; consult peer-reviewed sources for definitive information.
</footer>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # Close main container