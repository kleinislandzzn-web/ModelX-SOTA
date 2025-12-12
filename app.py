import streamlit as st
import time
import requests
from PIL import Image
import io
import os

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="Visionary Lab - 模型评测",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. 核心：Google API 接入逻辑 ---
def call_google_gen_ai(uploaded_file, prompt):
    """
    🔴 这里是接入 Google 模型的关键部分
    """
    
    # [场景 A]: 如果你是指 Google Cloud Vertex AI (Imagen 3 / Gemini)
    # 你需要先: pip install google-cloud-aiplatform
    """
    import vertexai
    from vertexai.preview.vision_models import ImageGenerationModel

    # 初始化 (替换你的项目ID)
    vertexai.init(project="your-google-project-id", location="us-central1")
    
    model = ImageGenerationModel.from_pretrained("imagegeneration@006") # 或你的微调模型
    
    # 读取上传的图片作为参考 (如果模型支持 Image-to-Image)
    # 或者是纯文本生成，视你的 API 能力而定
    
    images = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        language="zh",
    )
    # 返回第一张图
    return images[0]._pil_image
    """

    # [场景 B]: 如果你是指调用自己部署在 Google Cloud Run 的自定义模型 API
    # api_url = "https://your-custom-model-url.run.app/predict"
    # headers = {"Content-Type": "application/json"}
    # payload = {"prompt": prompt, "image_data": "base64_string..."}
    # response = requests.post(api_url, json=payload)
    # return Image.open(io.BytesIO(response.content))

    # [当前演示]: 模拟返回，让你先跑通流程
    time.sleep(1.5) 
    st.toast("正在连接 Google API...", icon="☁️")
    # 简单的本地处理模拟生成
    try:
        img = Image.open(uploaded_file).convert("RGB")
        # 模拟：给图片加个滤镜表示“生成了”
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(1.2) # 变亮一点
    except:
        return None

# --- 3. 状态管理 ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'role' not in st.session_state: st.session_state.role = None
if 'generated_image' not in st.session_state: st.session_state.generated_image = None
if 'img_prompt' not in st.session_state: st.session_state.img_prompt = ""

# --- 4. 极简视觉 CSS (核心修改：大卡片按钮) ---
st.markdown("""
<style>
    /* 全局字体 */
    .stApp { background-color: #FAFAFA; font-family: 'Helvetica Neue', sans-serif; }
    header {visibility: hidden;}

    /* === 核心交互：把按钮伪装成大卡片 === */
    /* 针对首页的三个主要按钮进行样式覆盖 */
    div.stButton > button {
        width: 100%;
        border-radius: 20px;
        border: 1px solid #eee;
        background-color: white;
        color: #444;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
        padding: 0; /* 清除内边距，完全由内容控制 */
        
        /* 强制让按钮内的文字换行显示 */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: auto;
        min-height: 280px; /* 卡片高度 */
    }

    /* 悬停效果 */
    div.stButton > button:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(108, 92, 231, 0.15);
        border-color: #a29bfe;
        color: #6c5ce7;
    }
    
    /* 选中后的状态 (可选) */
    div.stButton > button:active {
        background-color: #f8f9fa;
        transform: translateY(-2px);
    }
    
    /* 按钮内部文本大小调整 */
    div.stButton > button p {
        font-size: 16px;
    }

    /* 提示词输入框样式 */
    .stTextArea textarea {
        background-color: #fcfcfc;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
    }
    
    /* 灵感标签 */
    .inspiration-tag {
        cursor: pointer;
        padding: 5px 10px;
        background: #eee;
        border-radius: 15px;
        font-size: 12px;
        margin-right: 5px;
    }

</style>
""", unsafe_allow_html=True)

# --- 5. 逻辑流 ---
def set_role(role):
    st.session_state.role = role
    st.session_state.step = 1
    st.rerun()

