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
def convert_to_kansai_ben():
    try:
        data = request.get_json()
        if not data or 'original_text' not in data:
            return jsonify({'error': '元の文章が指定されていません。'}), 400

        original_text = data['original_text']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、大阪生まれ大阪育ちの、生粋の関西人です。
今から入力される標準語の文章を、まるでネイティブが話しているかのような、自然で面白い関西弁に変換してください。

【元の文章】
{original_text}

変換する際は、単に語尾を「～やで」「～ねん」に変えるだけでなく、イントネーションや言葉の選び方、ユーモアのセンスまで、関西人らしいニュアンスを完全に再現してください。
変換後の文章のみを出力してください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"関西弁変換中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)