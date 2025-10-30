# app.py - PHIÊN BẢN CUỐI CÙNG VÀ HOÀN CHỈNH NHẤT
# Tác giả: AI Assistant & Hướng dẫn của bạn

import streamlit as st
import pandas as pd
from supabase import create_client, Client
import json
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# PHẦN 1: CÁC HÀM HỖ TRỢ GIAO DIỆN (UI HELPERS)
# ==============================================================================

def show_welcome_page():
    """
    Hàm này chứa TẤT CẢ MỌI THỨ cho trang chào mừng:
    Cả hiệu ứng nền sao chổi, style CSS, và nội dung HTML.
    Nút GitHub đã được xóa.
    """
    welcome_html = """
    <style>
        /* === Hiệu ứng Nền Sao Chổi === */
        .stars-container {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: -1; overflow: hidden; pointer-events: none;
        }
        @keyframes animStar {
            from { transform: translate(-200px, -200px); opacity: 0; }
            to { transform: translate(calc(100vw + 200px), calc(100vh + 200px)); opacity: 1; }
        }
        .shooting-star {
            position: absolute; width: 2px; height: 200px;
            background: linear-gradient(45deg, rgba(150, 150, 150, 0.5), rgba(150, 150, 150, 0));
            animation-name: animStar; animation-timing-function: linear; animation-iteration-count: infinite;
            filter: drop-shadow(0 0 6px rgba(150, 150, 150, 0.3));
        }

        /* === Style cho Trang Chào mừng === */
        @keyframes appear { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .welcome-container { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 3rem 1rem; }
        .welcome-title { font-size: 3.5rem; font-weight: 700; background: linear-gradient(90deg, #1E293B, #64748B); -webkit-background-clip: text; background-clip: text; color: transparent; animation: appear 0.5s ease-out forwards; padding-bottom: 1rem; }
        .welcome-description { max-width: 600px; font-size: 1.125rem; color: #475569; animation: appear 0.5s ease-out 100ms forwards; opacity: 0; margin-bottom: 2rem; }
        .mockup-frame { position: relative; margin-top: 4rem; border-radius: 0.75rem; background: #F8FAFC; padding: 0.75rem; border: 1px solid #E2E8F0; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); animation: appear 0.5s ease-out 700ms forwards; opacity: 0; }
        .glow-effect { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80%; height: 80%; background: radial-gradient(ellipse at center, rgba(79, 70, 229, 0.15) 10%, rgba(255, 255, 255, 0) 60%); filter: blur(40px); z-index: -1; }
        .welcome-image { border-radius: 0.25rem; width: 100%; max-width: 800px; }
    </style>

    <!-- HTML cho Hiệu ứng nền -->
    <div class="stars-container">
        <script>
            const starsContainer = document.querySelector('.stars-container');
            if (starsContainer && starsContainer.childElementCount === 0) {
                const numStars = 20;
                for (let i = 0; i < numStars; i++) {
                    const star = document.createElement('div');
                    star.className = 'shooting-star';
                    star.style.top = (Math.random() * 150 - 50) + 'vh';
                    star.style.left = (Math.random() * 150 - 50) + 'vw';
                    star.style.animationDuration = (Math.random() * 2 + 1) + 's';
                    star.style.animationDelay = (Math.random() * 3) + 's';
                    starsContainer.appendChild(star);
                }
            }
        </script>
    </div>

    <!-- HTML cho Nội dung Trang -->
    <div class="welcome-container">
        <h1 class="welcome-title">Chào mừng đến với Trình tạo Dashboard bằng AI</h1>
        <p class="welcome-description">
            Biến dữ liệu của bạn thành câu chuyện chỉ trong vài phút. Ứng dụng này sử dụng một chuỗi các Agent AI thông minh để tự động hóa toàn bộ quy trình, từ phân tích dữ liệu đến thiết kế một dashboard chuyên nghiệp và có tính tương tác cao.
        </p>

        <div class="mockup-frame">
            <div class="glow-effect"></div>
            <img src="https://www.launchuicomponents.com/app-dark.png" class="welcome-image" alt="Dashboard Preview">
        </div>

        <div style="height: 100px;"></div>

        <div class="welcome-description">
             <p>👉 Để bắt đầu, hãy sử dụng bot Telegram để gửi dữ liệu và yêu cầu của bạn. Hệ thống N8N sẽ tự động tạo một ID và đường link dashboard dành riêng cho bạn.</p>
             <p style="background-color: #F1F5F9; padding: 0.5rem; border-radius: 0.5rem; color: #334155;">Ví dụ về một đường link hợp lệ: <b>/?dashboard_id=dash-abc-123</b></p>
        </div>
    </div>
    """
    st.markdown(welcome_html, unsafe_allow_html=True)

