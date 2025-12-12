import streamlit as st
import time
from PIL import Image

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="Visionary Lab - 创作者内测",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. 核心 CSS (视觉重构) ---
st.markdown("""
<style>
    /* 全局背景与字体 */
    .stApp {
        background-color: #F8FAFC; /* 极淡的灰蓝色底，更有质感 */
        font-family: 'PingFang SC', 'Helvetica Neue', sans-serif;
    }
    
    /* 隐藏默认头部 */
    header {visibility: hidden;}

    /* =============================================
       核心交互：大方块卡片 (Square Cards)
       ============================================= */
    
    /* 1. 基础按钮样式重置 */
    div.stButton > button {
        width: 100%;
        height: 320px; /* 强制高度，形成长方/正方的大卡片感 */
        border-radius: 24px;
        border: 2px solid transparent;
        color: #334155;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* 丝滑动画 */
        padding: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05); /* 柔和阴影 */
    }

    /* 2. 针对不同列的卡片赋予不同的“底色分布” */
    
    /* 第一列：大众创作者 - 清新青色系 */
    div[data-testid="column"]:nth-of-type(1) div.stButton > button {
        background: linear-gradient(145deg, #ffffff 0%, #F0FDF4 100%);
    }
    
    /* 第二列：设计师 - 梦幻紫色系 */
    div[data-testid="column"]:nth-of-type(2) div.stButton > button {
        background: linear-gradient(145deg, #ffffff 0%, #FAF5FF 100%);
    }
    
    /* 第三列：专家 - 极客蓝色系 */
    div[data-testid="column"]:nth-of-type(3) div.stButton > button {
        background: linear-gradient(145deg, #ffffff 0%, #F0F9FF 100%);
    }

    /* 3. 悬停 (Hover) 与 激活 (Active) - 统一变身“浅蓝色系” */
    div.stButton > button:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px -10px rgba(56, 189, 248, 0.2); /* 蓝色投影 */
        border-color: #BAE6FD; /* 浅蓝边框 */
        background: #F0F9FF; /* 整个卡片变浅蓝 */
    }

    div.stButton > button:active {
        background-color: #E0F2FE !important;
        border-color: #38BDF8 !important;
        transform: scale(0.98);
    }

    /* 4. 卡片内部文字样式优化 */
    div.stButton > button p {
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* =============================================
       其他 UI 组件优化
       ============================================= */
    
    /* 输入框与上传区域 */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        transition: border-color 0.2s;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #38BDF8; /* 聚焦时的亮蓝色 */
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
    }

    /* 灵感标签 (Tags) */
    .inspiration-tag {
        background-color: #F1F5F9;
        color: #64748B;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        margin: 4px;
        border: 1px solid transparent;
        display: inline-block;
        cursor: pointer;
    }

</style>
""", unsafe_allow_html=True)

# --- 3. 模拟 API (保留功能) ---
def call_google_gen_ai(uploaded_file, prompt):
    time.sleep(1.5)
    try:
        img = Image.open(uploaded_file).convert("RGB")
        # 简单模拟处理
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(1.2)
    except:
        return None

# --- 4. 状态管理 ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'role' not in st.session_state: st.session_state.role = None
if 'generated_image' not in st.session_state: st.session_state.generated_image = None
if 'img_prompt' not in st.session_state: st.session_state.img_prompt = ""

def set_role(role):
    st.session_state.role = role
    st.session_state.step = 1
    st.rerun()

# ==========================================
# STEP 0: 首页 - 炫彩方块入口
# ==========================================
if st.session_state.step == 0:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #1E293B;'>✨ Visionary Lab 内测</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 60px; font-size: 18px;'>选择创作者身份，开启图生图体验</p>", unsafe_allow_html=True)

    # 布局：三列大卡片
    c1, c2, c3 = st.columns(3, gap="large")

    # 利用 \n 换行符来排版卡片内容
    # 注意：这里的样式完全由上方的 CSS nth-of-type 控制
    
    with c1:
        # 清新青色系卡片
        if st.button("🌱\n\n大众创作者\n\nSocial Media & Life", key="btn_user"):
            set_role("user")

    with c2:
        # 梦幻紫色系卡片
        if st.button("🎨\n\n视觉设计师\n\nProfessional & Creative", key="btn_designer"):
            set_role("designer")

    with c3:
        # 极客蓝色系卡片
        if st.button("⚡\n\nAIGC 专家\n\nFine-tuning & Logic", key="btn_expert"):
            set_role("expert")

