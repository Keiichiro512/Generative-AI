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
def generate_product_review():
    try:
        data = request.get_json()
        if not data or 'product_name' not in data:
            return jsonify({'error': '商品名が指定されていません。'}), 400

        product_name = data['product_name']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、最新ガジェットや未来の製品をレビューするのが得意な、人気ブロガーです。
今から指定する「架空の商品」を実際に使ってみたかのように、リアルで面白いレビュー記事を作成してください。

【架空の商品】
{product_name}

レビューは、読者が購入を検討したくなるように、以下の要素を含んだ形式でお願いします。

【出力フォーマット】
レビュータイトル：(記事のキャッチーなタイトル)
評価：(星5段階評価で、★の数で表現)

本文：
(ここに、商品の第一印象、使ってみて良かった点、少し気になった点などを、具体的なエピソードを交えて記述)

まとめ：(どんな人におすすめか)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"レビュー生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)