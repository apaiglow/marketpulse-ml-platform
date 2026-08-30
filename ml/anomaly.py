from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

anomaly_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', IsolationForest(contamination = 'auto', random_state = 42))
])