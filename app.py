import streamlit as st
import time

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="Image Model UX Test",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 极简美学视觉系统 (CSS) ---
st.markdown("""
<style>
    /* 全局重置：纯白背景，深灰字体 */
    .stApp {
        background-color: #FFFFFF;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #444444;
    }
    
    /* ------------------------------------------------ */
    /* 🔘 幽灵按钮系统 (完全去除红色) */
    /* ------------------------------------------------ */
    
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #666666 !important;
        border: 1px solid #EAEAEA !important;
        border-radius: 100px !important; /* 全圆角，更灵动 */
        padding: 10px 28px;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    
    /* Hover: 极淡蓝背景 + 稍微深一点的描边 */
    div.stButton > button:hover {
        background-color: #F7FBFF !important;
        border-color: #D1E9FF !important;
        color: #007AFF !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,122,255,0.08);
    }
    
    /* Active: 点击瞬间 */
    div.stButton > button:active {
        background-color: #EEF7FF !important;
        transform: scale(0.98);
    }

    /* ------------------------------------------------ */
    /* 🃏 空气感身份卡片 (Ultra-Light) */
    /* ------------------------------------------------ */
    
    .role-card-base {
        padding: 30px 20px;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 20px;
        transition: all 0.3s ease;
        border: 1px solid transparent;
        cursor: pointer;
    }
    
    .role-card-base:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
    }
    
    /* 1. 大众用户: 极淡云雾绿 */
    .card-public {
        background-color: #FAFCFA; 
        border-color: #F0F7F0;
    }
    .card-public h3 { color: #5D8F6E; }
    
    /* 2. 设计师: 极淡冰川蓝 */
    .card-designer {
        background-color: #FAFCFF;
        border-color: #F0F5FA;
    }
    .card-designer h3 { color: #5B86B0; }
    
    /* 3. 专家: 极淡晨曦紫 */
    .card-expert {
        background-color: #FCFAFD;
        border-color: #F7F0F9;
    }
    .card-expert h3 { color: #9B7FA8; }
    
    /* Emoji 大小 */
    .card-emoji { font-size: 42px; margin-bottom: 10px; display: block; }
    
    /* 卡片描述字 */
    .card-desc { font-size: 12px; color: #999; letter-spacing: 0.5px; margin-top: 8px; }

    /* ------------------------------------------------ */
    /* 🧼 界面降噪 (隐藏无关元素) */
    /* ------------------------------------------------ */
    
    /* 隐藏标题锚点 */
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a { display: none !important; }
    [data-testid="stHeaderActionElements"] { display: none !important; }
    #MainMenu, footer {visibility: hidden;}
    
    /* 进度条极简细线化 */
    .stProgress > div > div { height: 4px !important; border-radius: 2px; }
    .stProgress > div > div > div > div { background-color: #E0E0E0; background-image: linear-gradient(to right, #E0E0E0, #AECBFA); }
    
    /* 输入框极简 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #FCFCFC;
        border: 1px solid #EFEFEF;
        border-radius: 12px;
        color: #555;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #D1E9FF;
        box-shadow: 0 0 0 2px rgba(209, 233, 255, 0.3);
    }
    
    /* 标题样式 */
    h1 { font-weight: 700; color: #222; letter-spacing: -1px; font-size: 2.2rem; }
    h3 { font-weight: 600; color: #444; font-size: 1.4rem; }
</style>
""", unsafe_allow_html=True)

# --- 3. 状态管理 ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'role' not in st.session_state: st.session_state.role = None
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'questions' not in st.session_state: st.session_state.questions = []

