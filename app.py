# app.py - The Universal Dashboard Rendering Engine V2.0
# Tác giả: AI Assistant & Hướng dẫn của bạn

import streamlit as st
import pandas as pd
from supabase import create_client, Client
import json
import plotly.express as px
import plotly.graph_objects as go

# ==============================================================================
# KHỐI CODE TẠO HIỆU ỨNG NỀN ĐỘNG BẰNG CSS
# ==============================================================================
def animated_background():
    css_code = """
    <style>
        /* CSS để tạo một canvas trống nằm dưới cùng */
        .background-canvas {
            position: fixed; /* Cố định vị trí */
            top: 0;
            left: 0;
            width: 100vw; /* Chiếm toàn bộ chiều rộng */
            height: 100vh; /* Chiếm toàn bộ chiều cao */
            z-index: -1;  /* ĐÂY LÀ ĐIỀU QUAN TRỌNG NHẤT: Đảm bảo nó nằm dưới mọi thứ khác */
            overflow: hidden;
        }
        
        /* CSS cho các đường kẻ động */
        @keyframes move {
            0% {
                transform: translateX(0);
            }
            100% {
                transform: translateX(-100%);
            }
        }
        .line {
            position: absolute;
            height: 1px;
            background: linear-gradient(90deg, rgba(200,200,200,0), rgba(200,200,200,0.5), rgba(200,200,200,0));
            animation: move linear infinite;
        }
    </style>
    
    <div class="background-canvas">
        <script>
            // JavaScript để tạo ra nhiều đường kẻ ngẫu nhiên
            const container = document.querySelector('.background-canvas');
            for (let i = 0; i < 50; i++) {
                const line = document.createElement('div');
                line.className = 'line';
                line.style.top = Math.random() * 100 + 'vh';
                line.style.width = Math.random() * 50 + 50 + 'vw';
                line.style.animationDuration = (Math.random() * 20 + 20) + 's';
                line.style.animationDelay = Math.random() * -40 + 's'; // Bắt đầu ở các vị trí khác nhau
                container.appendChild(line);
            }
        </script>
    </div>
    """
    st.markdown(css_code, unsafe_allow_html=True)

