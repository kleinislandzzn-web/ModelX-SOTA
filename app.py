import streamlit as st
import streamlit.components.v1 as components

# 设置页面配置，使其在浏览器中看起来更像一个原生 App
st.set_page_config(layout="wide", page_title="Model X Evaluation", page_icon="🎨")

# 隐藏 Streamlit 默认的汉堡菜单和页脚，以获得更沉浸的体验
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
body {margin: 0; padding: 0;}
/* 移除 Streamlit 默认的内边距 */
.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}
iframe {
    width: 100vw;
    height: 100vh;
    border: none;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- 核心 React 代码 ---
# 注意：为了在 Streamlit 中直接运行 React，我们使用 CDN 引入 React 和 Babel。
# 所有的 Lucide 图标引用已被替换为全局对象访问 (lucide.IconName)。

react_app_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Model X Test</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- React & ReactDOM -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <!-- Babel for JSX -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Lucide Icons (Global build) -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        /* 隐藏滚动条但保留功能 */
        .scrollbar-hide::-webkit-scrollbar {
            display: none;
        }
        .scrollbar-hide {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        /* 确保输入框在移动端不放大 */
        input, textarea {
            font-size: 16px;
        }
    </style>
</head>
<body class="bg-gray-50">
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect } = React;
        
        // Lucide Icons Wrapper for CDN
        // 在 CDN 模式下，图标需要通过 lucide.icons 访问并创建组件
        const Icon = ({ name, size = 24, className = "" }) => {
            const iconName = name.charAt(0).toUpperCase() + name.slice(1);
            // 简单的 SVG 渲染逻辑，因为直接使用 lucide-react 库在单文件中比较复杂
            // 这里我们使用 Lucide 的 createIcons 或者是简单的占位符逻辑
            // 为了简化，我们使用一个简单的 SVG 映射或直接用 lucide 全局对象
            
            // 实际上，为了最好的效果，我们定义几个核心图标的 SVG
            // 或者更简单：我们不依赖复杂的 lucide-react 组件，而是直接使用类名
            
            useEffect(() => {
                lucide.createIcons();
            });

            return <i data-lucide={name} className={className} style={{width: size, height: size, display: 'inline-block'}}></i>;
        };

        // 为了 React 组件化，我们重新封装几个常用图标
        const ChevronRight = (props) => <Icon name="chevron-right" {...props} />;
        const ChevronLeft = (props) => <Icon name="chevron-left" {...props} />;
        const CheckCircle2 = (props) => <Icon name="check-circle-2" {...props} />;
        const User = (props) => <Icon name="user" {...props} />;
        const Palette = (props) => <Icon name="palette" {...props} />;
        const Zap = (props) => <Icon name="zap" {...props} />;
        const Send = (props) => <Icon name="send" {...props} />;
        const ImageIcon = (props) => <Icon name="image" {...props} />;
        const AlertTriangle = (props) => <Icon name="alert-triangle" {...props} />;
        const Wand2 = (props) => <Icon name="wand-2" {...props} />;
        const Shirt = (props) => <Icon name="shirt" {...props} />;
        const Eraser = (props) => <Icon name="eraser" {...props} />;
        const History = (props) => <Icon name="history" {...props} />;
        const Camera = (props) => <Icon name="camera" {...props} />;
        const Sparkles = (props) => <Icon name="sparkles" {...props} />;
        const MoreHorizontal = (props) => <Icon name="more-horizontal" {...props} />;

        // --- Mock Image Component ---
        const MockImage = ({ label, color, type, onClick }) => (
            <div onClick={onClick} className={`w-full aspect-square rounded-2xl overflow-hidden relative group cursor-pointer transition-all duration-300 ${type === 'selected' ? 'ring-4 ring-blue-500 shadow-xl shadow-blue-500/20' : 'ring-1 ring-gray-200 hover:ring-blue-300'}`}>
                <div className={`w-full h-full ${color} flex flex-col items-center justify-center p-6 text-center`}>
                <ImageIcon className="text-white/80 mb-4" size={48} />
                <span className="text-white font-mono text-sm tracking-widest uppercase mb-2">Image {label}</span>
                <p className="text-white/80 text-xs">此处将显示模型生成的真实图片</p>
                </div>
                {type === 'selected' && (
                <div className="absolute top-4 right-4 bg-blue-500 text-white p-1.5 rounded-full shadow-sm animate-in zoom-in">
                    <CheckCircle2 size={20} />
                </div>
                )}
            </div>
        );

        const INITIAL_STEPS = [
            { id: 'welcome', title: '欢迎 👋' },
            { id: 'role', title: '身份确认 🆔' }
        ];

        function App() {
            const [activeSteps, setActiveSteps] = useState(INITIAL_STEPS);
            const [currentStepIndex, setCurrentStepIndex] = useState(0);
            const [userRole, setUserRole] = useState(null);
            const [answers, setAnswers] = useState({});
            const [isSubmitting, setIsSubmitting] = useState(false);

            const currentStep = activeSteps[currentStepIndex];
            const progress = ((currentStepIndex + 1) / activeSteps.length) * 100;

            const generateStepsForRole = (role) => {
                let specificSteps = [];
                if (role === 'newbie') {
                specificSteps = [
                    { id: 'img2img_scenario', title: '脑洞时刻 🧠' },
                    { id: 'ab_test_aesthetic', title: '审美测试 🌸' },
                ];
                } else if (role === 'designer') {
                specificSteps = [
                    { id: 'ab_test_anatomy', title: '结构测试 🦴' },
                    { id: 'ab_test_style', title: '风格一致性 🎭' },
                ];
                } else if (role === 'expert') {
                specificSteps = [
                    { id: 'ab_test_semantic', title: '语义理解 🤯' },
                    { id: 'ab_test_text', title: '文字渲染 🔤' },
                    { id: 'expert_input', title: '压力测试 🤔' },
                ];
                }
                return [...INITIAL_STEPS, ...specificSteps, { id: 'feedback', title: '体验反馈 📝' }, { id: 'finish', title: '完成 🎉' }];
            };

            const handleNext = () => {
                if (currentStepIndex < activeSteps.length - 1) {
                setCurrentStepIndex(currentStepIndex + 1);
                window.scrollTo({ top: 0, behavior: 'smooth' });
                }
            };

            const handlePrev = () => {
                if (currentStepIndex > 0) {
                setCurrentStepIndex(currentStepIndex - 1);
                }
            };

            const recordAnswer = (key, value) => {
                setAnswers(prev => ({ ...prev, [key]: value }));
            };

            // --- Render Functions ---

            const renderWelcome = () => (
                <div className="flex flex-col items-center justify-center min-h-[60vh] text-center space-y-8 animate-in fade-in zoom-in duration-500 py-10">
                <div className="w-24 h-24 bg-gradient-to-tr from-blue-500 to-purple-600 rounded-3xl flex items-center justify-center shadow-xl shadow-blue-500/20">
                    <Zap className="text-white" size={48} />
                </div>
                <div className="space-y-4 px-4">
                    <h1 className="text-4xl md:text-5xl font-bold text-gray-900 tracking-tight">Model X 体验测试 👋</h1>
                    <p className="text-gray-600 max-w-lg mx-auto text-lg leading-relaxed">
                    我们将根据您的身份（用户/设计师/专家）定制专属测试题。<br className="hidden md:block"/>测试约需 2-3 分钟。
                    </p>
                </div>
                <button 
                    onClick={handleNext}
                    className="w-full md:w-auto px-10 py-4 bg-gray-900 text-white font-bold text-lg rounded-full hover:bg-gray-800 transition-all flex items-center justify-center gap-2 shadow-lg hover:shadow-xl hover:-translate-y-1 active:scale-95"
                >
                    开始定制评测 <ChevronRight size={20} />
                </button>
                </div>
            );

            const renderRoleSelection = () => {
                const roles = [
                { id: 'newbie', label: 'AI 尝鲜者 🍉', desc: '偶尔玩玩，主要是修图或娱乐', icon: <User /> },
                { id: 'designer', label: '设计师/创作者 🎨', desc: '关注审美、构图与工作流落地', icon: <Palette /> },
                { id: 'expert', label: 'AIGC 极客 🧑‍💻', desc: '关注 Prompt 响应、LoRA 及底层逻辑', icon: <Zap /> },
                ];

                return (
                <div className="space-y-8 animate-in slide-in-from-right duration-500 max-w-xl mx-auto">
                    <div className="text-center pb-4">
                    <h2 className="text-3xl font-bold text-gray-900">您更符合哪种身份？🤔</h2>
                    <p className="text-gray-600 mt-3 text-lg">系统将为您生成不同的测试题目</p>
                    </div>
                    <div className="grid gap-4">
                    {roles.map((role) => (
                        <button
                        key={role.id}
                        onClick={() => {
                            setUserRole(role.id);
                            recordAnswer('user_role', role.id);
                            const newSteps = generateStepsForRole(role.id);
                            setActiveSteps(newSteps);
                            setTimeout(() => { setCurrentStepIndex(2); window.scrollTo(0,0); }, 150);
                        }}
                        className="group relative flex items-center p-6 bg-white border border-gray-100 rounded-3xl hover:border-blue-500 hover:shadow-lg hover:shadow-blue-500/10 transition-all text-left"
                        >
                        <div className="p-4 bg-blue-50 rounded-2xl text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                            {React.cloneElement(role.icon, { size: 28 })}
                        </div>
                        <div className="ml-5">
                            <h3 className="text-xl font-bold text-gray-900">{role.label}</h3>
                            <p className="text-base text-gray-500 mt-1">{role.desc}</p>
                        </div>
                        <ChevronRight className="absolute right-6 text-gray-300 group-hover:text-blue-500 opacity-50 group-hover:opacity-100 group-hover:translate-x-1 transition-all" />
                        </button>
                    ))}
                    </div>
                </div>
                );
            };

            const renderImg2ImgScenario = () => {
                const scenarios = [
                { id: 'anime', label: '变动漫/二次元 🎌', icon: <Wand2 /> },
                { id: 'tryon', label: 'AI 试衣/换装 👗', icon: <Shirt /> },
                { id: 'remove', label: '消除路人/杂物 🪄', icon: <Eraser /> },
                { id: 'restore', label: '老照片修复 🎞️', icon: <History /> },
                { id: 'expand', label: '扩充背景 🏞️', icon: <Camera /> },
                { id: 'other', label: '其他脑洞 🧠', icon: <MoreHorizontal /> },
                ];
                const selected = answers['img2img_wish'];

                return (
                <div className="space-y-8 animate-in slide-in-from-right duration-500 max-w-xl mx-auto flex flex-col h-full">
                    <div className="text-center space-y-3">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-pink-100 text-pink-500 mb-2 shadow-sm">
                        <Sparkles size={32} />
                    </div>
                    <h2 className="text-3xl font-bold text-gray-900">如果给您一张“魔法画布”...✨</h2>
                    <p className="text-gray-600 text-lg">您最希望 AI 帮您做什么？</p>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mt-6">
                    {scenarios.map((item) => (
                        <button
                        key={item.id}
                        onClick={() => recordAnswer('img2img_wish', item.id)}
                        className={`flex flex-col items-center justify-center p-6 rounded-3xl border transition-all duration-300 ${selected === item.id ? 'bg-gray-900 border-gray-900 text-white shadow-xl scale-105' : 'bg-white border-gray-100 text-gray-600 hover:border-gray-300 hover:shadow-md'}`}
                        >
                        <div className="mb-3 opacity-90">{item.icon}</div>
                        <span className="text-base font-bold">{item.label}</span>
                        </button>
                    ))}
                    </div>
                    
                    {selected === 'other' && (
                    <input 
                        type="text" 
                        placeholder="请告诉我们您的独特想法... 💭"
                        className="w-full bg-white border border-gray-200 rounded-2xl p-5 text-gray-900 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 outline-none animate-in fade-in shadow-sm text-lg"
                        onChange={(e) => recordAnswer('img2img_wish_custom', e.target.value)}
                    />
                    )}

                    <div className="pt-8 flex justify-center w-full sticky bottom-6 md:static">
                    <button
                        disabled={!selected}
                        onClick={handleNext}
                        className={`w-full md:w-auto px-12 py-4 rounded-full font-bold text-lg transition-all shadow-lg ${selected ? 'bg-blue-600 text-white hover:bg-blue-700 hover:scale-105 shadow-blue-500/30' : 'bg-gray-200 text-gray-400 cursor-not-allowed'}`}
                    >
                        继续 👉
                    </button>
                    </div>
                </div>
                );
            };

            const renderABTest = (key, prompt, context, colorA, colorB) => (
                <div className="space-y-6 animate-in slide-in-from-right duration-500 max-w-2xl mx-auto flex flex-col h-full">
                <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm">
                    <span className="text-xs font-bold text-blue-600 uppercase tracking-widest mb-3 block">Prompt</span>
                    <p className="text-gray-900 font-medium italic text-xl leading-relaxed">“{prompt}”</p>
                    <div className="mt-4 pt-4 border-t border-gray-100 flex items-start gap-3">
                    <AlertTriangle size={20} className="text-amber-500 shrink-0 mt-0.5" /> 
                    <span className="text-gray-600 text-sm font-medium">{context}</span>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 flex-1">
                    <div onClick={() => recordAnswer(key, 'A')}>
                    <MockImage label="A" color={colorA} type={answers[key] === 'A' ? 'selected' : 'default'} onClick={() => recordAnswer(key, 'A')} />
                    </div>
                    <div onClick={() => recordAnswer(key, 'B')}>
                    <MockImage label="B" color={colorB} type={answers[key] === 'B' ? 'selected' : 'default'} onClick={() => recordAnswer(key, 'B')} />
                    </div>
                </div>

                <div className="pt-6 sticky bottom-6 md:static bg-gradient-to-t from-gray-50 via-gray-50 to-transparent pb-2 md:pb-0">
                    <button
                        disabled={!answers[key]}
                        onClick={handleNext}
                        className={`w-full py-4 rounded-full font-bold text-lg transition-all shadow-lg ${answers[key] ? 'bg-blue-600 text-white hover:bg-blue-700 hover:-translate-y-1 shadow-blue-500/30' : 'bg-gray-200 text-gray-400 cursor-not-allowed'}`}
                    >
                    {answers[key] ? '确认并继续 👉' : '请先选择一张图片'}
                    </button>
                </div>
                </div>
            );

            const renderExpertInput = () => (
                <div className="space-y-8 animate-in slide-in-from-right duration-500 max-w-xl mx-auto">
                <div className="text-center">
                    <h2 className="text-3xl font-bold text-gray-900">寻找 Corner Case 🤔</h2>
                    <p className="text-gray-600 mt-2 text-lg">专家模式：请输入一个复杂的 Prompt 来测试模型极限。</p>
                </div>
                <textarea 
                    className="w-full h-48 bg-white border border-gray-200 rounded-3xl p-6 text-gray-900 focus:outline-none focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all resize-none shadow-sm text-lg leading-relaxed"
                    placeholder="例如：一个红色的苹果在一个蓝色的盒子里，盒子放在一张绿色的圆桌上... 🍎📦🟢"
                    onChange={(e) => recordAnswer('stress_prompt', e.target.value)}
                />
                <div className="flex justify-end gap-4 pt-4">
                    <button onClick={handleNext} className="px-8 py-3 text-gray-500 hover:text-gray-900 font-medium transition-colors">跳过</button>
                    <button onClick={handleNext} className="px-10 py-3 bg-gray-900 text-white font-bold rounded-full hover:bg-gray-800 shadow-lg transition-all">提交测试 🚀</button>
                </div>
                </div>
            );

            const renderFeedback = () => (
                <div className="space-y-12 animate-in slide-in-from-right duration-500 max-w-xl mx-auto py-6">
                <div className="text-center">
                    <h2 className="text-3xl font-bold text-gray-900">最后一步 🏁</h2>
                </div>
                <div className="space-y-4">
                    <label className="text-lg font-bold text-gray-900 block">生成速度体验 ⏳</label>
                    <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
                    {['太慢 😫', '稍慢 😟', '正常 🙂', '很快 😀', '秒出 🚀'].map((opt) => (
                        <button
                            key={opt}
                            onClick={() => recordAnswer('speed_perception', opt)}
                            className={`flex-1 min-w-[80px] py-4 rounded-2xl text-sm font-bold border transition-all ${answers['speed_perception'] === opt ? 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-500/20' : 'bg-white border-gray-200 text-gray-600 hover:border-blue-300'}`}
                        >
                        {opt}
                        </button>
                    ))}
                    </div>
                </div>
                <div className="space-y-4">
                    <label className="text-lg font-bold text-gray-900 block">推荐指数 (NPS) 💖</label>
                    <div className="flex justify-between gap-1 md:gap-2">
                    {[0,1,2,3,4,5,6,7,8,9,10].map((num) => (
                        <button
                        key={num}
                        onClick={() => recordAnswer('nps', num)}
                        className={`w-full aspect-[3/4] rounded-xl text-sm font-bold transition-all ${answers['nps'] === num ? 'bg-green-500 text-white scale-110 shadow-lg shadow-green-500/30' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                        >
                        {num}
                        </button>
                    ))}
                    </div>
                    <div className="flex justify-between text-xs text-gray-400 px-1 font-medium uppercase tracking-wider">
                    <span>绝对不推荐</span>
                    <span>极力推荐</span>
                    </div>
                </div>
                <button 
                    onClick={() => { setIsSubmitting(true); setTimeout(() => handleNext(), 1500); }} 
                    className="w-full py-5 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold text-xl rounded-full hover:shadow-2xl hover:shadow-blue-500/40 hover:-translate-y-1 transition-all flex items-center justify-center gap-3 active:scale-95"
                >
                    {isSubmitting ? '提交数据中... 🔄' : '提交评估结果 ✅'}
                </button>
                </div>
            );

            const renderFinish = () => (
                <div className="flex flex-col items-center justify-center min-h-[60vh] text-center space-y-8 animate-in zoom-in duration-500">
                <div className="w-28 h-28 bg-green-500 rounded-full flex items-center justify-center shadow-2xl shadow-green-500/30">
                    <CheckCircle2 className="text-white" size={56} />
                </div>
                <div className="px-6">
                    <h1 className="text-4xl font-bold text-gray-900 mb-4">感谢您的参与！🎉</h1>
                    <p className="text-gray-600 text-xl leading-relaxed">
                    您的反馈已根据您的身份<br/>
                    <span className="font-bold text-blue-600 inline-block mt-2 px-4 py-1 bg-blue-50 rounded-full">{answers.user_role}</span><br/>
                    进行了分类存储。
                    </p>
                </div>
                <button onClick={() => window.location.reload()} className="text-gray-400 hover:text-gray-900 font-medium flex items-center gap-2 mt-8 transition-colors">
                    <History size={18} /> 重新测试
                </button>
                </div>
            );

            const renderContent = () => {
                if (!currentStep) return null;
                switch(currentStep.id) {
                case 'welcome': return renderWelcome();
                case 'role': return renderRoleSelection();
                case 'img2img_scenario': return renderImg2ImgScenario();
                case 'ab_test_aesthetic': 
                    return renderABTest('ab_aesthetic', '一位在雨中撑伞的少女，色彩鲜艳，吉卜力风格。', '直觉选择：哪一张图给您的感觉更美好？', 'bg-gradient-to-br from-indigo-400 to-purple-500', 'bg-gradient-to-br from-pink-400 to-rose-500');
                case 'ab_test_anatomy':
                    return renderABTest('ab_anatomy', '手部特写：钢琴家正在演奏复杂的和弦。', '重点考察：手指关节与按键位置的逻辑。', 'bg-gradient-to-br from-gray-100 to-gray-300', 'bg-gradient-to-br from-slate-200 to-slate-400');
                case 'ab_test_style':
                    return renderABTest('ab_style', '极简主义海报设计，包含几何图形和柔和阴影。', '重点考察：构图平衡感与阴影真实度。', 'bg-gradient-to-br from-orange-100 to-amber-200', 'bg-gradient-to-br from-yellow-100 to-orange-200');
                case 'ab_test_semantic':
                    return renderABTest('ab_semantic', '一只穿着宇航服的柯基犬正在月球上骑自行车。', '重点考察：多主体共存（狗+宇航服+车+月球）。', 'bg-gradient-to-br from-blue-200 to-cyan-300', 'bg-gradient-to-br from-sky-200 to-indigo-300');
                case 'ab_test_text':
                    return renderABTest('ab_text', '霓虹灯招牌写着 "FUTURE"，赛博朋克背景。', '重点考察：文字拼写准确性。', 'bg-gradient-to-br from-fuchsia-200 to-pink-300', 'bg-gradient-to-br from-violet-200 to-purple-300');
                case 'expert_input': return renderExpertInput();
                case 'feedback': return renderFeedback();
                case 'finish': return renderFinish();
                default: return renderWelcome();
                }
            };

            return (
                <div className="min-h-screen w-full bg-gray-50 text-gray-900 font-sans selection:bg-blue-100 selection:text-blue-900 flex flex-col">
                {currentStepIndex > 0 && currentStepIndex < activeSteps.length - 1 && (
                    <div className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-gray-100 transition-all duration-300">
                    <div className="max-w-3xl mx-auto px-4 md:px-6 py-4 flex items-center justify-between">
                        <button onClick={handlePrev} className="p-2 -ml-2 hover:bg-gray-100 rounded-full transition-colors text-gray-500 hover:text-gray-900">
                        <ChevronLeft size={24} />
                        </button>
                        <div className="flex flex-col items-center">
                        <span className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-0.5">
                            Step {currentStepIndex} of {activeSteps.length - 2}
                        </span>
                        <span className="text-sm font-bold text-gray-900">{currentStep.title}</span>
                        </div>
                        <div className="w-10" />
                    </div>
                    <div className="h-1 w-full bg-gray-100">
                        <div 
                        className="h-full bg-blue-600 transition-all duration-500 ease-out"
                        style={{ width: `${progress}%` }}
                        />
                    </div>
                    </div>
                )}

                <div className="flex-1 w-full max-w-3xl mx-auto px-4 md:px-8 py-6 md:py-10 flex flex-col">
                    {renderContent()}
                </div>
                
                <div className="py-6 text-center opacity-30 pointer-events-none">
                    <span className="text-[10px] font-mono tracking-[0.3em] uppercase">Powered by Model X Engine</span>
                </div>
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
"""

components.html(react_app_html, height=1000, scrolling=True)