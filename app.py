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
def generate_game_idea():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、世界中で数々のヒット作を生み出してきた、天才的なゲームデザイナーです。
スマートフォンで、通学・通勤の合間や少しの休憩時間に、誰でも気軽に楽しめる、シンプルで中毒性の高いパズルゲームのアイデアを1つ考案してください。

考案する際は、以下の要素を含めて、具体的な企画書形式でお願いします。

【出力フォーマット】
ゲームタイトル案：(キャッチーな名前)
ゲームコンセプト：(どのようなゲームかの簡単な説明)
基本ルール：(ゲームの目的と操作方法)
面白さのポイント：(なぜこのゲームがハマるのか、工夫点など)
マネタイズ案：(例：広告表示、スキンやアイテムの販売など)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ゲームアイデア生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)