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
    # アプリケーションを終了させるか、エラーページを表示するなどの処理が必要
    # ここでは単純にプリントしていますが、本番環境ではより丁寧な処理が必要です。


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_nickname():
    try:
        # フロントエンドから送られてきたJSONデータを取得
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': '名前が指定されていません。'}), 400

        name = data['name']

        # AIへの指示（プロンプト）を入力された名前を使って動的に作成
        prompt = f"「{name}」という苗字または名前に、クリエイティブで面白いニックネームを3つ考えてください。箇条書きで、面白い理由も軽く添えてください。"
        
        response = model.generate_content(prompt)
        
        # 結果を整形して改行を保持
        formatted_response = response.text.strip()

        return jsonify({'nickname': formatted_response})

    except Exception as e:
        print(f"ニックネーム生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)