import streamlit as st
import time
import random

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="Image Model UX Test",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 自定义 CSS (保持不变) ---
st.markdown("""
<style>
    .stApp { background-color: #FAFAFA; font-family: 'Helvetica Neue', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    h1, h2, h3 { color: #333; font-weight: 600; }
    div.stButton > button {
        background-color: #FFFFFF; color: #4A4A4A; border: 1px solid #E0E0E0;
        border-radius: 12px; padding: 10px 24px; transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    div.stButton > button:hover {
        border-color: #B0C4DE; color: #2E86C1; background-color: #F0F8FF; transform: translateY(-2px);
    }
    div.stButton > button:active { background-color: #E6F2FF; border-color: #2E86C1; }
    .role-card {
        background-color: white; padding: 20px; border-radius: 15px;
        border: 1px solid #F0F0F0; text-align: center; margin-bottom: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    .stProgress > div > div > div > div { background-color: #ADD8E6; }
    .stTextInput > div > div > input { border-radius: 10px; border: 1px solid #E0E0E0; }
</style>
""", unsafe_allow_html=True)

# --- 3. 状态管理 (已修复: 确保 questions 被初始化) ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'role' not in st.session_state:
    st.session_state.role = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
# [关键修复] 必须初始化 questions，防止 key error
if 'questions' not in st.session_state:
    st.session_state.questions = []

# --- 4. 题目数据结构 ---
QUESTIONS = {
    "public": [
        {"type": "img_gen_ab", "title": "✨ 魔法变身测试", "desc": "上传一张照片，输入一句咒语，看看AI的魔法效果！"},
        {"type": "choice", "title": "👀 第一眼感觉", "desc": "你觉得这个模型生成的图片色彩风格更偏向？", "options": ["清新自然 🍃", "浓郁油画 🎨", "赛博朋克 🤖", "写实摄影 📷"]},
        {"type": "text", "title": "💭 脑洞时刻", "desc": "如果让你用这个AI生成一张图发朋友圈，你会让它画什么？"},
    ],
    "designer": [
        {"type": "ab_static", "title": "🔍 材质细节观察", "desc": "作为设计师，你觉得哪张图的【玻璃光影】处理更符合物理规律？", "img_src": ["img_a", "img_b"]},
        {"type": "slider", "title": "🎨 创意落地程度", "desc": "生成的图像是否可以直接用于商业海报草图？（1=完全不行，10=只需微调）"},
        {"type": "text", "title": "🛠️ 工具流接入", "desc": "你希望这个模型能导出分层PSD文件吗？还是只需要PNG？"},
    ],
    "expert": [
        {"type": "choice", "title": "🧠 语义对齐测试", "desc": "Prompt: '一只穿着宇航服的猫在水下骑自行车'。模型是否准确生成了所有元素？", "options": ["完美对齐 ✅", "漏了自行车 🚲", "环境不对 🌊", "伪影严重 😵"]},
        {"type": "text", "title": "🐛 找茬模式", "desc": "请指出上一张生成图中，手部或肢体结构的逻辑错误。"},
        {"type": "slider", "title": "⚡ 推理速度", "desc": "刚才的生成速度（Latency）在你的接受范围内吗？"},
    ]
}

def fill_questions(role_key):
    base_qs = QUESTIONS[role_key].copy() # 使用 copy 防止污染原始数据
    while len(base_qs) < 10:
        idx = len(base_qs) + 1
        base_qs.append({"type": "choice", "title": f"📝 测试题 #{idx}", "desc": "这是一个通用测试维度：你对图像的清晰度满意吗？", "options": ["非常满意 😍", "一般般 😐", "有待提高 🫠"]})
    return base_qs

# --- 5. 功能函数 ---
def next_step():
    st.session_state.step += 1
    st.rerun()

def select_role(role_name):
    st.session_state.role = role_name
    st.session_state.questions = fill_questions(role_name)
    next_step()

# --- 6. 页面渲染逻辑 ---

# [PAGE 0] 身份选择页
if st.session_state.step == 0:
    st.markdown("<div style='text-align: center; margin-top: 50px;'><h1>👋 欢迎来到视觉实验室</h1><p style='color:gray;'>请选择最符合你的身份卡片开启体验</p></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='role-card'><h2>🥑</h2><h3>大众体验官</h3></div>", unsafe_allow_html=True)
        if st.button("我是大众用户", key="btn_public", use_container_width=True):
            select_role("public")
    with col2:
        st.markdown("<div class='role-card'><h2>🎨</h2><h3>视觉设计师</h3></div>", unsafe_allow_html=True)
        if st.button("我是设计师", key="btn_designer", use_container_width=True):
            select_role("designer")
    with col3:
        st.markdown("<div class='role-card'><h2>🤖</h2><h3>AIGC 专家</h3></div>", unsafe_allow_html=True)
        if st.button("我是AI专家", key="btn_expert", use_container_width=True):
            select_role("expert")

