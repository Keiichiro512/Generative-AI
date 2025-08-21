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
def generate_headlines():
    try:
        data = request.get_json()
        if not data or 'theme' not in data:
            return jsonify({'error': 'テーマが指定されていません。'}), 400

        theme = data['theme']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、数々の人気メディアで記事をヒットさせてきた、敏腕編集者です。
今から指定する「テーマ」について、読者が思わずクリックして記事を読みたくなるような、魅力的で少し煽り気味な見出しを3つ提案してください。

【テーマ】
{theme}

提案する見出しは、それぞれ異なる切り口（例：問題提起型、ノウハウ型、逆張り型など）でお願いします。
具体的な数字や、読者の好奇心を刺激するような言葉（「知らないと損」「たった3つのコツ」など）を効果的に使ってください。

【出力フォーマット】
1. (見出し案1)
2. (見出し案2)
3. (見出し案3)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"見出し生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)