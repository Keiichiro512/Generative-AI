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
def generate_country_profile():
    try:
        data = request.get_json()
        if not data or 'concept' not in data:
            return jsonify({'error': '国のコンセプトが指定されていません。'}), 400

        concept = data['concept']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、壮大なファンタジー小説やSF作品の世界観設定を専門とする、世界的な作家です。
今から指定する「コンセプト」を持つ、魅力的で独創的な架空の国の設定を創作してください。

【国のコンセプト】
{concept}

設定は、読者やプレイヤーがその世界に没入できるように、以下の要素を具体的に記述してください。

【出力フォーマット】
国名：(国の名前)
首都：(首都の名前)
政体：(政治体制、例：王政、共和制、魔法議会制など)
主要産業：(国を支える主な産業や技術)
文化・風習：(国民の生活様式や独自の文化)
抱える問題：(その国が直面している社会問題や対立)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"国設定の生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)