# [PAGE 1-10] 答题页
elif 1 <= st.session_state.step <= 10:
    
    # [安全检查] 如果用户在答题中途刷新页面，questions 可能会变空，导致报错
    # 此时我们强制重置回首页
    if not st.session_state.questions:
        st.warning("⚠️ 页面已刷新，请重新选择身份。")
        st.session_state.step = 0
        if st.button("返回首页"):
            st.rerun()
        st.stop() # 停止后续代码执行

    q_index = st.session_state.step - 1
    current_q = st.session_state.questions[q_index]
    
    # 进度条
    st.progress(st.session_state.step / 10)
    st.caption(f"Question {st.session_state.step} / 10")
    
    st.markdown(f"### {current_q['title']}")
    st.markdown(f"{current_q['desc']}")
    
    # 类型1：图生图 + Prompt -> A/B 测试
    if current_q['type'] == 'img_gen_ab':
        uploaded_file = st.file_uploader("上传一张参考图 (可选)", type=['png', 'jpg'])
        prompt = st.text_input("输入你的Prompt (咒语)", placeholder="例如：把这张图变成梵高风格的油画...")
        
        if prompt:
            # 使用 session_state 记录生成状态，防止点击按钮后页面刷新重置
            if f"gen_done_{q_index}" not in st.session_state:
                 if st.button("✨ 开始生成 (模拟)", use_container_width=True):
                    with st.spinner('AI 正在挥洒笔墨...'):
                        time.sleep(1.5)
                    st.session_state[f"gen_done_{q_index}"] = True
                    st.rerun()
            
            if st.session_state.get(f"gen_done_{q_index}"):
                st.success("生成完毕！请选择你更喜欢的一张：")
                c1, c2 = st.columns(2)
                with c1:
                    st.image("https://placehold.co/400x400/EEE/31343C?text=Model+A", caption="模型 A")
                    if st.button("❤️ 喜欢 A", key=f"q{q_index}_a", use_container_width=True):
                        st.session_state.answers[f"q{q_index}"] = "Model A"
                        next_step()
                with c2:
                    st.image("https://placehold.co/400x400/EEE/31343C?text=Model+B", caption="模型 B")
                    if st.button("❤️ 喜欢 B", key=f"q{q_index}_b", use_container_width=True):
                        st.session_state.answers[f"q{q_index}"] = "Model B"
                        next_step()
                if st.button("🤷 差不多 / 都不行", key=f"q{q_index}_tie"):
                    st.session_state.answers[f"q{q_index}"] = "Tie"
                    next_step()

    # 类型2：固定单选题
    elif current_q['type'] == 'choice':
        choice = st.radio("请选择:", current_q['options'], index=None)
        if choice:
            if st.button("确认并继续 ➡️", key=f"btn_choice_{q_index}"):
                st.session_state.answers[f"q{q_index}"] = choice
                next_step()

    # 类型3：文本开放题
    elif current_q['type'] == 'text':
        txt = st.text_area("你的看法:", height=100, key=f"txt_{q_index}")
        if st.button("提交 ➡️", key=f"btn_text_{q_index}") and txt:
            st.session_state.answers[f"q{q_index}"] = txt
            next_step()

    # 类型4：滑块打分
    elif current_q['type'] == 'slider':
        score = st.slider("拖动滑块打分", 0, 10, 5, key=f"slider_{q_index}")
        if st.button("确认评分 ➡️", key=f"btn_slider_{q_index}"):
            st.session_state.answers[f"q{q_index}"] = score
            next_step()

    # 类型5：静态A/B测试
    elif current_q['type'] == 'ab_static':
        c1, c2 = st.columns(2)
        with c1:
            st.info("🖼️ 方案 A (模拟图)")
        with c2:
            st.info("🖼️ 方案 B (模拟图)")
        sel = st.radio("你的选择是？", ["方案 A 更好", "方案 B 更好", "无法判断"], key=f"radio_ab_{q_index}")
        if st.button("下一题 ➡️", key=f"btn_ab_{q_index}"):
            st.session_state.answers[f"q{q_index}"] = sel
            next_step()

# [PAGE 11] 结束页
elif st.session_state.step == 11:
    st.balloons()
    st.markdown(f"""
    <div style='text-align: center; margin-top: 50px;'>
        <h1>🎉 感谢你的参与！</h1>
        <div style='background-color:#F0F8FF; padding:20px; border-radius:10px; margin-top:20px;'>
            <p>✅ 身份: <strong>{st.session_state.role}</strong></p>
            <p>✅ 已完成测试</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("🔍 Debug 数据"):
        st.write(st.session_state.answers)
    
    if st.button("🔄 重新开始"):
        st.session_state.clear()
        st.rerun()
