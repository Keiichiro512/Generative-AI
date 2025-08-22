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
def generate_social_business_idea():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、社会問題を解決するためのビジネス（ソーシャルビジネス）を専門とする、経験豊富な起業家です。
現代社会が抱える問題（例：環境問題、高齢化、地域の過疎化など）の中から1つを取り上げ、その問題を解決するための、持続可能で革新的なビジネスアイデアを1つ提案してください。

提案は、投資家へのプレゼンテーションを想定し、以下の要素を含んだ具体的な企画書形式でお願いします。

【出力フォーマット】
事業名案：(事業の目的が伝わる名前)
解決したい社会問題：(どの社会問題をどう解決するか)
事業概要：(ビジネスモデルの簡単な説明)
主な提供価値：
　・(提供するサービスや商品の価値を箇条書きで2〜3個)
収益モデル：(どのようにして事業を継続させるか)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ビジネスアイデア生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)