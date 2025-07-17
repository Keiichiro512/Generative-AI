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
def reorder_to_conclusion_first():
    try:
        data = request.get_json()
        if not data or 'original_text' not in data:
            return jsonify({'error': '元の文章が指定されていません。'}), 400

        original_text = data['original_text']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、ロジカルシンキングと文章構成のプロフェッショナルです。
今から入力される文章を分析し、「結論ファースト」の構成に書き換えてください。

【元の文章】
{original_text}

書き換える際は、以下の点を遵守してください。
1.  まず、文章全体の「結論」や「最も言いたいこと」を最初に提示します。
2.  次に、その結論に至った「理由」や「背景」を述べます。
3.  最後に、必要であれば「具体例」や「詳細情報」を補足します。
4.  元の文章に含まれる重要な情報は、すべて含めるようにしてください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"構成変更中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)