# ==========================================
# STEP 1: 沉浸式图生图 (浅蓝色系交互)
# ==========================================
elif st.session_state.step == 1:
    # 顶部导航
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; color: #64748B;">
        <span>当前身份：<b style="color:#38BDF8">{st.session_state.role}</b></span>
        <a href="javascript:window.location.reload()" style="text-decoration: none; color: #94A3B8;">✕ 退出测试</a>
    </div>
    """, unsafe_allow_html=True)
    
    col_main, col_preview = st.columns([1.1, 1], gap="large")

    # --- 左侧：操作面板 ---
    with col_main:
        st.markdown("### 📸 上传原图")
        uploaded_file = st.file_uploader("支持 JPG / PNG / WEBP", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Reference Image", width=200)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 🪄 创意指令")
            
            # 灵感 Tag (用普通按钮模拟 Tag，利用 CSS 变好看)
            st.write("灵感推荐：")
            t1, t2, t3 = st.columns(3)
            if t1.button("💇‍♀️ 银灰酷短发"): st.session_state.img_prompt = "帮我换个银灰色的短发，赛博朋克风格，高对比度"
            if t2.button("🧥 90s 复古风"): st.session_state.img_prompt = "复古90年代胶片质感，重水洗牛仔外套，颗粒感"
            if t3.button("🧸 3D 卡通化"): st.session_state.img_prompt = "皮克斯风格3D卡通形象，柔和光照，可愛风格"

            # 文本框
            prompt = st.text_area(
                "", 
                value=st.session_state.img_prompt, 
                height=140,
                placeholder="在此输入您的提示词 (Prompt)..."
            )
            st.session_state.img_prompt = prompt

            st.markdown("<br>", unsafe_allow_html=True)
            
            # 主要行动按钮
            if st.button("✨ 立即生成 (Generate)", type="primary", use_container_width=True):
                if not prompt:
                    st.toast("⚠️ 请先输入一点想法", icon="💡")
                else:
                    with st.spinner("正在连接 Google 模型进行渲染..."):
                        res = call_google_gen_ai(uploaded_file, prompt)
                        if res:
                            st.session_state.generated_image = res
                            st.rerun()

    # --- 右侧：结果预览 ---
    with col_preview:
        if st.session_state.generated_image:
            st.markdown("### 🎉 生成结果")
            # 给结果图加一个好看的容器
            st.markdown('<div style="padding: 10px; background: white; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
            st.image(st.session_state.generated_image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 您的评价")
            
            # 简单的评价交互
            feedback = st.radio("效果如何？", ["超乎预期 😍", "还不错 🙂", "一般般 😐", "完全崩了 😵"], horizontal=True)
            
            c_retry, c_next = st.columns(2)
            with c_retry:
                if st.button("🔄 重画一张"):
                    st.session_state.generated_image = None
                    st.rerun()
            with c_next:
                if st.button("提交反馈 ➡️", type="primary"):
                    st.balloons()
                    st.success("反馈已记录！")
        else:
            # 极简的空状态
            st.markdown("""
            <div style="
                height: 550px; 
                background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%);
                border-radius: 24px; 
                border: 2px dashed #CBD5E1;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                color: #94A3B8;
            ">
                <div style="font-size: 60px; margin-bottom: 20px; opacity: 0.5;">🎨</div>
                <div style="font-weight: 500;">AI 绘图工作区</div>
                <div style="font-size: 12px; margin-top: 8px;">结果将在此处渲染</div>
            </div>
            """, unsafe_allow_html=True)
