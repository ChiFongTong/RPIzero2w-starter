import os
from openai import OpenAI

# 嘗試啟用 readline，讓 input() 支援方向鍵與歷史
try:
    import readline  # noqa: F401
except ImportError:
    readline = None


def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("請先在環境變數中設定 OPENAI_API_KEY 再執行程式。")

    if readline is None:
        print("※ 注意：系統沒有 readline 模組，方向鍵可能只會顯示 ^[[A / ^[[D，不會移動游標。")

    client = OpenAI(api_key=api_key)

    # 使用的模型（可依你帳號權限挑，例如 gpt-4.1-mini）
    model = "gpt-4.1-mini"

    system_prompt = "你是一個用繁體中文回答、簡潔有禮的終端機聊天機器人。"

    # 對話歷史，第一則當成開發者/系統訊息
    messages = [
        {"role": "developer", "content": system_prompt}
    ]

    print("=== ChatGPT 終端機聊天 ===")
    print("輸入 'exit' / 'quit' 或 Ctrl+C 離開。\n")

    while True:
        try:
            user_input = input("你：")
        except (EOFError, KeyboardInterrupt):
            print("\n再見！")
            break

        user_input = user_input.strip()
        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "q"}:
            print("再見！")
            break

        # 加入使用者訊息
        messages.append({"role": "user", "content": user_input})

        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages,
                max_completion_tokens=256,  # 回覆最多 token
                temperature=0.7,            # 創意程度
            )
        except Exception as e:
            print(f"[錯誤] 呼叫 OpenAI API 失敗：{e}")
            continue

        reply = completion.choices[0].message.content.strip()
        print(f"GPT：{reply}\n")

        # 把回覆也加進對話歷史
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
