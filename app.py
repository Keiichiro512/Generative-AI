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
def generate_location():
    try:
        data = request.get_json()
        if not data or 'item' not in data:
            return jsonify({'error': 'アイテムが指定されていません。'}), 400

        item = data['item']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、家の中でのモノの隠れ場所を的確に言い当てる、ちょっとおせっかいな妖精です。
今、家の中で「{item}」が見つからなくて困っています。

「まさか、そんなところに！」と思うような、でも「ありえるかも…」と思える絶妙な場所を3つ、可能性の高い順に提案してください。

【出力フォーマット】
1. (一番ありそうな場所)
2. (次点でありがちな場所)
3. (意外な盲点かもしれない場所)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"場所の生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)