import os
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# APIキーを設定
try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except AttributeError:
    print("エラー: GOOGLE_API_KEYが設定されていません。")
    exit()

# ホームページを表示するルート
@app.route('/')
def index():
    return render_template('index.html')

# 単語を生成するAPIのルート
@app.route('/generate', methods=['POST'])
def generate_word():
    try:
        # 生成AIへの指示（プロンプト）
        prompt = "思わずクスッとしてしまうような、面白い日本語の単語を1つだけ生成してください。"
        
        response = model.generate_content(prompt)
        
        # 生成されたテキストをクライアントに返す
        return jsonify({'word': response.text.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)