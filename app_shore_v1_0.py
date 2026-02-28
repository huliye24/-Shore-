# 岸 - 情绪安全表达与轻量匿名社交应用
# 版本：v1.0
# 根据PRD文档重构优化

import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta
import random
import json

# ==================== 全局样式 ====================
def render_global_styles():
    """渲染全局毛玻璃视觉风格"""
    st.markdown(
        """
        <style>
        /* 全局背景 */
        .stApp {
            background: linear-gradient(135deg, #f0f4f8 0%, #e6eef7 50%, #f5f7fa 100%);
        }
        
        /* 毛玻璃卡片效果 */
        .glass-card {
            background: rgba(255, 255, 255, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
            padding: 1.2rem;
            margin-bottom: 1rem;
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            box-shadow: 0 12px 40px rgba(31, 38, 135, 0.12);
            transform: translateY(-2px);
        }
        
        /* 毛玻璃输入框 */
        .glass-input {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(8px);
            border-radius: 12px;
            border: 1px solid rgba(22, 119, 255, 0.2);
            padding: 12px 16px;
            transition: all 0.3s ease;
        }
        
        .glass-input:focus {
            border-color: #1677ff;
            box-shadow: 0 0 0 3px rgba(22, 119, 255, 0.1);
        }
        
        /* 毛玻璃按钮 */
        .glass-button {
            background: linear-gradient(135deg, rgba(22, 119, 255, 0.9) 0%, rgba(64, 150, 255, 0.9) 100%);
            backdrop-filter: blur(4px);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 24px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(22, 119, 255, 0.3);
        }
        
        .glass-button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(22, 119, 255, 0.4);
        }
        
        .glass-button:active {
            transform: scale(0.98);
        }
        
        /* 情绪标签 */
        .mood-tag {
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            margin: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .mood-tag-calm {
            background: rgba(230, 247, 255, 0.9);
            color: #1677ff;
            border: 1px solid rgba(22, 119, 255, 0.2);
        }
        
        .mood-tag-emo {
            background: rgba(249, 240, 255, 0.9);
            color: #722ed1;
            border: 1px solid rgba(114, 46, 209, 0.2);
        }
        
        .mood-tag-creative {
            background: rgba(246, 255, 237, 0.9);
            color: #52c41a;
            border: 1px solid rgba(82, 196, 26, 0.2);
        }
        
        .mood-tag-heal {
            background: rgba(255, 247, 230, 0.9);
            color: #fa8c16;
            border: 1px solid rgba(250, 140, 22, 0.2);
        }
        
        .mood-tag-selected {
            background: #1677ff;
            color: white;
            box-shadow: 0 4px 12px rgba(22, 119, 255, 0.3);
        }
        
        /* 刮刮乐涂层 */
        .scratch-coating {
            background: repeating-linear-gradient(
                45deg,
                rgba(200, 200, 200, 0.8),
                rgba(200, 200, 200, 0.8) 8px,
                rgba(220, 220, 220, 0.8) 8px,
                rgba(220, 220, 220, 0.8) 16px
            );
            backdrop-filter: blur(8px);
            border-radius: 12px;
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #888;
            font-size: 0.9rem;
            transition: opacity 0.5s ease;
        }
        
        .scratch-coating.scratched {
            opacity: 0;
            pointer-events: none;
        }
        
        /* 底部导航 */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-top: 1px solid rgba(255, 255, 255, 0.6);
            padding: 10px 0;
            z-index: 1000;
            display: flex;
            justify-content: space-around;
            align-items: center;
        }
        
        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 8px 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: #999;
        }
        
        .nav-item.active {
            color: #1677ff;
            transform: scale(1.1);
        }
        
        .nav-icon {
            font-size: 1.4rem;
            margin-bottom: 2px;
        }
        
        .nav-label {
            font-size: 0.7rem;
        }
        
        /* 消息气泡 */
        .chat-bubble-real {
            background: linear-gradient(135deg, #1677ff 0%, #4096ff 100%);
            color: white;
            border-radius: 18px 18px 4px 18px;
            padding: 12px 16px;
            max-width: 70%;
            margin: 8px 0 8px auto;
            box-shadow: 0 4px 12px rgba(22, 119, 255, 0.2);
        }
        
        .chat-bubble-anon {
            background: rgba(240, 240, 240, 0.9);
            color: #333;
            border-radius: 18px 18px 18px 4px;
            padding: 12px 16px;
            max-width: 70%;
            margin: 8px auto 8px 0;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        /* 双身份切换 */
        .identity-tab {
            display: inline-block;
            padding: 10px 24px;
            border-radius: 24px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 0 8px;
        }
        
        .identity-tab.active {
            background: #1677ff;
            color: white;
            box-shadow: 0 4px 15px rgba(22, 119, 255, 0.3);
        }
        
        .identity-tab.inactive {
            background: rgba(200, 200, 200, 0.3);
            color: #666;
        }
        
        /* 品牌封面 */
        .brand-cover {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #e6f7ff 0%, #f0f4f8 50%, #fff7e6 100%);
            position: relative;
            overflow: hidden;
        }
        
        .brand-logo {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: float 3s ease-in-out infinite;
        }
        
        .brand-slogan {
            font-size: 1.5rem;
            color: #1677ff;
            font-weight: 300;
            letter-spacing: 0.1em;
            margin-bottom: 3rem;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        /* 隐藏Streamlit默认元素 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* 主内容区域 */
        .main-content {
            padding-bottom: 80px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ==================== 状态初始化 ====================
def init_state():
    """初始化所有会话状态"""
    # 页面导航
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"  # landing, login, main
    if "current_tab" not in st.session_state:
        st.session_state.current_tab = "now"  # now, square, tearoom, scratch, mine, chat
    
    # 用户身份
    if "real_name" not in st.session_state:
        st.session_state.real_name = "某一个在岸上的人"
    if "anonymous_id" not in st.session_state:
        st.session_state.anonymous_id = f"浪 #{random.randint(1000, 9999)}"
    if "is_logged_in" not in st.session_state:
        st.session_state.is_logged_in = False
    if "is_guest" not in st.session_state:
        st.session_state.is_guest = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user_{random.randint(10000, 99999)}"
    
    # 个人资料
    if "real_profile" not in st.session_state:
        st.session_state.real_profile = {
            "intro": "写一点关于自己的话，可以长一点，也可以只是一句。",
            "avatar_emoji": "🌊",
            "cover": None,
        }
    if "anon_profile" not in st.session_state:
        st.session_state.anon_profile = {
            "intro": "这是浪的自我介绍，在这里你可以更放松。",
            "avatar_emoji": "🌫️",
            "cover": None,
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
                "time": "3 分钟前",
                "author": "浪 #2048",
                "mood": "平静",
                "likes": 12,
                "comments": 3,
                "liked_by": [],
            },
            {
                "id": "sq_2",
                "text": "下班路上一个人走路，风有点冷，但路灯很好看。",
                "time": "47 分钟前",
                "author": "浪 #1024",
                "mood": "路上",
                "likes": 8,
                "comments": 1,
                "liked_by": [],
            },
            {
                "id": "sq_3",
                "text": "失眠第 27 天。打开这个页面，提醒自己还活着。",
                "time": "昨晚",
                "author": "浪 #4096",
                "mood": "失眠",
                "likes": 23,
                "comments": 7,
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
                "cover": "🌙",
                "members": 128,
                "posts": 342,
                "is_public": True,
                "tags": ["失眠", "倾诉"],
            },
            {
                "id": "c2",
                "name": "创作者角落",
                "desc": "分享你的创作，无论是什么形式",
                "cover": "✨",
                "members": 89,
                "posts": 156,
                "is_public": True,
                "tags": ["创作", "灵感"],
            },
            {
                "id": "c3",
                "name": "治愈系",
                "desc": "收集生活中的小确幸",
                "cover": "🌸",
                "members": 256,
                "posts": 892,
                "is_public": True,
                "tags": ["治愈", "温暖"],
            },
        ]
    if "current_circle" not in st.session_state:
        st.session_state.current_circle = None
    if "circle_posts" not in st.session_state:
        st.session_state.circle_posts = {}
    
    # 刮刮乐
    if "scratch_cards" not in st.session_state:
        st.session_state.scratch_cards = [
            {
                "id": "sc_1",
                "content": "其实我没有那么坚强，只是习惯了说'还行'。",
                "author": "浪 #1024",
                "coating_color": "gray",
                "visibility": "public",
                "scratches": 0,
            },
            {
                "id": "sc_2",
                "content": "谢谢你把这些话写出来，我也一直这样。",
                "author": "浪 #2048",
                "coating_color": "blue",
                "visibility": "public",
                "scratches": 0,
            },
        ]
    if "my_scratch_cards" not in st.session_state:
        st.session_state.my_scratch_cards = []
    if "scratched_cards" not in st.session_state:
        st.session_state.scratched_cards = set()
    
    # 聊天与好友
    if "friends_real" not in st.session_state:
        st.session_state.friends_real = []
    if "friends_anon" not in st.session_state:
        st.session_state.friends_anon = []
    if "friend_requests" not in st.session_state:
        st.session_state.friend_requests = []
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = {}  # {friend_id: [messages]}
    if "current_chat" not in st.session_state:
        st.session_state.current_chat = None
    
    # 设置
    if "muted_words" not in st.session_state:
        st.session_state.muted_words = []
    if "notifications" not in st.session_state:
        st.session_state.notifications = {
            "chat": True,
            "circle": True,
            "square": True,
        }

# ==================== 启动与登录页 ====================
def page_landing():
    """品牌封面页"""
    st.markdown(
        """
        <div class="brand-cover">
            <div class="brand-logo">🌊</div>
            <div class="brand-slogan">不需要变好，只需要坐下。</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 滑动进入提示
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("👆 滑动进入", use_container_width=True, type="primary"):
            st.session_state.current_page = "login"
            st.rerun()
    
    # 动态背景效果说明
    st.caption("")
    st.caption("💡 背景随手指滑动产生轻微模糊变化，增强沉浸感")


def page_login():
    """登录/注册页"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Logo与标题
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center; font-size: 3rem;'>🌊</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; font-size: 1.5rem; color: #1677ff;'>岸</div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; color: #888; margin-bottom: 2rem;'>不需要变好，只需要坐下。</div>", unsafe_allow_html=True)
    
    # 登录选项
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    # 微信登录
    if st.button("🟢 微信一键登录", use_container_width=True, type="primary"):
        st.session_state.is_logged_in = True
        st.session_state.is_guest = False
        st.session_state.real_name = f"微信用户{random.randint(1000, 9999)}"
        st.session_state.current_page = "main"
        st.success("登录成功！")
        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 手机号登录
    phone = st.text_input("📱 手机号/邮箱", placeholder="请输入手机号或邮箱")
    if phone:
        code_col1, code_col2 = st.columns([2, 1])
        with code_col1:
            code = st.text_input("验证码", placeholder="输入验证码")
        with code_col2:
            if st.button("获取验证码", use_container_width=True):
                st.info("验证码已发送（原型演示：任意输入即可）")
        
        if code and st.button("登录", use_container_width=True, type="primary"):
            st.session_state.is_logged_in = True
            st.session_state.is_guest = False
            st.session_state.real_name = f"用户{random.randint(1000, 9999)}"
            st.session_state.current_page = "main"
            st.success("登录成功！")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 游客模式
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("👤 游客模式浏览", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.is_guest = True
        st.session_state.current_page = "main"
        st.info("已进入游客模式，仅可浏览匿名广场内容")
        st.rerun()
    
    st.caption("⚠️ 游客模式限制：数据不云端同步，无法发布内容、添加好友")


# ==================== 底部导航 ====================
def render_bottom_nav():
    """渲染底部Tab导航"""
    tabs = [
        ("now", "✨", "现在"),
        ("square", "🌊", "广场"),
        ("tearoom", "🍵", "茶室"),
        ("scratch", "🎁", "刮刮乐"),
        ("mine", "🏠", "我的岸"),
        ("chat", "💬", "聊天"),
    ]
    
    # 使用Streamlit的列来模拟底部导航
    cols = st.columns(len(tabs))
    for i, (tab_id, icon, label) in enumerate(tabs):
        with cols[i]:
            is_active = st.session_state.current_tab == tab_id
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}\n{label}", key=f"nav_{tab_id}", use_container_width=True, type=btn_type):
                # 游客模式限制
                if st.session_state.is_guest and tab_id not in ["square", "login"]:
                    st.warning("游客模式仅可浏览匿名广场")
                    return
                st.session_state.current_tab = tab_id
                st.rerun()


# ==================== 现在页（情绪发布） ====================
def page_now():
    """现在页 - 情绪发布入口"""
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # 页面标题
    st.markdown("<h2 style='color: #1677ff; margin-bottom: 0.5rem;'>✨ 现在</h2>", unsafe_allow_html=True)
    st.caption("这一刻，你想和谁说话？是和所有人，还是只和自己。")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 发布卡片
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    # 内容输入
    content = st.text_area(
        "",
        placeholder="我在想什么？",
        height=120,
        label_visibility="collapsed",
    )
    
    # 情绪标签
    st.markdown("<div style='margin: 1rem 0;'>", unsafe_allow_html=True)
    st.caption("给这句话贴一个小情绪")
    
    mood_tags = {
        "平静": ("calm", "#e6f7ff", "#1677ff"),
        "emo": ("emo", "#f9f0ff", "#722ed1"),
        "创作": ("creative", "#f6ffed", "#52c41a"),
        "治愈": ("heal", "#fff7e6", "#fa8c16"),
        "开心": ("calm", "#e6f7ff", "#1677ff"),
        "难过": ("emo", "#f9f0ff", "#722ed1"),
        "焦虑": ("emo", "#f9f0ff", "#722ed1"),
        "失眠": ("emo", "#f9f0ff", "#722ed1"),
        "路上": ("creative", "#f6ffed", "#52c41a"),
        "想家": ("heal", "#fff7e6", "#fa8c16"),
    }
    
    selected_mood = st.selectbox(
        "选择情绪标签",
        [""] + list(mood_tags.keys()),
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 可见范围选项
    st.markdown("<div style='margin: 1rem 0;'>", unsafe_allow_html=True)
    st.caption("谁可以看到这条")
    
    visibility = st.radio(
        "",
        ["🌊 以浪的身份说（匿名发布）", "🔒 只发给自己（私密笔记）", "👤 真身发布"],
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 发布按钮
    if st.button("📝 发布", use_container_width=True, type="primary"):
        if not content.strip():
            st.warning("请输入内容后再发布")
        else:
            now_str = datetime.now().strftime("今天 %H:%M")
            post_data = {
                "id": f"post_{random.randint(10000, 99999)}",
                "text": content.strip(),
                "time": now_str,
                "mood": selected_mood or "未标注",
            }
            
            if "浪的身份" in visibility:
                # 匿名发布到广场
                post_data["author"] = st.session_state.anonymous_id
                st.session_state.square_posts.insert(0, post_data)
                st.session_state.anon_posts.insert(0, post_data)
                st.success("已经以「浪」的身份，把这句话放进广场了。")
            elif "只发给自己" in visibility:
                # 私密笔记
                st.session_state.private_notes.insert(0, post_data)
                st.success("这句话只会留在这里，只属于你自己。")
            else:
                # 真身发布
                post_data["visibility"] = "好友"  # 默认仅好友可见
                st.session_state.real_posts.insert(0, post_data)
                st.success("真身的这一条，被安静地放在了这里。")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 最近发布
    if st.session_state.anon_posts or st.session_state.real_posts or st.session_state.private_notes:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("最近说过的")
        
        all_posts = (st.session_state.anon_posts + st.session_state.real_posts + st.session_state.private_notes)[:5]
        for post in all_posts:
            st.markdown(
                f"""
                <div class='glass-card'>
                    <div style='font-size: 1rem; color: #333; margin-bottom: 0.5rem;'>{post['text']}</div>
                    <div style='font-size: 0.8rem; color: #999;'>
                        {post['time']} · {post.get('mood', '未标注')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== 匿名广场页 ====================
def page_square():
    """匿名广场页 - 匿名内容信息流"""
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # 页面标题
    st.markdown(f"<h2 style='color: #1677ff; margin-bottom: 0.5rem;'>🌊 匿名广场</h2>", unsafe_allow_html=True)
    st.caption(f"这里只有浪和浪之间的碰撞。你现在的身份是：**{st.session_state.anonymous_id}**")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 排序与筛选
    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("排序", ["最新", "热门"], label_visibility="collapsed")
    with col2:
        filter_mood = st.selectbox(
            "筛选情绪",
            ["全部情绪", "平静", "emo", "创作", "治愈", "开心", "难过", "焦虑", "失眠", "路上", "想家"],
            label_visibility="collapsed",
        )
    
    # 获取帖子列表
    posts = st.session_state.square_posts.copy()
    
    # 排序
    if sort_by == "热门":
        posts.sort(key=lambda x: x.get("likes", 0), reverse=True)
    
    # 筛选
    if filter_mood != "全部情绪":
        posts = [p for p in posts if p.get("mood") == filter_mood]
    
    # 屏蔽词过滤
    muted = [w for w in st.session_state.muted_words if w.strip()]
    posts = [p for p in posts if not any(word in p.get("text", "") for word in muted)]
    
    # 展示帖子
    for post in posts:
        st.markdown(
            f"""
            <div class='glass-card'>
                <div style='display: flex; align-items: center; margin-bottom: 0.8rem;'>
                    <span style='font-size: 1.5rem; margin-right: 0.5rem;'>🌊</span>
                    <div>
                        <div style='font-weight: 500; color: #333;'>{post['author']}</div>
                        <div style='font-size: 0.75rem; color: #999;'>{post['time']}</div>
                    </div>
                </div>
                <div style='font-size: 1rem; color: #333; margin-bottom: 0.8rem; line-height: 1.6;'>
                    {post['text']}
                </div>
                <div style='display: flex; gap: 8px; margin-bottom: 0.8rem;'>
                    <span class='mood-tag mood-tag-calm'>{post.get('mood', '未标注')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # 互动按钮
        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
        
        with c1:
            is_liked = st.session_state.user_id in post.get("liked_by", [])
            like_icon = "❤️" if is_liked else "🤍"
            if st.button(f"{like_icon} {post.get('likes', 0)}", key=f"like_{post['id']}", use_container_width=True):
                if is_liked:
                    post["likes"] = post.get("likes", 0) - 1
                    post["liked_by"] = [u for u in post.get("liked_by", []) if u != st.session_state.user_id]
                else:
                    post["likes"] = post.get("likes", 0) + 1
                    post["liked_by"] = post.get("liked_by", []) + [st.session_state.user_id]
                st.rerun()
        
        with c2:
            if st.button(f"💬 {post.get('comments', 0)}", key=f"comment_{post['id']}", use_container_width=True):
                st.info("评论功能开发中...")
        
        with c3:
            if st.button("👋 打招呼", key=f"greet_{post['id']}", use_container_width=True):
                # 添加好友申请
                request = {
                    "id": f"req_{random.randint(10000, 99999)}",
                    "from": st.session_state.anonymous_id,
                    "to": post['author'],
                    "message": "想和你成为朋友",
                    "source": "广场",
                    "time": datetime.now().strftime("%H:%M"),
                }
                st.session_state.friend_requests.append(request)
                st.success("已发送打招呼申请！")
        
        with c4:
            if st.button("📤 分享", key=f"share_{post['id']}", use_container_width=True):
                st.info("分享功能开发中...")
    
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== 茶室页 ====================
def page_tearoom():
    """茶室页 - 情绪圈子/树洞"""
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # 页面标题
    st.markdown("<h2 style='color: #1677ff; margin-bottom: 0.5rem;'>🍵 茶室</h2>", unsafe_allow_html=True)
    st.caption("找到你的专属情绪树洞与同频伙伴")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 搜索
    search = st.text_input("🔍 搜索圈子", placeholder="输入圈子名称或标签")
    
    # 创建圈子按钮
    if st.button("➕ 创建圈子", use_container_width=True):
        st.session_state.show_create_circle = True
    
    # 创建圈子表单
    if st.session_state.get("show_create_circle"):
        with st.expander("创建新圈子", expanded=True):
            circle_name = st.text_input("圈子名称", max_chars=20)
            circle_desc = st.text_area("圈子简介", max_chars=100, placeholder="简单介绍一下这个圈子")
            circle_tags = st.text_input("标签（用空格分隔，最多3个）")
            circle_public = st.radio("权限", ["公开", "私密"], horizontal=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("取消", use_container_width=True):
                    st.session_state.show_create_circle = False
                    st.rerun()
            with col2:
                if st.button("创建", use_container_width=True, type="primary"):
                    if circle_name:
                        new_circle = {
                            "id": f"circle_{random.randint(10000, 99999)}",
                            "name": circle_name,
                            "desc": circle_desc,
                            "cover": random.choice(["🌙", "✨", "🌸", "🍃", "🌊", "🔥"]),
                            "members": 1,
                            "posts": 0,
                            "is_public": circle_public == "公开",
                            "tags": circle_tags.split()[:3] if circle_tags else ["新圈子"],
                            "creator": st.session_state.user_id,
                        }
                        st.session_state.circles.insert(0, new_circle)
                        st.session_state.show_create_circle = False
                        st.success(f"圈子「{circle_name}」创建成功！")
                        st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 圈子列表
    circles = st.session_state.circles
    if search:
        circles = [c for c in circles if search.lower() in c["name"].lower() or 
                   any(search.lower() in tag.lower() for tag in c.get("tags", []))]
    
    for circle in circles:
        st.markdown(
            f"""
            <div class='glass-card' style='cursor: pointer;'>
                <div style='display: flex; align-items: flex-start;'>
                    <div style='font-size: 3rem; margin-right: 1rem;'>{circle['cover']}</div>
                    <div style='flex: 1;'>
                        <div style='font-size: 1.1rem; font-weight: 600; color: #333; margin-bottom: 0.3rem;'>
                            {circle['name']}
                            {' 🔒' if not circle['is_public'] else ''}
                        </div>
                        <div style='font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;'>{circle['desc']}</div>
                        <div style='display: flex; gap: 8px; margin-bottom: 0.5rem;'>
                            {''.join([f"<span class='mood-tag mood-tag-calm'>{tag}</span>" for tag in circle.get('tags', [])])}
                        </div>
                        <div style='font-size: 0.8rem; color: #999;'>
                            👥 {circle['members']} 成员 · 📝 {circle['posts']} 帖子
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if st.button("进入圈子", key=f"enter_circle_{circle['id']}", use_container_width=True):
            st.session_state.current_circle = circle
            st.info(f"进入圈子：{circle['name']}")
    
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== 刮刮乐页 ====================
def page_scratch():
    """刮刮乐页 - 趣味匿名互动"""
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # 页面标题
    st.markdown("<h2 style='color: #1677ff; margin-bottom: 0.5rem;'>🎁 刮刮乐</h2>", unsafe_allow_html=True)
    st.caption("拖动擦除式刮开，发现藏在涂层下的秘密")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 创建刮刮乐
    with st.expander("✨ 创建新的刮刮乐"):
        scratch_content = st.text_area("内容", max_chars=140, placeholder="写下你想说的话...")
        scratch_image = st.file_uploader("添加图片（可选）", type=["png", "jpg", "jpeg"])
        
        col1, col2 = st.columns(2)
        with col1:
            coating_color = st.selectbox("涂层颜色", ["浅灰", "浅蓝", "浅紫"])
        with col2:
            visibility = st.selectbox("可见范围", ["仅自己可见", "好友可见", "公开"])
        
        if st.button("创建刮刮乐", use_container_width=True, type="primary"):
            if scratch_content:
                new_card = {
                    "id": f"sc_{random.randint(10000, 99999)}",
                    "content": scratch_content,
                    "image": scratch_image.name if scratch_image else None,
                    "author": st.session_state.anonymous_id,
                    "coating_color": coating_color,
                    "visibility": visibility,
                    "created_at": datetime.now().strftime("%H:%M"),
                    "scratches": 0,
                }
                st.session_state.scratch_cards.insert(0, new_card)
                st.session_state.my_scratch_cards.append(new_card)
                st.success("刮刮乐创建成功！")
            else:
                st.warning("请输入内容")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 刮刮乐列表
    st.subheader("🔍 探索刮刮乐")
    
    for card in st.session_state.scratch_cards[:10]:  # 显示前10个
        is_scratched = card["id"] in st.session_state.scratched_cards
        
        st.markdown(
            f"""
            <div class='glass-card' style='position: relative; min-height: 120px;'>
                <div style='display: flex; align-items: center; margin-bottom: 0.5rem;'>
                    <span style='font-size: 1.2rem; margin-right: 0.5rem;'>🎁</span>
                    <span style='font-size: 0.9rem; color: #666;'>来自 {card['author']}</span>
                </div>
            """,
            unsafe_allow_html=True,
        )
        
        if not is_scratched:
            # 未刮开状态
            st.markdown(
                f"""
                <div style='background: {"#e0e0e0" if card["coating_color"] == "浅灰" else "#e6f0ff" if card["coating_color"] == "浅蓝" else "#f0e6ff"}; 
                            border-radius: 12px; padding: 40px; text-align: center; color: #888;'>
                    ✨ 内容被涂层遮住，刮开才可见
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"🔍 刮一刮", key=f"scratch_{card['id']}", use_container_width=True):
                st.session_state.scratched_cards.add(card["id"])
                card["scratches"] = card.get("scratches", 0) + 1
                st.success("你选择看见这一句了。")
                st.rerun()
        else:
            # 已刮开状态
            st.markdown(
                f"""
                <div style='background: rgba(255,255,255,0.9); border-radius: 12px; padding: 20px; 
                            border: 1px solid rgba(22,119,255,0.2);'>
                    <div style='font-size: 1rem; color: #333; line-height: 1.6;'>{card['content']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("❤️ 喜欢", key=f"like_sc_{card['id']}", use_container_width=True):
                    st.toast("已收藏这条刮刮乐")
            with col2:
                if st.button("📤 分享", key=f"share_sc_{card['id']}", use_container_width=True):
                    st.info("分享功能开发中...")
            with col3:
                if st.button("💬 评论", key=f"comment_sc_{card['id']}", use_container_width=True):
                    st.info("评论功能开发中...")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== 我的岸页 ====================
def page_mine():
    """我的岸页 - 个人主页"""
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # 页面标题
    st.markdown("<h2 style='color: #1677ff; margin-bottom: 0.5rem;'>🏠 我的岸</h2>", unsafe_allow_html=True)
    st.caption("你的数字自留地，双身份完全隔离")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 双身份切换
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👤 真身 · 我", use_container_width=True, 
                     type="primary" if st.session_state.get("mine_tab") != "anon" else "secondary"):
            st.session_state.mine_tab = "real"
            st.rerun()
    with col2:
        if st.button("🌊 匿名 · 浪", use_container_width=True,
                     type="primary" if st.session_state.get("mine_tab") == "anon" else "secondary"):
            st.session_state.mine_tab = "anon"
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 根据当前身份显示内容
    is_anon = st.session_state.get("mine_tab") == "anon"
    
    if is_anon:
        # 匿名身份
        profile = st.session_state.anon_profile
        posts = st.session_state.anon_posts
        identity_id = st.session_state.anonymous_id
        identity_label = "浪"
    else:
        # 真身身份
        profile = st.session_state.real_profile
        posts = st.session_state.real_posts
        identity_id = st.session_state.real_name
        identity_label = "真身"
    
    # 个人封面与资料
    st.markdown(
        f"""
        <div class='glass-card' style='text-align: center;'>
            <div style='font-size: 4rem; margin-bottom: 0.5rem;'>{profile['avatar_emoji']}</div>
            <div style='font-size: 1.3rem; font-weight: 600; color: #333; margin-bottom: 0.3rem;'>
                {identity_id}
            </div>
            <div style='font-size: 0.9rem; color: #666; margin-bottom: 1rem;'>
                {profile['intro']}
            </div>
            <div style='font-size: 0.8rem; color: #999;'>
                📝 {len(posts)} 条动态 · 👥 {len(st.session_state.friends_real if not is_anon else st.session_state.friends_anon)} 位好友
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 编辑资料
    with st.expander("✏️ 编辑资料"):
        new_intro = st.text_area("个人介绍", value=profile['intro'], max_chars=200)
        new_avatar = st.selectbox("头像", ["🌊", "🌫️", "✨", "🌙", "🌸", "🍃", "🔥", "💧"])
        if st.button("保存", use_container_width=True, type="primary"):
            profile['intro'] = new_intro
            profile['avatar_emoji'] = new_avatar
            st.success("资料已更新")
            st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 动态列表
    st.subheader(f"📋 {identity_label}的动态")
    
    if not posts:
        st.info(f"还没有{identity_label}动态，去「现在」页发布一条吧")
    else:
        for post in posts:
            st.markdown(
                f"""
                <div class='glass-card'>
                    <div style='font-size: 1rem; color: #333; margin-bottom: 0.5rem; line-height: 1.6;'>
                        {post['text']}
                    </div>
                    <div style='font-size: 0.8rem; color: #999;'>
                        {post['time']} · {post.get('mood', '未标注')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    # 私密笔记（仅真身身份显示）
    if not is_anon and st.session_state.private_notes:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔒 私密笔记（仅自己可见）")
        for note in st.session_state.private_notes:
            st.markdown(
                f"""
                <div class='glass-card' style='background: rgba(255,255,255,0.5);'>
                    <div style='font-size: 1rem; color: #333; margin-bottom: 0.5rem;'>{note['text']}</div>
                    <div style='font-size: 0.8rem; color: #999;'>{note['time']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== 聊天页 ====================
def page_chat():
    """聊天页 - 好友系统与私聊"""
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # 页面标题
    st.markdown("<h2 style='color: #1677ff; margin-bottom: 0.5rem;'>💬 聊天</h2>", unsafe_allow_html=True)
    st.caption("轻量私聊与好友管理，双身份好友完全隔离")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 好友申请
    if st.session_state.friend_requests:
        with st.expander(f"🔔 好友申请 ({len(st.session_state.friend_requests)})", expanded=True):
            for req in st.session_state.friend_requests:
                st.markdown(
                    f"""
                    <div class='glass-card'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <div style='font-weight: 500;'>来自 {req['from']}</div>
                                <div style='font-size: 0.8rem; color: #999;'>{req['source']} · {req['time']}</div>
                                <div style='font-size: 0.9rem; color: #666; margin-top: 0.3rem;'>{req['message']}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✓ 同意", key=f"accept_{req['id']}", use_container_width=True, type="primary"):
                        # 添加到匿名好友列表
                        st.session_state.friends_anon.append({
                            "id": req['from'],
                            "name": req['from'],
                            "source": req['source'],
                        })
                        st.session_state.friend_requests = [r for r in st.session_state.friend_requests if r['id'] != req['id']]
                        st.success(f"已添加 {req['from']} 为好友")
                        st.rerun()
                with col2:
                    if st.button("✗ 拒绝", key=f"reject_{req['id']}", use_container_width=True):
                        st.session_state.friend_requests = [r for r in st.session_state.friend_requests if r['id'] != req['id']]
                        st.rerun()
    
    # 添加好友
    with st.expander("➕ 添加好友"):
        search_id = st.text_input("输入用户ID", placeholder="输入真身或匿名ID")
        if st.button("搜索", use_container_width=True):
            if search_id:
                st.info(f"已发送好友申请给 {search_id}")
            else:
                st.warning("请输入用户ID")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 好友列表
    tab_real, tab_anon = st.tabs(["真身好友", "匿名好友"])
    
    with tab_real:
        if not st.session_state.friends_real:
            st.info("还没有真身好友")
        else:
            for friend in st.session_state.friends_real:
                st.markdown(
                    f"""
                    <div class='glass-card'>
                        <div style='display: flex; align-items: center;'>
                            <span style='font-size: 2rem; margin-right: 1rem;'>👤</span>
                            <div style='flex: 1;'>
                                <div style='font-weight: 500;'>{friend['name']}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    
    with tab_anon:
        if not st.session_state.friends_anon:
            st.info("还没有匿名好友，去广场打招呼添加吧")
        else:
            for friend in st.session_state.friends_anon:
                st.markdown(
                    f"""
                    <div class='glass-card'>
                        <div style='display: flex; align-items: center; justify-content: space-between;'>
                            <div style='display: flex; align-items: center;'>
                                <span style='font-size: 2rem; margin-right: 1rem;'>🌊</span>
                                <div>
                                    <div style='font-weight: 500;'>{friend['name']}</div>
                                    <div style='font-size: 0.8rem; color: #999;'>来自 {friend.get('source', '广场')}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("💬 聊天", key=f"chat_{friend['id']}", use_container_width=True):
                    st.session_state.current_chat = friend
                    st.info(f"开始与 {friend['name']} 聊天")
    
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== 设置页 ====================
def page_settings():
    """设置页"""
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #1677ff; margin-bottom: 0.5rem;'>⚙️ 设置</h2>", unsafe_allow_html=True)
    st.caption("管理你的岸与安全感")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 账号信息
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("👤 账号信息")
    st.write(f"**当前身份：** {st.session_state.real_name}")
    st.write(f"**匿名代号：** {st.session_state.anonymous_id}")
    st.write(f"**用户ID：** {st.session_state.user_id}")
    if st.session_state.is_guest:
        st.warning("当前为游客模式，部分功能受限")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 屏蔽词设置
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🛡️ 屏蔽词")
    st.caption("包含以下词语的内容会在匿名广场中被自动折叠")
    muted_str = ", ".join(st.session_state.muted_words) if st.session_state.muted_words else ""
    new_muted = st.text_input("屏蔽词（用英文逗号分隔）", value=muted_str, placeholder="例如：加班, 分手")
    if new_muted != muted_str:
        st.session_state.muted_words = [w.strip() for w in new_muted.split(",") if w.strip()]
        st.success("屏蔽词已更新")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 通知设置
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔔 通知设置")
    st.session_state.notifications["chat"] = st.toggle("私聊消息", value=st.session_state.notifications.get("chat", True))
    st.session_state.notifications["circle"] = st.toggle("圈子动态", value=st.session_state.notifications.get("circle", True))
    st.session_state.notifications["square"] = st.toggle("广场互动", value=st.session_state.notifications.get("square", True))
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 退出登录
    if st.session_state.is_logged_in:
        if st.button("🚪 退出登录", use_container_width=True, type="secondary"):
            st.session_state.is_logged_in = False
            st.session_state.current_page = "login"
            st.success("已退出登录")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)


# ==================== 主入口 ====================
def main():
    """主入口函数"""
    # 页面配置
    st.set_page_config(
        page_title="岸 - 不需要变好，只需要坐下",
        page_icon="🌊",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    
    # 初始化状态
    init_state()
    
    # 渲染全局样式
    render_global_styles()
    
    # 根据当前页面状态渲染不同内容
    if st.session_state.current_page == "landing":
        page_landing()
    elif st.session_state.current_page == "login":
        page_login()
    else:  # main
        # 主应用页面
        tab_pages = {
            "now": page_now,
            "square": page_square,
            "tearoom": page_tearoom,
            "scratch": page_scratch,
            "mine": page_mine,
            "chat": page_chat,
            "settings": page_settings,
        }
        
        # 渲染当前Tab页面
        current_tab = st.session_state.current_tab
        if current_tab in tab_pages:
            tab_pages[current_tab]()
        else:
            page_now()
        
        # 渲染底部导航
        st.markdown("<hr style='margin: 2rem 0;'>", unsafe_allow_html=True)
        render_bottom_nav()


if __name__ == "__main__":
    main()
