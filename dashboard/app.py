import streamlit as st
from api_client import (get_product, get_product_analytics, get_anomaly, get_recommendations, predict_sentiment)
import plotly.express as px

st.set_page_config(page_title = 'MarketPulse', page_icon = '📊', layout = 'wide')
st.title('MarketPulse')
st.caption('E-Commerce Intelligence Platform')

st.sidebar.title('Navigation')
page = st.sidebar.selectbox('Go to', [
    'Overview', 'Product Explorer', 'Recommendations', 'Sentiment', 'Anomaly Monitor'
])
if page == 'Overview':
    st.header('Overview')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('Products', '112,590')
    with col2:
        st.metric('Reviews', '701,528')
    with col3:
        st.metric('ML Models', '3')
    st.subheader('MarketPulse Architecture')
    st.dataframe({
        'Layer' : [
            'Data',
            'Processing',
            'Machine Learning',
            'Database',
            'API',
            'Frontend'
        ],
        'Technology' : [
            'Amazon Reviews 2023',
            'PySpark',
            'Scikit-learn',
            'PostgreSQL',
            'FastAPI',
            'Streamlit'
        ]
    },
    use_container_width = True)
elif page == 'Product Explorer':
    st.header('Product Explorer')
    product_id = st.text_input('Enter Product ID', placeholder = 'Example : B01CUPMQZE')
    if st.button('Explore Product'):
        if not product_id:
            st.warning('Please enter a product ID.')
        else:
            try:
                product = get_product(product_id)
                analytics = get_product_analytics(product_id)
                st.subheader(product['title'])
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric('Average Rating', product['average_rating'])
                with col2:
                    st.metric('Reviews', analytics['review_count'])
                with col3:
                    st.metric('Unique Users', analytics['unique_user_count'])
                st.subheader('Product Information')
                st.dataframe({
                    'Field' : [
                        'Product ID',
                        'Category',
                        'Price',
                        'Rating Count'
                    ],
                    'Value' : [
                        product['parent_asin'],
                        product['main_category'],
                        product['price'],
                        product['rating_number']
                    ]
                },
                use_container_width = True)
                st.subheader('Product Analytics')
                chart_data = {
                    'Metric' : [
                        'Positive Ratio',
                        'Negative Ratio'
                    ],
                    'Value' : [
                        analytics['positive_ratio'],
                        analytics['negative_ratio']
                    ]
                }
                fig = px.bar(chart_data, x = 'Metric', y = 'Value', title = 'Review Sentiment Distribution', range_y = [0, 1])
                st.plotly_chart(fig, use_container_width = True)
                st.dataframe(analytics, use_container_width = True)
            except Exception as e:
                st.error(f'Unable to retrieve product : {e}')
elif page == 'Recommendations':
    st.header('Product Recommendations')
    product_id = st.text_input('Enter Product ID', placeholder = 'Example : B01CUPMQZE', key = 'recommendation_product_id')
    limit = st.selectbox('Number of recommendations', [3, 5, 10, 15, 20], index = 1)
    if st.button('Get Recommendations'):
        if not product_id:
            st.warning('Please enter a product ID.')
        else:
            try:
                result = get_recommendations(product_id, limit)
                recommendations = result['recommendations']
                if not recommendations:
                    st.info('No recommendations found.')
                else:
                    st.subheader(f'Similar products to {product_id}')
                    st.dataframe(recommendations, use_container_width = True)
            except Exception as e:
                st.error(f'Unable to retrieve recommendations : {e}')
elif page == 'Sentiment':
    st.header('Review Sentiment Analysis')
    review_text = st.text_area('Enter a product review', placeholder = 'Write or paste a product review here...')
    if st.button('Analyze Sentiment'):
        if not review_text.strip():
            st.warning('Please enter a review.')
        else:
            try:
                result = predict_sentiment(review_text)
                sentiment = result['sentiment']
                label = result['label']
                if sentiment == 'positive':
                    st.success('Positive sentiment')
                else:
                    st.error('Negative sentiment')
                col1, col2 = st.columns(2)
                with col1:
                    st.metric('Sentiment', sentiment.upper())
                with col2:
                    st.metric('Model Label', label)
            except Exception as e:
                st.error(f'unable to analyse sentiment : {e}')
elif page == 'Anomaly Monitor':
    st.header('Anomaly Monitor')
    product_id = st.text_input('Enter product ID', placeholder = 'Example : B01CUPMQZE', key = 'anomaly_product_id')
    if st.button('Check Anomaly'):
        if not product_id:
            st.warning('Please enter a product ID.')
        else:
            try:
                result = get_anomaly(product_id)
                prediction = result['anomaly_prediction']
                score = result['anomaly_score']
                col1, col2 = st.columns(2)
                with col1:
                    st.metric('Anomaly Prediction', prediction)
                with col2:
                    st.metric('Anomaly Score', score)
                if prediction == -1:
                    st.warning('This product has an unusual feature profile.')
                else:
                    st.success('this product has a normal feature profile.')
            except Exception as e:
                st.error(f'Unable to retrieve anomaly result : {e}')