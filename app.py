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
def create_pr_outline():
    try:
        data = request.get_json()
        if not data or 'announcement_details' not in data:
            return jsonify({'error': '発表内容が指定されていません。'}), 400

        announcement_details = data['announcement_details']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、数々の企業の広報・PRを成功させてきた、ベテランのPRコンサルタントです。
クライアントから伝えられた以下の「発表内容」を元に、メディア関係者がすぐに内容を理解できるような、論理的で分かりやすいプレスリリースの骨子（構成案）を作成してください。

【発表内容】
{announcement_details}

作成する骨子は、一般的なプレスリリースの構成（タイトル、リード文、本文、会社概要など）に沿ってください。
各項目で、どのような内容を記述すべきかを簡潔に示してください。

【出力フォーマット】
件名（タイトル案）：
リード文（発表内容の要約）：
本文：
　1. 背景・経緯：(なぜこの発表に至ったのか)
　2. 製品・サービスの詳細：(スペック、特徴、価格など)
　3. 今後の展望：(将来的に何を目指すのか)
会社概要：
問い合わせ先：
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"プレスリリース骨子作成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)