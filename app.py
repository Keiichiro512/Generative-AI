import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

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

@app.route('/generate', methods=['POST'])
def suggest_emojis():
    try:
        data = request.get_json()
        if not data or 'original_text' not in data:
            return jsonify({'error': '元の文章が指定されていません。'}), 400

        original_text = data['original_text']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、世界中のSNSで活躍する、絵文字の使い方の達人です。
今から入力される文章の文脈や感情を読み取り、その文章に添えるのに最適な絵文字を3つ提案してください。

【元の文章】
{original_text}

絵文字を提案する際は、それぞれの絵文字がなぜその文章に合うのか、簡単な理由も添えてください。

【出力フォーマット】
1. (絵文字1) 理由：(なぜ合うかの簡単な説明)
2. (絵文字2) 理由：(なぜ合うかの簡単な説明)
3. (絵文字3) 理由：(なぜ合うかの簡単な説明)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"絵文字提案中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)