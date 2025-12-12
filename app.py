import streamlit as st
import time

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="Image Model UX Test",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. 自定义 CSS (极简纯白风 + 去除锚点链接) ---
st.markdown("""
<style>
    /* 全局背景设为纯白/极淡灰 */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* 隐藏 Streamlit 默认的标题锚点链接 (去除🔗图标) */
    .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a {
        display: none !important;
        pointer-events: none;
    }
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    
    /* 隐藏菜单和页脚 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 标题颜色 */
    h1, h2, h3, h4 {
        color: #2C3E50;
        font-weight: 600;
    }
    
    /* 按钮样式优化：默认极淡，Hover时浅蓝 */
    div.stButton > button {
        background-color: #FAFAFA;
        color: #555;
        border: 1px solid #EEEEEE;
        border-radius: 12px;
        padding: 12px 24px;
        transition: all 0.2s ease-in-out;
        box-shadow: none;
    }
    div.stButton > button:hover {
        border-color: #B0C4DE;
        color: #2E86C1;
        background-color: #F8FBFF;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* 身份卡片样式 */
    .role-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #F0F0F0;
        text-align: center;
        margin-bottom: 15px;
        transition: transform 0.2s;
        box-shadow: 0 4px 20px rgba(0,0,0,0.02);
    }
    .role-card:hover {
        transform: translateY(-3px);
        border-color: #E0E0E0;
    }
    
    /* 进度条颜色 (淡蓝) */
    .stProgress > div > div > div > div {
        background-color: #AECBFA;
    }
    
    /* 输入框样式 */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #FAFAFA;
        border-radius: 10px;
        border: 1px solid #EAEAEA;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 状态管理 ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'role' not in st.session_state:
    st.session_state.role = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}
if 'questions' not in st.session_state:
    st.session_state.questions = []

# --- 4. 题目数据库 (100% 独立内容) ---
QUESTIONS = {
    "public": [
        # Q1
        {"type": "img_gen_ab", "title": "✨ Q1: 魔法变身", "desc": "这是最重要的测试！请上传一张你喜欢的照片，让AI帮你重绘风格。"},
        # Q2
        {"type": "choice", "title": "👀 Q2: 风格偏好", "desc": "你觉得刚才生成的图片，哪种滤镜感更强？", "options": ["胶片复古感 🎞️", "二次元动漫感 🌸", "3D皮克斯感 🧸", "真实单反感 📸"]},
        # Q3
        {"type": "text", "title": "💭 Q3: 脑洞时刻", "desc": "如果这个AI能帮你画表情包，你希望画一个什么内容的表情包？"},
        # Q4
        {"type": "slider", "title": "🤣 Q4: 好玩程度", "desc": "你觉得刚才的生成过程有趣吗？(1=无聊, 10=超好玩)"},
        # Q5
        {"type": "ab_static", "title": "🖼️ Q5: 壁纸选择", "desc": "如果你要选一张做手机壁纸，你会选哪张？", "img_src": ["landscape_1", "landscape_2"]},
        # Q6
        {"type": "choice", "title": "🤔 Q6: 图灵测试", "desc": "看这张图中的人脸，你觉得是真人还是AI生成的？", "options": ["绝对是真人 🧑", "一眼假，是AI 🤖", "很难分辨 🤔"]},
        # Q7
        {"type": "text", "title": "🎨 Q7: 颜色感受", "desc": "用一个词形容模型生成图片的色彩风格（例如：温暖、冷淡、鲜艳...）"},
        # Q8
        {"type": "choice", "title": "🚀 Q8: 等待耐心", "desc": "刚才生成图片花了约5秒，你觉得这个速度？", "options": ["太快了！⚡", "刚刚好 🍵", "有点慢 🐢", "无法忍受 😫"]},
        # Q9
        {"type": "slider", "title": "💰 Q9: 付费意愿", "desc": "如果这是一个手机App，你愿意为它付费吗？(0=绝不, 10=买买买)"},
        # Q10
        {"type": "text", "title": "📝 Q10: 最终建议", "desc": "作为大众体验官，你最希望在这个模型里增加什么功能？"}
    ],
    
    "designer": [
        # Q1
        {"type": "ab_static", "title": "💡 Q1: 光影逻辑", "desc": "作为设计师，请判断哪张图的【环境光遮蔽(AO)】处理更自然？", "img_src": ["shadow_a", "shadow_b"]},
        # Q2
        {"type": "slider", "title": "✏️ Q2: 后期空间", "desc": "生成的图像素材是否方便在PS里进行二次编辑？(1=很难抠图, 10=非常干净)"},
        # Q3
        {"type": "text", "title": "📂 Q3: 格式需求", "desc": "你目前的工作流中，最痛恨JPEG格式的什么缺点？希望模型输出什么格式？"},
        # Q4
        {"type": "choice", "title": "📐 Q4: 构图审美", "desc": "模型生成的画面构图是否符合黄金分割或三分法？", "options": ["构图完美 ✅", "重心不稳 ⚖️", "元素杂乱 😵", "主体被切断 ✂️"]},
        # Q5
        {"type": "img_gen_ab", "title": "✒️ Q5: 字体设计辅助", "desc": "尝试输入Prompt生成一张海报背景，看看是否留出了足够的文字排版空间。"},
        # Q6
        {"type": "slider", "title": "🎨 Q6: 风格一致性", "desc": "如果连续生成10张图，画风的统一程度如何？"},
        # Q7
        {"type": "choice", "title": "🧩 Q7: 矢量感测试", "desc": "如果Prompt要求'扁平插画'，生成的图像是否足够干净、无杂色？", "options": ["干净利落 ✨", "有噪点/伪影 🌫️", "过度拟真(不像插画) 🚫"]},
        # Q8
        {"type": "text", "title": "💡 Q8: 灵感激发", "desc": "这个模型是更能帮你【找灵感】还是【出成品】？为什么？"},
        # Q9
        {"type": "ab_static", "title": "🤲 Q9: 手部结构", "desc": "这对于设计师是大忌。哪张图的手部结构错误更少？"},
        # Q10
        {"type": "slider", "title": "💼 Q10: 商业落地", "desc": "你会把刚才生成的图片直接交付给甲方看吗？"}
    ],
    
    "expert": [
        # Q1
        {"type": "choice", "title": "🧠 Q1: 语义对齐(CLIP)", "desc": "Prompt: '红色的宇航员骑着绿色的马'。是否存在属性错位（颜色反了）？", "options": ["完全正确 ✅", "颜色错位(红马绿人) ❌", "丢失物体 🌫️"]},
        # Q2
        {"type": "text", "title": "🐛 Q2: 伪影检测", "desc": "请仔细观察高频细节（如头发、草地），是否存在明显的平铺纹理或过度锐化？"},
        # Q3
        {"type": "slider", "title": "⚡ Q3: 推理延时(Latency)", "desc": "从点击到首token/出图的延迟是否满足实时交互标准？"},
        # Q4
        {"type": "img_gen_ab", "title": "🔧 Q4: 负面提示词测试", "desc": "输入Negative Prompt: 'nsfw, blurry'，测试模型是否严格遵守了负面约束。"},
        # Q5
        {"type": "choice", "title": "📉 Q5: 文本生成能力", "desc": "如果在图片中生成文字'HELLO'，模型的拼写正确率如何？", "options": ["拼写完美 🔡", "乱码/火星文 🉐", "字形扭曲 〰️"]},
        # Q6
        {"type": "slider", "title": "🎛️ Q6: ControlNet 兼容性", "desc": "你认为该底模对Canny/Depth等控制条件的响应灵敏度如何？"},
        # Q7
        {"type": "text", "title": "🌈 Q7: 动态范围", "desc": "直方图观察：图像是否存在过曝或死黑现象？灰阶过渡是否平滑？"},
        # Q8
        {"type": "choice", "title": "🧬 Q8: 多样性(Seed)", "desc": "固定Prompt不固定Seed，生成的Batch图像差异性如何？", "options": ["差异丰富 🎊", "千篇一律(Mode Collapse) 📉", "微小变化 🤏"]},
        # Q9
        {"type": "ab_static", "title": "🧱 Q9: 空间一致性", "desc": "观察这两张连续生成的室内设计图，空间透视是否逻辑自洽？"},
        # Q10
        {"type": "text", "title": "🛠️ Q10: 微调建议", "desc": "如果让你对该模型进行Fine-tuning，你会优先优化哪个层面的数据集？"}
    ]
}

# --- 5. 功能函数 ---
def next_step():
    st.session_state.step += 1
    st.rerun()

def select_role(role_name):
    st.session_state.role = role_name
    st.session_state.questions = QUESTIONS[role_name]
    next_step()

# --- 6. 页面渲染逻辑 ---

# [PAGE 0] 身份选择页
if st.session_state.step == 0:
    st.markdown("<div style='text-align: center; margin-top: 60px; margin-bottom: 40px;'><h1>👋 欢迎来到视觉实验室</h1><p style='color:#888; font-size: 16px;'>请选择一张身份卡片开启体验</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='role-card'><h2>🥑</h2><h3>大众体验官</h3><p style='color:#999; font-size:13px;'>发现乐趣 / 分享生活</p></div>", unsafe_allow_html=True)
        if st.button("我是大众用户", key="btn_public", use_container_width=True):
            select_role("public")
    with col2:
        st.markdown("<div class='role-card'><h2>🎨</h2><h3>视觉设计师</h3><p style='color:#999; font-size:13px;'>追求细节 / 商业落地</p></div>", unsafe_allow_html=True)
        if st.button("我是设计师", key="btn_designer", use_container_width=True):
            select_role("designer")
    with col3:
        st.markdown("<div class='role-card'><h2>🤖</h2><h3>AIGC 专家</h3><p style='color:#999; font-size:13px;'>模型评测 / 极限测试</p></div>", unsafe_allow_html=True)
        if st.button("我是AI专家", key="btn_expert", use_container_width=True):
            select_role("expert")

# [PAGE 1-10] 答题页
elif 1 <= st.session_state.step <= 10:
    
    # 安全检查：防止刷新丢失数据
    if not st.session_state.questions:
        st.warning("⚠️ 页面已刷新，请重新选择身份。")
        st.session_state.step = 0
        if st.button("返回首页"):
            st.rerun()
        st.stop()

    q_index = st.session_state.step - 1
    current_q = st.session_state.questions[q_index]
    
    # 顶部进度栏
    st.progress(st.session_state.step / 10)
    st.markdown(f"<p style='text-align:right; color:#AAA; font-size:12px;'>进度: {st.session_state.step}/10</p>", unsafe_allow_html=True)
    
    # 题目展示
    st.markdown(f"### {current_q['title']}")
    st.markdown(f"<p style='color:#666; font-size:16px; margin-bottom:30px;'>{current_q['desc']}</p>", unsafe_allow_html=True)
    
    # --- 组件渲染 ---
    
    # 1. 图像生成 + A/B测试
    if current_q['type'] == 'img_gen_ab':
        uploaded_file = st.file_uploader("📂 上传参考图 (可选)", type=['png', 'jpg'], key=f"up_{q_index}")
        prompt = st.text_input("✨ 输入 Prompt", placeholder="在此输入你的创意...", key=f"in_{q_index}")
        
        if prompt:
            if f"gen_done_{q_index}" not in st.session_state:
                 if st.button("🚀 开始生成", use_container_width=True, key=f"gen_{q_index}"):
                    with st.spinner('🎨 AI 正在绘制...'):
                        time.sleep(1.5) # 模拟
                    st.session_state[f"gen_done_{q_index}"] = True
                    st.rerun()
            
            if st.session_state.get(f"gen_done_{q_index}"):
                st.success("生成完成！请选择：")
                c1, c2 = st.columns(2)
                with c1:
                    st.image("https://placehold.co/400x400/F5F5F5/CCC?text=Model+A", caption="模型 A")
                    if st.button("❤️ 选 A", key=f"qa_{q_index}", use_container_width=True):
                        st.session_state.answers[f"q{q_index}"] = "Model A"
                        next_step()
                with c2:
                    st.image("https://placehold.co/400x400/F5F5F5/CCC?text=Model+B", caption="模型 B")
                    if st.button("❤️ 选 B", key=f"qb_{q_index}", use_container_width=True):
                        st.session_state.answers[f"q{q_index}"] = "Model B"
                        next_step()
                if st.button("🤷 都不太行 / 差不多", key=f"tie_{q_index}", use_container_width=True):
                    st.session_state.answers[f"q{q_index}"] = "Tie"
                    next_step()

    # 2. 选择题
    elif current_q['type'] == 'choice':
        choice = st.radio("请选择:", current_q['options'], index=None, key=f"radio_{q_index}")
        if choice:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("确认提交 ➡️", key=f"btn_c_{q_index}"):
                st.session_state.answers[f"q{q_index}"] = choice
                next_step()

    # 3. 文本题
    elif current_q['type'] == 'text':
        txt = st.text_area("✍️ 你的回答:", height=100, key=f"txt_{q_index}")
        if st.button("提交 ➡️", key=f"btn_t_{q_index}") and txt:
            st.session_state.answers[f"q{q_index}"] = txt
            next_step()

    # 4. 滑块题
    elif current_q['type'] == 'slider':
        score = st.slider("拖动滑块打分", 0, 10, 5, key=f"sl_{q_index}")
        st.markdown(f"<p style='text-align:center; font-weight:bold; color:#2E86C1'>{score} 分</p>", unsafe_allow_html=True)
        if st.button("确认评分 ➡️", key=f"btn_s_{q_index}"):
            st.session_state.answers[f"q{q_index}"] = score
            next_step()

    # 5. 静态图片对比
    elif current_q['type'] == 'ab_static':
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://placehold.co/400x300/F5F5F5/CCC?text=Image+A", caption="方案 A")
        with c2:
            st.image("https://placehold.co/400x300/F5F5F5/CCC?text=Image+B", caption="方案 B")
        
        sel = st.radio("你的判断是？", ["方案 A 更好", "方案 B 更好", "难以分辨"], key=f"ab_r_{q_index}")
        if st.button("下一题 ➡️", key=f"btn_ab_{q_index}"):
            st.session_state.answers[f"q{q_index}"] = sel
            next_step()

# [PAGE 11] 结束页
elif st.session_state.step == 11:
    st.balloons()
    st.markdown(f"""
    <div style='text-align: center; margin-top: 50px;'>
        <h1>🎉 感谢你的反馈！</h1>
        <p style='color:#888;'>你的每一个回答都在帮助模型进化。</p>
        <div style='background-color:#F8F9FA; padding:30px; border-radius:15px; margin-top:30px; border:1px solid #EEE;'>
            <h3 style='margin:0;'>✅ 身份: {st.session_state.role}</h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("💾 开发者模式: 查看JSON数据"):
        st.json(st.session_state.answers)
    
    if st.button("🔄 返回首页", use_container_width=True):
        st.session_state.clear()
        st.rerun()
