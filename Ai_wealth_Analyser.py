import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from sklearn.linear_model import LinearRegression

# 1. Page Config
st.set_page_config(page_title="AI Wealth Visualizer", layout="wide")
st.title("📈 AI-Powered Financial Strategy & Visualization")

# 2. Sidebar Inputs
st.sidebar.header("📝 Financial Profile")
income = st.sidebar.number_input("Monthly Income ($)", value=5000, step=100)
expenses = st.sidebar.number_input("Current Monthly Spending ($)", value=3200, step=100)
target_savings = st.sidebar.number_input("Target Monthly Savings ($)", value=1000, step=50)

# 3. AI Prediction Logic
@st.cache_data
def get_ai_prediction(inc, exp):
    # Mock training data: Higher income + controlled spending = higher suggested budget
    X = np.array([[2000, 1800], [4000, 3200], [6000, 4500], [10000, 7000]])
    y = np.array([1700, 3100, 4800, 7500])
    model = LinearRegression().fit(X, y)
    return model.predict([[inc, exp]])[0]

# 4. Action Button
if st.button("📊 Analyze & Visualize My Future"):
    with st.status("Analyzing trends...", expanded=True) as status:
        st.write("Running Linear Regression on spending patterns...")
        time.sleep(1)
        suggested_budget = get_ai_prediction(income, expenses)
        
        st.write("Calculating 12-month wealth projection...")
        time.sleep(1)
        status.update(label="Analysis Complete!", state="complete", expanded=False)

    # --- VISUALIZATION SECTION ---
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("🎯 Suggested Budget Allocation")
        # Pie Chart Data
        pie_data = pd.DataFrame({
            "Category": ["Necessities", "Leisure", "Investment/Savings"],
            "Amount": [suggested_budget * 0.5, suggested_budget * 0.3, (income - suggested_budget)]
        })
        fig_pie = px.pie(pie_data, values='Amount', names='Category', 
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("🚀 12-Month Savings Forecast")
        # Line Chart Data (Projection)
        months = ["Month " + str(i) for i in range(1, 13)]
        monthly_surplus = income - suggested_budget
        cumulative_savings = np.cumsum([monthly_surplus] * 12)
        
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=months, y=cumulative_savings, 
                                      mode='lines+markers', name='Wealth Growth',
                                      line=dict(color='firebrick', width=4)))
        fig_line.update_layout(xaxis_title="Timeline", yaxis_title="Total Savings ($)")
        st.plotly_chart(fig_line, use_container_width=True)

    # 5. Key Metrics Summary
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Recommended Spend", f"${suggested_budget:,.2f}", f"{(suggested_budget/income)*100:.1f}% of Income")
    m2.metric("Monthly Surplus", f"${income - suggested_budget:,.2f}", "Available for Growth", delta_color="normal")
    m3.metric("Annual Net Worth Gain", f"${(income - suggested_budget)*12:,.2f}")

else:
    st.info("👋 Welcome! Adjust your details in the sidebar and click the button to see your AI-generated financial roadmap.")

