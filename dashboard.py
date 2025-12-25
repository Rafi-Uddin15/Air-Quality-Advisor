import streamlit as st
import pandas as pd
import time
import os
import plotly.graph_objects as go
from advisor import advisor

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AirMonitor Pro",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    /* 1. Global Reset & Gradient Background */
    .stApp {
        background: radial-gradient(circle at top left, #1b2735 0%, #090a0f 100%);
        color: #e0e0e0;
    }
    
    /* 2. Glassmorphism Card System */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow: 0 12px 40px 0 rgba(0, 190, 255, 0.1);
    }

    /* 3. Typography & Headers */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        background: -webkit-linear-gradient(120deg, #ffffff, #89f7fe, #66a6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    p.subtitle {
        color: #8899a6;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    /* 4. Pulse Animation for "Live" Status */
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(0, 230, 118, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(0, 230, 118, 0); }
        100% { box-shadow: 0 0 0 0 rgba(0, 230, 118, 0); }
    }
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #00e676;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse-green 2s infinite;
    }

    /* 5. Custom Widgets (Buttons, Sliders) */
    .stButton > button {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: #00d2ff !important;
        border-radius: 12px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background: rgba(0, 210, 255, 0.15) !important;
        border-color: #00d2ff !important;
        color: #fff !important;
    }
    
    /* Hide Streamlit Cruft */
    #MainMenu, footer, .stDeployButton { visibility: hidden; }
    
    /* Metric Value Styling */
    .hero-metric {
        font-size: 3rem;
        font-weight: 700;
        color: #fff;
    }
    .metric-unit {
        font-size: 1.2rem;
        color: #aaa;
        font-weight: 400;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def get_status_color(aqi):
    if aqi <= 50: return "#00e676"  # Safe Green
    if aqi <= 100: return "#ffea00" # Caution Yellow
    if aqi <= 150: return "#ff9100" # Warning Orange
    if aqi <= 200: return "#ff3d00" # Danger Red
    return "#d500f9"               # Hazardous Purple

LOG_FILE = "air_quality_log.csv"

def load_data():
    if not os.path.exists(LOG_FILE):
        return None
    try:
        # Simple robust read
        df = pd.read_csv(LOG_FILE)
        return df
    except Exception as e:
        return None

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("<h1><span class='live-indicator'></span>Intelligent Air Monitor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>AI-Powered Indoor Environmental Analysis System</p>", unsafe_allow_html=True)
with col_head2:
    if st.button("🔄 System Refresh"):
        st.rerun()

# --- MAIN CONTENT ---
placeholder = st.empty()

# The container loop logic
with placeholder.container():
    df = load_data()
    
    # Defaults
    temp, hum, mq135, predicted_aqi = 0, 0, 0, 0
    advice_cat, advice_text = "OFFLINE", "Waiting for sensor data stream..."
    
    if df is not None and not df.empty:
        try:
            latest = df.iloc[-1]
            temp = float(latest['temperature_c'])
            hum = float(latest['humidity_pct'])
            mq135 = float(latest['mq135_raw'])
            predicted_aqi = advisor.predict_aqi(mq135, temp, hum)
            advice_cat, advice_text = advisor.get_advice(predicted_aqi)
        except Exception as e:
            advice_cat = "ERROR"
            advice_text = "Data formatting issue."

    # --- ROW 1: METRICS GRID ---
    m1, m2, m3, m4 = st.columns(4)
    
    # Helper to draw metric cards
    def metric_card(col, title, value, unit, icon, color):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="padding: 15px; text-align: center; border-bottom: 3px solid {color};">
                <div style="font-size: 2rem; margin-bottom: 5px;">{icon}</div>
                <div style="color: #aaa; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">{title}</div>
                <div class="hero-metric">{value}<span class="metric-unit">{unit}</span></div>
            </div>
            """, unsafe_allow_html=True)

    metric_card(m1, "Temperature", f"{temp:.0f}", "°C", "🌡️", "#ff5252")
    metric_card(m2, "Humidity", f"{hum:.0f}", "%", "💧", "#448aff")
    metric_card(m3, "Air Quality", f"{predicted_aqi:.0f}", " AQI", "🍃", get_status_color(predicted_aqi))
    metric_card(m4, "Sensor Raw", f"{int(mq135)}", " Ω", "⚡", "#ffd740")

    # --- ROW 2: VISUALIZATION & INTELLIGENCE ---
    c_gauge, c_advice = st.columns([1, 2])
    
    with c_gauge:
        # Clean Gauge Implementation
        color = get_status_color(predicted_aqi)
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", 
            value = predicted_aqi,
            number = {'font': {'size': 40, 'color': "white"}, 'suffix': " AQI"},
            gauge = {
                'axis': {'range': [None, 300], 'visible': True, 'tickwidth': 1, 'tickcolor': "white", 'tickmode': "array", 'tickvals': [0, 50, 100, 150, 200, 300], 'ticktext': ['0', 'Good', 'Mod', 'Unhealthy', 'Dang', 'Max']},
                'bar': {'color': color, 'thickness': 0.75}, 
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 0,
                'steps': [{'range': [0, 300], 'color': "rgba(255,255,255,0.05)"}],
            }))
            
        # We simulate the card look using the Plotly background directly
        fig_gauge.update_layout(
            font = {'color': "white", 'family': "Inter"}, 
            height=320, 
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor='rgba(255,255,255,0.03)', # Glass effect built-in to chart
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with c_advice:
        # Premium Advice Card
        color = get_status_color(predicted_aqi)
        
        # IMPORTANT: NO INDENTATION in the HTML string to avoid Code Block rendering
        html_content = f"""
<div class="glass-card" style="height: 320px; position: relative;">
<div style="position: absolute; top: 20px; right: 20px; color: rgba(255,255,255,0.3); font-size: 0.8rem;">
AI MODEL V1.0 • UPDATED {time.strftime("%H:%M:%S")}
</div>
<h3 style="color: {color}; margin-bottom: 5px;">AI DIAGNOSIS: {advice_cat}</h3>
<div style="height: 2px; width: 100px; background: {color}; margin-bottom: 20px;"></div>
<p style="font-size: 1.5rem; line-height: 1.6; color: #fff; font-weight: 300; margin-top: 30px;">
"{advice_text}"
</p>
<div style="margin-top: 40px; display: flex; gap: 10px;">
<div style="background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 15px; font-size: 0.8rem;">House: Indoor</div>
<div style="background: rgba(255,255,255,0.1); padding: 5px 15px; border-radius: 15px; font-size: 0.8rem;">Sensor: Online</div>
</div>
</div>
"""
        st.markdown(html_content, unsafe_allow_html=True)

    # --- ROW 3: DEEP DIVE HISTORY ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c_tools1, c_tools2 = st.columns([3, 1])
    
    with c_tools1:
        st.markdown("### 🔍 Historical Analysis Trend")
        
    with c_tools2:
        # Compact segmented control
        metric_view = st.radio("Overlay Metric", ["Temperature", "Humidity"], horizontal=True, label_visibility="collapsed")

    if df is not None and not df.empty:
        chart_df = df.tail(100).reset_index(drop=True)
        
        fig = go.Figure()
        
        # AQI Area Chart
        fig.add_trace(go.Scatter(
            y=chart_df['mq135_raw'],
            name="Pollutants",
            fill='tozeroy',
            line=dict(color='#00d2ff', width=2),
            fillcolor='rgba(0, 210, 255, 0.15)'
        ))
        
        # Overlay Line
        sec_y = chart_df['temperature_c'] if metric_view == "Temperature" else chart_df['humidity_pct']
        sec_color = '#ff5252' if metric_view == "Temperature" else '#448aff'
        
        fig.add_trace(go.Scatter(
            y=sec_y,
            name=metric_view,
            yaxis="y2",
            line=dict(color=sec_color, width=3)
        ))
        
        fig.update_layout(
            height=300,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#888'),
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(showgrid=False, title='Time Steps'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            yaxis2=dict(overlaying='y', side='right', showgrid=False),
            hovermode="x unified",
            legend=dict(orientation="h", y=1.1, x=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Action Bar in Footer
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        row_act1, row_act2 = st.columns([4, 1])
        with row_act1:
            st.caption("Data logging remotely. Showing last 100 points.")
        with row_act2:
             csv = chart_df.to_csv(index=False)
             st.download_button("📥 Export CSV", data=csv, file_name="aqi_data.csv", mime="text/csv")
            
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. Non-Blocking Refresh Loop
    time.sleep(2)
    st.rerun()
