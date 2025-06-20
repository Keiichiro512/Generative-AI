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
def generate_blog_titles():
    try:
        # フロントエンドから送られてきたJSONデータを取得
        data = request.get_json()
        if not data or 'keyword' not in data:
            return jsonify({'error': 'キーワードが指定されていません。'}), 400

        keyword = data['keyword']

        # AIへの指示（プロンプト）を入力されたキーワードを使って動的に作成
        prompt = f"""
「{keyword}」というキーワードをテーマにした、読者のクリックを誘うような魅力的なブログ記事のタイトルを3つ提案してください。
それぞれ異なる切り口で、具体的な数字やパワーワード（「知らないと損」「完全ガイド」など）を入れるなど、SEO（検索エンジン最適化）も少し意識してください。
箇条書きで、読みやすく提示してください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ブログタイトル生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)