import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"APIキーの設定でエラーが発生しました: {e}")


@app.route('/')
def index():
    return render_template('index.html')

# POSTメソッドは維持しつつ、リクエストボディは使わない
@app.route('/generate', methods=['POST'])
def generate_lucky_color():
    try:
        # 今日の日付を取得
        today = datetime.now().strftime("%Y年%m月%d日")

        # AIへの指示（プロンプト）を固定
        prompt = f"{today}のラッキーカラーを1つ、その色にまつわるポジティブな一言アドバイスと一緒に教えてください。色の名前は一般的な名称でお願いします。フォーマットは「ラッキーカラー：色名\nアドバイス：一言」のようにしてください。"
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        # キーを 'result' に変更
        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ラッキーカラー生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)