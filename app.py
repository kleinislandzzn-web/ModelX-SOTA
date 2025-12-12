import streamlit as st
import time
from PIL import Image

# --- 1. 页面配置 ---
st.set_page_config(
    page_title="Visionary Lab",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. 状态管理 ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'role' not in st.session_state: st.session_state.role = None
if 'generated_image' not in st.session_state: st.session_state.generated_image = None
if 'img_prompt' not in st.session_state: st.session_state.img_prompt = ""

def set_role(role):
    st.session_state.role = role
    st.session_state.step = 1
    st.rerun()

# --- 3. 模拟 Google Nano API ---
def call_google_gen_ai(uploaded_file, prompt):
    time.sleep(1.5)
    try:
        return Image.open(uploaded_file).convert("RGB")
    except:
        return None

# =========================================================
# 场景 A: 首页 (STEP 0) - 5:4 巨型卡片 CSS
# =========================================================
if st.session_state.step == 0:
    st.markdown("""
    <style>
        .stApp { background-color: #F8FAFC; font-family: 'Helvetica Neue', sans-serif; }
        header {visibility: hidden;}
        
        /* 首页专用：大卡片样式 */
        div.stButton > button {
            width: 100%;
            aspect-ratio: 5 / 4; /* 保持宽高比 */
            min-height: 300px;
            border-radius: 32px;
            border: 0px solid transparent;
            color: #334155;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        /* 悬停特效：整体上浮 + 蓝光 */
        div.stButton > button:hover {
            transform: translateY(-12px);
            box-shadow: 0 25px 60px -12px rgba(56, 189, 248, 0.4);
        }
        
        /* 颜色分布 */
        div[data-testid="column"]:nth-of-type(1) div.stButton > button { background: linear-gradient(135deg, #fff 0%, #ECFDF5 100%); }
        div[data-testid="column"]:nth-of-type(2) div.stButton > button { background: linear-gradient(135deg, #fff 0%, #F5F3FF 100%); }
        div[data-testid="column"]:nth-of-type(3) div.stButton > button { background: linear-gradient(135deg, #fff 0%, #F0F9FF 100%); }

        /* 字体修正 */
        div.stButton > button p { font-size: 16px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #0F172A; font-size: 40px;'>Visionary Lab</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; margin-bottom: 50px;'>Choose your identity to start</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3, gap="large")
    with c1:
        if st.button("🌱\n\n大 众 创 作 者\n\nSocial & Life", key="btn_user"): set_role("user")
    with c2:
        if st.button("🎨\n\n视 觉 设 计 师\n\nPro Creative", key="btn_designer"): set_role("designer")
    with c3:
        if st.button("⚡\n\nA I G C 专 家\n\nFine-tuning", key="btn_expert"): set_role("expert")


# =========================================================
# 场景 B: 工作台 (STEP 1) - 精致 Tags & 白玉按钮 CSS
# =========================================================
elif st.session_state.step == 1:
    st.markdown("""
    <style>
        .stApp { background-color: #FAFAFA; }
        header {visibility: hidden;}

        /* --- 1. 灵感 Tag 样式 (重写 Secondary Button) --- */
        /* 定位：把所有次级按钮(secondary)变成小标签 */
        button[kind="secondary"] {
            background-color: #F1F5F9; /* 浅灰底 */
            color: #64748B;            /* 灰字 */
            border-radius: 20px;       /* 药丸形状 */
            border: 1px solid transparent;
            height: 32px;
            font-size: 13px !important;
            padding: 0px 15px;
            margin-right: 5px;
            transition: all 0.2s;
            width: auto !important;    /* 只有文字那么宽 */
        }
        
        /* Tag 悬停 */
        button[kind="secondary"]:hover {
            background-color: #E2E8F0;
            color: #334155;
            border-color: #CBD5E1;
            transform: scale(1.02);
        }

        /* --- 2. 生成按钮样式 (重写 Primary Button) --- */
        /* 要求：圆角小矩形，浅白色，无红色 */
        button[kind="primary"] {
            background-color: #FFFFFF; /* 浅白色 */
            color: #475569;            /* 深灰字 */
            border: 1px solid #E2E8F0; /* 极淡的边框 */
            border-radius: 12px;       /* 圆角小矩形 */
            height: 48px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        }

        /* 生成按钮 - 悬停 (变成浅蓝色系) */
        button[kind="primary"]:hover {
            background-color: #F0F9FF; /* 极淡蓝底 */
            border-color: #7DD3FC;     /* 亮蓝边框 */
            color: #0284C7;            /* 亮蓝文字 */
            box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2); /* 蓝色柔光 */
        }
        
        /* 去除 Streamlit 默认的红色 Focus 边框 */
        button[kind="primary"]:focus:not(:active) {
            border-color: #7DD3FC;
            color: #0284C7;
        }

        /* 输入框美化 */
        .stTextArea textarea {
            background-color: white;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
        }
        .stTextArea textarea:focus {
            border-color: #38BDF8;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.1);
        }

    </style>
    """, unsafe_allow_html=True)

    # 顶部导航
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; border-bottom:1px solid #eee; padding-bottom:15px;">
        <div style="font-weight:bold; color:#333;">{st.session_state.role} <span style="font-weight:normal; color:#aaa;">/ Workspace</span></div>
        <a href="javascript:window.location.reload()" style="font-size:13px; color:#999; text-decoration:none;">✕ Close</a>
    </div>
    """, unsafe_allow_html=True)

    col_main, col_preview = st.columns([1, 1], gap="large")

    # --- 左侧：编辑器 ---
    with col_main:
        st.markdown("##### 1. 上传图片")
        uploaded_file = st.file_uploader("", type=['png', 'jpg'])
        
        if uploaded_file:
            st.image(uploaded_file, width=150) # 预览小一点
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("##### 2. 灵感 Tag")
            
            # 使用 columns 布局让 tag 紧凑排列
            # 注意：这里 type="secondary" 会触发上面的 Tag CSS
            t1, t2, t3, t4 = st.columns([1, 1, 1, 2]) 
            
            with t1:
                if st.button("💇‍♀️ 银灰短发", type="secondary"): 
                    st.session_state.img_prompt = "赛博朋克风格，银灰色短发，高冷酷炫"
            with t2:
                if st.button("🧥 90s 复古", type="secondary"): 
                    st.session_state.img_prompt = "90年代复古胶片感，重水洗牛仔外套，怀旧颗粒"
            with t3:
                if st.button("🧸 3D 卡通", type="secondary"): 
                    st.session_state.img_prompt = "皮克斯3D动画风格，柔和光照，Q版可爱"
            
            # 输入框
            prompt = st.text_area("", value=st.session_state.img_prompt, height=100, placeholder="点击上方Tag或输入提示词...")
            st.session_state.img_prompt = prompt

            st.markdown("<br>", unsafe_allow_html=True)
            
            # 生成按钮 (type="primary" 会触发上面的白玉按钮 CSS)
            if st.button("✨ 立即生成 (Generate)", type="primary", use_container_width=True):
                if prompt:
                    with st.spinner("Connecting to Nano Model..."):
                        res = call_google_gen_ai(uploaded_file, prompt)
                        st.session_state.generated_image = res
                        st.rerun()

    # --- 右侧：预览区 ---
    with col_preview:
        if st.session_state.generated_image:
            st.markdown("##### 3. 结果预览")
            # 结果图容器
            st.markdown('<div style="padding:10px; background:white; border-radius:16px; border:1px solid #eee; box-shadow:0 5px 15px rgba(0,0,0,0.03);">', unsafe_allow_html=True)
            st.image(st.session_state.generated_image, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            c_fb, c_sub = st.columns([1, 1])
            with c_sub:
                # 提交也用白玉按钮风格，保持统一
                if st.button("提交反馈 ➡️", type="primary"):
                    st.balloons()
                    st.success("Feedback Sent!")
        else:
            # 空状态
            st.markdown("""
            <div style="height: 450px; background: #F8FAFC; border-radius: 20px; border: 2px dashed #E2E8F0; display: flex; align-items: center; justify-content: center; color: #CBD5E1; flex-direction: column;">
               <div style="font-size:40px; margin-bottom:10px;">🎨</div>
               <div>等待生成指令</div>
            </div>
            """, unsafe_allow_html=True)
