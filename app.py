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
def explain_simply():
    try:
        data = request.get_json()
        if not data or 'term' not in data:
            return jsonify({'error': '言葉が指定されていません。'}), 400

        term = data['term']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、どんなに難しいことでも、小学生に分かるように説明するのが大得意な、天才的な先生です。
今から入力される専門用語や難しい言葉を、身近なものに例えながら、非常に分かりやすく説明してください。

【難しい言葉】
{term}

説明する際は、以下の点を守ってください。
1.  専門用語は使わない。
2.  子供が興味を持つような、面白い例え話を使う。
3.  まず一言で「〇〇みたいなものだよ」と結論を言ってから、詳しい説明を始める。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"説明生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)