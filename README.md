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

📦 Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔐 Set Up Environment Variables
Create a .env file in the root directory:

env
Copy
Edit
HF_API_KEY=your_huggingface_api_key
▶️ Run the App
bash
Copy
Edit
streamlit run app.py
📌 Usage
🌡️ Explore Global Trends
Use the slider to select a time range and visualize temperature anomalies, CO₂ levels, and sea-level rise.

🧠 Generate AI Summaries
Click the "Generate AI Summary" button to receive a concise overview of trends.

❓ Ask Questions
Type your question in the text box under the "Ask Questions About the Data" section for AI-powered answers.

🔮 Predict CO₂ Levels
View predictions for future CO₂ levels based on historical trends using ML.

🌍 Analyze Regional Data
Interact with the choropleth map to explore regional temperature anomalies and metrics.

📚 Dependencies
This project uses the following libraries:

Streamlit – UI and interactivity

Pandas & NumPy – Data manipulation

Plotly & Matplotlib – Dynamic visualizations

GeoPandas & Folium – Geospatial visualizations

Hugging Face Transformers – AI/NLP summarization & Q&A

Scikit-Learn – Predictive analytics

Requests – API requests to Hugging Face

Python-Dotenv – Environment variable management

🤝 Contributing
We welcome contributions from the community!

Fork the repository.

Create your feature branch:

bash
Copy
Edit
git checkout -b feature/YourFeatureName
Commit your changes:

bash
Copy
Edit
git commit -m "Add YourFeatureName"
Push to GitHub:

bash
Copy
Edit
git push origin feature/YourFeatureName
Open a pull request and describe your changes.

📄 License
This project is licensed under the MIT License.
See the LICENSE file for more details.

🙏 Acknowledgments
Streamlit – For making interactive data apps easy to build.

Hugging Face – For their powerful NLP APIs and models.

GeoPandas & Folium – For geospatial magic.

Climate Scientists & Advocates – For inspiring action through data.

📬 Contact
GitHub: sfantaye

Email: santafantaye@gmail.com

🌱 About the Project
ClimateCanvas was created to bridge the gap between complex climate data and actionable insights.

By combining AI, geospatial tools, and interactive storytelling, we aim to empower individuals and organizations to better understand and address the challenges of climate change.

### 📥 Clone the Repository

```bash
git clone https://github.com/sfantaye/climatecanvas.git
cd climatecanvas
