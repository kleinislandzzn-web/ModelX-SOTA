import streamlit as st
import time
import requests
from PIL import Image, ImageOps, ImageFilter
import io

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="Visionary Lab - 创作者内测",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. 核心：自定义 API 接口 (接入你的 Nano Banana/模型) ---
def call_custom_api(uploaded_file, prompt):
    """
    🔴 重点：在这里接入你的真实 API。
    """
    
    # --- 方式 A: 如果你有真实的 API URL (取消下方注释并修改) ---
    # api_url = "https://api.your-domain.com/v1/img2img"
    # api_key = "sk-xxxxxxxxxxxx"
    # headers = {"Authorization": f"Bearer {api_key}"}
    
    # files = {"file": uploaded_file.getvalue()}
    # data = {"prompt": prompt, "strength": 0.75}
    
    # response = requests.post(api_url, headers=headers, files=files, data=data)
    # if response.status_code == 200:
    #     return Image.open(io.BytesIO(response.content))
    # else:
    #     st.error(f"API Error: {response.text}")
    #     return None

    # --- 方式 B: 本地模拟 (演示用，正式部署请删除) ---
    # 为了让你现在运行代码时不报错，我写了一个假的“滤镜”来模拟生成效果
    time.sleep(2) # 模拟网络延迟
    original_img = Image.open(uploaded_file)
    
    # 模拟：根据 Prompt 做简单的图像处理
    if "黑白" in prompt or "银灰" in prompt:
        return ImageOps.grayscale(original_img)
    elif "模糊" in prompt or "梦幻" in prompt:
        return original_img.filter(ImageFilter.GaussianBlur(5))
    else:
        # 默认把图片色调变暖，模拟“生成”
        return ImageOps.colorize(ImageOps.grayscale(original_img), '#4a4e69', '#f2e9e4')

# --- 3. 状态管理 ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'role' not in st.session_state: st.session_state.role = None
if 'generated_image' not in st.session_state: st.session_state.generated_image = None
if 'img_prompt' not in st.session_state: st.session_state.img_prompt = ""

# --- 4. 极简视觉 CSS ---
st.markdown("""
<style>
    /* 全局 */
    .stApp { background-color: #FAFAFA; font-family: 'Helvetica Neue', sans-serif; }
    
    /* 隐藏 Streamlit 默认头部 */
    header {visibility: hidden;}
    
    /* 首页卡片容器 */
    .role-card {
        background: white;
        border-radius: 24px;
        padding: 40px 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 2px solid transparent;
        transition: all 0.3s ease;
        height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    /* 鼠标悬停特效 - 只有视觉反馈，点击逻辑在下方的透明按钮 */
    .role-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.08);
        border-color: #a29bfe;
    }
    
    .role-icon { font-size: 60px; margin-bottom: 20px; }
    .role-name { font-size: 24px; font-weight: 700; color: #333; }
    .role-desc { color: #888; font-size: 14px; margin-top: 10px; }

    /* 按钮样式重置 */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: 600;
        border: none;
    }
    
    /* 让首页的选择按钮看起来像卡片的一部分 */
    .select-btn > button {
        background-color: transparent;
        color: #6c5ce7;
        border: 1px solid #6c5ce7;
        margin-top: -20px; /* 视觉上向上拉 */
    }
    .select-btn > button:hover {
        background-color: #6c5ce7;
        color: white;
    }

</style>
""", unsafe_allow_html=True)

# --- 5. 逻辑流 ---

def set_role(role):
    st.session_state.role = role
    st.session_state.step = 1
    st.rerun()