# --- 4. 题目数据库 (保持不变，内容完整) ---
QUESTIONS = {
    "public": [
        {"type": "img_gen_ab", "title": "✨ Q1: 魔法变身", "desc": "这是最重要的测试！请上传一张你喜欢的照片，让AI帮你重绘风格。"},
        {"type": "choice", "title": "👀 Q2: 风格偏好", "desc": "你觉得刚才生成的图片，哪种滤镜感更强？", "options": ["胶片复古感 🎞️", "二次元动漫感 🌸", "3D皮克斯感 🧸", "真实单反感 📸"]},
        {"type": "text", "title": "💭 Q3: 脑洞时刻", "desc": "如果这个AI能帮你画表情包，你希望画一个什么内容的表情包？"},
        {"type": "slider", "title": "🤣 Q4: 好玩程度", "desc": "你觉得刚才的生成过程有趣吗？(1=无聊, 10=超好玩)"},
        {"type": "ab_static", "title": "🖼️ Q5: 壁纸选择", "desc": "如果你要选一张做手机壁纸，你会选哪张？", "img_src": ["landscape_1", "landscape_2"]},
        {"type": "choice", "title": "🤔 Q6: 图灵测试", "desc": "看这张图中的人脸，你觉得是真人还是AI生成的？", "options": ["绝对是真人 🧑", "一眼假，是AI 🤖", "很难分辨 🤔"]},
        {"type": "text", "title": "🎨 Q7: 颜色感受", "desc": "用一个词形容模型生成图片的色彩风格（例如：温暖、冷淡、鲜艳...）"},
        {"type": "choice", "title": "🚀 Q8: 等待耐心", "desc": "刚才生成图片花了约5秒，你觉得这个速度？", "options": ["太快了！⚡", "刚刚好 🍵", "有点慢 🐢", "无法忍受 😫"]},
        {"type": "slider", "title": "💰 Q9: 付费意愿", "desc": "如果这是一个手机App，你愿意为它付费吗？(0=绝不, 10=买买买)"},
        {"type": "text", "title": "📝 Q10: 最终建议", "desc": "作为大众体验官，你最希望在这个模型里增加什么功能？"}
    ],
    "designer": [
        {"type": "ab_static", "title": "💡 Q1: 光影逻辑", "desc": "作为设计师，请判断哪张图的【环境光遮蔽(AO)】处理更自然？", "img_src": ["shadow_a", "shadow_b"]},
        {"type": "slider", "title": "✏️ Q2: 后期空间", "desc": "生成的图像素材是否方便在PS里进行二次编辑？(1=很难抠图, 10=非常干净)"},
        {"type": "text", "title": "📂 Q3: 格式需求", "desc": "你目前的工作流中，最痛恨JPEG格式的什么缺点？希望模型输出什么格式？"},
        {"type": "choice", "title": "📐 Q4: 构图审美", "desc": "模型生成的画面构图是否符合黄金分割或三分法？", "options": ["构图完美 ✅", "重心不稳 ⚖️", "元素杂乱 😵", "主体被切断 ✂️"]},
        {"type": "img_gen_ab", "title": "✒️ Q5: 字体设计辅助", "desc": "尝试输入Prompt生成一张海报背景，看看是否留出了足够的文字排版空间。"},
        {"type": "slider", "title": "🎨 Q6: 风格一致性", "desc": "如果连续生成10张图，画风的统一程度如何？"},
        {"type": "choice", "title": "🧩 Q7: 矢量感测试", "desc": "如果Prompt要求'扁平插画'，生成的图像是否足够干净、无杂色？", "options": ["干净利落 ✨", "有噪点/伪影 🌫️", "过度拟真(不像插画) 🚫"]},
        {"type": "text", "title": "💡 Q8: 灵感激发", "desc": "这个模型是更能帮你【找灵感】还是【出成品】？为什么？"},
        {"type": "ab_static", "title": "🤲 Q9: 手部结构", "desc": "这对于设计师是大忌。哪张图的手部结构错误更少？"},
        {"type": "slider", "title": "💼 Q10: 商业落地", "desc": "你会把刚才生成的图片直接交付给甲方看吗？"}
    ],
    "expert": [
        {"type": "choice", "title": "🧠 Q1: 语义对齐(CLIP)", "desc": "Prompt: '红色的宇航员骑着绿色的马'。是否存在属性错位（颜色反了）？", "options": ["完全正确 ✅", "颜色错位(红马绿人) ❌", "丢失物体 🌫️"]},
        {"type": "text", "title": "🐛 Q2: 伪影检测", "desc": "请仔细观察高频细节（如头发、草地），是否存在明显的平铺纹理或过度锐化？"},
        {"type": "slider", "title": "⚡ Q3: 推理延时(Latency)", "desc": "从点击到首token/出图的延迟是否满足实时交互标准？"},
        {"type": "img_gen_ab", "title": "🔧 Q4: 负面提示词测试", "desc": "输入Negative Prompt: 'nsfw, blurry'，测试模型是否严格遵守了负面约束。"},
        {"type": "choice", "title": "📉 Q5: 文本生成能力", "desc": "如果在图片中生成文字'HELLO'，模型的拼写正确率如何？", "options": ["拼写完美 🔡", "乱码/火星文 🉐", "字形扭曲 〰️"]},
        {"type": "slider", "title": "🎛️ Q6: ControlNet 兼容性", "desc": "你认为该底模对Canny/Depth等控制条件的响应灵敏度如何？"},
        {"type": "text", "title": "🌈 Q7: 动态范围", "desc": "直方图观察：图像是否存在过曝或死黑现象？灰阶过渡是否平滑？"},
        {"type": "choice", "title": "🧬 Q8: 多样性(Seed)", "desc": "固定Prompt不固定Seed，生成的Batch图像差异性如何？", "options": ["差异丰富 🎊", "千篇一律(Mode Collapse) 📉", "微小变化 🤏"]},
        {"type": "ab_static", "title": "🧱 Q9: 空间一致性", "desc": "观察这两张连续生成的室内设计图，空间透视是否逻辑自洽？"},
        {"type": "text", "title": "🛠️ Q10: 微调建议", "desc": "如果让你对该模型进行Fine-tuning，你会优先优化哪个层面的数据集？"}
    ]
}

