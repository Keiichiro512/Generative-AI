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
def generate_gift_ideas():
    try:
        data = request.get_json()
        if not data or 'recipient_info' not in data:
            return jsonify({'error': '相手の情報が指定されていません。'}), 400

        recipient_info = data['recipient_info']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、相手の好みや性格に合わせて、最適なプレゼントを提案するプロのギフトコンシェルジュです。
今から指定する「相手」の情報を元に、誕生日プレゼントにぴったりの気の利いたアイデアを3つ提案してください。

【相手】
{recipient_info}

提案する際は、ただの品物名だけでなく、なぜそのプレゼントが良いかの「提案理由」を簡潔に添えてください。価格帯は幅広く、実用的なものから体験型のものまで含めてください。

【出力フォーマット】
1. (プレゼントアイデア1)
   提案理由：(なぜこのプレゼントが良いかの説明)
2. (プレゼントアイデア2)
   提案理由：(なぜこのプレゼントが良いかの説明)
3. (プレゼントアイデア3)
   提案理由：(なぜこのプレゼントが良いかの説明)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"プレゼント提案中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)