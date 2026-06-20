import pandas as pd
import numpy as np

def generate_mall_customers(n_samples=200):
    np.random.seed(42)
    
    # Generate CustomerID
    customer_ids = range(1, n_samples + 1)
    
    # Generate Gender
    genders = np.random.choice(['Male', 'Female'], size=n_samples, p=[0.44, 0.56])
    
    # Generate Age (18 to 70)
    ages = np.random.randint(18, 71, size=n_samples)
    
    # Generate Annual Income (15k to 137k)
    incomes = np.random.randint(15, 138, size=n_samples)
    
    # Generate Spending Score (1 to 100)
    spending_scores = np.random.randint(1, 101, size=n_samples)
    
    # Introduce some correlations to mimic the typical Kaggle dataset 
    # (e.g., specific clusters of income/spending)
    for i in range(n_samples):
        # Cluster: High Income, High Spending
        if i % 5 == 0:
            incomes[i] = np.random.randint(70, 138)
            spending_scores[i] = np.random.randint(70, 101)
        # Cluster: High Income, Low Spending
        elif i % 5 == 1:
            incomes[i] = np.random.randint(70, 138)
            spending_scores[i] = np.random.randint(1, 40)
        # Cluster: Low Income, High Spending
        elif i % 5 == 2:
            incomes[i] = np.random.randint(15, 40)
            spending_scores[i] = np.random.randint(60, 101)
        # Cluster: Low Income, Low Spending
        elif i % 5 == 3:
            incomes[i] = np.random.randint(15, 40)
            spending_scores[i] = np.random.randint(1, 40)
        # Cluster: Average Income, Average Spending
        else:
            incomes[i] = np.random.randint(40, 70)
            spending_scores[i] = np.random.randint(40, 60)
            
    df = pd.DataFrame({
        'CustomerID': customer_ids,
        'Gender': genders,
        'Age': ages,
        'Annual Income (k$)': incomes,
        'Spending Score (1-100)': spending_scores
    })
    
    # Shuffle the dataset to avoid perfect ordering of clusters
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df['CustomerID'] = range(1, n_samples + 1)
    
    return df

if __name__ == '__main__':
    df = generate_mall_customers()
    df.to_csv('Mall_Customers.csv', index=False)
    print("Dataset generated successfully as 'Mall_Customers.csv'")
