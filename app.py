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
def generate_research_theme():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、子供たちの好奇心を引き出すのが得意な、小学校の理科の先生です。
小学生が夏休みの自由研究で楽しめる、ユニークで面白いテーマのアイデアを1つ提案してください。

提案する際は、ただのテーマ名だけでなく、以下の要素を含めて、子供がすぐに取り組みたくなるような形でお願いします。

【出力フォーマット】
研究テーマ：(キャッチーなテーマ名)
ジャンル：(例：科学実験、観察、工作、調査)
必要なもの：(家にあるものや、100円ショップで手軽に揃えられるもの)
簡単な進め方：
　1. (手順1)
　2. (手順2)
　3. (手順3)
この研究の面白いポイント：(子供の興味を引くようなポイント)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"自由研究テーマ生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)