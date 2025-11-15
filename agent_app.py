import os
from pathlib import Path
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types

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

# 交互式聊天循环
async def chat():
    print("🤖 Agent 已启动！输入 'quit' 或 'exit' 退出。\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 再见！")
                break
            
            if not user_input:
                continue
            
            print("\n🔍 Agent 思考中...\n")
            response = await runner.run_debug(user_input)
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"\n❌ 错误: {e}\n")

if __name__ == "__main__":
    import asyncio
    asyncio.run(chat())
