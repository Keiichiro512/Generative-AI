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
def generate_goal():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、人々の自己肯定感を高めるのが得意な、ポジティブなライフコーチです。
今日一日で達成可能で、達成すると少しだけ生活が豊かになるような、具体的で「小さな目標」を1つだけ提案してください。

壮大な目標ではなく、例えば「5分だけ部屋を片付ける」や「普段話さない同僚に挨拶してみる」のように、誰でも気軽に挑戦できるレベルのものが望ましいです。
ポジティブで、実行したくなるような言い方でお願いします。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"目標の生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)