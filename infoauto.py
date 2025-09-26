import streamlit as st 
import pandas as pd 
import plotly.express as px 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import classification_report 

@st.cache_data 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "industrial_fault_detection_data_1000.csv")
@st.cache_data
def load_data():
    df = pd.read_csv(FILE_PATH)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
return df
df = load_data() 
df.columns = df.columns.str.strip().str.replace("Â", "", regex=False) 

st.title("🏭 Manufacturing IoT - Intelligent Automation Dashboard") 
st.sidebar.header("⚙️ Controls") 
n_rows = st.sidebar.slider("Number of rows to display", 10, 100, 20) 
st.subheader("📋 Sample Data") 
st.dataframe(df.head(n_rows)) 

st.subheader("📊 Sensor Trends") 
col1, col2 = st.columns(2) 
with col1: 
    fig1 = px.line(df, x="Timestamp", y="Temperature (°C)", title="Temperature Over Time") 
    st.plotly_chart(fig1, use_container_width=True) 
with col2: 
    fig2 = px.line(df, x="Timestamp", y="Vibration (mm/s)", title="Vibration Over Time") 
    st.plotly_chart(fig2, use_container_width=True) 
fig3 = px.line(df, x="Timestamp", y="Pressure (bar)", title="Pressure Over Time") 
st.plotly_chart(fig3, use_container_width=True) 

def check_alerts(row): 
    alerts = [] 
    if row["Temperature (°C)"] > 100: 
        alerts.append("🔥 Overheating") 
    if row["Vibration (mm/s)"] > 0.9: 
        alerts.append("⚠️ High Vibration") 
    if row["Pressure (bar)"] > 9.5: 
        alerts.append("💨 High Pressure") 
    if row["Fault Label"] != 0: 
        alerts.append(f"❌ Fault Detected (Type {row['Fault Label']})") 
    return "; ".join(alerts) if alerts else "✅ Normal" 
df["Alerts"] = df.apply(check_alerts, axis=1) 
st.subheader("🚨 Live Alerts") 
st.dataframe(df[["Timestamp","Temperature (°C)", "Vibration (mm/s)", "Pressure (bar)", "Alerts"]].tail(10)) 

st.subheader("AI Fault Prediction") 
feature_order = [
    "Vibration (mm/s)", 
    "Temperature (°C)", 
    "Pressure (bar)", 
    "RMS Vibration", 
    "Mean Temp"
]
X = df[feature_order] 
y = df["Fault Label"] 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
model = RandomForestClassifier(n_estimators=100, random_state=42) 
model.fit(X_train, y_train) 
y_pred = model.predict(X_test) 
report = classification_report(y_test, y_pred, output_dict=True) 
report_df = pd.DataFrame(report).transpose() 
st.write("Model Performance:") 
st.dataframe(report_df) 

latest = df.tail(1)
X_latest = latest[feature_order]
latest_pred = model.predict(X_latest) 
st.success(f"🔮 Latest Fault Prediction: Type {latest_pred[0]}")

