import streamlit as st
import time

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="Visionary Lab - 创作者内测",
    page_icon="✨",
    layout="wide", # 改为宽屏以容纳左右分栏的图生图界面
    initial_sidebar_state="collapsed"
)

# --- 2. 状态管理 (Session State) ---
if 'step' not in st.session_state:
    st.session_state.step = 0 
if 'role' not in st.session_state:
    st.session_state.role = None
if 'user_img' not in st.session_state:
    st.session_state.user_img = None
if 'img_prompt' not in st.session_state:
    st.session_state.img_prompt = ""

# --- 3. 高级 CSS (视觉设计核心) ---
st.markdown("""
<style>
    /* 全局字体与背景 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
    
    .stApp {
        background-color: #FAFAFA; /* 极简灰白底 */
        font-family: 'Noto Sans SC', sans-serif;
    }

    /* 隐藏顶部红线和菜单 */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* 首页身份卡片样式 */
    .role-card-container {
        background-color: white;
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        border: 1px solid #f0f0f0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s;
        height: 100%;
    }
    .role-card-container:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 30px rgba(108, 92, 231, 0.15);
        border-color: #a29bfe;
    }
    
    /* 身份图标 */
    .role-icon { font-size: 48px; margin-bottom: 15px; }
    
    /* 身份标题 */
    .role-title { 
        font-size: 22px; 
        font-weight: 700; 
        color: #2d3436; 
        margin-bottom: 10px; 
    }
    
    /* 标签 (Tags) 样式 */
    .role-badge {
        display: inline-block;
        background-color: #f1f2f6;
        color: #636e72;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 500;
        margin: 2px;
    }
    
    /* 按钮美化 */
    .stButton>button {
        border-radius: 12px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #6c5ce7 0%, #8e44ad 100%);
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3);
    }

    /* 灵感胶囊样式 */
    div[data-testid="stMarkdownContainer"] p {
        font-size: 16px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. 辅助逻辑函数 ---
def next_step():
    st.session_state.step += 1
    st.rerun()

def prev_step():
    if st.session_state.step > 0:
        st.session_state.step -= 1
        st.rerun()

def set_role(role):
    st.session_state.role = role
    next_step()

def use_inspiration(text):
    st.session_state.img_prompt = text

# --- 5. 页面流 ---

# =================================================
# STEP 0: 首页 - 身份选择 (卡片化设计)
# =================================================
if st.session_state.step == 0:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #2d3436;'>✨ Visionary Lab 模型公测</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #b2bec3; margin-bottom: 50px;'>请选择最符合您的创作者画像，开启定制化评测之旅</p>", unsafe_allow_html=True)
    
    # 使用列布局来模拟卡片网格
    c1, c2, c3 = st.columns([1, 1, 1])
    
    # 卡片 1: 大众/创作者
    with c1:
        st.markdown("""
        <div class="role-card-container">
            <div class="role-icon">🌱</div>
            <div class="role-title">大众创作者</div>
            <div>
                <span class="role-badge">社交媒体</span>
                <span class="role-badge">生活记录</span>
                <span class="role-badge">趣味/修图</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("进入通道 →", key="btn_user", use_container_width=True):
            set_role("user")

    # 卡片 2: 设计师
    with c2:
        st.markdown("""
        <div class="role-card-container">
            <div class="role-icon">🎨</div>
            <div class="role-title">专业设计师</div>
            <div>
                <span class="role-badge">视觉传达</span>
                <span class="role-badge">商业修图</span>
                <span class="role-badge">AI辅助工作流</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("进入通道 →", key="btn_designer", use_container_width=True):
            set_role("designer")

    # 卡片 3: 专家
    with c3:
        st.markdown("""
        <div class="role-card-container">
            <div class="role-icon">⚡</div>
            <div class="role-title">AIGC 专家</div>
            <div>
                <span class="role-badge">模型微调</span>
                <span class="role-badge">Prompt Engineering</span>
                <span class="role-badge">技术评测</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("进入通道 →", key="btn_expert", use_container_width=True):
            set_role("expert")

# =================================================
# STEP 1: 全员通用题 - 开放式图生图 (Img2Img)
# =================================================
elif st.session_state.step == 1:
    st.markdown(f"### Step 1: 🔮 风格重塑实验室")
    st.caption("上传一张照片，告诉我们你想把它变成什么样。请测试模型的语义理解与风格化能力。")
    st.divider()

    col_upload, col_control = st.columns([1, 1.2], gap="large")
    
    with col_upload:
        st.markdown("**1. 上传原图**")
        uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            st.session_state.user_img = uploaded_file
            st.image(uploaded_file, caption="原图预览", use_container_width=True)
        else:
            # 默认占位符，保持排版美观
            st.info("👋 请先上传一张图片开启测试")
            st.markdown("""
            <div style="height: 300px; background: #f0f2f6; border-radius: 15px; display: flex; align-items: center; justify-content: center; color: #ccc;">
                等待上传...
            </div>
            """, unsafe_allow_html=True)

    with col_control:
        st.markdown("**2. 输入咒语 (Prompt)**")
        
        # 灵感胶囊 (点击即用)
        st.write("✨ 灵感快捷键：")
        
        inspiration_map = {
            "💇‍♀️ 银灰酷短发": "帮我换个银灰色的短发，要赛博朋克风格，很酷的那种",
            "🧥 90s 复古牛仔": "把衣服换成复古的 90 年代重水洗牛仔外套，胶片质感",
            "🧸 3D 皮克斯风": "把我变成皮克斯风格的 3D 卡通形象，柔和光照，可愛风格",
            "🏘️ 怪奇物语小镇": "保持人物不变，把背景换成《怪奇物语》里的霍金斯小镇，霓虹灯光氛围"
        }
        
        # 使用列布局放置灵感按钮
        ic1, ic2 = st.columns(2)
        with ic1:
            if st.button("💇‍♀️ 银灰酷短发", use_container_width=True):
                use_inspiration(inspiration_map["💇‍♀️ 银灰酷短发"])
            if st.button("🧸 3D 皮克斯风", use_container_width=True):
                use_inspiration(inspiration_map["🧸 3D 皮克斯风"])
        with ic2:
            if st.button("🧥 90s 复古牛仔", use_container_width=True):
                use_inspiration(inspiration_map["🧥 90s 复古牛仔"])
            if st.button("🏘️ 怪奇物语小镇", use_container_width=True):
                use_inspiration(inspiration_map["🏘️ 怪奇物语小镇"])

        # 输入框 (绑定 session_state 以支持按钮填入)
        prompt_input = st.text_area(
            "或者输入你自己的想法...", 
            value=st.session_state.img_prompt,
            height=150,
            placeholder="例如：把背景换成星空，让画面更有电影感..."
        )
        # 更新状态
        st.session_state.img_prompt = prompt_input
        
        if st.session_state.user_img and st.session_state.img_prompt:
             st.success("✅ 任务已就绪 (后台模拟生成中...)")
        
# =================================================
# STEP 2 & 3: 分人群的差异化题目
# =================================================
elif st.session_state.step >= 2 and st.session_state.step < 4:
    
    # 顶部进度提示
    st.progress(st.session_state.step / 4)
    
    # --- A. 普通用户 (Step 2 & 3) ---
    if st.session_state.role == "user":
        if st.session_state.step == 2:
            st.subheader("Step 2: ⚖️ A/B 盲测")
            st.write("基于您刚才的描述，我们生成了两个版本，您更喜欢哪个？")
            c1, c2 = st.columns(2)
            with c1:
                st.image("https://placehold.co/400x400/EEE/31343C?text=Version+A", caption="版本 A")
                st.button("❤️ 投给 A", key="vote_a", use_container_width=True)
            with c2:
                st.image("https://placehold.co/400x400/EEE/31343C?text=Version+B", caption="版本 B")
                st.button("❤️ 投给 B", key="vote_b", use_container_width=True)
                
        elif st.session_state.step == 3:
            st.subheader("Step 3: 💬 体验官吐槽")
            st.write("在使用刚才的图生图功能时，你觉得哪里最不方便？")
            st.radio("单选：", ["生成速度太慢", "不像我本人了", "背景融合生硬", "没有理解我的指令"], key="u_q3")

    # --- B. 设计师 (Step 2 & 3) ---
    elif st.session_state.role == "designer":
        if st.session_state.step == 2:
            st.subheader("Step 2: 📐 可用性分析")
            st.info(f"Prompt: {st.session_state.img_prompt}")
            st.image("https://placehold.co/800x400/EEE/31343C?text=Generated+Result", caption="模拟生成结果")
            st.write("如果不修图直接交付，这张图能打几分？")
            st.slider("商用可用度打分", 0, 10, 5)
            
        elif st.session_state.step == 3:
            st.subheader("Step 3: 🔧 生产力工具链")
            st.write("您希望这个模型支持导出什么格式以配合 Photoshop/Figma？")
            st.multiselect("多选：", ["带透明通道的 PNG", "分层 PSD", "SVG 矢量图", "Depth Map 深度图"], key="d_q3")

    # --- C. 专家 (Step 2 & 3) ---
    elif st.session_state.role == "expert":
        if st.session_state.step == 2:
            st.subheader("Step 2: 🧠 语义一致性 (Semantic Alignment)")
            st.write(f"针对指令：**{st.session_state.img_prompt}**")
            st.image("https://placehold.co/800x400/EEE/31343C?text=Edge+Case+Test", caption="生成结果")
            st.markdown("##### 细粒度评估：")
            c1, c2 = st.columns(2)
            with c1:
                st.checkbox("❌ 存在概念融合 (Concept Bleeding)")
                st.checkbox("❌ 属性泄露 (Attribute Leakage)")
            with c2:
                st.checkbox("✅ 风格对齐 (Style Match)")
                st.checkbox("✅ 主体ID保持 (Identity Preservation)")

        elif st.session_state.step == 3:
            st.subheader("Step 3: 🔬 极限与幻觉")
            st.text_input("如果我们要针对该模型进行红队测试 (Red Teaming)，你会输入什么 Prompt 来攻击它？")

# =================================================
# 底部导航栏 (保持常驻)
# =================================================
if st.session_state.step > 0 and st.session_state.step < 4:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c_prev, c_next = st.columns([1, 5])
    
    with c_prev:
        if st.button("⬅️ 上一步", type="secondary", use_container_width=True):
            prev_step()
            
    with c_next:
        # 只有在第一步且未上传图片时，禁用下一步（这里做个软提示，不强制禁用以免卡住）
        if st.session_state.step == 1 and not st.session_state.user_img:
            if st.button("跳过上传 (仅预览)", type="secondary"):
                next_step()
        elif st.session_state.step == 3:
            if st.button("🚀 提交报告", type="primary", use_container_width=True):
                next_step()
        else:
            if st.button("下一步 ➡️", type="primary", use_container_width=True):
                next_step()

# =================================================
# STEP 4: 结束页
# =================================================
elif st.session_state.step == 4:
    st.balloons()
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1 style="color: #6c5ce7;">🎉 评测完成</h1>
        <p style="font-size: 18px; color: #666;">感谢您从 <b>{}</b> 视角提供的宝贵数据。</p>
    </div>
    """.format("设计专家" if st.session_state.role == 'designer' else "AIGC极客" if st.session_state.role == 'expert' else "生活记录者"), unsafe_allow_html=True)
    
    with st.expander("💾 查看本次评测数据 (JSON)"):
        st.json({
            "role": st.session_state.role,
            "img_prompt": st.session_state.img_prompt,
            "status": "success"
        })
        
    if st.button("🔄 返回首页", use_container_width=True):
        st.session_state.step = 0
        st.session_state.img_prompt = ""
        st.rerun()
