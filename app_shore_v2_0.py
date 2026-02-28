# 岸 - 情绪安全表达与轻量匿名社交应用 v2.0
# 全新视觉设计 - 精致、艺术、有温度

import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta
import random
import json
import time

# ==================== 设计系统 ====================
DESIGN_TOKENS = {
    # 主色调 - 温暖治愈的蓝绿色系
    "primary": "#4ECDC4",
    "primary_dark": "#3DBDB5",
    "primary_light": "#7EDDD7",
    "secondary": "#FFE66D",
    "accent": "#FF6B6B",
    
    # 背景色
    "bg_main": "#FAFBFC",
    "bg_card": "#FFFFFF",
    "bg_soft": "#F0F4F8",
    
    # 文字色
    "text_primary": "#2D3748",
    "text_secondary": "#718096",
    "text_light": "#A0AEC0",
    
    # 情绪色彩
    "mood_calm": "#4ECDC4",
    "mood_happy": "#FFE66D",
    "mood_sad": "#95A5A6",
    "mood_angry": "#FF6B6B",
    "mood_love": "#F8B4C0",
    "mood_creative": "#C9B1FF",
    
    # 间距
    "space_xs": "4px",
    "space_sm": "8px",
    "space_md": "16px",
    "space_lg": "24px",
    "space_xl": "32px",
    
    # 圆角
    "radius_sm": "8px",
    "radius_md": "16px",
    "radius_lg": "24px",
    "radius_full": "9999px",
}

# 卡通形象 SVG
MASCOT_SVG = """
<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- 小岸 - 温暖的陪伴者 -->
  <defs>
    <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4ECDC4;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#3DBDB5;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="bellyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:#F0F4F8;stop-opacity:0.9" />
    </linearGradient>
  </defs>
  
  <!-- 身体 -->
  <ellipse cx="100" cy="130" rx="60" ry="55" fill="url(#bodyGrad)"/>
  
  <!-- 肚子 -->
  <ellipse cx="100" cy="140" rx="35" ry="30" fill="url(#bellyGrad)"/>
  
  <!-- 耳朵 -->
  <ellipse cx="55" cy="70" rx="20" ry="25" fill="url(#bodyGrad)" transform="rotate(-20 55 70)"/>
  <ellipse cx="145" cy="70" rx="20" ry="25" fill="url(#bodyGrad)" transform="rotate(20 145 70)"/>
  
  <!-- 内耳 -->
  <ellipse cx="55" cy="70" rx="12" ry="15" fill="#7EDDD7" transform="rotate(-20 55 70)"/>
  <ellipse cx="145" cy="70" rx="12" ry="15" fill="#7EDDD7" transform="rotate(20 145 70)"/>
  
  <!-- 眼睛 -->
  <circle cx="75" cy="110" r="8" fill="#2D3748"/>
  <circle cx="125" cy="110" r="8" fill="#2D3748"/>
  <circle cx="77" cy="108" r="3" fill="#FFFFFF"/>
  <circle cx="127" cy="108" r="3" fill="#FFFFFF"/>
  
  <!-- 腮红 -->
  <ellipse cx="60" cy="125" rx="10" ry="6" fill="#F8B4C0" opacity="0.6"/>
  <ellipse cx="140" cy="125" rx="10" ry="6" fill="#F8B4C0" opacity="0.6"/>
  
  <!-- 嘴巴 -->
  <path d="M 90 125 Q 100 135 110 125" stroke="#2D3748" stroke-width="3" fill="none" stroke-linecap="round"/>
  
  <!-- 小手 -->
  <ellipse cx="45" cy="140" rx="12" ry="15" fill="url(#bodyGrad)" transform="rotate(-30 45 140)"/>
  <ellipse cx="155" cy="140" rx="12" ry="15" fill="url(#bodyGrad)" transform="rotate(30 155 140)"/>
  
  <!-- 波浪装饰 -->
  <path d="M 60 175 Q 80 165 100 175 Q 120 185 140 175" stroke="#7EDDD7" stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>
"""

WAVE_ANIMATION = """
<svg viewBox="0 0 400 100" xmlns="http://www.w3.org/2000/svg" style="position: absolute; bottom: 0; left: 0; width: 100%; opacity: 0.3;">
  <path d="M 0 50 Q 50 30 100 50 T 200 50 T 300 50 T 400 50 V 100 H 0 Z" fill="#4ECDC4">
    <animate attributeName="d" 
      dur="4s" 
      repeatCount="indefinite"
      values="M 0 50 Q 50 30 100 50 T 200 50 T 300 50 T 400 50 V 100 H 0 Z;
              M 0 50 Q 50 70 100 50 T 200 50 T 300 50 T 400 50 V 100 H 0 Z;
              M 0 50 Q 50 30 100 50 T 200 50 T 300 50 T 400 50 V 100 H 0 Z"/>
  </path>
</svg>
"""

