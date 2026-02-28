# 岸 - 情绪安全表达与轻量匿名社交应用 v2.2
# 优化版 - 艺术字封面、卡通形象、聊天功能

import streamlit as st
from pathlib import Path
from datetime import datetime
import random
import json

# ==================== 数据持久化 ====================
DATA_FILE = Path(__file__).parent / "shore_data.json"

def save_data():
    """保存数据到本地文件"""
    data = {
        "real_name": st.session_state.get("real_name", "岸上的朋友"),
        "anonymous_id": st.session_state.get("anonymous_id", f"浪_{random.randint(1000, 9999)}"),
        "is_logged_in": st.session_state.get("is_logged_in", False),
        "real_profile": st.session_state.get("real_profile", {}),
        "anon_profile": st.session_state.get("anon_profile", {}),
        "real_posts": st.session_state.get("real_posts", []),
        "anon_posts": st.session_state.get("anon_posts", []),
        "private_notes": st.session_state.get("private_notes", []),
        "square_posts": st.session_state.get("square_posts", []),
        "circles": st.session_state.get("circles", []),
        "circle_posts_data": st.session_state.get("circle_posts_data", {}),
        "scratch_cards": st.session_state.get("scratch_cards", []),
        "scratched_cards": list(st.session_state.get("scratched_cards", set())),
        "friends_real": st.session_state.get("friends_real", []),
        "friends_anon": st.session_state.get("friends_anon", []),
        "friend_requests": st.session_state.get("friend_requests", []),
        "chat_messages": st.session_state.get("chat_messages", {}),
        "muted_words": st.session_state.get("muted_words", []),
    }
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存数据失败: {e}")

def load_data():
    """从本地文件加载数据"""
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载数据失败: {e}")
    return None

