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
def generate_question():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、どんな人ともすぐに打ち解けられる、コミュニケーションの達人です。
初対面の人との会話のきっかけになるような、ユニークで面白い質問を1つだけ生成してください。

ただし、相手が答えに困るようなプライベートすぎる質問や、はい/いいえで終わってしまう質問は避けてください。
相手の価値観や人柄が少し見えるような、ポジティブで楽しい会話につながる質問が望ましいです。

良い例：
・もし1ヶ月間、どこでも好きな場所に住めるとしたら、どこでどんなことをしてみたいですか？
・子供の頃、一番熱中していた遊びは何ですか？
・今までで一番「これは運が良かった！」と思えるエピソードがあれば教えてください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"質問の生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)