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
def generate_review_response():
    try:
        data = request.get_json()
        if not data or 'rating' not in data or 'comment' not in data:
            return jsonify({'error': '評価とコメントが指定されていません。'}), 400

        rating = data['rating']
        comment = data['comment']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、顧客対応のプロフェッショナルであり、レストランやオンラインストアの店長です。
お客様から寄せられた以下の「レビュー」に対して、感謝の気持ちが伝わる、丁寧で誠実な返信文を作成してください。

【お客様のレビュー】
星評価：{rating}つ星
コメント：{comment}

返信する際は、以下の点を考慮してください。
1. まず、レビューを投稿してくださったことへの感謝を述べます。
2. もしポジティブなレビュー（星4つ以上）であれば、お客様の具体的な褒め言葉に触れて喜びを伝えます。
3. もしネガティブなレビュー（星3つ以下）であれば、ご不便をおかけしたことを真摯に謝罪し、具体的なコメント内容に触れて改善策や今後の対応について言及します。
4. 最後に、お客様の再訪や再利用を促す言葉で締めくくります。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"レビュー返信文作成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)