# ==================== 全局样式 ====================
def render_global_styles():
    """渲染全局样式"""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
        
        * {
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        .stApp {
            background: linear-gradient(180deg, #FAFBFC 0%, #F0F4F8 100%);
        }
        
        /* 主容器 */
        .main-container {
            max-width: 480px;
            margin: 0 auto;
            padding: 20px 20px 100px 20px;
        }
        
        /* 卡片样式 */
        .art-card {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        }
        
        /* 按钮样式 */
        .stButton > button {
            border-radius: 12px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* 输入框 */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 12px !important;
            border: 2px solid #E2E8F0 !important;
            padding: 12px 16px !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #4ECDC4 !important;
            box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1) !important;
        }
        
        /* 隐藏默认元素 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 启动页 */
        .landing-page {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: linear-gradient(180deg, #E0F7FA 0%, #B2EBF2 30%, #FAFBFC 100%);
            text-align: center;
            padding: 40px 20px;
            position: relative;
            overflow: hidden;
        }
        
        /* 艺术字标题 */
        .art-title {
            font-size: 80px;
            font-weight: 900;
            background: linear-gradient(135deg, #4ECDC4 0%, #3DBDB5 50%, #2C9E96 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 16px;
            text-shadow: 0 4px 20px rgba(78, 205, 196, 0.3);
            letter-spacing: 20px;
            animation: titlePulse 3s ease-in-out infinite;
        }
        
        @keyframes titlePulse {
            0%, 100% { transform: scale(1); filter: brightness(1); }
            50% { transform: scale(1.02); filter: brightness(1.1); }
        }
        
        /* 卡通形象容器 */
        .mascot-container {
            width: 200px;
            height: 200px;
            margin-bottom: 32px;
            animation: mascotFloat 4s ease-in-out infinite;
        }
        
        @keyframes mascotFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(3deg); }
        }
        
        /* Slogan */
        .landing-slogan {
            font-size: 18px;
            color: #5A6C7D;
            margin-bottom: 48px;
            letter-spacing: 4px;
            font-weight: 300;
        }
        
        /* 装饰波浪 */
        .wave-decoration {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 150px;
            opacity: 0.3;
        }
        
        /* 登录页 */
        .login-container {
            max-width: 380px;
            margin: 0 auto;
            padding-top: 40px;
        }
        
        .login-card {
            background: #FFFFFF;
            border-radius: 24px;
            padding: 32px 28px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        }
        
        /* 社交登录按钮 */
        .social-login-btn {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 16px;
            border-radius: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid #E2E8F0;
            background: #FFFFFF;
        }
        
        .social-login-btn:hover {
            border-color: #4ECDC4;
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(78, 205, 196, 0.2);
        }
        
        .social-icon {
            font-size: 32px;
            margin-bottom: 8px;
        }
        
        .social-text {
            font-size: 13px;
            color: #4A5568;
            font-weight: 500;
        }
        
        /* 底部导航 */
        .bottom-nav {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 28px;
            padding: 8px 16px;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
            display: flex;
            gap: 8px;
            z-index: 1000;
        }
        
        /* 聊天消息气泡 */
        .chat-bubble-sent {
            background: linear-gradient(135deg, #4ECDC4 0%, #3DBDB5 100%);
            color: white;
            border-radius: 20px 20px 4px 20px;
            padding: 12px 16px;
            max-width: 75%;
            margin: 8px 0 8px auto;
            box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);
        }
        
        .chat-bubble-received {
            background: #F7FAFC;
            color: #2D3748;
            border-radius: 20px 20px 20px 4px;
            padding: 12px 16px;
            max-width: 75%;
            margin: 8px auto 8px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        /* 帖子卡片 */
        .post-card {
            background: #FFFFFF;
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        }
        
        /* 刮刮乐 */
        .scratch-card {
            background: linear-gradient(135deg, #E2E8F0 0%, #CBD5E0 100%);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.5s ease;
        }
        
        .scratch-card.revealed {
            background: #FFFFFF;
            border: 2px solid #4ECDC4;
        }
        
        /* 好友列表项 */
        .friend-item {
            display: flex;
            align-items: center;
            padding: 16px;
            background: #FFFFFF;
            border-radius: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .friend-item:hover {
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ==================== 状态初始化 ====================
def init_state():
    """初始化状态"""
    saved_data = load_data()
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "now"
    if "current_circle" not in st.session_state:
        st.session_state.current_circle = None
    if "current_chat_friend" not in st.session_state:
        st.session_state.current_chat_friend = None
    
    if "real_name" not in st.session_state:
        st.session_state.real_name = saved_data.get("real_name", "岸上的朋友") if saved_data else "岸上的朋友"
    if "anonymous_id" not in st.session_state:
        st.session_state.anonymous_id = saved_data.get("anonymous_id", f"浪_{random.randint(1000, 9999)}") if saved_data else f"浪_{random.randint(1000, 9999)}"
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = saved_data.get("is_logged_in", False) if saved_data else False
    if "is_guest" not in st.session_state:
        st.session_state.is_guest = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user_{random.randint(10000, 99999)}"
    
    if "real_profile" not in st.session_state:
        st.session_state.real_profile = saved_data.get("real_profile", {"intro": "在这里，做真实的自己", "avatar": "👤"}) if saved_data else {"intro": "在这里，做真实的自己", "avatar": "👤"}
    if "anon_profile" not in st.session_state:
        st.session_state.anon_profile = saved_data.get("anon_profile", {"intro": "在这里，自由流淌", "avatar": "🌊"}) if saved_data else {"intro": "在这里，自由流淌", "avatar": "🌊"}
    
    if "real_posts" not in st.session_state:
        st.session_state.real_posts = saved_data.get("real_posts", []) if saved_data else []
    if "anon_posts" not in st.session_state:
        st.session_state.anon_posts = saved_data.get("anon_posts", []) if saved_data else []
    if "private_notes" not in st.session_state:
        st.session_state.private_notes = saved_data.get("private_notes", []) if saved_data else []
    
    if "square_posts" not in st.session_state:
        default_posts = [
            {"id": "sq_1", "text": "今天没有什么特别的事，只是想说，我还在。", "time": "3分钟前", "author": "浪_2048", "mood": "平静", "likes": 12, "liked_by": []},
            {"id": "sq_2", "text": "下班路上一个人走路，风有点冷，但路灯很好看。", "time": "47分钟前", "author": "浪_1024", "mood": "路上", "likes": 8, "liked_by": []},
            {"id": "sq_3", "text": "失眠第27天。打开这个页面，提醒自己还活着。", "time": "昨晚", "author": "浪_4096", "mood": "失眠", "likes": 23, "liked_by": []},
        ]
        st.session_state.square_posts = saved_data.get("square_posts", default_posts) if saved_data else default_posts
    
    if "circles" not in st.session_state:
        default_circles = [
            {"id": "c1", "name": "深夜树洞", "desc": "想说的话，留在这里", "icon": "🌙", "members": 128, "posts": 342, "color": "#9B7ED8", "is_public": True},
            {"id": "c2", "name": "创作者角落", "desc": "分享你的创作", "icon": "✨", "members": 89, "posts": 156, "color": "#FFE66D", "is_public": True},
            {"id": "c3", "name": "治愈系", "desc": "收集生活中的小确幸", "icon": "🌸", "members": 256, "posts": 892, "color": "#F8B4C0", "is_public": True},
        ]
        st.session_state.circles = saved_data.get("circles", default_circles) if saved_data else default_circles
    
    if "circle_posts_data" not in st.session_state:
        st.session_state.circle_posts_data = saved_data.get("circle_posts_data", {}) if saved_data else {}
    
    if "scratch_cards" not in st.session_state:
        default_cards = [
            {"id": "sc_1", "content": "其实我没有那么坚强，只是习惯了说'还行'。", "author": "浪_1024"},
            {"id": "sc_2", "content": "谢谢你把这些话写出来，我也一直这样。", "author": "浪_2048"},
        ]
        st.session_state.scratch_cards = saved_data.get("scratch_cards", default_cards) if saved_data else default_cards
    if "scratched_cards" not in st.session_state:
        scratched = saved_data.get("scratched_cards", []) if saved_data else []
        st.session_state.scratched_cards = set(scratched)
    
    if "friends_real" not in st.session_state:
        st.session_state.friends_real = saved_data.get("friends_real", []) if saved_data else []
    if "friends_anon" not in st.session_state:
        st.session_state.friends_anon = saved_data.get("friends_anon", []) if saved_data else []
    if "friend_requests" not in st.session_state:
        st.session_state.friend_requests = saved_data.get("friend_requests", []) if saved_data else []
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = saved_data.get("chat_messages", {}) if saved_data else {}
    
    if "muted_words" not in st.session_state:
        st.session_state.muted_words = saved_data.get("muted_words", []) if saved_data else []

# ==================== SVG 卡通形象 ====================
def get_mascot_svg():
    """返回卡通形象 SVG"""
    return """
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: 100%;">
        <defs>
            <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#4ECDC4"/>
                <stop offset="100%" style="stop-color:#3DBDB5"/>
            </linearGradient>
            <linearGradient id="bellyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#FFFFFF;stop-opacity:0.95"/>
                <stop offset="100%" style="stop-color:#E0F7FA;stop-opacity:0.9"/>
            </linearGradient>
            <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                <feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#4ECDC4" flood-opacity="0.3"/>
            </filter>
        </defs>
        
        <!-- 身体 -->
        <ellipse cx="100" cy="125" rx="65" ry="58" fill="url(#bodyGrad)" filter="url(#shadow)"/>
        
        <!-- 肚子 -->
        <ellipse cx="100" cy="135" rx="38" ry="32" fill="url(#bellyGrad)"/>
        
        <!-- 耳朵 -->
        <ellipse cx="48" cy="65" rx="22" ry="28" fill="url(#bodyGrad)" transform="rotate(-15 48 65)"/>
        <ellipse cx="152" cy="65" rx="22" ry="28" fill="url(#bodyGrad)" transform="rotate(15 152 65)"/>
        <ellipse cx="48" cy="65" rx="14" ry="18" fill="#7EDDD7" transform="rotate(-15 48 65)"/>
        <ellipse cx="152" cy="65" rx="14" ry="18" fill="#7EDDD7" transform="rotate(15 152 65)"/>
        
        <!-- 眼睛 -->
        <circle cx="72" cy="105" r="10" fill="#2D3748"/>
        <circle cx="128" cy="105" r="10" fill="#2D3748"/>
        <circle cx="75" cy="102" r="4" fill="#FFFFFF"/>
        <circle cx="131" cy="102" r="4" fill="#FFFFFF"/>
        
        <!-- 腮红 -->
        <ellipse cx="55" cy="120" rx="12" ry="7" fill="#FFB6C1" opacity="0.6"/>
        <ellipse cx="145" cy="120" rx="12" ry="7" fill="#FFB6C1" opacity="0.6"/>
        
        <!-- 嘴巴 -->
        <path d="M 88 122 Q 100 135 112 122" stroke="#2D3748" stroke-width="3" fill="none" stroke-linecap="round"/>
        
        <!-- 小手 -->
        <ellipse cx="38" cy="138" rx="14" ry="18" fill="url(#bodyGrad)" transform="rotate(-25 38 138)"/>
        <ellipse cx="162" cy="138" rx="14" ry="18" fill="url(#bodyGrad)" transform="rotate(25 162 138)"/>
        
        <!-- 波浪装饰 -->
        <path d="M 50 175 Q 75 165 100 175 Q 125 185 150 175" stroke="#7EDDD7" stroke-width="5" fill="none" stroke-linecap="round"/>
    </svg>
    """

# ==================== 启动页 ====================
def page_landing():
    """品牌启动页 - 简洁版"""
    # 使用 Streamlit 原生组件，避免 SVG 渲染问题
    st.markdown("""
    <style>
    .simple-landing {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(180deg, #E0F7FA 0%, #FAFBFC 100%);
    }
    .simple-title {
        font-size: 72px;
        font-weight: 900;
        color: #4ECDC4;
        margin-bottom: 8px;
        text-shadow: 0 4px 20px rgba(78, 205, 196, 0.3);
    }
    .simple-slogan {
        font-size: 16px;
        color: #5A6C7D;
        margin-bottom: 40px;
        letter-spacing: 2px;
    }
    .simple-mascot {
        font-size: 100px;
        margin-bottom: 20px;
        animation: bounce 2s ease-in-out infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    </style>
    <div class='simple-landing'>
        <div class='simple-mascot'>🌊</div>
        <div class='simple-title'>岸</div>
        <div class='simple-slogan'>不需要变好，只需要坐下</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 进入按钮 - 放在 HTML 外面使用 Streamlit 原生按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌊 轻轻一点，进入岸边", type="primary", use_container_width=True):
            st.session_state.current_page = "login"
            save_data()
            st.rerun()
    


# ==================== 登录页 ====================
def page_login():
    """登录页 - 带文字标识的社交登录"""
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    
    # Logo和标题
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center; font-size: 64px; margin-bottom: 8px;'>🌊</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 24px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>欢迎回到岸边</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 14px; color: #718096; margin-bottom: 28px;'>找到属于你的安静角落</div>", unsafe_allow_html=True)
    
    # 社交登录 - 带文字标识
    st.markdown("<div style='margin-bottom: 8px; font-size: 13px; color: #718096;'>选择登录方式</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 16px 8px; border: 2px solid #E2E8F0; border-radius: 16px; cursor: pointer; transition: all 0.3s;' 
             onmouseover="this.style.borderColor='#07C160';this.style.transform='translateY(-3px)';this.style.boxShadow='0 8px 20px rgba(7,193,96,0.2)'"
             onmouseout="this.style.borderColor='#E2E8F0';this.style.transform='translateY(0)';this.style.boxShadow='none'">
            <div style='font-size: 32px; margin-bottom: 8px;'>💬</div>
            <div style='font-size: 13px; color: #07C160; font-weight: 600;'>微信登录</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("微信", key="wechat_btn", use_container_width=True):
            st.session_state.is_logged_in = True
            st.session_state.is_guest = False
            st.session_state.real_name = f"微信用户{random.randint(1000, 9999)}"
            save_data()
            st.session_state.current_page = "main"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 16px 8px; border: 2px solid #E2E8F0; border-radius: 16px; cursor: pointer; transition: all 0.3s;'
             onmouseover="this.style.borderColor='#4ECDC4';this.style.transform='translateY(-3px)';this.style.boxShadow='0 8px 20px rgba(78,205,196,0.2)'"
             onmouseout="this.style.borderColor='#E2E8F0';this.style.transform='translateY(0)';this.style.boxShadow='none'">
            <div style='font-size: 32px; margin-bottom: 8px;'>📱</div>
            <div style='font-size: 13px; color: #4ECDC4; font-weight: 600;'>手机号</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("手机", key="phone_btn", use_container_width=True):
            st.info("手机号登录功能开发中")
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 16px 8px; border: 2px solid #E2E8F0; border-radius: 16px; cursor: pointer; transition: all 0.3s;'
             onmouseover="this.style.borderColor='#9B7ED8';this.style.transform='translateY(-3px)';this.style.boxShadow='0 8px 20px rgba(155,126,216,0.2)'"
             onmouseout="this.style.borderColor='#E2E8F0';this.style.transform='translateY(0)';this.style.boxShadow='none'">
            <div style='font-size: 32px; margin-bottom: 8px;'>✉️</div>
            <div style='font-size: 13px; color: #9B7ED8; font-weight: 600;'>邮箱</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("邮箱", key="email_btn", use_container_width=True):
            st.info("邮箱登录功能开发中")
    
    # 分割线
    st.markdown("<div style='display: flex; align-items: center; margin: 24px 0; color: #A0AEC0; font-size: 13px;'><div style='flex: 1; height: 1px; background: #E2E8F0; margin-right: 12px;'></div>或使用账号密码<div style='flex: 1; height: 1px; background: #E2E8F0; margin-left: 12px;'></div></div>", unsafe_allow_html=True)
    
    # 账号密码
    username = st.text_input("用户名/邮箱/手机号", placeholder="请输入账号")
    password = st.text_input("密码", type="password", placeholder="请输入密码")
    
    if st.button("🔐 安全登录", type="primary", use_container_width=True):
        st.session_state.is_logged_in = True
        st.session_state.is_guest = False
        st.session_state.real_name = username or f"用户{random.randint(1000, 9999)}"
        save_data()
        st.session_state.current_page = "main"
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 游客模式
    st.markdown("<div style='text-align: center; margin-top: 20px;'>", unsafe_allow_html=True)
    if st.button("👤 先逛逛，不登录", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.is_guest = True
        save_data()
        st.session_state.current_page = "main"
        st.rerun()
    st.markdown("<div style='font-size: 12px; color: #A0AEC0; margin-top: 8px;'>游客模式仅可浏览广场内容</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 底部导航 ====================
def render_bottom_nav():
    """渲染底部导航"""
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
    
    tabs = [
        ("now", "✨", "现在"),
        ("square", "🌊", "广场"),
        ("tearoom", "🍵", "茶室"),
        ("scratch", "🎁", "刮刮乐"),
        ("chat", "💬", "聊天"),
        ("mine", "🏠", "我的"),
    ]
    
    cols = st.columns(len(tabs))
    for i, (tab_id, icon, label) in enumerate(tabs):
        with cols[i]:
            is_active = st.session_state.current_tab == tab_id
            if st.button(f"{icon}\n{label}", key=f"nav_{tab_id}", use_container_width=True, 
                        type="primary" if is_active else "secondary"):
                if st.session_state.is_guest and tab_id not in ["square", "mine"]:
                    st.warning("游客模式仅可浏览广场")
                    return
                st.session_state.current_tab = tab_id
                st.rerun()

# ==================== 现在页 ====================
def page_now():
    """现在页"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 24px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>✨ 现在</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 14px; color: #718096; margin-bottom: 20px;'>这一刻，你想留下什么？</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='art-card'>", unsafe_allow_html=True)
    
    content = st.text_area("", placeholder="写下此刻的心情...", height=100, label_visibility="collapsed")
    
    st.caption("选择一个情绪")
    mood_cols = st.columns(6)
    moods = ["😌 平静", "😊 开心", "😢 难过", "🥰 温暖", "✨ 创作", "🤔 思考"]
    
    for i, mood in enumerate(moods):
        with mood_cols[i]:
            if st.button(mood, key=f"mood_{i}", use_container_width=True):
                st.session_state.selected_mood = mood.split()[1]
                st.rerun()
    
    if st.session_state.get("selected_mood"):
        st.info(f"已选择：{st.session_state.selected_mood}")
    
    visibility = st.radio("谁可以看到", ["🌊 匿名发布到广场", "🔒 私密仅自己可见", "👤 真身动态"], horizontal=True)
    
    if st.button("📝 发布", type="primary", use_container_width=True):
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
                post_data["likes"] = 0
                post_data["liked_by"] = []
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
            save_data()
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    recent = (st.session_state.anon_posts + st.session_state.real_posts)[:3]
    if recent:
        st.markdown("<div style='font-size: 14px; color: #718096; margin: 20px 0 12px 0;'>最近发布</div>", unsafe_allow_html=True)
        for post in recent:
            st.markdown(f"""
            <div class='art-card' style='padding: 16px;'>
                <div style='font-size: 14px; color: #2D3748; margin-bottom: 8px;'>{post['text'][:50]}{'...' if len(post['text']) > 50 else ''}</div>
                <div style='font-size: 12px; color: #A0AEC0;'>{post['time']} · {post.get('mood', '未标注')}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 广场页 ====================
def page_square():
    """广场页"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='font-size: 24px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>🌊 广场</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 14px; color: #718096; margin-bottom: 20px;'>你是 {st.session_state.anonymous_id}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("排序", ["最新", "热门"])
    with col2:
        filter_mood = st.selectbox("情绪", ["全部", "平静", "开心", "难过", "温暖", "创作", "思考"])
    
    posts = st.session_state.square_posts.copy()
    if filter_mood != "全部":
        posts = [p for p in posts if p.get("mood") == filter_mood]
    if sort_by == "热门":
        posts.sort(key=lambda x: x.get("likes", 0), reverse=True)
    
    for post in posts:
        st.markdown(f"""
        <div class='post-card'>
            <div style='display: flex; align-items: center; margin-bottom: 12px;'>
                <div style='width: 44px; height: 44px; background: linear-gradient(135deg, #4ECDC4 0%, #7EDDD7 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; margin-right: 12px;'>🌊</div>
                <div>
                    <div style='font-size: 15px; font-weight: 600; color: #2D3748;'>{post['author']}</div>
                    <div style='font-size: 12px; color: #A0AEC0;'>{post['time']}</div>
                </div>
            </div>
            <div style='font-size: 15px; color: #2D3748; line-height: 1.6; margin-bottom: 12px;'>{post['text']}</div>
            <div style='display: inline-block; padding: 6px 14px; background: rgba(78, 205, 196, 0.12); color: #3DBDB5; border-radius: 20px; font-size: 12px; font-weight: 500;'>{post.get('mood', '未标注')}</div>
        </div>
        """, unsafe_allow_html=True)
        
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
                save_data()
                st.rerun()
        with c2:
            if st.button("💬", key=f"comment_{post['id']}", use_container_width=True):
                st.session_state.show_comment = post['id']
        with c3:
            if st.button("👋", key=f"greet_{post['id']}", use_container_width=True):
                st.session_state.friend_requests.append({
                    "id": f"req_{random.randint(10000, 99999)}",
                    "from": st.session_state.anonymous_id,
                    "to": post['author'],
                    "source": "广场",
                    "time": datetime.now().strftime("%H:%M"),
                })
                save_data()
                st.success("已发送打招呼")
        
        if st.session_state.get("show_comment") == post['id']:
            with st.container():
                comment = st.text_input("写评论", key=f"comment_input_{post['id']}")
                if st.button("发送", key=f"send_comment_{post['id']}"):
                    if comment:
                        if "comments" not in post:
                            post["comments"] = []
                        post["comments"].append({
                            "author": st.session_state.anonymous_id,
                            "text": comment,
                            "time": datetime.now().strftime("%H:%M"),
                        })
                        save_data()
                        st.session_state.show_comment = None
                        st.rerun()
        
        if post.get("comments"):
            with st.expander(f"查看 {len(post['comments'])} 条评论"):
                for c in post["comments"]:
                    st.markdown(f"**{c['author']}**: {c['text']} *({c['time']})*")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 茶室页 ====================
def page_tearoom():
    """茶室页"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 24px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>🍵 茶室</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 14px; color: #718096; margin-bottom: 20px;'>找到你的专属树洞</div>", unsafe_allow_html=True)
    
    if st.session_state.current_circle:
        circle = st.session_state.current_circle
        
        if st.button("← 返回圈子列表"):
            st.session_state.current_circle = None
            st.rerun()
        
        st.markdown(f"""
        <div class='art-card' style='text-align: center;'>
            <div style='font-size: 72px; margin-bottom: 12px;'>{circle['icon']}</div>
            <div style='font-size: 24px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>{circle['name']}</div>
            <div style='font-size: 14px; color: #718096; margin-bottom: 16px;'>{circle['desc']}</div>
            <div style='font-size: 13px; color: #A0AEC0;'>👥 {circle['members']} 成员 · 📝 {circle['posts']} 帖子</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("✏️ 发布新帖子"):
            post_content = st.text_area("内容", placeholder="分享你的想法...")
            if st.button("发布", type="primary", use_container_width=True):
                if post_content:
                    circle_id = circle['id']
                    if circle_id not in st.session_state.circle_posts_data:
                        st.session_state.circle_posts_data[circle_id] = []
                    
                    st.session_state.circle_posts_data[circle_id].insert(0, {
                        "id": f"cp_{random.randint(10000, 99999)}",
                        "author": st.session_state.anonymous_id,
                        "text": post_content,
                        "time": datetime.now().strftime("%H:%M"),
                        "likes": 0,
                    })
                    circle["posts"] = circle.get("posts", 0) + 1
                    save_data()
                    st.success("发布成功")
                    st.rerun()
        
        circle_id = circle['id']
        posts = st.session_state.circle_posts_data.get(circle_id, [])
        
        if posts:
            st.markdown(f"<div style='font-size: 14px; color: #718096; margin: 20px 0 12px 0;'>帖子 ({len(posts)})</div>", unsafe_allow_html=True)
            for post in posts:
                st.markdown(f"""
                <div class='art-card'>
                    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
                        <div style='font-size: 14px; font-weight: 600; color: #2D3748; margin-right: 8px;'>{post['author']}</div>
                        <div style='font-size: 12px; color: #A0AEC0;'>{post['time']}</div>
                    </div>
                    <div style='font-size: 15px; color: #2D3748; line-height: 1.6;'>{post['text']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("还没有帖子，来发布第一条吧")
        
        return
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("", placeholder="🔍 搜索圈子", label_visibility="collapsed")
    with col2:
        if st.button("➕ 创建", use_container_width=True):
            st.session_state.show_create_circle = True
    
    if st.session_state.get("show_create_circle"):
        with st.expander("创建新圈子", expanded=True):
            name = st.text_input("圈子名称", max_chars=20)
            desc = st.text_area("简介", max_chars=100)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("取消", use_container_width=True):
                    st.session_state.show_create_circle = False
                    st.rerun()
            with col2:
                if st.button("创建", type="primary", use_container_width=True):
                    if name:
                        new_circle = {
                            "id": f"circle_{random.randint(10000, 99999)}",
                            "name": name,
                            "desc": desc,
                            "icon": random.choice(["🌙", "✨", "🌸", "🍃", "🔥", "💧"]),
                            "members": 1,
                            "posts": 0,
                            "color": "#4ECDC4",
                            "is_public": True,
                        }
                        st.session_state.circles.insert(0, new_circle)
                        st.session_state.show_create_circle = False
                        save_data()
                        st.success(f"圈子「{name}」创建成功")
                        st.rerun()
    
    circles = st.session_state.circles
    if search:
        circles = [c for c in circles if search.lower() in c["name"].lower()]
    
    for circle in circles:
        if st.button(f"{circle['icon']} {circle['name']}\n{circle['desc']}\n👥 {circle['members']} 成员 · 📝 {circle['posts']} 帖子", 
                     key=f"circle_{circle['id']}", use_container_width=True):
            st.session_state.current_circle = circle
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 刮刮乐页 ====================
def page_scratch():
    """刮刮乐页"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 24px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>🎁 刮刮乐</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 14px; color: #718096; margin-bottom: 20px;'>刮开涂层，发现惊喜</div>", unsafe_allow_html=True)
    
    with st.expander("✨ 创建新的刮刮乐"):
        content = st.text_area("内容", max_chars=140, placeholder="写下你想说的话...")
        if st.button("创建", type="primary", use_container_width=True):
            if content:
                st.session_state.scratch_cards.insert(0, {
                    "id": f"sc_{random.randint(10000, 99999)}",
                    "content": content,
                    "author": st.session_state.anonymous_id,
                })
                save_data()
                st.success("刮刮乐创建成功")
                st.rerun()
    
    for card in st.session_state.scratch_cards[:6]:
        is_scratched = card["id"] in st.session_state.scratched_cards
        
        if not is_scratched:
            if st.button(f"🎁 来自 {card['author']}\n\n✨ 点击刮开看看里面是什么", 
                        key=f"scratch_btn_{card['id']}", use_container_width=True):
                st.session_state.scratched_cards.add(card["id"])
                save_data()
                st.rerun()
        else:
            st.markdown(f"""
            <div class='art-card' style='border: 2px solid #4ECDC4;'>
                <div style='font-size: 16px; color: #2D3748; line-height: 1.6; margin-bottom: 12px;'>{card['content']}</div>
                <div style='font-size: 12px; color: #A0AEC0;'>来自 {card['author']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 聊天页 ====================
def page_chat():
    """聊天页 - 私聊功能"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # 如果有当前聊天好友，显示聊天界面
    if st.session_state.current_chat_friend:
        friend = st.session_state.current_chat_friend
        
        # 返回按钮
        if st.button("← 返回好友列表"):
            st.session_state.current_chat_friend = None
            st.rerun()
        
        # 聊天头部
        st.markdown(f"""
        <div style='display: flex; align-items: center; padding: 16px; background: #FFFFFF; border-radius: 16px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);'>
            <div style='font-size: 40px; margin-right: 12px;'>🌊</div>
            <div>
                <div style='font-size: 16px; font-weight: 600; color: #2D3748;'>{friend['name']}</div>
                <div style='font-size: 12px; color: #4ECDC4;'>● 在线</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 获取聊天记录
        chat_key = f"{st.session_state.user_id}_{friend['id']}"
        if chat_key not in st.session_state.chat_messages:
            st.session_state.chat_messages[chat_key] = []
        messages = st.session_state.chat_messages[chat_key]
        
        # 显示消息
        for msg in messages:
            if msg['from'] == st.session_state.user_id:
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-end; margin-bottom: 12px;'>
                    <div style='background: linear-gradient(135deg, #4ECDC4 0%, #3DBDB5 100%); color: white; border-radius: 20px 20px 4px 20px; padding: 12px 16px; max-width: 75%; box-shadow: 0 2px 8px rgba(78, 205, 196, 0.3);'>
                        <div style='font-size: 14px;'>{msg['text']}</div>
                        <div style='font-size: 10px; opacity: 0.8; text-align: right; margin-top: 4px;'>{msg['time']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='display: flex; justify-content: flex-start; margin-bottom: 12px;'>
                    <div style='background: #F7FAFC; color: #2D3748; border-radius: 20px 20px 20px 4px; padding: 12px 16px; max-width: 75%; box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>
                        <div style='font-size: 14px;'>{msg['text']}</div>
                        <div style='font-size: 10px; color: #A0AEC0; margin-top: 4px;'>{msg['time']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # 输入框
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns([4, 1])
        with col1:
            message = st.text_input("", placeholder="输入消息...", label_visibility="collapsed", key="chat_input")
        with col2:
            if st.button("发送 📤", type="primary", use_container_width=True):
                if message:
                    messages.append({
                        "from": st.session_state.user_id,
                        "to": friend['id'],
                        "text": message,
                        "time": datetime.now().strftime("%H:%M"),
                    })
                    save_data()
                    st.rerun()
        
        return
    
    # 好友列表页面
    st.markdown("<div style='font-size: 24px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>💬 聊天</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 14px; color: #718096; margin-bottom: 20px;'>与好友私密交流</div>", unsafe_allow_html=True)
    
    # 添加好友
    with st.expander("➕ 添加好友"):
        search_id = st.text_input("输入用户ID", placeholder="例如：浪_1024")
        if st.button("搜索并添加", type="primary"):
            if search_id:
                # 添加好友申请
                st.session_state.friend_requests.append({
                    "id": f"req_{random.randint(10000, 99999)}",
                    "from": st.session_state.anonymous_id,
                    "to": search_id,
                    "source": "搜索",
                    "time": datetime.now().strftime("%H:%M"),
                })
                save_data()
                st.success(f"已向 {search_id} 发送好友申请")
    
    # 好友申请
    if st.session_state.friend_requests:
        with st.expander(f"🔔 好友申请 ({len(st.session_state.friend_requests)})"):
            for req in st.session_state.friend_requests:
                st.write(f"来自 {req['from']} ({req['source']})")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✓ 同意", key=f"accept_{req['id']}"):
                        st.session_state.friends_anon.append({
                            "id": req['from'],
                            "name": req['from'],
                            "source": req['source'],
                        })
                        st.session_state.friend_requests = [r for r in st.session_state.friend_requests if r['id'] != req['id']]
                        save_data()
                        st.rerun()
                with col2:
                    if st.button("✗ 拒绝", key=f"reject_{req['id']}"):
                        st.session_state.friend_requests = [r for r in st.session_state.friend_requests if r['id'] != req['id']]
                        save_data()
                        st.rerun()
    
    # 好友列表
    tab_anon, tab_real = st.tabs(["🌊 匿名好友", "👤 真身好友"])
    
    with tab_anon:
        if not st.session_state.friends_anon:
            st.info("还没有匿名好友，去广场打招呼添加吧")
        else:
            for friend in st.session_state.friends_anon:
                # 计算未读消息数
                chat_key = f"{st.session_state.user_id}_{friend['id']}"
                unread = 0  # 简化版，实际应该计算未读消息
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"🌊 {friend['name']}\n来自{friend.get('source', '广场')}", 
                                key=f"friend_{friend['id']}", use_container_width=True):
                        st.session_state.current_chat_friend = friend
                        st.rerun()
                with col2:
                    st.markdown(f"<div style='background: #4ECDC4; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 12px;'>{unread}</div>" if unread > 0 else "", unsafe_allow_html=True)
    
    with tab_real:
        if not st.session_state.friends_real:
            st.info("还没有真身好友")
        else:
            for friend in st.session_state.friends_real:
                if st.button(f"👤 {friend['name']}", key=f"real_friend_{friend['id']}", use_container_width=True):
                    st.session_state.current_chat_friend = friend
                    st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 我的页 ====================
def page_mine():
    """我的页"""
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 24px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>🏠 我的岸</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 14px; color: #718096; margin-bottom: 20px;'>你的数字自留地</div>", unsafe_allow_html=True)
    
    tab_real, tab_anon, tab_settings = st.tabs(["👤 真身", "🌊 匿名", "⚙️ 设置"])
    
    with tab_real:
        profile = st.session_state.real_profile
        posts = st.session_state.real_posts
        
        st.markdown(f"""
        <div class='art-card' style='text-align: center;'>
            <div style='font-size: 72px; margin-bottom: 12px;'>{profile['avatar']}</div>
            <div style='font-size: 22px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>{st.session_state.real_name}</div>
            <div style='font-size: 14px; color: #718096; margin-bottom: 20px;'>{profile['intro']}</div>
            <div style='display: flex; justify-content: center; gap: 40px;'>
                <div style='text-align: center;'>
                    <div style='font-size: 24px; font-weight: 700; color: #4ECDC4;'>{len(posts)}</div>
                    <div style='font-size: 12px; color: #A0AEC0;'>动态</div>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 24px; font-weight: 700; color: #4ECDC4;'>{len(st.session_state.friends_real)}</div>
                    <div style='font-size: 12px; color: #A0AEC0;'>好友</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("✏️ 编辑资料"):
            new_intro = st.text_area("个人介绍", value=profile['intro'])
            new_avatar = st.selectbox("头像", ["👤", "🌊", "✨", "🌙", "🌸", "🍃", "🔥", "💧"])
            if st.button("保存", type="primary"):
                profile['intro'] = new_intro
                profile['avatar'] = new_avatar
                save_data()
                st.success("资料已更新")
                st.rerun()
        
        if posts:
            st.markdown(f"<div style='font-size: 14px; color: #718096; margin: 20px 0 12px 0;'>动态 ({len(posts)})</div>", unsafe_allow_html=True)
            for post in posts[:5]:
                st.markdown(f"""
                <div class='art-card' style='padding: 16px;'>
                    <div style='font-size: 15px; color: #2D3748; margin-bottom: 8px;'>{post['text'][:80]}{'...' if len(post['text']) > 80 else ''}</div>
                    <div style='font-size: 12px; color: #A0AEC0;'>{post['time']} · {post.get('mood', '未标注')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("还没有发布过动态")
    
    with tab_anon:
        profile = st.session_state.anon_profile
        posts = st.session_state.anon_posts
        
        st.markdown(f"""
        <div class='art-card' style='text-align: center;'>
            <div style='font-size: 72px; margin-bottom: 12px;'>{profile['avatar']}</div>
            <div style='font-size: 22px; font-weight: 700; color: #2D3748; margin-bottom: 4px;'>{st.session_state.anonymous_id}</div>
            <div style='font-size: 14px; color: #718096; margin-bottom: 20px;'>{profile['intro']}</div>
            <div style='display: flex; justify-content: center; gap: 40px;'>
                <div style='text-align: center;'>
                    <div style='font-size: 24px; font-weight: 700; color: #4ECDC4;'>{len(posts)}</div>
                    <div style='font-size: 12px; color: #A0AEC0;'>动态</div>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 24px; font-weight: 700; color: #4ECDC4;'>{len(st.session_state.friends_anon)}</div>
                    <div style='font-size: 12px; color: #A0AEC0;'>好友</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("✏️ 编辑资料"):
            new_intro = st.text_area("个人介绍", value=profile['intro'], key="anon_intro")
            new_avatar = st.selectbox("头像", ["🌊", "🌫️", "✨", "🌙", "🌸", "🍃", "🔥", "💧"], key="anon_avatar")
            if st.button("保存", type="primary", key="save_anon"):
                profile['intro'] = new_intro
                profile['avatar'] = new_avatar
                save_data()
                st.success("资料已更新")
                st.rerun()
        
        if posts:
            st.markdown(f"<div style='font-size: 14px; color: #718096; margin: 20px 0 12px 0;'>动态 ({len(posts)})</div>", unsafe_allow_html=True)
            for post in posts[:5]:
                st.markdown(f"""
                <div class='art-card' style='padding: 16px;'>
                    <div style='font-size: 15px; color: #2D3748; margin-bottom: 8px;'>{post['text'][:80]}{'...' if len(post['text']) > 80 else ''}</div>
                    <div style='font-size: 12px; color: #A0AEC0;'>{post['time']} · {post.get('mood', '未标注')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("还没有匿名动态")
    
    with tab_settings:
        st.markdown("<div class='art-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 16px; font-weight: 600; margin-bottom: 16px;'>账号信息</div>", unsafe_allow_html=True)
        st.write(f"**真身：** {st.session_state.real_name}")
        st.write(f"**匿名：** {st.session_state.anonymous_id}")
        st.write(f"**用户ID：** {st.session_state.user_id}")
        if st.session_state.is_guest:
            st.warning("当前为游客模式")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='art-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 16px; font-weight: 600; margin-bottom: 16px;'>屏蔽词</div>", unsafe_allow_html=True)
        muted = st.text_input("用逗号分隔", value=", ".join(st.session_state.muted_words))
        if st.button("保存屏蔽词"):
            st.session_state.muted_words = [w.strip() for w in muted.split(",") if w.strip()]
            save_data()
            st.success("已保存")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.session_state.is_logged_in:
            if st.button("🚪 退出登录", type="secondary"):
                st.session_state.is_logged_in = False
                st.session_state.is_guest = False
                st.session_state.current_page = "landing"
                save_data()
                st.rerun()
        else:
            if st.button("🔐 登录账号", type="primary"):
                st.session_state.current_page = "login"
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==================== 主应用 ====================
def main():
    """主应用"""
    st.set_page_config(
        page_title="岸",
        page_icon="🌊",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    
    render_global_styles()
    init_state()
    
    # 路由
    if st.session_state.current_page == "landing":
        page_landing()
    elif st.session_state.current_page == "login":
        page_login()
    elif st.session_state.current_page == "main":
        # 主页面
        if st.session_state.current_tab == "now":
            page_now()
        elif st.session_state.current_tab == "square":
            page_square()
        elif st.session_state.current_tab == "tearoom":
            page_tearoom()
        elif st.session_state.current_tab == "scratch":
            page_scratch()
        elif st.session_state.current_tab == "chat":
            page_chat()
        elif st.session_state.current_tab == "mine":
            page_mine()
        
        render_bottom_nav()

if __name__ == "__main__":
    main()