def generate_dashboard_theme_css(theme_config):
    typography = theme_config.get('typography', {})
    font_family = typography.get('fontFamily', 'sans-serif')
    header_size = typography.get('headerSize', '28px')
    body_size = typography.get('bodySize', '16px')

    font_import_url = ""
    if "sans-serif" not in font_family and "monospace" not in font_family:
        font_url_name = font_family.split(',')[0].replace(' ', '+')
        font_import_url = f"@import url('https://fonts.googleapis.com/css2?family={font_url_name}:wght@400;700&display=swap');"

    css = f"""
        <style>
            {font_import_url}
            body, .stApp {{
                font-family: {font_family} !important;
                background-color: {theme_config.get('backgroundColor', '#FFFFFF')};
                color: {theme_config.get('textColor', '#000000')};
            }}
            h1, .stHeadingContainer h1 {{ font-size: {header_size} !important; font-weight: 700; }}
            h2, h3 {{ font-size: calc({header_size} * 0.8) !important; font-weight: 700; }}
            .stMarkdown, p, div, span, label, th, td, .stButton button {{ font-size: {body_size} !important; }}
            .stDataFrame, .stPlotlyChart, .stMetric, [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stHorizontalBlock"] {{
                background-color: rgba(128, 128, 128, 0.1); border: 1px solid {theme_config.get('primaryColor', '#CCCCCC')}33;
                border-radius: 10px; padding: 1rem; box-shadow: 0 0 15px {theme_config.get('primaryColor', '#CCCCCC')}1A; margin-bottom: 1rem;
            }}
            .stMetric > div:nth-child(2) {{ color: {theme_config.get('primaryColor', '#0000FF')}; }}
        </style>
    """
    return css

# ==============================================================================
# PHẦN 2: CÁC HÀM XỬ LÝ DỮ LIỆU VÀ "CỖ MÁY VẼ"
# ==============================================================================

st.set_page_config(layout="wide", page_title="AI-Generated Dashboard")

@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Lỗi kết nối Supabase. Vui lòng kiểm tra file Secrets. Lỗi: {e}")
        return None

supabase = init_connection()

@st.cache_data(ttl=300)
def load_dashboard_data(_dashboard_id):
    if not _dashboard_id or not supabase: return None, None
    try:
        config_response = supabase.table("dashboards").select("config").eq("id", _dashboard_id).single().execute()
        data_response = supabase.table("user_data").select("*").eq("dashboard_id", _dashboard_id).execute()

        if not config_response.data or not data_response.data: return None, None

        dashboard_config = config_response.data['config']
        df = pd.DataFrame(data_response.data)
        
        for col in df.columns:
            if 'date' in col or 'time' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
        return dashboard_config, df
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu cho dashboard ID '{_dashboard_id}'. Lỗi: {e}")
        return None, None

def render_dashboard(config, df):
    # Áp dụng theme CSS cho dashboard
    for element in config:
        if element.get("type") == "theme_config":
            css_style = generate_dashboard_theme_css(element.get("config", {}))
            st.markdown(css_style, unsafe_allow_html=True)

    # Render các thành phần UI
    for element in config:
        el_type = element.get("type")

        if el_type == "header": st.header(element.get("text", ""))
        elif el_type == "markdown": st.markdown(element.get("text", ""))
        elif el_type == "metric": st.metric(label=element.get("label", ""), value=f"{df[element.get('column')].sum():,}")
        elif el_type in ["bar_chart", "line_chart", "area_chart"]:
            st.subheader(element.get("title", ""))
            chart_func = getattr(px, el_type.replace('_', ''))
            fig = chart_func(df, x=element.get("x"), y=element.get("y"), title="")
            st.plotly_chart(fig, use_container_width=True)
        elif el_type == "donut_chart":
            st.subheader(element.get("title", ""))
            fig = px.pie(df, names=element.get("label_column"), values=element.get("value_column"), hole=0.5, title="")
            st.plotly_chart(fig, use_container_width=True)
        elif el_type == "table":
            st.subheader(element.get("title", "Dữ liệu chi tiết"))
            st.dataframe(df)
        # Các loại biểu đồ khác có thể thêm vào đây
            
# ==============================================================================
# PHẦN 3: CHƯƠNG TRÌNH CHÍNH (MAIN EXECUTION) - PHIÊN BẢN CUỐI CÙNG
# ==============================================================================

dashboard_id = st.query_params.get("dashboard_id")

if not dashboard_id:
    show_welcome_page()
else:
    with st.spinner('Đang tải dữ liệu và bản thiết kế...'):
        dashboard_config, df = load_dashboard_data(dashboard_id)

    if dashboard_config and df is not None and not df.empty:
        render_dashboard(dashboard_config, df)
    else:
        st.error(f"Rất tiếc, không thể tải được dashboard với ID: `{dashboard_id}`. Vui lòng kiểm tra lại ID hoặc đảm bảo dashboard đã được tạo thành công.")
