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
def translate_to_english():
    try:
        data = request.get_json()
        if not data or 'japanese_text' not in data:
            return jsonify({'error': '日本語の文章が指定されていません。'}), 400

        japanese_text = data['japanese_text']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、日本語と英語の両方に堪能な、プロの翻訳家です。
今から入力される日本語の文章を、ネイティブスピーカーが話すような、自然で流暢な英語に翻訳してください。

【日本語の文章】
{japanese_text}

翻訳する際は、単語を直訳するのではなく、元の文章の意図、文脈、ニュアンスを正確に捉え、最も適切な英語表現を選んでください。
翻訳後の英語のみを出力してください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"翻訳中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)