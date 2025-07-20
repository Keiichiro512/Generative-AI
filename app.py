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
def rate_word_difficulty():
    try:
        data = request.get_json()
        if not data or 'word' not in data:
            return jsonify({'error': '単語が指定されていません。'}), 400

        word = data['word']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、英語教育の専門家であり、英単語の難易度を正確に評価することができます。
今から入力される英単語について、一般的な英語学習者にとっての難易度を「簡単」「普通」「難しい」の3段階で判定してください。

【判定対象の英単語】
{word}

判定結果に加えて、なぜそのように判断したのか、簡単な「判定の根拠」も示してください。
（例：中学校で習う基本的な単語のため、日常会話でよく使われるため、専門的な文脈で使われることが多いため、など）

【出力フォーマット】
判定結果：(簡単/普通/難しい)
判定の根拠：(なぜそのように判断したかを簡潔に説明)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"難易度判定中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)