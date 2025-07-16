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
def check_round_trip_translation():
    try:
        data = request.get_json()
        if not data or 'original_japanese' not in data:
            return jsonify({'error': '元の日本語が指定されていません。'}), 400

        original_japanese = data['original_japanese']

        # --- ステップ1: 日本語から英語への翻訳 ---
        prompt_to_english = f"""
あなたはプロの翻訳家です。以下の日本語の文章を、自然で流暢な英語に翻訳してください。
翻訳後の英語のみを出力してください。
【日本語の文章】
{original_japanese}
"""
        english_response = model.generate_content(prompt_to_english)
        english_text = english_response.text.strip()

        # --- ステップ2: 英語から日本語への逆翻訳 ---
        prompt_to_japanese = f"""
あなたはプロの翻訳家です。以下の英語の文章を、自然で流暢な日本語に翻訳してください。
翻訳後の日本語のみを出力してください。
【英語の文章】
{english_text}
"""
        final_japanese_response = model.generate_content(prompt_to_japanese)
        final_japanese_text = final_japanese_response.text.strip()

        return jsonify({'result': final_japanese_text})

    except Exception as e:
        print(f"逆翻訳中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)