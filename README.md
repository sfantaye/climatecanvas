# 🌍 ClimateCanvas

**ClimateCanvas** is an AI-powered, interactive storytelling platform designed to explore climate change data through dynamic visualizations, geospatial insights, and predictive analytics.

By combining cutting-edge technologies like Hugging Face's NLP models, geospatial mapping, and machine learning, **ClimateCanvas** empowers users to uncover meaningful insights about temperature anomalies, CO₂ levels, and sea-level rise.

---

## 🚀 Features

### 📖 Interactive Storytelling
- Engage with a narrative-driven exploration of global climate data.
- Use sliders, dropdowns, and widgets to interactively explore trends over time.

### 🗺️ Geospatial Visualization
- Explore regional impacts of climate change with interactive choropleth maps.
- Hover over countries to view temperature anomalies and other key metrics (powered by **Folium** and **GeoPandas**).

### 🤖 AI-Powered Insights
- Generate summaries of selected time periods using Hugging Face's **summarization models**.
- Ask questions in plain English and receive AI-generated answers via **question-answering models**.

### 📈 Predictive Analytics
- Train a simple ML model to predict future CO₂ levels based on historical data.
- Visualize predictions with dynamic **Plotly** charts.

### 🔐 Secure API Key Management
- API keys are securely managed using `.env` files.

---

## 🛠️ Installation

### 📋 Prerequisites
- Python 3.8 or higher
- Git (optional, for cloning the repo)

### 📥 Clone the Repository

```bash
git clone https://github.com/yourusername/climatecanvas.git
cd climatecanvas
