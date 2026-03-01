# app.py   岸 Demo v2.5 - 社交页「一个+号 + 卷帘门」版
import streamlit as st
import sys

# 强制 UTF-8 防乱码
if sys.stdout.encoding != 'utf-8':
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)
if sys.stderr.encoding != 'utf-8':
    sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf-8', buffering=1)


def init_engine():
    if "is_init" not in st.session_state:
        st.session_state.is_init = True
        st.session_state.active_section = "用户"  # 仅用于兼容，其他页面不影响
        st.session_state.tea_balance = 12
        st.session_state.tea_sent_today = 3
        st.session_state.current_identity_index = 0

        st.session_state.identities = [
            {"id": 0, "name": "野狐狸", "avatar": "🦊", "type": "真身", "is_anon": False},
            {"id": 1, "name": "匿名的云", "avatar": "☁️", "type": "分身", "is_anon": True},
            {"id": 2, "name": "深夜的灯", "avatar": "🪔", "type": "分身", "is_anon": True},
            {"id": 3, "name": "漂流的瓶", "avatar": "📜", "type": "分身", "is_anon": True},
        ]

        st.session_state.chat_list = [
            {"name": "摆渡人", "type": "用户", "last_msg": "晚安，记得关灯", "icon": "🧭"},
            {"name": "失眠聊天室", "type": "话题", "last_msg": "今晚 4.7k 人在线", "icon": "🌑"},
            {"name": "无人电台", "type": "群聊", "last_msg": "正在播放：雨声", "icon": "📻"},
            {"name": "旧时光", "type": "用户", "last_msg": "你还记得那年夏天吗", "icon": "📷"},
            {"name": "咖啡因过量", "type": "话题", "last_msg": "2.1k 人共鸣", "icon": "☕"},
        ]

        st.session_state.posts = [
            {"id": 1, "content": "今天又加班到凌晨，地铁已经停了，只能走回家。", "tea": 5, "author": "匿名的云",
             "avatar": "☁️", "comments": ["辛苦了，注意身体哦"]},
            {"id": 2, "content": "突然很想吃小时候巷口的那家肠粉。", "tea": 3, "author": "野狐狸", "avatar": "🦊",
             "comments": ["+1"]},
        ]


