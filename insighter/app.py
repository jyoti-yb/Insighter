from flask import Flask, render_template
import pandas as pd
from ml.clustering import cluster_users
from ml.association import find_patterns
from ml.shapley import generate_shap_plot
from db import fetch_user_data, store_clusters

app = Flask(__name__)

@app.route("/")
def index():
    df = fetch_user_data()

    if df.empty or df[["sessions", "time_spent", "clicks"]].dropna().shape[0] == 0:
      return "No valid user data available yet. Please ingest Mixpanel JSON first."


    # Clustering
    clustered_df, cluster_labels = cluster_users(df, return_labels=True)
    store_clusters(cluster_labels, df["id"].tolist())

    # Association rules
    action_lists = df['actions'].apply(lambda x: x.split(';'))
    rules = find_patterns(action_lists)

    # SHAP plot
    shap_path = generate_shap_plot(df)

    return render_template("index.html",
                           tables=[clustered_df.head().to_html(classes='data')],
                           titles=clustered_df.columns.values,
                           rules=rules.to_html(classes='data'),
                           shap_plot=shap_path)

if __name__ == "__main__":
    app.run(debug=True)
