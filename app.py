import streamlit as st
import time

# --- 1. 页面基础配置 ---
st.set_page_config(
    page_title="Visionary Lab - 沉浸式评测",
    page_icon="✨",
    layout="centered", # 改为居中布局，更适合问卷
    initial_sidebar_state="collapsed" # 隐藏侧边栏
)

# --- 2. 状态初始化 (Session State) ---
# 这是实现“记忆”和“翻页”的核心
if 'step' not in st.session_state:
    st.session_state.step = 0  # 0: 首页, 1-3: 题目, 4: 结束
if 'role' not in st.session_state:
    st.session_state.role = None
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# --- 3. 自定义 CSS (灵动极简风 - 升级版) ---
st.markdown("""
<style>
    /* 全局背景 */
    .stApp {
        background-color: #fafafa;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 隐藏默认的主菜单和页脚 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 卡片容器样式 */
    .css-1r6slb0 {
        background-color: white;
        padding: 2rem;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.04);
        border: 1px solid #f0f0f0;
    }
    
    /* 标题样式 */
    h1 { color: #2d3436; font-weight: 700; letter-spacing: -1px; }
    h3 { color: #636e72; font-weight: 500; }
    p { color: #636e72; }

    /* 按钮美化 - 重点优化导航按钮 */
    div.stButton > button {
        width: 100%;
        border-radius: 16px;
        height: 50px;
        font-weight: 600;
        border: none;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    /* 主要按钮 (下一步/提交) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3);
    }
    
    /* 次要按钮 (上一步/选项) */
    div.stButton > button[kind="secondary"] {
        background-color: #f1f2f6;
        color: #2d3436;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
    }

    /* 身份选择卡片特效 */
    .role-card {
        padding: 20px;
        border-radius: 16px;
        background: white;
        text-align: center;
        border: 2px solid transparent;
        cursor: pointer;
        transition: all 0.3s;
    }
    .role-card:hover {
        border-color: #a29bfe;
        background-color: #f8f7ff;
    }
    
    /* 进度条颜色 */
    .stProgress > div > div > div > div {
        background-color: #6c5ce7;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. 辅助函数 ---
def next_step():
    st.session_state.step += 1
    # 强制重跑脚本以更新页面
    # st.rerun() 在旧版本 Streamlit 中可能是 st.experimental_rerun()

def prev_step():
    if st.session_state.step > 0:
        st.session_state.step -= 1

def select_role(role_name):
    st.session_state.role = role_name
    next_step()

def show_placeholder(text, h=250):
    st.markdown(f"""
    <div style="
        background-color: #f1f3f5; 
        height: {h}px; 
        border-radius: 16px; 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        color: #adb5bd; 
        font-weight: 500;
        border: 2px dashed #dee2e6;
        margin-bottom: 20px;">
        🖼️ {text}
    </div>
    """, unsafe_allow_html=True)

# --- 5. 页面逻辑控制 ---

# >>> 步骤 0: 首页身份选择 <<<
if st.session_state.step == 0:
    st.markdown("<div style='text-align: center; padding-top: 20px;'>", unsafe_allow_html=True)
    st.title("✨ Visionary Lab 内测")
    st.markdown("### 请选择你的身份开启体验")
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div style='font-size: 40px;'>🌱</div>", unsafe_allow_html=True)
        st.subheader("探索者")
        st.caption("普通用户 / 爱好者")
        if st.button("我是探索者", key="role_1", type="secondary"):
            select_role("user")
            st.rerun()

    with c2:
        st.markdown("<div style='font-size: 40px;'>🎨</div>", unsafe_allow_html=True)
        st.subheader("设计师")
        st.caption("视觉 / 创意工作者")
        if st.button("我是设计师", key="role_2", type="secondary"):
            select_role("designer")
            st.rerun()

    with c3:
        st.markdown("<div style='font-size: 40px;'>⚡</div>", unsafe_allow_html=True)
        st.subheader("极客专家")
        st.caption("AIGC / 模型训练师")
        if st.button("我是极客", key="role_3", type="secondary"):
            select_role("expert")
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)


# >>> 步骤 1-3: 问卷环节 <<<
elif 1 <= st.session_state.step <= 3:
    
    # 顶部进度条
    progress = st.session_state.step / 3
    st.progress(progress)
    st.caption(f"Step {st.session_state.step} / 3 · 当前身份: {st.session_state.role.upper()}")
    
    # --- 题目内容生成器 ---
    
    # === A. 普通用户题目 ===
    if st.session_state.role == "user":
        if st.session_state.step == 1:
            st.header("1. 第一眼感觉 📸")
            st.write("哪张图让你觉得更开心、更温暖？")
            col_a, col_b = st.columns(2)
            with col_a:
                show_placeholder("模型 V1 (暖色调)")
                st.checkbox("喜欢左边", key="u_q1_left")
            with col_b:
                show_placeholder("模型 V2 (冷色调)")
                st.checkbox("喜欢右边", key="u_q1_right")
                
        elif st.session_state.step == 2:
            st.header("2. 真实度测试 ⭐")
            show_placeholder("生成的人像照片", h=300)
            st.write("如果不告诉你这是AI画的，你会觉得它是真照片吗？")
            st.slider("拖动滑块打分 (0=假, 10=真)", 0, 10, key="u_q2_score")
            
        elif st.session_state.step == 3:
            st.header("3. 许愿池 💭")
            st.write("你希望下一代模型能帮你画什么？")
            st.text_area("比如：画我的宠物、画二次元头像...", height=150, key="u_q3_text")

    # === B. 设计师题目 ===
    elif st.session_state.role == "designer":
        if st.session_state.step == 1:
            st.header("1. 可编辑性评估 📐")
            show_placeholder("带复杂背景的产品图", h=300)
            st.write("作为素材，这张图的**抠图难度**和**构图预留空间**如何？")
            st.select_slider("选择评价", options=["完全无法商用", "需大量修图", "尚可", "构图优秀", "完美分层"], key="d_q1_rating")
            
        elif st.session_state.step == 2:
            st.header("2. 瑕疵多选 🔍")
            st.write("请指出图中所有不符合解剖学或物理规律的地方：")
            c1, c2 = st.columns([1, 1])
            with c1:
                show_placeholder("手部与光影测试图")
            with c2:
                st.multiselect("点击添加瑕疵标签：", 
                               ["🖐️ 手指数目错误", "💡 阴影方向矛盾", "🧊 材质质感塑料", "🌫️ 边缘过度模糊", "🧱 结构透视错误"],
                               key="d_q2_tags")
                               
        elif st.session_state.step == 3:
            st.header("3. 风格迁移需求 🎨")
            st.write("对于您的设计工作流，目前最痛点的风格是什么？")
            st.text_input("例如：3D粘土风、扁平插画、写实摄影...", key="d_q3_text")

    # === C. 极客专家题目 ===
    elif st.session_state.role == "expert":
        if st.session_state.step == 1:
            st.header("1. 语义对齐 (Prompt Adherence) 🧠")
            st.info("Prompt: A red cube ON TOP OF a blue sphere, cinematic lighting.")
            c1, c2 = st.columns(2)
            with c1:
                show_placeholder("Result Image")
            with c2:
                st.radio("空间逻辑判断：", 
                         ["完全错误 (位置颠倒)", "部分正确 (物体对但位置偏)", "完全正确 (Spatial Relations OK)"],
                         key="e_q1_logic")
                         
        elif st.session_state.step == 2:
            st.header("2. 文本渲染能力 (OCR) 🔠")
            show_placeholder("Signboard with text 'FUTURE'")
            st.write("评价文字生成的字形一致性 (Glyph Consistency)：")
            st.number_input("打分 (1-5分)", 1, 5, 3, key="e_q2_score")
            
        elif st.session_state.step == 3:
            st.header("3. 鲁棒性分析 🧪")
            st.write("在高 CFG Scale (15+) 下，你观察到了什么现象？")
            st.text_area("描述过饱和、伪影或构图崩坏的情况...", key="e_q3_text")

    # --- 底部导航栏 ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_prev, col_next = st.columns([1, 3])
    
    with col_prev:
        if st.button("⬅️ 上一步", type="secondary"):
            prev_step()
            st.rerun()
            
    with col_next:
        if st.session_state.step < 3:
            if st.button("下一步 ➡️", type="primary"):
                next_step()
                st.rerun()
        else:
            if st.button("🚀 提交反馈", type="primary"):
                next_step() # 去往 Step 4
                st.rerun()

# >>> 步骤 4: 结束页 <<<
elif st.session_state.step == 4:
    st.balloons()
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    st.title("🎉 感谢参与！")
    st.subheader("您的专业反馈已归档")
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("数据已成功发送至后台")
    
    # 展示一下刚才填的内容（模拟Debug）
    with st.expander("查看您的回答记录"):
        st.json(st.session_state)
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 返回首页", type="secondary"):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
