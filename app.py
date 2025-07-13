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
def change_tone():
    try:
        data = request.get_json()
        if not data or 'original_text' not in data:
            return jsonify({'error': '元の文章が指定されていません。'}), 400

        original_text = data['original_text']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、優れたコミュニケーターであり、文章のトーン＆マナーを調整する専門家です。
今から入力される文章の核心的な意味を変えずに、もっと親しみやすく、フレンドリーなトーンに書き換えてください。

【元の文章】
{original_text}

変換する際は、絵文字を適切に使ったり、少しだけ砕けた表現を用いたりして、相手にポジティブな印象を与えるように工夫してください。
ただし、ビジネスシーンでも使える範囲の、丁寧さは失わないようにしてください。
変換後の文章のみを出力してください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"トーン変更中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)