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
def reframe_to_positive():
    try:
        data = request.get_json()
        if not data or 'original_text' not in data:
            return jsonify({'error': '元の文章が指定されていません。'}), 400

        original_text = data['original_text']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、認知行動療法（CBT）と思考のリフレーミングの専門家です。
今から入力される、ネガティブな、あるいは中立的な文章を、自己肯定感を高めるような、前向きでポジティブな文章に書き換えてください。

【元の文章】
{original_text}

変換する際は、元の事実を歪めるのではなく、物事の捉え方や視点を変えることで、ポジティブな側面に光を当てるようにしてください。
修正後の文章だけでなく、なぜそのように捉え直せるのか、簡単な「視点のヒント」も添えてください。

【出力フォーマット】
ポジティブな捉え方：
「(ここにポジティブに変換した文章)」

視点のヒント：
(なぜそのように考えられるのか、簡単な解説)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ポジティブ変換中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)