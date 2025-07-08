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
def check_text():
    try:
        data = request.get_json()
        if not data or 'original_text' not in data:
            return jsonify({'error': '元の文章が指定されていません。'}), 400

        original_text = data['original_text']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、出版社に勤務する、経験豊富な校正者です。
今から入力される日本語の文章をプロの目でチェックし、誤字、脱字、文法的な誤り、不自然な表現をすべて指摘してください。

【元の文章】
{original_text}

指摘する際は、単に修正後の文章を提示するのではなく、どの部分がなぜ間違っているのか、そしてどのように修正すれば良いのかを、箇条書きで分かりやすく説明してください。
もし誤りが見つからなかった場合は、「この文章に明らかな誤字脱字は見つかりませんでした。」と回答してください。

【出力フォーマット】
- 指摘箇所：「(間違いのある部分を引用)」
  問題点：(なぜ間違っているかの説明)
  修正案：「(正しい表現の提案)」
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"校正中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)