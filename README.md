ClimateCanvas is an AI-powered, interactive storytelling platform designed to explore climate change data through dynamic visualizations, geospatial insights, and predictive analytics. By combining cutting-edge technologies like Hugging Face's NLP models, geospatial mapping, and machine learning, ClimateCanvas empowers users to uncover meaningful insights about temperature anomalies, CO2 levels, and sea-level rise.

Features
1. Interactive Storytelling
Engage with a narrative-driven exploration of global climate data.
Use sliders, dropdowns, and other widgets to interactively explore trends over time.
2. Geospatial Visualization
Explore regional impacts of climate change using interactive choropleth maps powered by Folium and GeoPandas.
Hover over countries to view temperature anomalies and other metrics.
3. AI-Powered Insights
Generate summaries of selected time periods using Hugging Face's summarization models.
Ask questions in plain English and receive AI-generated answers using question-answering models.
4. Predictive Analytics
Train a simple machine learning model to predict future CO2 levels based on historical trends.
Visualize predictions with dynamic Plotly charts.
5. Secure API Key Management
API keys are securely managed using .env files to protect sensitive information.

Installation
Prerequisites
Python 3.8 or higher
Git (optional, for cloning the repository)
Steps
Clone the Repository
bash
Copy
1
2
git clone https://github.com/yourusername/climatecanvas.git
cd climatecanvas
Install Dependencies
Install the required libraries using pip:
bash
Copy
1
pip install -r requirements.txt
Set Up Environment Variables
Create a .env file in the project directory and add your Hugging Face API key:
env
Copy
1
HF_API_KEY=your_huggingface_api_key
Run the App
Start the Streamlit app:
bash
Copy
1
streamlit run app.py
Usage
Explore Global Trends
Use the slider to select a time range and visualize temperature anomalies, CO2 levels, and sea-level rise.
Generate AI Summaries
Click the "Generate AI Summary" button to get a concise summary of trends for the selected period.
Ask Questions
Enter your question in the text box under the "Ask Questions About the Data" section to receive AI-powered answers.
Predict Future CO2 Levels
View predictions for future CO2 levels based on historical trends.
Analyze Regional Data
Interact with the choropleth map to explore temperature anomalies across different regions.
Dependencies
The following libraries are used in this project:

Streamlit : For building the interactive web app.
Pandas & NumPy : For data manipulation and analysis.
Plotly & Matplotlib : For dynamic visualizations.
GeoPandas & Folium : For geospatial data visualization.
Hugging Face Transformers : For AI-powered insights (summarization and question-answering).
Scikit-Learn : For predictive analytics.
Requests : For making API calls to Hugging Face.
Python-Dotenv : For managing environment variables securely.
Contributing
We welcome contributions from the community! If you'd like to contribute to ClimateCanvas, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/YourFeatureName).
Commit your changes (git commit -m "Add YourFeatureName").
Push to the branch (git push origin feature/YourFeatureName).
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Streamlit : For providing an intuitive framework for building data apps.
Hugging Face : For their powerful NLP models and inference API.
GeoPandas & Folium : For enabling geospatial data visualization.
Climate Scientists : For inspiring us to create tools that make climate data accessible and actionable.
Contact
For questions, feedback, or collaboration opportunities, feel free to reach out:

GitHub : github.com/sfantaye
Email : santafantaye@gmail.com
About the Project
ClimateCanvas was created to bridge the gap between complex climate data and actionable insights. By leveraging AI, geospatial tools, and interactive storytelling, we aim to empower individuals and organizations to better understand and address the challenges of climate change.

Let me know if you'd like to customize this further! 🌍
