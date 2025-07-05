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
def summarize_text():
    try:
        data = request.get_json()
        if not data or 'original_text' not in data:
            return jsonify({'error': '元の文章が指定されていません。'}), 400

        original_text = data['original_text']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、長文の読解と要点抽出に長けた、優秀な編集者です。
今から入力される文章の要点を的確に捉え、最も重要な部分を抽出し、日本語で3行の簡潔な箇条書きで要約してください。

【元の文章】
{original_text}

要約する際は、元の文章の核心的なメッセージを維持し、専門用語もできるだけ分かりやすい言葉で表現してください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"要約中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)