# ===========================
# Step 0: 首页 (全卡片点击)
# ===========================
if st.session_state.step == 0:
    st.markdown("<br><br><h1 style='text-align: center; color: #2d3436;'>✨ Visionary Lab 内测</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #999; margin-bottom: 60px;'>请点击下方卡片选择您的身份</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="medium")

    # 注意：Streamlit 按钮不支持复杂的 HTML 嵌套，
    # 我们利用 \n 换行符和 Emoji 来模拟卡片视觉结构
    
    with c1:
        # 大众用户卡片
        if st.button("🌱\n\n大众创作者\n\n(生活记录 / 趣味修图)", key="card_user"):
            set_role("user")

    with c2:
        # 设计师卡片
        if st.button("🎨\n\n视觉设计师\n\n(工作流 / 商业素材)", key="card_designer"):
            set_role("designer")

    with c3:
        # 专家卡片
        if st.button("⚡\n\nAIGC 专家\n\n(模型微调 / 极限测试)", key="card_expert"):
            set_role("expert")

# ===========================
# Step 1: 开放式图生图测试
# ===========================
elif st.session_state.step == 1:
    # 顶部导航条
    st.markdown(f"**当前身份：** {st.session_state.role} | [返回首页](javascript:window.location.reload())", unsafe_allow_html=True)
    st.divider()
    
    col_left, col_right = st.columns([1, 1.2], gap="large")

    # --- 左侧：操作区 ---
    with col_left:
        st.subheader("1. 上传参考图")
        uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            st.image(uploaded_file, caption="原始图片", width=250)
            
            st.markdown("---")
            st.subheader("2. 输入提示词 (Prompt)")
            
            # 灵感按钮区
            tags = {
                "💇‍♀️ 银灰酷短发": "帮我换个银灰色的短发，赛博朋克风格",
                "🧥 90s复古风": "复古90年代胶片质感，颗粒感",
                "🧸 3D卡通化": "皮克斯风格3D卡通形象，可爱"
            }
            
            # 使用小的 col 来排列 Tag 按钮
            tag_cols = st.columns(3)
            for i, (label, prompt_text) in enumerate(tags.items()):
                if tag_cols[i].button(label, key=f"tag_{i}"):
                    st.session_state.img_prompt = prompt_text

            # 文本输入框
            prompt = st.text_area(
                "", 
                value=st.session_state.img_prompt, 
                height=120,
                placeholder="在此输入您的创意指令..."
            )
            st.session_state.img_prompt = prompt

            st.markdown("<br>", unsafe_allow_html=True)
            
            # 生成按钮
            if st.button("✨ 开始生成 (Run Model)", type="primary", use_container_width=True):
                if not prompt:
                    st.warning("请输入提示词")
                else:
                    with st.spinner("正在请求 Google 模型计算..."):
                        res = call_google_gen_ai(uploaded_file, prompt)
                        if res:
                            st.session_state.generated_image = res
                            st.rerun()

    # --- 右侧：结果展示区 ---
    with col_right:
        if st.session_state.generated_image:
            st.subheader("生成结果")
            st.image(st.session_state.generated_image, use_container_width=True)
            
            st.markdown("### 📝 快速反馈")
            with st.container(border=True):
                st.slider("效果满意度", 0, 10, 5)
                st.text_input("如果有瑕疵，主要在哪里？", placeholder="例如：手指变形，光影不自然...")
                
                c_btn1, c_btn2 = st.columns(2)
                with c_btn1:
                    if st.button("🔄 重新生成"):
                        st.session_state.generated_image = None
                        st.rerun()
                with c_btn2:
                    if st.button("提交并下一题 ➡️", type="primary"):
                        st.balloons()
                        st.success("反馈已提交！")
        else:
            # 空状态占位符
            st.markdown("""
            <div style="
                height: 500px; 
                background-color: #f8f9fa; 
                border-radius: 20px; 
                border: 2px dashed #e0e0e0;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #adb5bd;
                flex-direction: column;
            ">
                <div style="font-size: 50px; margin-bottom: 20px;">🖼️</div>
                <div>结果将在此显示</div>
            </div>
            """, unsafe_allow_html=True)
