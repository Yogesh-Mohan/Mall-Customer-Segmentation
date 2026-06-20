from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import numpy as np
import sqlite3
import joblib
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_mall_segmentation'

# Load models safely
MODEL_PATH = 'models/clustering_model.pkl'
SCALER_PATH = 'models/scaler.pkl'

kmeans_model = None
scaler = None

if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    kmeans_model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- Authentication Middleware ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html')

@app.route('/clusters')
@login_required
def clusters():
    return render_template('clusters.html')

@app.route('/insights')
@login_required
def insights():
    return render_template('insights.html')

@app.route('/customers')
@login_required
def customers():
    conn = get_db_connection()
    cust_data = conn.execute('SELECT * FROM Customers ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('customers.html', customers=cust_data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        admin = conn.execute('SELECT * FROM Admins WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid Credentials')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

# --- API Endpoints ---

def get_segment_label(cluster_id):
    labels = {
        0: "Average Customers",
        1: "High Income - Low Spending",
        2: "Low Income - Low Spending",
        3: "High Income - High Spending",
        4: "Low Income - High Spending"
    }
    return labels.get(cluster_id, "Unknown Segment")

@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.json
        age = int(data['age'])
        gender = data['gender']
        income = float(data['annual_income'])
        spending = float(data['spending_score'])
        
        if kmeans_model is None or scaler is None:
            return jsonify({'error': 'Models are not trained yet. Please train the model first.'}), 400
            
        # Prepare input
        input_data = pd.DataFrame([[income, spending]], columns=['Annual Income (k$)', 'Spending Score (1-100)'])
        scaled_data = scaler.transform(input_data)
        
        cluster_id = int(kmeans_model.predict(scaled_data)[0])
        customer_type = get_segment_label(cluster_id)
        
        # Determine business value and recommendation
        business_value = "High" if cluster_id in [3, 4] else "Medium" if cluster_id == 0 else "Low"
        if cluster_id == 3:
            marketing_recommendation = "Target with premium loyalty programs and exclusive offers."
        elif cluster_id == 4:
            marketing_recommendation = "Upsell volume products; they spend high despite lower income."
        elif cluster_id == 1:
            marketing_recommendation = "Run targeted campaigns to convert their high income into higher spending."
        elif cluster_id == 2:
            marketing_recommendation = "Provide discount-driven offers."
        else:
            marketing_recommendation = "Maintain regular promotional cadence."
        
        # Save to database
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO Customers (age, gender, annual_income, spending_score, cluster, customer_type)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (age, gender, income, spending, cluster_id, customer_type))
        conn.commit()
        conn.close()
        
        return jsonify({
            'cluster_id': cluster_id,
            'customer_type': customer_type,
            'business_value': business_value,
            'marketing_recommendation': marketing_recommendation
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard_stats')
@login_required
def dashboard_stats():
    # Provide data for the charts based on the dataset
    df = pd.read_csv('dataset/Mall_Customers.csv')
    
    # We apply the model to the whole dataset to get segments if not already in df
    if kmeans_model is not None and scaler is not None:
         X = df[['Annual Income (k$)', 'Spending Score (1-100)']]
         X_scaled = scaler.transform(X)
         df['Cluster'] = kmeans_model.predict(X_scaled)
         df['SegmentLabel'] = df['Cluster'].apply(get_segment_label)
    else:
         df['Cluster'] = 0
         df['SegmentLabel'] = "Unknown"
         
    stats = {
        'total_customers': len(df),
        'avg_age': float(df['Age'].mean()),
        'avg_income': float(df['Annual Income (k$)'].mean()),
        'avg_spending': float(df['Spending Score (1-100)'].mean()),
        'num_segments': df['Cluster'].nunique()
    }
    
    # Segment distribution
    dist = df['SegmentLabel'].value_counts().to_dict()
    stats['distribution_labels'] = list(dist.keys())
    stats['distribution_values'] = list(dist.values())
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
