import requests
import streamlit as st
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def handle_response(response):
    if response.status_code == 404:
        raise ValueError('Product not found.')
    response.raise_for_status()
    return response.json()

def get_health():
    response = requests.get(f"{API_BASE_URL}/health")
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl=300)
def get_product(product_id):
    response = requests.get(f'{API_BASE_URL}/products/{product_id}')
    return handle_response(response)

@st.cache_data(ttl=300)
def get_product_analytics(product_id):
    response = requests.get(f'{API_BASE_URL}/products/{product_id}/analytics')
    return handle_response(response)

def get_recommendations(product_id, limit = 5):
    response = requests.get(f'{API_BASE_URL}/recommendations/{product_id}', params = {'limit' : limit})
    return handle_response(response)

def get_anomaly(product_id):
    response = requests.get(f'{API_BASE_URL}/anomalies/{product_id}')
    return handle_response(response)

def predict_sentiment(text):
    response = requests.post(f'{API_BASE_URL}/sentiment', json = {'text' : text})
    return handle_response(response)