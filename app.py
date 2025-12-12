import streamlit as st
import time

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="Visionary Lab - 模型评测",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 自定义 CSS (灵动极简风) ---
st.markdown("""
<style>
    /* 全局字体与背景 */
    .reportview-container {
        background: #fdfdfd;
    }
    .main {
        background-color: #fdfdfd;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: #333;
        font-weight: 600;
    }
    
    /* 按钮样式：圆角与悬浮效果 */
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #e0e0e0;
        background-color: #ffffff;
        color: #333;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .stButton>button:hover {
        border-color: #83c5be;
        color: #83c5be;
        transform: translateY(-2px);
    }

    /* 输入框样式 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #f8f9fa;
        border-radius: 12px;
        border: none;
    }
    
    /* 侧边栏美化 */
    [data-testid="stSidebar"] {
        background-color: #f4f6f8;
        border-right: 1px solid #efefef;
    }
    
    /* 提示框美化 */
    .stAlert {
        background-color: #eaf4f4;
        border: none;
        border-radius: 15px;
        color: #2c5f5b;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. 辅助函数：模拟图片展示 ---
# 在实际部署时，请将这里替换为你模型生成的真实图片路径或URL
def show_placeholder_img(label, height=300):
    st.markdown(
        f"""
        <div style="background-color:#eee; height:{height}px; border-radius:15px; display:flex; align-items:center; justify-content:center; color:#888; margin-bottom:10px;">
            {label} (Image Placeholder)
        </div>
        """,
        unsafe_allow_html=True
    )

# --- 4. 侧边栏：身份选择 ---
with st.sidebar:
    st.title("✨ Visionary Lab")
    st.write("欢迎参与图像模型内测计划")
    st.markdown("---")
    
    user_role = st.radio(
        "👋 请选择你的身份:",
        ("🌱 探索者 (普通用户)", "🎨 设计师 (专业视角)", "⚡ 极客 (AIGC专家)"),
        index=0
    )
    
    st.markdown("---")
    st.info("💡 你的反馈将直接决定下一代模型的进化方向。")

# --- 5. 主界面逻辑 ---

# 标题区
st.title("🎨 图像生成模型 · 体验反馈")
st.markdown("我们正在构建下一代图像引擎，类似于 **Nano Banana Pro** 或 **GPT-Vision**。")
st.markdown(f"当前模式：**{user_role}**")
st.divider()

# 表单容器
with st.form("feedback_form"):

    # ==========================================
    # 场景 A: 普通用户 (注重直觉、美感、趣味)
    # ==========================================
    if "探索者" in user_role:
        st.subheader("1. 📸 直觉测试：你更喜欢哪一张？")
        st.caption("请忽略技术细节，仅凭第一眼的感觉选择。")
        
        c1, c2 = st.columns(2)
        with c1:
            show_placeholder_img("模型版本 A (V1.0)")
            st.checkbox("我觉得左边这张更有氛围感", key="q1_a")
        with c2:
            show_placeholder_img("模型版本 B (V1.2)")
            st.checkbox("我觉得右边这张更清晰好看", key="q1_b")

        st.markdown("---")
        
        st.subheader("2. 💬 开放脑洞：它听懂你的话了吗？")
        st.markdown("**Prompt:** *一只穿着宇航服的柯基犬在火星上烤棉花糖*")
        show_placeholder_img("Prompt生成结果")
        q2_general = st.text_area("如果让你给这张图挑一个毛病，或者加一个赞美，你会说什么？", placeholder="比如：柯基的腿太长了，或者光影很棒...")

        st.markdown("---")

        st.subheader("3. ⭐ 灵动指数")
        q3_general = st.slider("这张图给你的真实感有多少？(0=一眼假，10=像照片一样)", 0, 10, 5)

    # ==========================================
    # 场景 B: 设计师 (注重构图、可用性、后期空间)
    # ==========================================
    elif "设计师" in user_role:
        st.subheader("1. 📐 构图与审美评估")
        st.caption("我们生成了一组海报背景，请评估其在实际设计中的可用性。")
        show_placeholder_img("设计素材样张", height=400)
        
        q1_designer = st.select_slider(
            "作为一个设计底图，它的留白和构图平衡性如何？",
            options=["完全不可用", "需大量修图", "尚可", "结构优秀", "直接商用"]
        )

        st.markdown("---")

        st.subheader("2. 🔍 细节瑕疵捕捉 (多选)")
        c1, c2 = st.columns([1, 1])
        with c1:
            show_placeholder_img("人像细节生成")
        with c2:
            st.write("请观察左图，勾选你认为明显的崩坏点：")
            q2_designer = st.multiselect(
                "请选择所有存在的问题：",
                ["🖐️ 手部/肢体结构错误", "👁️ 眼神/面部扭曲", "🧱 纹理过度锐化/涂抹感", "💡 光源方向不统一", "🌌 伪影/噪点过多", "✅ 完美，无明显瑕疵"]
            )

        st.markdown("---")

        st.subheader("3. 🎨 风格化迁移建议")
        st.write("如果你希望这个模型能更好地辅助你的工作流，你最希望它加强哪个能力？")
        q3_designer = st.text_input("例如：更好的矢量图生成、分层输出能力、或是特定的艺术风格...", placeholder="输入你的需求...")

    # ==========================================
    # 场景 C: AIGC专家 (注重语义对齐、逻辑、鲁棒性)
    # ==========================================
    elif "极客" in user_role:
        st.subheader("1. 🧠 复杂语义理解 (Spatial & Logic)")
        st.markdown("To test: **Obj A is strictly behind Obj B, and lighting is volumetric.**")
        
        c1, c2 = st.columns(2)
        with c1:
            show_placeholder_img("Expert Model Output")
        with c2:
            st.radio(
                "模型是否严格遵循了空间逻辑指令？",
                ("❌ 严重失败 (物体融合/位置颠倒)", "⚠️ 部分遵循 (位置对但透视错)", "✅ 完美遵循 (空间关系准确)")
            )

        st.markdown("---")

        st.subheader("2. 🧪 压力测试 (Edge Cases)")
        st.caption("我们尝试生成了密集文字排版图。")
        show_placeholder_img("Text Rendering Test")
        q2_expert = st.text_area("请从技术角度评价模型的文本渲染能力 (OCR-free generation) 及伪影控制：", placeholder="Char consistency, glpyh correctness...")

        st.markdown("---")

        st.subheader("3. 🔧 参数敏感度猜想")
        st.write("观察以下两张图，它们使用了相同的 Seed 但不同的 CFG Scale。")
        c1, c2 = st.columns(2)
        with c1:
            show_placeholder_img("Image CFG 7.0")
            st.caption("Image A")
        with c2:
            show_placeholder_img("Image CFG 15.0")
            st.caption("Image B")
        
        q3_expert = st.selectbox(
            "你认为该模型在高 CFG 下表现出了什么特征？",
            ["色彩过饱和/炸裂", "构图更紧凑但细节丢失", "语义对齐增强但自然度下降", "无明显变化"]
        )

    # ==========================================
    # 提交区域
    # ==========================================
    st.markdown("<br><br>", unsafe_allow_html=True)
    submit_btn = st.form_submit_button("🚀 发送评测报告", type="primary")

# --- 6. 提交后的反馈逻辑 ---
if submit_btn:
    # 这里可以添加将数据保存到数据库或CSV的代码
    st.balloons() # 撒花特效
    st.success(f"🎉 感谢你的反馈！作为 {user_role.split(' ')[1]}，你的意见对我们至关重要。")
    
    with st.expander("查看数据预览 (Debug Mode)"):
        st.json({
            "role": user_role,
            "timestamp": time.time(),
            "status": "submitted"
        })
    
    st.markdown("### 下一步")
    st.write("我们会根据你的反馈优化 V2.0 版本，敬请期待！")
