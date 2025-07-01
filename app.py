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
def generate_pet_name():
    try:
        data = request.get_json()
        if not data or 'pet_info' not in data:
            return jsonify({'error': 'ペットの情報が指定されていません。'}), 400

        pet_info = data['pet_info']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、世界一のペットネーミングの専門家です。
飼い主から伝えられたペットの情報にぴったりの、愛情がこもった素敵な名前を3つ提案してください。

【ペットの情報】
{pet_info}

提案する名前には、それぞれ簡単な「名前の由来や意味」も添えてください。

【出力フォーマット】
1. **(名前1)**
   由来：(名前の由来や意味を簡潔に説明)

2. **(名前2)**
   由来：(名前の由来や意味を簡潔に説明)

3. **(名前3)**
   由来：(名前の由来や意味を簡潔に説明)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ペットの名前生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)