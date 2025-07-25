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
def generate_app_idea():
    try:
        data = request.get_json()
        if not data or 'target_audience' not in data:
            return jsonify({'error': 'ターゲット層が指定されていません。'}), 400

        target_audience = data['target_audience']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、シリコンバレーで活躍する、経験豊富なプロダクトマネージャーです。
今から指定する「ターゲット層」が抱える悩みやニーズを深く洞察し、それを解決するための革新的なスマートフォンのアプリのアイデアを1つ提案してください。

【ターゲット層】
{target_audience}

提案する際は、単なる思いつきではなく、以下の要素を含んだ、具体的な企画書形式でお願いします。

【出力フォーマット】
アプリ名案：(キャッチーなアプリ名)
コンセプト：(どのようなアプリかの簡単な説明)
主な機能：
　・(主要な機能を箇条書きで3つほど)
マネタイズ案：(どのように収益を上げるかのアイデア)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"アプリアイデア生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)