# ==================== 全局样式 ====================
def render_global_styles():
    """渲染精致的艺术风格样式"""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
        
        * {{
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
        }}
        
        /* 全局背景 - 柔和渐变 */
        .stApp {{
            background: linear-gradient(180deg, #FAFBFC 0%, #F0F4F8 50%, #E8F4F8 100%);
            background-attachment: fixed;
        }}
        
        /* 主容器 */
        .main-container {{
            max-width: 480px;
            margin: 0 auto;
            padding: 0 20px 100px 20px;
        }}
        
        /* 卡片样式 - 柔和阴影 */
        .art-card {{
            background: #FFFFFF;
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 16px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04), 0 0 1px rgba(0, 0, 0, 0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .art-card:hover {{
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08), 0 0 1px rgba(0, 0, 0, 0.08);
            transform: translateY(-2px);
        }}
        
        /* 输入框 - 极简风格 */
        .art-input {{
            background: #F7FAFC;
            border: 2px solid transparent;
            border-radius: 16px;
            padding: 16px 20px;
            font-size: 15px;
            color: #2D3748;
            width: 100%;
            transition: all 0.3s ease;
            outline: none;
        }}
        
        .art-input:focus {{
            background: #FFFFFF;
            border-color: #4ECDC4;
            box-shadow: 0 0 0 4px rgba(78, 205, 196, 0.1);
        }}
        
        .art-input::placeholder {{
            color: #A0AEC0;
        }}
        
        /* 按钮样式 */
        .art-button {{
            background: linear-gradient(135deg, #4ECDC4 0%, #3DBDB5 100%);
            color: white;
            border: none;
            border-radius: 16px;
            padding: 16px 32px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            width: 100%;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
        }}
        
        .art-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(78, 205, 196, 0.4);
        }}
        
        .art-button:active {{
            transform: translateY(0);
        }}
        
        .art-button-secondary {{
            background: #F7FAFC;
            color: #4ECDC4;
            border: 2px solid #E2E8F0;
            box-shadow: none;
        }}
        
        .art-button-secondary:hover {{
            background: #FFFFFF;
            border-color: #4ECDC4;
            box-shadow: 0 2px 8px rgba(78, 205, 196, 0.15);
        }}
        
        /* 情绪标签 - 胶囊形状 */
        .mood-pill {{
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 500;
            margin: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 2px solid transparent;
        }}
        
        .mood-pill-calm {{
            background: rgba(78, 205, 196, 0.12);
            color: #3DBDB5;
        }}
        
        .mood-pill-happy {{
            background: rgba(255, 230, 109, 0.25);
            color: #D4A017;
        }}
        
        .mood-pill-sad {{
            background: rgba(149, 165, 166, 0.15);
            color: #7F8C8D;
        }}
        
        .mood-pill-love {{
            background: rgba(248, 180, 192, 0.25);
            color: #E891A0;
        }}
        
        .mood-pill-creative {{
            background: rgba(201, 177, 255, 0.2);
            color: #9B7ED8;
        }}
        
        .mood-pill-selected {{
            border-color: currentColor;
            transform: scale(1.05);
        }}
        
        /* 底部导航 - 悬浮胶囊 */
        .bottom-nav {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 28px;
            padding: 8px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1), 0 0 1px rgba(0, 0, 0, 0.1);
            display: flex;
            gap: 4px;
            z-index: 1000;
        }}
        
        .nav-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px 16px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #A0AEC0;
            border: none;
            background: transparent;
            font-size: 11px;
            min-width: 56px;
        }}
        
        .nav-item:hover {{
            color: #4ECDC4;
            background: rgba(78, 205, 196, 0.08);
        }}
        
        .nav-item.active {{
            color: #4ECDC4;
            background: rgba(78, 205, 196, 0.12);
        }}
        
        .nav-icon {{
            font-size: 22px;
            margin-bottom: 2px;
        }}
        
        /* 启动页动画 */
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            50% {{ transform: translateY(-15px) rotate(2deg); }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.05); opacity: 0.9; }}
        }}
        
        @keyframes wave {{
            0% {{ transform: translateX(0) translateY(0); }}
            50% {{ transform: translateX(-25%) translateY(-10px); }}
            100% {{ transform: translateX(-50%) translateY(0); }}
        }}
        
        .mascot-container {{
            animation: float 4s ease-in-out infinite;
        }}
        
        .pulse-animation {{
            animation: pulse 2s ease-in-out infinite;
        }}
        
        /* 登录卡片 */
        .login-card {{
            background: #FFFFFF;
            border-radius: 28px;
            padding: 40px 32px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            max-width: 380px;
            margin: 0 auto;
        }}
        
        /* 社交登录按钮 */
        .social-btn {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        
        .social-btn-wechat {{
            background: #07C160;
            color: white;
        }}
        
        .social-btn-wechat:hover {{
            background: #06AD56;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(7, 193, 96, 0.3);
        }}
        
        .social-btn-phone {{
            background: #4ECDC4;
            color: white;
        }}
        
        .social-btn-phone:hover {{
            background: #3DBDB5;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
        }}
        
        /* 分割线 */
        .divider {{
            display: flex;
            align-items: center;
            margin: 24px 0;
            color: #A0AEC0;
            font-size: 13px;
        }}
        
        .divider::before,
        .divider::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: #E2E8F0;
        }}
        
        .divider::before {{
            margin-right: 16px;
        }}
        
        .divider::after {{
            margin-left: 16px;
        }}
        
        /* 标题样式 */
        .title-large {{
            font-size: 28px;
            font-weight: 700;
            color: #2D3748;
            margin-bottom: 8px;
        }}
        
        .title-medium {{
            font-size: 20px;
            font-weight: 600;
            color: #2D3748;
            margin-bottom: 8px;
        }}
        
        .subtitle {{
            font-size: 15px;
            color: #718096;
            line-height: 1.5;
        }}
        
        /* 刮刮乐涂层 */
        .scratch-surface {{
            background: linear-gradient(135deg, #E2E8F0 0%, #CBD5E0 50%, #E2E8F0 100%);
            background-size: 200% 200%;
            border-radius: 16px;
            position: relative;
            overflow: hidden;
        }}
        
        .scratch-surface::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 10px,
                rgba(255,255,255,0.1) 10px,
                rgba(255,255,255,0.1) 20px
            );
        }}
        
        /* 隐藏默认元素 */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* 自定义滚动条 */
        ::-webkit-scrollbar {{
            width: 6px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: transparent;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: #CBD5E0;
            border-radius: 3px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: #A0AEC0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ==================== 状态初始化 ====================
def init_state():
    """初始化所有会话状态"""
    # 页面导航
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "now"
    
    # 用户身份
    if "real_name" not in st.session_state:
        st.session_state.real_name = "岸上的朋友"
    if "anonymous_id" not in st.session_state:
        st.session_state.anonymous_id = f"浪_{random.randint(1000, 9999)}"
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "is_guest" not in st.session_state:
        st.session_state.is_guest = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user_{random.randint(10000, 99999)}"
    
    # 个人资料
    if "real_profile" not in st.session_state:
        st.session_state.real_profile = {
            "intro": "在这里，做真实的自己",
            "avatar": "👤",
        }
    if "anon_profile" not in st.session_state:
        st.session_state.anon_profile = {
            "intro": "在这里，自由流淌",
            "avatar": "🌊",
        }
    
    # 动态内容
    if "real_posts" not in st.session_state:
        st.session_state.real_posts = []
    if "anon_posts" not in st.session_state:
        st.session_state.anon_posts = []
    if "private_notes" not in st.session_state:
        st.session_state.private_notes = []
    
    # 匿名广场
    if "square_posts" not in st.session_state:
        st.session_state.square_posts = [
            {
                "id": "sq_1",
                "text": "今天没有什么特别的事，只是想说，我还在。",
                "time": "3分钟前",
                "author": "浪_2048",
                "mood": "平静",
                "likes": 12,
                "comments": [],
                "liked_by": [],
            },
            {
                "id": "sq_2",
                "text": "下班路上一个人走路，风有点冷，但路灯很好看。",
                "time": "47分钟前",
                "author": "浪_1024",
                "mood": "路上",
                "likes": 8,
                "comments": [],
                "liked_by": [],
            },
            {
                "id": "sq_3",
                "text": "失眠第27天。打开这个页面，提醒自己还活着。",
                "time": "昨晚",
                "author": "浪_4096",
                "mood": "失眠",
                "likes": 23,
                "comments": [],
                "liked_by": [],
            },
        ]
    
    # 茶室圈子
    if "circles" not in st.session_state:
        st.session_state.circles = [
            {
                "id": "c1",
                "name": "深夜树洞",
                "desc": "想说的话，留在这里",
                "icon": "🌙",
                "members": 128,
                "posts": 342,
                "color": "#9B7ED8",
            },
            {
                "id": "c2",
                "name": "创作者角落",
                "desc": "分享你的创作",
                "icon": "✨",
                "members": 89,
                "posts": 156,
                "color": "#FFE66D",
            },
            {
                "id": "c3",
                "name": "治愈系",
                "desc": "收集生活中的小确幸",
                "icon": "🌸",
                "members": 256,
                "posts": 892,
                "color": "#F8B4C0",
            },
        ]
    
    # 刮刮乐
    if "scratch_cards" not in st.session_state:
        st.session_state.scratch_cards = [
            {
                "id": "sc_1",
                "content": "其实我没有那么坚强，只是习惯了说'还行'。",
                "author": "浪_1024",
                "scratches": 0,
            },
            {
                "id": "sc_2",
                "content": "谢谢你把这些话写出来，我也一直这样。",
                "author": "浪_2048",
                "scratches": 0,
            },
        ]
    if "scratched_cards" not in st.session_state:
        st.session_state.scratched_cards = set()
    
    # 聊天与好友
    if "friends_real" not in st.session_state:
        st.session_state.friends_real = []
    if "friends_anon" not in st.session_state:
        st.session_state.friends_anon = []
    if "friend_requests" not in st.session_state:
        st.session_state.friend_requests = []
    
    # 设置
    if "muted_words" not in st.session_state:
        st.session_state.muted_words = []

# ==================== 启动页 ====================
def page_landing():
    """品牌启动页 - 温暖治愈"""
    st.markdown(
        """
        <div style="
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: linear-gradient(180deg, #E8F8F5 0%, #D5F5E3 30%, #FAFBFC 100%);
            position: relative;
            overflow: hidden;
        ">
            <!-- 装饰波浪 -->
            <div style="
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 200px;
                background: url('data:image/svg+xml,<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1440 320\"><path fill=\"%234ECDC4\" fill-opacity=\"0.1\" d=\"M0,192L48,197.3C96,203,192,213,288,229.3C384,245,480,267,576,250.7C672,235,768,181,864,181.3C960,181,1056,235,1152,234.7C1248,235,1344,181,1392,154.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z\"></path></svg>');
                background-size: cover;
            "></div>
            
            <!-- 吉祥物 -->
            <div class="mascot-container" style="margin-bottom: 40px;">
                <div style="
                    width: 180px;
                    height: 180px;
                    background: linear-gradient(135deg, #4ECDC4 0%, #3DBDB5 100%);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 80px;
                    box-shadow: 0 20px 40px rgba(78, 205, 196, 0.3);
                ">🌊</div>
            </div>
            
            <!-- 品牌名 -->
            <div style="
                font-size: 48px;
                font-weight: 700;
                color: #2D3748;
                margin-bottom: 12px;
                letter-spacing: 8px;
            ">岸</div>
            
            <!-- Slogan -->
            <div style="
                font-size: 18px;
                color: #718096;
                margin-bottom: 60px;
                letter-spacing: 2px;
            ">不需要变好，只需要坐下</div>
            
            <!-- 进入按钮 -->
            <button onclick="
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
            " style="
                background: linear-gradient(135deg, #4ECDC4 0%, #3DBDB5 100%);
                color: white;
                border: none;
                border-radius: 30px;
                padding: 18px 60px;
                font-size: 17px;
                font-weight: 500;
                cursor: pointer;
                box-shadow: 0 8px 24px rgba(78, 205, 196, 0.35);
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='translateY(-3px)';this.style.boxShadow='0 12px 32px rgba(78, 205, 196, 0.45)';" 
            onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='0 8px 24px rgba(78, 205, 196, 0.35)';">
                轻轻一点，进入岸边
            </button>
            
            <!-- 小提示 -->
            <div style="
                position: absolute;
                bottom: 40px;
                font-size: 13px;
                color: #A0AEC0;
            ">🌊 一个接住脆弱的空间</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 使用 Streamlit 按钮作为 fallback
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
        if st.button("进入岸边", use_container_width=True, type="primary"):
            st.session_state.current_page = "login"
            st.rerun()

# ==================== 登录页 ====================
def page_login():
    """登录页 - 简约卡片设计"""
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    
    # 登录卡片
    st.markdown(
        """
        <div class="login-card">
            <div style="text-align: center; margin-bottom: 32px;">
                <div style="
                    width: 72px;
                    height: 72px;
                    background: linear-gradient(135deg, #4ECDC4 0%, #3DBDB5 100%);
                    border-radius: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 36px;
                    margin: 0 auto 16px;
                    box-shadow: 0 8px 24px rgba(78, 205, 196, 0.25);
                ">🌊</div>
                <div style="font-size: 24px; font-weight: 600; color: #2D3748; margin-bottom: 4px;">欢迎回来</div>
                <div style="font-size: 14px; color: #718096;">在岸，找到属于你的安静角落</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 社交登录
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🟢", use_container_width=True, help="微信登录"):
            st.session_state.is_logged_in = True
            st.session_state.is_guest = False
            st.session_state.real_name = f"微信用户{random.randint(1000, 9999)}"
            st.session_state.current_page = "main"
            st.rerun()
    with col2:
        if st.button("📱", use_container_width=True, help="手机号登录"):
            st.info("手机号登录功能开发中")
    with col3:
        if st.button("✉️", use_container_width=True, help="邮箱登录"):
            st.info("邮箱登录功能开发中")
    
    st.markdown("<div class='divider'>或使用账号密码</div>", unsafe_allow_html=True)
    
    # 账号密码登录
    username = st.text_input("", placeholder="用户名/邮箱/手机号", label_visibility="collapsed")
    password = st.text_input("", placeholder="密码", type="password", label_visibility="collapsed")
    
    if st.button("安全登录", use_container_width=True, type="primary"):
        st.session_state.is_logged_in = True
        st.session_state.is_guest = False
        st.session_state.real_name = username or f"用户{random.randint(1000, 9999)}"
        st.session_state.current_page = "main"
        st.rerun()
    
    # 游客模式
    st.markdown("<div style='text-align: center; margin-top: 24px;'>", unsafe_allow_html=True)
    if st.button("👤 先逛逛，不登录", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.is_guest = True
        st.session_state.current_page = "main"
        st.rerun()
    st.markdown("<div style='font-size: 12px; color: #A0AEC0; margin-top: 8px;'>游客模式仅可浏览广场内容</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 底部导航 ====================
def render_bottom_nav():
    """渲染底部悬浮导航"""
    tabs = [
        ("now", "✨", "现在"),
        ("square", "🌊", "广场"),
        ("tearoom", "🍵", "茶室"),
        ("scratch", "🎁", "刮刮乐"),
        ("mine", "🏠", "我的"),
    ]
    
    cols = st.columns(len(tabs))
    for i, (tab_id, icon, label) in enumerate(tabs):
        with cols[i]:
            is_active = st.session_state.current_tab == tab_id
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}", key=f"nav_{tab_id}", use_container_width=True, type=btn_type):
                if st.session_state.is_guest and tab_id not in ["square", "login"]:
                    st.warning("游客模式仅可浏览广场")
                    return
                st.session_state.current_tab = tab_id
                st.rerun()
            st.caption(label)

# ==================== 现在页 ====================
def page_now():
    """现在页 - 情绪发布"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # 页面标题
    st.markdown(
        """
        <div style="margin-bottom: 24px;">
            <div class="title-medium">✨ 现在</div>
            <div class="subtitle">这一刻，你想留下什么？</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 发布卡片
    st.markdown("<div class='art-card'>", unsafe_allow_html=True)
    
    # 内容输入
    content = st.text_area(
        "",
        placeholder="写下此刻的心情...",
        height=120,
        label_visibility="collapsed",
    )
    
    # 情绪选择
    st.markdown("<div style='margin: 16px 0;'>", unsafe_allow_html=True)
    st.caption("选择一个情绪标签")
    
    moods = [
        ("😌", "平静", "calm"),
        ("😊", "开心", "happy"),
        ("😢", "难过", "sad"),
        ("🥰", "温暖", "love"),
        ("✨", "创作", "creative"),
        ("🤔", "思考", "calm"),
    ]
    
    selected_mood = None
    mood_cols = st.columns(len(moods))
    for i, (emoji, label, mood_type) in enumerate(moods):
        with mood_cols[i]:
            if st.button(f"{emoji}", key=f"mood_{i}", use_container_width=True):
                selected_mood = label
                st.session_state.selected_mood = label
    
    if st.session_state.get("selected_mood"):
        st.markdown(f"<div style='text-align: center; margin-top: 8px; color: #4ECDC4; font-size: 14px;'>已选择：{st.session_state.selected_mood}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 可见范围
    st.markdown("<div style='margin: 16px 0;'>", unsafe_allow_html=True)
    visibility = st.segmented_control(
        "谁可以看到",
        ["🌊 匿名", "🔒 私密", "👤 真身"],
        default="🌊 匿名",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 发布按钮
    if st.button("📝 发布", use_container_width=True, type="primary"):
        if not content.strip():
            st.warning("写点什么再发布吧")
        else:
            now_str = datetime.now().strftime("%H:%M")
            post_data = {
                "id": f"post_{random.randint(10000, 99999)}",
                "text": content.strip(),
                "time": now_str,
                "mood": st.session_state.get("selected_mood", "未标注"),
            }
            
            if "匿名" in visibility:
                post_data["author"] = st.session_state.anonymous_id
                st.session_state.square_posts.insert(0, post_data)
                st.session_state.anon_posts.insert(0, post_data)
                st.success("已匿名发布到广场")
            elif "私密" in visibility:
                st.session_state.private_notes.insert(0, post_data)
                st.success("已保存到私密笔记")
            else:
                st.session_state.real_posts.insert(0, post_data)
                st.success("已发布到真身动态")
            
            st.session_state.selected_mood = None
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 最近发布
    recent_posts = (st.session_state.anon_posts + st.session_state.real_posts)[:3]
    if recent_posts:
        st.markdown("<div style='margin-top: 24px;'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 14px; color: #718096; margin-bottom: 12px;'>最近发布</div>", unsafe_allow_html=True)
        
        for post in recent_posts:
            st.markdown(
                f"""
                <div class='art-card' style='padding: 16px;'>
                    <div style='font-size: 15px; color: #2D3748; margin-bottom: 8px; line-height: 1.5;'>{post['text'][:50]}{'...' if len(post['text']) > 50 else ''}</div>
                    <div style='font-size: 12px; color: #A0AEC0;'>{post['time']} · {post.get('mood', '未标注')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 广场页 ====================
def page_square():
    """广场页 - 匿名信息流"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # 页面标题
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div class="title-medium">🌊 广场</div>
            <div class="subtitle">你是 {st.session_state.anonymous_id}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 筛选
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("排序", ["最新", "热门"], label_visibility="collapsed")
    with col2:
        filter_mood = st.selectbox("情绪", ["全部"] + ["平静", "开心", "难过", "温暖", "创作"], label_visibility="collapsed")
    
    # 获取帖子
    posts = st.session_state.square_posts.copy()
    if filter_mood != "全部":
        posts = [p for p in posts if p.get("mood") == filter_mood]
    
    # 展示帖子
    for post in posts:
        st.markdown(
            f"""
            <div class='art-card'>
                <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                    <div style='
                        width: 40px;
                        height: 40px;
                        background: linear-gradient(135deg, #4ECDC4 0%, #7EDDD7 100%);
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 18px;
                        margin-right: 12px;
                    '>🌊</div>
                    <div>
                        <div style='font-size: 14px; font-weight: 500; color: #2D3748;'>{post['author']}</div>
                        <div style='font-size: 12px; color: #A0AEC0;'>{post['time']}</div>
                    </div>
                </div>
                <div style='font-size: 15px; color: #2D3748; line-height: 1.6; margin-bottom: 12px;'>{post['text']}</div>
                <div style='display: flex; gap: 8px; margin-bottom: 12px;'>
                    <span class='mood-pill mood-pill-calm'>{post.get('mood', '未标注')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # 互动按钮
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            is_liked = st.session_state.user_id in post.get("liked_by", [])
            if st.button(f"{'❤️' if is_liked else '🤍'} {post.get('likes', 0)}", key=f"like_{post['id']}", use_container_width=True):
                if is_liked:
                    post["likes"] = post.get("likes", 0) - 1
                    post["liked_by"] = [u for u in post.get("liked_by", []) if u != st.session_state.user_id]
                else:
                    post["likes"] = post.get("likes", 0) + 1
                    post["liked_by"] = post.get("liked_by", []) + [st.session_state.user_id]
                st.rerun()
        with c2:
            if st.button("💬", key=f"comment_{post['id']}", use_container_width=True):
                st.info("评论功能开发中")
        with c3:
            if st.button("👋", key=f"greet_{post['id']}", use_container_width=True):
                st.session_state.friend_requests.append({
                    "id": f"req_{random.randint(10000, 99999)}",
                    "from": st.session_state.anonymous_id,
                    "to": post['author'],
                    "source": "广场",
                    "time": datetime.now().strftime("%H:%M"),
                })
                st.success("已发送打招呼")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 茶室页 ====================
def page_tearoom():
    """茶室页 - 情绪圈子"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div class="title-medium">🍵 茶室</div>
            <div class="subtitle">找到你的专属树洞</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 搜索和创建
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("", placeholder="🔍 搜索圈子", label_visibility="collapsed")
    with col2:
        if st.button("➕", use_container_width=True):
            st.session_state.show_create_circle = True
    
    # 创建圈子
    if st.session_state.get("show_create_circle"):
        with st.expander("创建新圈子", expanded=True):
            name = st.text_input("圈子名称", max_chars=20)
            desc = st.text_area("简介", max_chars=100)
            if st.button("创建", use_container_width=True, type="primary"):
                if name:
                    st.session_state.circles.insert(0, {
                        "id": f"circle_{random.randint(10000, 99999)}",
                        "name": name,
                        "desc": desc,
                        "icon": random.choice(["🌙", "✨", "🌸", "🍃"]),
                        "members": 1,
                        "posts": 0,
                        "color": "#4ECDC4",
                    })
                    st.session_state.show_create_circle = False
                    st.success("圈子创建成功")
                    st.rerun()
    
    # 圈子列表
    circles = st.session_state.circles
    if search:
        circles = [c for c in circles if search.lower() in c["name"].lower()]
    
    for circle in circles:
        st.markdown(
            f"""
            <div class='art-card'>
                <div style='display: flex; align-items: center;'>
                    <div style='
                        width: 56px;
                        height: 56px;
                        background: {circle['color']}20;
                        border-radius: 16px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 28px;
                        margin-right: 16px;
                    '>{circle['icon']}</div>
                    <div style='flex: 1;'>
                        <div style='font-size: 16px; font-weight: 600; color: #2D3748; margin-bottom: 4px;'>{circle['name']}</div>
                        <div style='font-size: 13px; color: #718096; margin-bottom: 6px;'>{circle['desc']}</div>
                        <div style='font-size: 12px; color: #A0AEC0;'>👥 {circle['members']} 成员 · 📝 {circle['posts']} 帖子</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 刮刮乐页 ====================
def page_scratch():
    """刮刮乐页"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div class="title-medium">🎁 刮刮乐</div>
            <div class="subtitle">刮开涂层，发现惊喜</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 创建刮刮乐
    with st.expander("✨ 创建刮刮乐"):
        content = st.text_area("内容", max_chars=140, placeholder="写下你想说的话...")
        if st.button("创建", use_container_width=True, type="primary"):
            if content:
                st.session_state.scratch_cards.insert(0, {
                    "id": f"sc_{random.randint(10000, 99999)}",
                    "content": content,
                    "author": st.session_state.anonymous_id,
                })
                st.success("刮刮乐创建成功")
                st.rerun()
    
    # 刮刮乐列表
    for card in st.session_state.scratch_cards[:5]:
        is_scratched = card["id"] in st.session_state.scratched_cards
        
        if not is_scratched:
            # 未刮开
            st.markdown(
                f"""
                <div class='art-card' style='background: linear-gradient(135deg, #E2E8F0 0%, #CBD5E0 100%); text-align: center; padding: 40px;'>
                    <div style='font-size: 48px; margin-bottom: 12px;'>🎁</div>
                    <div style='font-size: 14px; color: #718096; margin-bottom: 8px;'>来自 {card['author']}</div>
                    <div style='font-size: 13px; color: #A0AEC0;'>刮开看看里面是什么</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("🔍 刮开", key=f"scratch_{card['id']}", use_container_width=True):
                st.session_state.scratched_cards.add(card["id"])
                st.rerun()
        else:
            # 已刮开
            st.markdown(
                f"""
                <div class='art-card' style='border: 2px solid #4ECDC4;'>
                    <div style='font-size: 15px; color: #2D3748; line-height: 1.6; margin-bottom: 12px;'>{card['content']}</div>
                    <div style='font-size: 12px; color: #A0AEC0;'>来自 {card['author']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 我的页 ====================
def page_mine():
    """我的页"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div class="title-medium">🏠 我的岸</div>
            <div class="subtitle">你的数字自留地</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 身份切换
    tab_real, tab_anon = st.tabs(["👤 真身", "🌊 匿名"])
    
    with tab_real:
        profile = st.session_state.real_profile
        posts = st.session_state.real_posts
        
        # 个人卡片
        st.markdown(
            f"""
            <div class='art-card' style='text-align: center;'>
                <div style='font-size: 64px; margin-bottom: 12px;'>{profile['avatar']}</div>
                <div style='font-size: 20px; font-weight: 600; color: #2D3748; margin-bottom: 4px;'>{st.session_state.real_name}</div>
                <div style='font-size: 14px; color: #718096; margin-bottom: 16px;'>{profile['intro']}</div>
                <div style='display: flex; justify-content: center; gap: 24px;'>
                    <div style='text-align: center;'>
                        <div style='font-size: 20px; font-weight: 600; color: #4ECDC4;'>{len(posts)}</div>
                        <div style='font-size: 12px; color: #A0AEC0;'>动态</div>
                    </div>
                    <div style='text-align: center;'>
                        <div style='font-size: 20px; font-weight: 600; color: #4ECDC4;'>{len(st.session_state.friends_real)}</div>
                        <div style='font-size: 12px; color: #A0AEC0;'>好友</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # 动态列表
        if posts:
            for post in posts[:3]:
                st.markdown(
                    f"""
                    <div class='art-card' style='padding: 16px;'>
                        <div style='font-size: 14px; color: #2D3748; margin-bottom: 8px;'>{post['text'][:60]}{'...' if len(post['text']) > 60 else ''}</div>
                        <div style='font-size: 12px; color: #A0AEC0;'>{post['time']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("还没有发布过动态")
    
    with tab_anon:
        profile = st.session_state.anon_profile
        posts = st.session_state.anon_posts
        
        st.markdown(
            f"""
            <div class='art-card' style='text-align: center;'>
                <div style='font-size: 64px; margin-bottom: 12px;'>{profile['avatar']}</div>
                <div style='font-size: 20px; font-weight: 600; color: #2D3748; margin-bottom: 4px;'>{st.session_state.anonymous_id}</div>
                <div style='font-size: 14px; color: #718096; margin-bottom: 16px;'>{profile['intro']}</div>
                <div style='display: flex; justify-content: center; gap: 24px;'>
                    <div style='text-align: center;'>
                        <div style='font-size: 20px; font-weight: 600; color: #4ECDC4;'>{len(posts)}</div>
                        <div style='font-size: 12px; color: #A0AEC0;'>动态</div>
                    </div>
                    <div style='text-align: center;'>
                        <div style='font-size: 20px; font-weight: 600; color: #4ECDC4;'>{len(st.session_state.friends_anon)}</div>
                        <div style='font-size: 12px; color: #A0AEC0;'>好友</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if posts:
            for post in posts[:3]:
                st.markdown(
                    f"""
                    <div class='art-card' style='padding: 16px;'>
                        <div style='font-size: 14px; color: #2D3748; margin-bottom: 8px;'>{post['text'][:60]}{'...' if len(post['text']) > 60 else ''}</div>
                        <div style='font-size: 12px; color: #A0AEC0;'>{post['time']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("还没有匿名动态")
    
    # 设置入口
    if st.button("⚙️ 设置", use_container_width=True):
        st.session_state.current_tab = "settings"
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 设置页 ====================
def page_settings():
    """设置页"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div class="title-medium">⚙️ 设置</div>
            <div class="subtitle">管理你的岸</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 账号信息
    st.markdown("<div class='art-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 16px; font-weight: 600; margin-bottom: 16px;'>账号信息</div>", unsafe_allow_html=True)
    st.write(f"**真身：** {st.session_state.real_name}")
    st.write(f"**匿名：** {st.session_state.anonymous_id}")
    if st.session_state.is_guest:
        st.warning("当前为游客模式")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 屏蔽词
    st.markdown("<div class='art-card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 16px; font-weight: 600; margin-bottom: 16px;'>屏蔽词</div>", unsafe_allow_html=True)
    muted = st.text_input("", value=", ".join(st.session_state.muted_words), placeholder="用逗号分隔")
    if muted:
        st.session_state.muted_words = [w.strip() for w in muted.split(",") if w.strip()]
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 退出
    if st.button("🚪 退出登录", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.current_page = "login"
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 主入口 ====================
def main():
    """主入口"""
    st.set_page_config(
        page_title="岸 - 不需要变好，只需要坐下",
        page_icon="🌊",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    
    init_state()
    render_global_styles()
    
    # 路由
    if st.session_state.current_page == "landing":
        page_landing()
    elif st.session_state.current_page == "login":
        page_login()
    else:
        # 主应用
        pages = {
            "now": page_now,
            "square": page_square,
            "tearoom": page_tearoom,
            "scratch": page_scratch,
            "mine": page_mine,
            "settings": page_settings,
        }
        
        current = st.session_state.current_tab
        if current in pages:
            pages[current]()
        else:
            page_now()
        
        # 底部导航
        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
        render_bottom_nav()

if __name__ == "__main__":
    main()
