import shap
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import os
import matplotlib.pyplot as plt

def generate_shap_plot(df, label_col='converted', out_file='static/shap_plot.png'):
    os.makedirs('static', exist_ok=True)

    # Prepare the data
    y = df[label_col]
    X = df.drop(columns=[label_col])
    X = X.select_dtypes(include=['number'])

    # Fit model
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)

    # SHAP Explainer
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)

    # ⚠️ Take only class 1 if model is binary classification
    if len(shap_values.values.shape) == 3:
        shap_values = shap_values[:, :, 1]  # class 1 only

    # Plot beeswarm
    plt.figure()
    shap.plots.beeswarm(shap_values, show=False)
    plt.savefig(out_file, bbox_inches='tight')
    plt.close()

    return out_file
