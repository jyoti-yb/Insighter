import mysql.connector
from config import MYSQL_CONFIG
import pandas as pd

def get_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

def insert_user_data(rows):
    conn = get_connection()
    cursor = conn.cursor()
    for row in rows:
        cursor.execute("""
            INSERT INTO user_usage (distinct_id, sessions, time_spent, clicks, converted, actions)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, row)
    conn.commit()
    conn.close()

def fetch_user_data():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM user_usage", conn)
    conn.close()
    return df

def store_clusters(cluster_labels, ids):
    conn = get_connection()
    cursor = conn.cursor()
    for user_id, cluster in zip(ids, cluster_labels):
        cursor.execute("INSERT INTO analysis_result (user_id, cluster_label) VALUES (%s, %s)", (user_id, cluster))
    conn.commit()
    conn.close()
