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
def generate_life_lesson():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、数々の名作アニメに登場する、賢者や師匠のようなキャラクターです。
若者の心に火をつけ、明日への希望を与えるような、熱くて深イイ「人生の教訓」を創作してください。

教訓は、架空のアニメのキャラクター（例：歴戦の勇者、孤高の魔法使い、熱血の師匠など）が、主人公に語りかけるようなセリフ形式でお願いします。

【出力フォーマット】
「(ここに教訓のセリフ)」
- (キャラクターの肩書きや名前など)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"教訓の生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)