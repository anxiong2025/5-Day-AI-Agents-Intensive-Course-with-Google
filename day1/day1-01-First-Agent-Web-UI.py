import os
from pathlib import Path
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# 读取 .env 文件
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    for line in env_file.read_text().splitlines():
        if line.startswith('GOOGLE_API_KEY='):
            os.environ["GOOGLE_API_KEY"] = line.split('=', 1)[1].strip()
            break

# 配置重试选项
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

# 创建 Agent
root_agent = Agent(
    name="helpful_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)

# 创建 Runner
runner = InMemoryRunner(agent=root_agent, app_name="agents")

# 创建 FastAPI 应用
app = FastAPI(title="Day1 First Agent - Prompt to Action")

class ChatRequest(BaseModel):
    message: str
    session_id: str = "web_session"

@app.get("/", response_class=HTMLResponse)
async def home():
    """返回聊天界面的 HTML"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Day1 First Agent - Prompt to Action</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                width: 90%;
                max-width: 800px;
                height: 90vh;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                display: flex;
                flex-direction: column;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px 30px;
                border-radius: 20px 20px 0 0;
                font-size: 20px;
                font-weight: 600;
            }
            .chat-area {
                flex: 1;
                overflow-y: auto;
                padding: 20px 30px;
                background: #f7f7f8;
            }
            .message {
                margin-bottom: 15px;
                display: flex;
                align-items: flex-start;
            }
            .message.user { justify-content: flex-end; }
            .message-content {
                max-width: 70%;
                padding: 12px 18px;
                border-radius: 18px;
                line-height: 1.5;
                word-wrap: break-word;
            }
            .message.user .message-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .message.agent .message-content {
                background: white;
                border: 1px solid #e0e0e0;
                color: #333;
            }
            .input-area {
                padding: 20px 30px;
                background: white;
                border-radius: 0 0 20px 20px;
                border-top: 1px solid #e0e0e0;
            }
            .input-form {
                display: flex;
                gap: 10px;
            }
            #message-input {
                flex: 1;
                padding: 12px 18px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 15px;
                outline: none;
                transition: border-color 0.3s;
            }
            #message-input:focus {
                border-color: #667eea;
            }
            #send-button {
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }
            #send-button:hover {
                transform: scale(1.05);
            }
            #send-button:disabled {
                opacity: 0.6;
                cursor: not-allowed;
            }
            .loading {
                display: none;
                padding: 12px 18px;
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 18px;
                color: #666;
            }
            .loading.show { display: block; }
            .dot-flashing {
                position: relative;
                width: 10px;
                height: 10px;
                border-radius: 5px;
                background-color: #667eea;
                color: #667eea;
                animation: dot-flashing 1s infinite linear alternate;
                animation-delay: 0.5s;
                display: inline-block;
                margin: 0 5px;
            }
            .dot-flashing::before, .dot-flashing::after {
                content: '';
                display: inline-block;
                position: absolute;
                top: 0;
            }
            .dot-flashing::before {
                left: -15px;
                width: 10px;
                height: 10px;
                border-radius: 5px;
                background-color: #667eea;
                color: #667eea;
                animation: dot-flashing 1s infinite alternate;
                animation-delay: 0s;
            }
            .dot-flashing::after {
                left: 15px;
                width: 10px;
                height: 10px;
                border-radius: 5px;
                background-color: #667eea;
                color: #667eea;
                animation: dot-flashing 1s infinite alternate;
                animation-delay: 1s;
            }
            @keyframes dot-flashing {
                0% { background-color: #667eea; }
                50%, 100% { background-color: rgba(102, 126, 234, 0.2); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                🤖 Day1 First Agent - Prompt to Action
            </div>
            <div class="chat-area" id="chat-area">
                <div class="message agent">
                    <div class="message-content">
                        你好！我是 Google ADK Agent。我可以帮你搜索信息、回答问题。有什么我可以帮助你的吗？
                    </div>
                </div>
            </div>
            <div class="input-area">
                <form class="input-form" id="chat-form">
                    <input 
                        type="text" 
                        id="message-input" 
                        placeholder="输入你的问题..."
                        autocomplete="off"
                        required
                    />
                    <button type="submit" id="send-button">发送</button>
                </form>
            </div>
        </div>

        <script>
            const chatArea = document.getElementById('chat-area');
            const chatForm = document.getElementById('chat-form');
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-button');
            const sessionId = 'session_' + Date.now();

            console.log('页面加载完成');

            chatForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                console.log('表单提交');
                
                const message = messageInput.value.trim();
                console.log('消息内容:', message);
                
                if (!message) return;

                // 添加用户消息
                addMessage(message, 'user');
                messageInput.value = '';
                sendButton.disabled = true;

                // 显示加载动画
                const loadingDiv = document.createElement('div');
                loadingDiv.className = 'message agent';
                loadingDiv.innerHTML = '<div class="message-content loading show">思考中<div class="dot-flashing"></div></div>';
                chatArea.appendChild(loadingDiv);
                chatArea.scrollTop = chatArea.scrollHeight;

                try {
                    console.log('发送请求到 /chat');
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message, session_id: sessionId })
                    });

                    console.log('收到响应:', response.status);
                    const data = await response.json();
                    console.log('响应数据:', data);
                    
                    // 移除加载动画
                    loadingDiv.remove();

                    // 添加 Agent 回复
                    addMessage(data.response, 'agent');
                } catch (error) {
                    console.error('错误:', error);
                    loadingDiv.remove();
                    addMessage('抱歉，发生了错误：' + error.message, 'agent');
                } finally {
                    sendButton.disabled = false;
                    messageInput.focus();
                }
            });

            function addMessage(text, sender) {
                console.log('添加消息:', sender, text);
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                messageDiv.innerHTML = `<div class="message-content">${escapeHtml(text)}</div>`;
                chatArea.appendChild(messageDiv);
                chatArea.scrollTop = chatArea.scrollHeight;
            }

            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML.replace(/\\n/g, '<br>');
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat(request: ChatRequest):
    """处理聊天请求"""
    try:
        print(f"\n收到消息: {request.message}")
        
        # 使用 run_debug 获取完整响应
        response_list = await runner.run_debug(
            request.message,
            session_id=request.session_id
        )
        
        # 提取最后的 Agent 响应文本
        final_response = ""
        
        if response_list:
            # 遍历所有事件，找到 Agent 的响应
            for event in reversed(response_list):
                # 检查是否有 content 属性
                if hasattr(event, 'content') and event.content:
                    content = event.content
                    # 检查 content 是否有 parts
                    if hasattr(content, 'parts') and content.parts:
                        # 提取所有 parts 的文本
                        texts = []
                        for part in content.parts:
                            if hasattr(part, 'text') and part.text:
                                texts.append(part.text)
                        if texts:
                            final_response = ''.join(texts)
                            break
        
        if not final_response:
            final_response = "抱歉，我无法处理这个请求。"
        
        print(f"最终返回: {final_response}\n")
        
        return {
            "response": final_response,
            "session_id": request.session_id
        }
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            {"error": str(e), "response": f"处理请求时出错：{str(e)}"},
            status_code=500
        )

if __name__ == "__main__":
    print("🚀 启动 Web UI...")
    print("📱 访问: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
