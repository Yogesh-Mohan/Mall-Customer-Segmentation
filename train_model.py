import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import joblib
import os

def prepare_data():
    df = pd.read_csv('dataset/Mall_Customers.csv')
    
    # Data Cleaning and Validation
    df.dropna(inplace=True) # Missing Value Handling
    
    # Feature selection: typically Annual Income and Spending Score for this problem
    X = df[['Annual Income (k$)', 'Spending Score (1-100)']]
    
    # Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    joblib.dump(scaler, 'models/scaler.pkl')
    
    return X, X_scaled, df

def train_and_evaluate(X, X_scaled):
    best_score = -1
    best_model = None
    best_name = ""
    
    # K-Means Evaluation
    for n_clusters in range(3, 8):
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        score = silhouette_score(X_scaled, labels)
        if score > best_score:
            best_score = score
            best_model = kmeans
            best_name = f"K-Means (k={n_clusters})"
            
    print(f"Best Model Evaluated: {best_name} with Silhouette Score: {best_score:.4f}")
    
    # Since we need to predict on new data in the web app, K-Means is preferred.
    # The elbow method typically points to 5 clusters for this dataset.
    print("Training final K-Means model with 5 clusters for production...")
    
    final_kmeans = KMeans(n_clusters=5, init='k-means++', random_state=42, n_init=10)
    final_kmeans.fit(X_scaled)
    
    joblib.dump(final_kmeans, 'models/clustering_model.pkl')
    print("Model saved to 'models/clustering_model.pkl'")
    
    return final_kmeans

if __name__ == "__main__":
    print("Starting Machine Learning Pipeline...")
    X, X_scaled, df = prepare_data()
    train_and_evaluate(X, X_scaled)
    print("Pipeline completed.")