def apply_style():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {max-width:460px !important; margin:0 auto; background:#fdfaf3;}
    .expander-header {font-size:18px; font-weight:600;}
    .chat-card {
        padding:14px 10px; border-bottom:1px solid #e8dfc7; display:flex; gap:12px; align-items:center;
    }
    .avatar {
        width:48px; height:48px; border-radius:12px; background:#f0e6d2;
        display:flex; align-items:center; justify-content:center; font-size:24px;
    }
    .muted {color:#8b7d66; font-size:13px;}
    </style>
    """, unsafe_allow_html=True)


def render_current_identity():
    idx = st.session_state.current_identity_index
    iden = st.session_state.identities[idx]
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;padding:12px;background:#f0e6d2;border-radius:12px;margin-bottom:16px;">
        <div style="font-size:48px;">{iden['avatar']}</div>
        <div>
            <div style="font-weight:bold;font-size:18px;">{iden['name']}</div>
            <div class="muted">{iden['type']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ====================== 社交页（核心升级） ======================
def page_social():
    st.markdown("### 发现")

    # 1. 搜索框
    search_term = st.text_input("🔍 搜索...", placeholder="用户 / 话题 / 群聊", key="social_search")

    # 2. 一个 + 号入口（卷帘门式菜单）
    with st.expander("＋ 新建 / 添加", expanded=False):
        st.markdown("**选择操作**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👤 添加好友"):
                friend_id = st.text_input("输入对方 ID 或昵称", key="add_friend_id")
                if st.button("确认添加", key="confirm_add"):
                    st.success("已发送好友请求！（模拟）")

        with col2:
            if st.button("📷 扫一扫"):
                st.info("摄像头扫描二维码（Demo 暂不支持真实扫码）")

        st.divider()
        topic = st.text_input("💬 创建新话题", key="new_topic")
        if st.button("创建话题", key="btn_create_topic") and topic.strip():
            st.session_state.chat_list.append({
                "name": topic, "type": "话题", "last_msg": "刚刚创建 · 0 人参与", "icon": "🔥"
            })
            st.success(f"话题「{topic}」已创建！")

        group = st.text_input("👥 创建新群聊", key="new_group")
        if st.button("创建群聊", key="btn_create_group") and group.strip():
            st.session_state.chat_list.append({
                "name": group, "type": "群聊", "last_msg": "你创建的群聊 · 1/50", "icon": "🫂"
            })
            st.success(f"群聊「{group}」创建成功！")

    st.divider()

    # 3. 三个卷帘门（大标题 + 点击展开列表）
    with st.expander("👤 用户", expanded=False):
        for item in st.session_state.chat_list:
            if item["type"] == "用户" and (not search_term or search_term.lower() in item["name"].lower()):
                st.markdown(f"""
                <div class="chat-card">
                    <div class="avatar">{item['icon']}</div>
                    <div>
                        <div style="font-weight:600;">{item['name']}</div>
                        <div class="muted">{item['last_msg']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with st.expander("💬 话题", expanded=False):
        for item in st.session_state.chat_list:
            if item["type"] == "话题" and (not search_term or search_term.lower() in item["name"].lower()):
                st.markdown(f"""
                <div class="chat-card">
                    <div class="avatar">{item['icon']}</div>
                    <div>
                        <div style="font-weight:600;">{item['name']}</div>
                        <div class="muted">{item['last_msg']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with st.expander("👥 群聊", expanded=False):
        for item in st.session_state.chat_list:
            if item["type"] == "群聊" and (not search_term or search_term.lower() in item["name"].lower()):
                st.markdown(f"""
                <div class="chat-card">
                    <div class="avatar">{item['icon']}</div>
                    <div>
                        <div style="font-weight:600;">{item['name']}</div>
                        <div class="muted">{item['last_msg']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# 其他页面函数保持不变（复制你上一个版本的 page_feed、page_post、page_profile 即可）
# 为完整性，这里给出简版（你可以直接粘贴替换）

def page_feed():
    for post in st.session_state.posts:
        st.markdown(f"""
        <div style="padding:16px; background:white; border-radius:12px; margin-bottom:12px; border:1px solid #e8dfc7;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:32px;">{post['avatar']}</span>
                <strong>{post['author']}</strong>
            </div>
            <div style="margin:12px 0;">{post['content']}</div>
            <div class="muted">🍵 {post['tea']} 杯茶</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🍵 送茶", key=f"tea_{post['id']}"):
                if st.session_state.tea_balance > 0:
                    post["tea"] += 1
                    st.session_state.tea_balance -= 1
                    st.session_state.tea_sent_today += 1
                    st.rerun()
        with c2:
            if st.button("查看回应", key=f"view_{post['id']}"):
                st.session_state[f"show_{post['id']}"] = not st.session_state.get(f"show_{post['id']}", False)
                st.rerun()
            if st.session_state.get(f"show_{post['id']}", False):
                for c in post.get("comments", []):
                    st.write(f"• {c}")


def page_post():
    curr = st.session_state.identities[st.session_state.current_identity_index]
    st.write(f"以 **{curr['avatar']} {curr['name']}** 发布")
    content = st.text_area("此刻想说点什么？", height=150)
    if st.button("投递到芦花荡", type="primary") and content.strip():
        st.session_state.posts.insert(0, {
            "id": len(st.session_state.posts) + 100,
            "content": content,
            "tea": 0,
            "author": curr["name"],
            "avatar": curr["avatar"],
            "comments": []
        })
        st.success("已投递～")
        st.rerun()


def page_profile():
    st.subheader("我的茶仓")
    st.metric("当前茶叶", f"{st.session_state.tea_balance} 杯")
    st.metric("今日送出", f"{st.session_state.tea_sent_today} 杯")
    if st.button("补充 10 杯茶叶"):
        st.session_state.tea_balance += 10
        st.rerun()

    st.divider()
    st.subheader("身份切换（旋转门）")
    idx = st.session_state.current_identity_index
    curr = st.session_state.identities[idx]
    st.markdown(f"<div style='text-align:center;font-size:90px;margin:10px 0;'>{curr['avatar']}</div>",
                unsafe_allow_html=True)
    st.subheader(curr['name'])
    st.caption(curr['type'])

    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.button("←"):
            st.session_state.current_identity_index = (idx - 1) % 4
            st.rerun()
    with c2:
        st.markdown(
            f"<div style='text-align:center;padding:10px;background:#f0e6d2;border-radius:8px;'>第 {idx + 1} 个身份</div>",
            unsafe_allow_html=True)
    with c3:
        if st.button("→"):
            st.session_state.current_identity_index = (idx + 1) % 4
            st.rerun()


def main():
    st.set_page_config(page_title="岸", layout="centered", page_icon="🌾")
    init_engine()
    apply_style()

    render_current_identity()

    tab1, tab2, tab3, tab4 = st.tabs(["💬 社交", "🌾 芦花荡", "➕ 发布", "👤 我"])
    with tab1: page_social()
    with tab2: page_feed()
    with tab3: page_post()
    with tab4: page_profile()


if __name__ == "__main__":
    main()