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
def invent_new_sport():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、世界中の人々を熱狂させる新しいスポーツを生み出す、天才的なゲームデザイナーです。
子供からお年寄りまで、運動神経に関わらず誰もが一緒に楽しめる、全く新しいスポーツのアイデアとルールを1つ考案してください。

考案する際は、以下の要素を含めて、すぐにでも遊べるように具体的に説明してください。

【出力フォーマット】
スポーツ名：(キャッチーな名前)
コンセプト：(どんなスポーツかの簡単な説明)
プレイ人数：(推奨される人数)
必要な道具：(手軽に用意できるもの)
基本ルール：
　1. (最も重要なルール)
　2. (次に重要なルール)
　3. (その他のルール)
このスポーツの魅力：(なぜこれが面白いのか、どういう効果があるのか)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"新スポーツ考案中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)