# ==============================================================================
# KHỐI CODE TẠO HIỆU ỨNG VIỀN CẦU VỒNG PHÁT SÁNG
# ==============================================================================
def glowing_border_css():
    css_code = """
    <style>
        @keyframes rotate_glow {
            0% {
                transform: rotate(0deg);
            }
            100% {
                transform: rotate(360deg);
            }
        }

        .glowing-card {
            position: relative; /* Bắt buộc để định vị cho viền phát sáng */
            background-color: #1a1a1a; /* Màu nền cho thẻ, bạn có thể thay đổi */
            border-radius: 1.25rem; /* Bo góc giống với ví dụ */
            padding: 2rem; /* Khoảng đệm bên trong thẻ */
            margin-bottom: 1.5rem; /* Khoảng cách giữa các thẻ */
            overflow: hidden; /* Cần thiết để viền không bị tràn ra ngoài */
        }

        .glowing-card::before {
            content: '';
            position: absolute;
            left: -2px; /* Dịch ra ngoài một chút để không bị che */
            top: -2px;
            width: calc(100% + 4px); /* Lớn hơn thẻ một chút */
            height: calc(100% + 4px);
            
            /* Dải màu cầu vồng */
            background: conic-gradient(
                from 180deg at 50% 50%,
                #DD7BBB 0%,
                #D79F1E 25%,
                #5A922C 50%,
                #4C7894 75%,
                #DD7BBB 100%
            );
            
            z-index: 1; /* Nằm ngay sau nội dung thẻ */
            
            /* Animation xoay tròn liên tục */
            animation: rotate_glow 4s linear infinite;
        }

        .glowing-card > div { /* Nhắm vào container nội dung của Streamlit */
            position: relative; /* Đảm bảo nội dung nằm trên viền */
            z-index: 2;
            background-color: inherit; /* Nền của nội dung giống nền thẻ */
            padding: 1rem;
            border-radius: calc(1.25rem - 2px); /* Bo góc nhỏ hơn viền một chút */
        }
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)
# app.py -> Dán hàm mới này vào file của bạn, thay thế cho show_welcome_page cũ

# ==============================================================================
# HÀM HIỂN THỊ TRANG CHÀO MỪNG CHUYÊN NGHIỆP V2.0
# ==============================================================================
def show_professional_welcome_page():
    """
    Tạo một trang chào mừng thanh lịch, chuyên nghiệp, và hiện đại,
    lấy cảm hứng từ các thư viện UI hiện đại như Aceternity và LaunchUI.
    """

    # --- PHẦN 1: BỘ NÃO CSS ---
    # Toàn bộ "phép thuật" nằm ở đây. Chúng ta định nghĩa các style và animation.
    css_style = """
    <style>
        /* Animation cho hiệu ứng xuất hiện mềm mại */
        @keyframes appear {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Container chính để căn giữa mọi thứ */
        .welcome-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        /* Tiêu đề chính với hiệu ứng Gradient */
        .welcome-title {
            font-size: 3.5rem; /* 56px */
            font-weight: 700;
            background: linear-gradient(90deg, #1E293B, #64748B); /* Gradient xám đậm -> xám nhạt */
            -webkit-background-clip: text; /* Yêu cầu cho Chrome/Safari */
            background-clip: text;
            color: transparent;
            animation: appear 0.5s ease-out forwards;
            padding-bottom: 1rem;
        }

        /* Đoạn mô tả phụ */
        .welcome-description {
            max-width: 600px;
            font-size: 1.125rem; /* 18px */
            color: #475569; /* Màu xám nhạt hơn, tương phản vừa phải */
            animation: appear 0.5s ease-out 100ms forwards;
            opacity: 0; /* Ẩn đi lúc đầu để animation hoạt động */
            margin-bottom: 2rem;
        }
        
        /* Container cho các nút bấm */
        .welcome-buttons {
            display: flex;
            gap: 1rem;
            animation: appear 0.5s ease-out 300ms forwards;
            opacity: 0;
        }

        /* Style cho nút bấm (dùng thẻ <a>) */
        .welcome-buttons a {
            text-decoration: none;
            color: #FFFFFF;
            background-color: #0F172A; /* Màu nền đen-xám */
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            font-weight: 500;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .welcome-buttons a:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        
        /* Khung mockup cho hình ảnh */
        .mockup-frame {
            position: relative; /* Bắt buộc để đặt hiệu ứng glow */
            margin-top: 4rem;
            border-radius: 0.75rem; /* bo góc */
            background: #F8FAFC;
            padding: 0.75rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            animation: appear 0.5s ease-out 700ms forwards;
            opacity: 0;
        }
        
        /* Hiệu ứng ánh sáng lan tỏa phía sau hình ảnh */
        .glow-effect {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 80%;
            height: 80%;
            background: radial-gradient(ellipse at center, rgba(79, 70, 229, 0.15) 10%, rgba(255, 255, 255, 0) 60%);
            filter: blur(40px);
            z-index: -1;
        }

        .welcome-image {
            border-radius: 0.25rem;
            width: 100%;
            max-width: 800px;
        }

    </style>
    """
    st.markdown(css_style, unsafe_allow_html=True)
    
    # --- PHẦN 2: BỘ XƯƠNG HTML ---
    # Bây giờ chúng ta sử dụng các class CSS đã định nghĩa ở trên.
    st.markdown("""
    <div class="welcome-container">
        <h1 class="welcome-title">Chào mừng đến với Trình tạo Dashboard bằng AI</h1>
        
        <p class="welcome-description">
            Biến dữ liệu của bạn thành câu chuyện chỉ trong vài phút. Ứng dụng này sử dụng một chuỗi các Agent AI thông minh để tự động hóa toàn bộ quy trình, từ phân tích dữ liệu đến thiết kế một dashboard chuyên nghiệp và có tính tương tác cao.
        </p>

        <div class="welcome-buttons">
            <a href="https://github.com/Gobitangocbao/my-auto-dashboard" target="_blank">GitHub</a>
        </div>
        
        <div class="mockup-frame">
            <div class="glow-effect"></div>
            <img src="https://www.launchuicomponents.com/app-dark.png" class="welcome-image" alt="Dashboard Preview">
        </div>

        <div style="height: 100px;"></div> <!-- Thêm khoảng trống ở cuối -->

        <div class="welcome-description">
             <p>👉 Để bắt đầu, hãy sử dụng bot Telegram để gửi dữ liệu và yêu cầu của bạn. Hệ thống N8N sẽ tự động tạo một ID và đường link dashboard dành riêng cho bạn.</p>
             <p style="background-color: #F1F5F9; padding: 0.5rem; border-radius: 0.5rem; color: #334155;">Ví dụ về một đường link hợp lệ: <b>/?dashboard_id=dash-abc-123</b></p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
# ==============================================================================
# PHẦN 1: CẤU HÌNH TRANG VÀ KẾT NỐI DỮ LIỆU
# ==============================================================================

# Cấu hình layout trang rộng và tiêu đề mặc định
st.set_page_config(layout="wide", page_title="AI-Generated Dashboard")

# Hàm kết nối Supabase, cache lại để tăng hiệu suất
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

# Hàm tải dữ liệu và cấu hình từ Supabase
@st.cache_data(ttl=300) # Cache dữ liệu trong 5 phút
def load_dashboard_data(_dashboard_id):
    if not _dashboard_id or not supabase:
        return None, None
    try:
        config_response = supabase.table("dashboards").select("config").eq("id", _dashboard_id).single().execute()
        data_response = supabase.table("user_data").select("*").eq("dashboard_id", _dashboard_id).execute()

        if not config_response.data or not data_response.data:
            return None, None

        dashboard_config = config_response.data['config']
        df = pd.DataFrame(data_response.data)
        
        # Chuyển đổi các cột ngày tháng để Plotly hiểu đúng
        for col in df.columns:
            if 'date' in col or 'time' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
        return dashboard_config, df
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu cho dashboard ID '{_dashboard_id}'. Lỗi: {e}")
        return None, None

# ==============================================================================
# PHẦN 2: CÁC HÀM HỖ TRỢ VÀ "CỖ MÁY VẼ"
# ==============================================================================

def generate_css_from_theme(theme_config):
    """
    Tạo một chuỗi CSS phức tạp từ object theme để tùy chỉnh toàn diện giao diện,
    bao gồm màu sắc, phông chữ, và kiểu dáng panel.
    """
    # Trích xuất thông tin typography, cung cấp giá trị mặc định nếu không có
    typography = theme_config.get('typography', {})
    font_family = typography.get('fontFamily', 'sans-serif')
    header_size = typography.get('headerSize', '28px')
    body_size = typography.get('bodySize', '16px')
    
    # Tạo URL để import Google Font (nếu cần)
    font_import_url = ""
    if "sans-serif" not in font_family and "monospace" not in font_family:
        font_url_name = font_family.split(',')[0].replace(' ', '+')
        font_import_url = f"@import url('https://fonts.googleapis.com/css2?family={font_url_name}:wght@400;700&display=swap');"

    # Xây dựng chuỗi CSS hoàn chỉnh
    css = f"""
        <style>
            {font_import_url}

            /* Áp dụng font và màu sắc toàn cục */
            body, .stApp {{
                font-family: {font_family} !important;
                background-color: {theme_config.get('backgroundColor', '#FFFFFF')};
                color: {theme_config.get('textColor', '#000000')};
            }}

            /* Tùy chỉnh kích thước cho các tiêu đề */
            h1, .stHeadingContainer h1 {{
                font-size: {header_size} !important;
                font-weight: 700; /* In đậm cho tiêu đề */
            }}
            h2, h3 {{
                font-size: calc({header_size} * 0.8) !important;
                font-weight: 700;
            }}

            /* Tùy chỉnh kích thước cho văn bản thông thường */
            .stMarkdown, p, div, span, label, th, td, .stButton button {{
                font-size: {body_size} !important;
            }}

            /* Định dạng cho các "Card" hoặc "Panel" chứa biểu đồ và nội dung */
            /* Điều này tạo ra hiệu ứng panel phát sáng hoặc có bo góc */
            .stDataFrame, .stPlotlyChart, .stMetric, [data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stHorizontalBlock"] {{
                background-color: rgba(128, 128, 128, 0.1); /* Màu nền bán trong suốt */
                border: 1px solid {theme_config.get('primaryColor', '#CCCCCC')}33; /* Đường viền mờ */
                border-radius: 10px;
                padding: 1rem;
                box-shadow: 0 0 15px {theme_config.get('primaryColor', '#CCCCCC')}1A; /* Hiệu ứng đổ bóng/phát sáng */
                margin-bottom: 1rem;
            }}

            /* Tùy chỉnh riêng cho các thẻ KPI */
            .stMetric > div:nth-child(2) {{
                color: {theme_config.get('primaryColor', '#0000FF')}; /* Màu cho giá trị của KPI */
            }}

        </style>
    """
    return css
def render_dashboard(config, df):
    """
    "CỖ MÁY VẼ": Đọc file JSON và render từng thành phần của dashboard.
    """
    # ----- Vòng lặp 1: Xử lý các Cấu hình Toàn cục -----
    for element in config:
        if element.get("type") == "theme_config":
            css_style = generate_css_from_theme(element.get("config", {}))
            st.markdown(css_style, unsafe_allow_html=True)
            
        if element.get("type") == "special_effect":
            if element.get("effect") == "snow":
                st.snow()
            if element.get("effect") == "balloons":
                st.balloons()
            if element.get("effect") == "custom_css":
                css_payload = element.get("payload", {}).get("description", "") # Note: Đây chỉ là placeholder, logic thực tế sẽ phức tạp hơn
                st.markdown(f"<style>{css_payload}</style>", unsafe_allow_html=True)

    # ----- Vòng lặp 2: Render các Thành phần Giao diện -----
    for element in config:
        el_type = element.get("type")

        # --- Các thành phần cơ bản ---
        if el_type == "header":
            st.header(element.get("text", ""))
        elif el_type == "markdown":
            st.markdown(element.get("text", ""))
        elif el_type == "metric":
            # Nâng cấp để tính toán linh hoạt hơn trong tương lai
            st.metric(label=element.get("label", ""), value=f"{df[element.get('column')].sum():,}")

        # --- Các loại biểu đồ ---
        elif el_type == "bar_chart":
            st.subheader(element.get("title", ""))
            fig = px.bar(df, x=element.get("x"), y=element.get("y"), title="")
            st.plotly_chart(fig, use_container_width=True)
            
        elif el_type == "line_chart":
            st.subheader(element.get("title", ""))
            fig = px.line(df, x=element.get("x"), y=element.get("y"), title="")
            st.plotly_chart(fig, use_container_width=True)
            
        elif el_type == "area_chart":
            st.subheader(element.get("title", ""))
            fig = px.area(df, x=element.get("x"), y=element.get("y"), title="")
            st.plotly_chart(fig, use_container_width=True)

        elif el_type == "donut_chart":
            st.subheader(element.get("title", ""))
            fig = px.pie(df, names=element.get("label_column"), values=element.get("value_column"), hole=0.5, title="")
            st.plotly_chart(fig, use_container_width=True)
            
        elif el_type == "funnel_chart":
            st.subheader(element.get("title", ""))
            fig = px.funnel(df, x=element.get("x_values"), y=element.get("y_stages"), title="")
            st.plotly_chart(fig, use_container_width=True)
            
        elif el_type == "gauge_chart":
            st.subheader(element.get("title", ""))
            value = df[element.get("value_column")].iloc[0] # Lấy giá trị đầu tiên
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = value,
                title = {'text': element.get("title", "")},
                gauge = {
                    'axis': {'range': [element.get("min_value", 0), element.get("max_value", 100)]},
                    'bar': {'color': "darkblue"},
                }))
            st.plotly_chart(fig, use_container_width=True)
            
        elif el_type == "radar_chart":
             st.subheader(element.get("title", ""))
             # Plotly cần data ở định dạng phù hợp cho radar chart
             categories = element.get('categories') # Giả sử Agent4 trả về các cột cần vẽ
             fig = go.Figure()
             for index, row in df.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=[row[cat] for cat in categories],
                    theta=categories,
                    fill='toself',
                    name=row[element.get('name_column')] # Tên của mỗi đường radar
                ))
             st.plotly_chart(fig, use_container_width=True)
             
        elif el_type == "table":
            st.subheader(element.get("title", "Dữ liệu chi tiết"))
            st.dataframe(df)

        # Các loại biểu đồ khác có thể được thêm vào đây theo logic tương tự
            
# ==============================================================================
# PHẦN 3: CHƯƠNG TRÌNH CHÍNH (MAIN EXECUTION)
# ==============================================================================

# ==============================================================================
# Gọi các hàm CSS một lần ở đây
animated_background()
glowing_border_css() # <-- Dòng mới bạn vừa thêm
# ==============================================================================

# Lấy dashboard_id từ tham số URL
dashboard_id = st.query_params.get("dashboard_id")

if not dashboard_id:
    # Chỉ cần gọi hàm mới và chuyên nghiệp hơn của chúng ta ở đây!
    show_professional_welcome_page() 
else:
    # Phần còn lại để xử lý và vẽ dashboard không thay đổi
    with st.spinner('Đang tải dữ liệu và bản thiết kế từ cơ sở dữ liệu...'):
        dashboard_config, df = load_dashboard_data(dashboard_id)

    if dashboard_config and df is not None and not df.empty:
        render_dashboard(dashboard_config, df)
    else:
        st.error(f"Rất tiếc, không thể tải được dashboard với ID: `{dashboard_id}`. Vui lòng kiểm tra lại ID hoặc đảm bảo dashboard đã được tạo thành công.")