# ===========================
# Step 0: 首页 (极简卡片)
# ===========================
if st.session_state.step == 0:
    st.markdown("<br><br><h1 style='text-align: center; color: #2d3436;'>✨ Visionary Lab 内测</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #b2bec3; margin-bottom: 60px;'>选择身份 · 开启图生图体验</p>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1], gap="medium")

    # 卡片渲染函数
    def render_card(col, icon, title, desc, role_id):
        with col:
            # 视觉层：HTML 卡片
            st.markdown(f"""
            <div class="role-card">
                <div class="role-icon">{icon}</div>
                <div class="role-name">{title}</div>
                <div class="role-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            # 交互层：按钮 (紧贴卡片下方)
            st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True) # 间距
            if st.button(f"选择 {title}", key=f"btn_{role_id}", type="secondary"):
                set_role(role_id)

    render_card(c1, "🌱", "大众创作者", "生活记录 · 趣味修图", "user")
    render_card(c2, "🎨", "视觉设计师", "工作流 · 商业素材", "designer")
    render_card(c3, "⚡", "AIGC 专家", "模型微调 · 极限测试", "expert")

# ===========================
# Step 1: 真实 API 图生图测试
# ===========================
elif st.session_state.step == 1:
    st.markdown(f"### 🔮 灵感实验室 ({st.session_state.role}视角)")
    
    # 左右分栏：左边操作，右边结果
    col_input, col_result = st.columns([1, 1.2], gap="large")

    with col_input:
        st.info("💡 第一步：上传一张参考图")
        uploaded_file = st.file_uploader("支持 JPG/PNG", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            st.image(uploaded_file, caption="原始图片", use_container_width=True)
            
            st.markdown("---")
            st.write("💡 第二步：你想怎么改？")
            
            # 灵感 Tag (点击自动填入)
            tags = {
                "💇‍♀️ 银灰酷短发": "帮我换个银灰色的短发，赛博朋克风格",
                "🧥 90s复古风": "复古90年代胶片质感，颗粒感",
                "🧸 3D卡通化": "皮克斯风格3D卡通形象，可爱",
                "🌃 赛博背景": "背景替换为霓虹灯闪烁的未来城市"
            }
            
            # 显示灵感胶囊
            cols = st.columns(2)
            for i, (label, prompt_text) in enumerate(tags.items()):
                if cols[i % 2].button(label, use_container_width=True):
                    st.session_state.img_prompt = prompt_text

            # 输入框
            prompt = st.text_area("Prompt (咒语)", value=st.session_state.img_prompt, height=100)
            st.session_state.img_prompt = prompt

            # 生成按钮
            generate_btn = st.button("✨ 立即生成 (Call API)", type="primary", use_container_width=True)

            if generate_btn and prompt:
                with st.spinner("正在连接模型..."):
                    # === 调用 API 函数 ===
                    result_image = call_custom_api(uploaded_file, prompt)
                    
                    if result_image:
                        st.session_state.generated_image = result_image
                        st.rerun() # 刷新页面显示结果

    with col_result:
        if st.session_state.generated_image:
            st.success("✅ 生成完成！")
            st.image(st.session_state.generated_image, caption="模型生成结果", use_container_width=True)
            
            st.markdown("### 满意度反馈")
            st.slider("这张图符合你的预期吗？", 0, 10, 5, key="satisfaction_score")
            st.text_input("一句话评价（比如：头发纹理很真实，但背景有点乱）", key="comment")
            
            c_next_1, c_next_2 = st.columns(2)
            with c_next_1:
                if st.button("🔄 不满意，重画"):
                    st.session_state.generated_image = None
                    st.rerun()
            with c_next_2:
                if st.button("下一步 (更多测试) ➡️", type="primary"):
                    st.session_state.step = 2
                    st.rerun()
        else:
            # 空状态占位
            st.markdown("""
            <div style="height: 100%; min-height: 400px; background: #f8f9fa; border: 2px dashed #e9ecef; border-radius: 20px; display: flex; align-items: center; justify-content: center; flex-direction: column; color: #adb5bd;">
                <div style="font-size: 40px; margin-bottom: 10px;">🖼️</div>
                <div>AI 绘图结果将在此显示</div>
            </div>
            """, unsafe_allow_html=True)

# ===========================
# Step 2: 后续题目 (简略版)
# ===========================
elif st.session_state.step == 2:
    st.progress(0.6)
    st.subheader(f"针对 {st.session_state.role} 的进阶测试")
    st.info("这里放置你在 V2 版本中设计的那些 A/B 测试或逻辑题...")
    # ... (此处保留之前的题目逻辑) ...
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🚀 提交全部反馈", type="primary"):
        st.balloons()
        st.success("感谢参与！")
