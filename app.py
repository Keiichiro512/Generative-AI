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
def explain_katakana_word():
    try:
        data = request.get_json()
        if not data or 'katakana_word' not in data:
            return jsonify({'error': 'カタカナ語が指定されていません。'}), 400

        katakana_word = data['katakana_word']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、外来語やビジネス用語に詳しい、言語の専門家です。
今から入力されるカタカナ語を、誰にでも分かりやすい、シンプルな日本語に変換または説明してください。

【カタカナ語】
{katakana_word}

変換する際は、最も一般的で使われやすい日本語の代替案を提示し、必要であれば簡単な使用例も添えてください。

【出力フォーマット】
日本語での意味：(ここに日本語の訳や説明)
使用例：「(簡単な使用例)」
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"カタカナ語の変換中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)