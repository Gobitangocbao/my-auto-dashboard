# app.py - PHIÊN BẢN CUỐI CÙNG VÀ HOÀN CHỈNH NHẤT
# Tác giả: AI Assistant & Hướng dẫn của bạn

import streamlit as st
import pandas as pd
from supabase import create_client, Client
import json
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# HÀM HIỂN THỊ TRANG CHÀO MỪNG VỚI HIỆU ỨNG "SPARKLES" (V4.0)
# ==============================================================================
def show_welcome_page():
    """
    Hàm này chứa TẤT CẢ MỌI THỨ cho trang chào mừng mới:
    Hiệu ứng nền "Sparkles" (hạt lấp lánh), theme tối, và nội dung theo yêu cầu.
    """
    welcome_html_and_effects = """
    <style>
        /* --- Style CỐ ĐỊNH theme tối cho trang chào mừng --- */
        body, .stApp {
            background-color: #000000 !important; /* Nền đen tuyền */
            color: #E0E0E0 !important;
            overflow: hidden; /* Ngăn cuộn trang để hiệu ứng đẹp hơn */
        }

        /* === Hiệu ứng Nền "Sparkles" MỚI === */
        .sparkles-container {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: 1; /* Nằm ngay dưới nội dung */
            overflow: hidden;
            pointer-events: none; /* Cho phép click xuyên qua lớp hiệu ứng */
        }
        @keyframes sparkle-effect {
            0%, 100% { opacity: 0; transform: scale(0.5) rotate(0deg); }
            50% { opacity: 1; transform: scale(1) rotate(180deg); }
        }
        .sparkle {
            position: absolute;
            background-color: white;
            border-radius: 50%;
            animation-name: sparkle-effect;
            animation-timing-function: ease-in-out;
            animation-iteration-count: infinite;
        }

        /* === Style cho Nội dung Trang Chào mừng === */
        .welcome-content-container {
            position: relative; /* Bắt buộc để z-index có hiệu lực */
            z-index: 2; /* Nằm TRÊN lớp hiệu ứng */
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            height: 90vh; /* Chiếm gần toàn bộ chiều cao màn hình */
            padding: 2rem;
        }
        .welcome-title {
            font-size: 3rem; /* 48px */
            font-weight: 700;
            color: #FFFFFF;
            margin-bottom: 1rem;
        }
        .welcome-description {
            max-width: 600px;
            font-size: 1.125rem; /* 18px */
            color: #A1A1AA; /* Màu xám nhạt */
            line-height: 1.6;
        }
    </style>

    <!-- HTML cho Hiệu ứng nền -->
    <div class="sparkles-container">
        <script>
            // Bọc script trong trình lắng nghe sự kiện để đảm bảo nó chạy đúng lúc
            document.addEventListener('DOMContentLoaded', function() {
                const container = document.querySelector('.sparkles-container');
                // Chỉ chạy nếu container tồn tại và chưa có hạt nào
                if (container && container.childElementCount === 0) {
                    const numSparkles = 80; // Số lượng hạt lấp lánh
                    for (let i = 0; i < numSparkles; i++) {
                        const sparkle = document.createElement('div');
                        sparkle.className = 'sparkle';
                        const size = Math.random() * 2 + 1; // Kích thước ngẫu nhiên (1-3px)
                        sparkle.style.width = size + 'px';
                        sparkle.style.height = size + 'px';
                        sparkle.style.top = Math.random() * 100 + '%';
                        sparkle.style.left = Math.random() * 100 + '%';
                        sparkle.style.animationDuration = (Math.random() * 3 + 2) + 's'; // Tốc độ lấp lánh (2-5s)
                        sparkle.style.animationDelay = Math.random() * 5 + 's';
                        container.appendChild(sparkle);
                    }
                }
            });
        </script>
    </div>

    <!-- HTML cho Nội dung Trang -->
    <div class="welcome-content-container">
        <h1 class="welcome-title">Chào mừng đến với Trình tạo Dashboard bằng AI</h1>
        <p class="welcome-description">
            Biến dữ liệu của bạn thành câu chuyện chỉ trong vài phút. Ứng dụng này sử dụng một chuỗi các Agent AI thông minh để tự động hóa toàn bộ quy trình.
        </p>
    </div>
    """
    st.markdown(welcome_html_and_effects, unsafe_allow_html=True)
    
def generate_dashboard_theme_css(theme_config):
    # Hàm này không thay đổi
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
            
# ==============================================================================
# PHẦN 3: CHƯƠNG TRÌNH CHÍNH (MAIN EXECUTION)
# ==============================================================================

if not supabase:
    st.error("Lỗi kết nối Supabase. Vui lòng kiểm tra lại cấu hình Secrets trên Streamlit Cloud.")
else:
    dashboard_id = st.query_params.get("dashboard_id")
    if not dashboard_id:
        show_welcome_page()
    else:
        with st.spinner('Đang tải dữ liệu và bản thiết kế...'):
            dashboard_config, df = load_dashboard_data(dashboard_id)

        if dashboard_config and df is not None and not df.empty:
            render_dashboard(dashboard_config, df)
        else:
            st.error(f"Rất tiếc, không thể tải được dashboard với ID: `{dashboard_id}`. Vui lòng kiểm tra lại ID.")
