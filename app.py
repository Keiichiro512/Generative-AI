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
def extract_keywords():
    try:
        data = request.get_json()
        if not data or 'original_text' not in data:
            return jsonify({'error': '元の文章が指定されていません。'}), 400

        original_text = data['original_text']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、自然言語処理（NLP）を専門とする、データサイエンティストです。
今から入力される文章の内容を正確に分析し、その文章の主題や核心を表す最も重要なキーワードを5つ抽出してください。

【元の文章】
{original_text}

抽出するキーワードは、単なる頻出単語ではなく、文章全体の文脈を理解した上で、そのテーマを象徴する単語やフレーズを選んでください。
結果は箇条書きで、重要度が高い順に並べてください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"キーワード抽出中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)