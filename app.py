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
def generate_company_name():
    try:
        data = request.get_json()
        if not data or 'company_info' not in data:
            return jsonify({'error': '企業のコンセプトが指定されていません。'}), 400

        company_info = data['company_info']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、数々の成功企業を世に送り出してきた、ブランディングの専門家です。
クライアントから伝えられた企業のコンセプトに合った、未来的で覚えやすく、ドメインも取得できそうな架空の社名を3つ提案してください。

【企業のコンセプト】
{company_info}

提案する社名には、それぞれ簡単な「社名の由来やコンセプト」も添えてください。

【出力フォーマット】
1. **(社名1)**
   由来：(社名の由来やコンセプトを簡潔に説明)

2. **(社名2)**
   由来：(社名の由来やコンセプトを簡潔に説明)

3. **(社名3)**
   由来：(社名の由来やコンセプトを簡潔に説明)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"社名生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)