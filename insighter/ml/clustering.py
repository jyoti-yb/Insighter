from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def cluster_users(df, features=['sessions', 'time_spent', 'clicks'], n_clusters=3, return_labels=False):
    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    km = KMeans(n_clusters=n_clusters, random_state=42)
    labels = km.fit_predict(X_scaled)
    df['cluster'] = labels
    return (df, labels) if return_labels else df
