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
def generate_riddle():
    try:
        data = request.get_json()
        if not data or 'answer' not in data:
            return jsonify({'error': '答えが指定されていません。'}), 400

        answer = data['answer']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、子供から大人まで楽しめる、面白くて少しひねりのある「なぞなぞ」を作るのが得意な作家です。
今から指定する「答え」になるような、オリジナルのなぞなぞを1つ創作してください。

【答え】
{answer}

なぞなぞには、答えのヒントを入れつつも、すぐには分からないような言葉遊びや意外な視点を含めてください。
最後は必ず「〜なーんだ？」で終わるようにしてください。

【出力フォーマット】
(なぞなぞの問題文)

答え：{answer}
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"なぞなぞ生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)