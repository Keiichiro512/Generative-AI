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
def generate_youtube_title():
    try:
        data = request.get_json()
        if not data or 'theme' not in data:
            return jsonify({'error': 'テーマが指定されていません。'}), 400

        theme = data['theme']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、登録者数100万人を超える大人気YouTuberであり、動画のタイトル付けの達人です。
今から指定する「テーマ」で、視聴者が思わずクリックしたくなるような、魅力的で再生数が伸びる動画のタイトル案を3つ提案してください。

【動画のテーマ】
{theme}

提案は、それぞれ異なるアプローチ（例：権威性を示す、好奇心を煽る、具体的な結果を約束する）でお願いします。
タイトルには、SEO（検索対策）を意識したキーワードを含めつつ、視聴者の興味を引くような数字や衝撃的な言葉を入れてください。

【出力フォーマット】
1. (タイトル案1)
   [ポイント]：(このタイトルの狙いや、なぜクリックされやすいかの簡単な説明)

2. (タイトル案2)
   [ポイント]：(このタイトルの狙いや、なぜクリックされやすいかの簡単な説明)

3. (タイトル案3)
   [ポイント]：(このタイトルの狙いや、なぜクリックされやすいかの簡単な説明)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"動画タイトル生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)