# --- 5. 辅助函数 ---
def next_step():
    st.session_state.step += 1
    st.rerun()

def select_role(role_name):
    st.session_state.role = role_name
    st.session_state.questions = QUESTIONS[role_name]
    next_step()

# --- 6. 页面逻辑 ---

# [PAGE 0] 极简首页
if st.session_state.step == 0:
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True) # 顶部留白
    st.markdown("<div style='text-align: center; margin-bottom: 60px;'><h1>Vision Lab</h1><p style='color:#AAA; font-size: 16px; font-weight:300;'>Choose your perspective</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='role-card-base card-public'>
            <span class='card-emoji'>🥑</span>
            <h3>Public</h3>
            <p class='card-desc'>CASUAL / FUN</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("我是大众用户", key="btn_public", use_container_width=True):
            select_role("public")

    with col2:
        st.markdown("""
        <div class='role-card-base card-designer'>
            <span class='card-emoji'>💎</span>
            <h3>Designer</h3>
            <p class='card-desc'>AESTHETIC / PRO</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("我是设计师", key="btn_designer", use_container_width=True):
            select_role("designer")

    with col3:
        st.markdown("""
        <div class='role-card-base card-expert'>
            <span class='card-emoji'>⚡</span>
            <h3>Expert</h3>
            <p class='card-desc'>TECH / LOGIC</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("我是AI专家", key="btn_expert", use_container_width=True):
            select_role("expert")

# [PAGE 1-10] 答题页
elif 1 <= st.session_state.step <= 10:
    
    # 刷新保护
    if not st.session_state.questions:
        st.warning("⚠️ Session expired. Please restart.")
        st.session_state.step = 0
        if st.button("Return Home"): st.rerun()
        st.stop()

    q_index = st.session_state.step - 1
    current_q = st.session_state.questions[q_index]
    
    # 极简进度条
    st.progress(st.session_state.step / 10)
    st.markdown(f"<div style='text-align:right; color:#CCC; font-size:11px; margin-top:-10px; margin-bottom:30px; font-family:monospace;'>STEP {st.session_state.step} / 10</div>", unsafe_allow_html=True)
    
    st.markdown(f"### {current_q['title']}")
    st.markdown(f"<p style='color:#777; font-size:15px; font-weight:300; line-height:1.6; margin-bottom:40px;'>{current_q['desc']}</p>", unsafe_allow_html=True)
    
    # --- 组件区 ---
    
    # 1. 图像生成 + A/B
    if current_q['type'] == 'img_gen_ab':
        uploaded_file = st.file_uploader(" ", type=['png', 'jpg'], key=f"up_{q_index}", label_visibility="collapsed")
        if uploaded_file: st.caption("✅ 图片已上传")
        
        prompt = st.text_input("Prompt", placeholder="Describe what you want to see...", key=f"in_{q_index}", label_visibility="collapsed")
        
        if prompt:
            st.markdown("<br>", unsafe_allow_html=True)
            if f"gen_done_{q_index}" not in st.session_state:
                 if st.button("Generate ✨", use_container_width=True, key=f"gen_{q_index}"):
                    with st.spinner('Dreaming...'):
                        time.sleep(1.5)
                    st.session_state[f"gen_done_{q_index}"] = True
                    st.rerun()
            
            if st.session_state.get(f"gen_done_{q_index}"):
                st.success("Ready.")
                c1, c2 = st.columns(2)
                with c1:
                    st.image("https://placehold.co/400x400/FAFAFA/DDD?text=Option+A", caption="A")
                    if st.button("Pick A", key=f"qa_{q_index}", use_container_width=True):
                        st.session_state.answers[f"q{q_index}"] = "Model A"
                        next_step()
                with c2:
                    st.image("https://placehold.co/400x400/FAFAFA/DDD?text=Option+B", caption="B")
                    if st.button("Pick B", key=f"qb_{q_index}", use_container_width=True):
                        st.session_state.answers[f"q{q_index}"] = "Model B"
                        next_step()
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Can't Decide", key=f"tie_{q_index}", use_container_width=True):
                    st.session_state.answers[f"q{q_index}"] = "Tie"
                    next_step()

    # 2. 单选
    elif current_q['type'] == 'choice':
        choice = st.radio(" ", current_q['options'], index=None, key=f"radio_{q_index}", label_visibility="collapsed")
        if choice:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Continue", key=f"btn_c_{q_index}"):
                st.session_state.answers[f"q{q_index}"] = choice
                next_step()

    # 3. 文本
    elif current_q['type'] == 'text':
        txt = st.text_area(" ", height=120, placeholder="Type here...", key=f"txt_{q_index}", label_visibility="collapsed")
        if st.button("Submit", key=f"btn_t_{q_index}") and txt:
            st.session_state.answers[f"q{q_index}"] = txt
            next_step()

    # 4. 滑块
    elif current_q['type'] == 'slider':
        score = st.slider(" ", 0, 10, 5, key=f"sl_{q_index}", label_visibility="collapsed")
        st.markdown(f"<div style='text-align:center; font-size:24px; font-weight:300; color:#5B86B0; margin: 20px 0;'>{score}</div>", unsafe_allow_html=True)
        if st.button("Confirm", key=f"btn_s_{q_index}"):
            st.session_state.answers[f"q{q_index}"] = score
            next_step()

    # 5. 静态AB
    elif current_q['type'] == 'ab_static':
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://placehold.co/400x300/FAFAFA/DDD?text=A", caption="A")
        with c2:
            st.image("https://placehold.co/400x300/FAFAFA/DDD?text=B", caption="B")
        
        st.markdown("<br>", unsafe_allow_html=True)
        sel = st.radio(" ", ["Option A", "Option B", "Unsure"], key=f"ab_r_{q_index}", label_visibility="collapsed")
        if st.button("Next", key=f"btn_ab_{q_index}"):
            st.session_state.answers[f"q{q_index}"] = sel
            next_step()

# [PAGE 11] 结束页
elif st.session_state.step == 11:
    st.balloons()
    st.markdown(f"""
    <div style='text-align: center; margin-top: 80px;'>
        <h1 style='color:#5B86B0;'>All Set!</h1>
        <p style='color:#AAA; margin-top:10px;'>Thank you for your contribution.</p>
        <div style='margin-top:40px; padding: 20px; background-color: #FAFAFA; border-radius: 12px; display:inline-block;'>
            <span style='color:#888; font-size:12px;'>ROLE</span><br>
            <strong style='color:#444;'>{st.session_state.role.upper()}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("Restart", use_container_width=True):
        st.session_state.clear()
        st.rerun()
