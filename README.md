# Mall Customer Segmentation and Customer Intelligence System

![Dashboard Preview](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![Flask](https://img.shields.io/badge/Framework-Flask-black.svg)

## 📌 Project Overview
A professional, AI-powered customer segmentation platform that helps shopping malls and retail businesses understand customer behavior, spending habits, and purchasing patterns. The system automatically groups customers into meaningful segments using unsupervised machine learning (K-Means Clustering) and provides actionable business insights for marketing and sales strategies.

## ✨ Features
- **AI-Powered Customer Segmentation**: Groups customers into 5 distinct categories based on Annual Income and Spending Score.
- **Premium Analytics Dashboard**: A sleek, modern dashboard with an interactive glassmorphism UI and real-time Chart.js visualizations.
- **Real-Time Predictions**: Input customer data (Age, Gender, Income, Spending) to instantly predict their segment and receive personalized marketing recommendations.
- **Data Visualization**: View the distribution of customer segments.
- **Secure Admin Login**: Basic authentication system for administrators to access business intelligence.

## 🛠️ Technology Stack
- **Frontend**: HTML5, CSS3, Bootstrap 5, Chart.js
- **Backend**: Python, Flask
- **Database**: SQLite
- **Machine Learning**: Pandas, NumPy, Scikit-Learn

## 🧠 Machine Learning Segments
The K-Means model segments customers into the following groups:
1. **High Income - High Spending**: Target with premium loyalty programs and exclusive offers.
2. **High Income - Low Spending**: Run targeted campaigns to convert their high income into higher spending.
3. **Low Income - High Spending**: Upsell volume products; they spend high despite lower income.
4. **Low Income - Low Spending**: Provide discount-driven offers.
5. **Average Customers**: Maintain regular promotional cadence.

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Yogesh-Mohan/Mall-Customer-Segmentation.git
   cd Mall-Customer-Segmentation
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Initialization Scripts**:
   Generate the dataset, initialize the database, and train the ML models:
   ```bash
   python dataset/generate_dataset.py
   python database_setup.py
   python train_model.py
   ```

5. **Start the Flask Application**:
   ```bash
   python app.py
   ```

6. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:5000/`.
   - **Admin Login Username:** `admin`
   - **Admin Login Password:** `admin123`

## 🔮 Future Enhancements
- Export PDF/CSV Reports
- Customer Lifetime Value (CLV) Estimation
- 3D Cluster Visualization using Plotly
