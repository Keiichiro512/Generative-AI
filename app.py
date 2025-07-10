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
def create_business_email():
    try:
        data = request.get_json()
        if not data or 'requirements' not in data:
            return jsonify({'error': '要件が指定されていません。'}), 400

        requirements = data['requirements']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、外資系コンサルティングファームに勤務する、経験豊富なビジネスパーソンです。
クライアントから伝えられた以下の「伝えたい要件」を元に、そのまま送れるレベルの、丁寧で分かりやすいビジネスメールの文章を作成してください。

【伝えたい要件】
{requirements}

メールを作成する際は、件名、宛名、挨拶、結びの言葉まで含めて、ビジネスメールの正式なフォーマットに沿ってください。
元の要件の意図を汲み取り、相手に失礼のない、かつ要点が明確に伝わる文章構成にしてください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ビジネスメール作成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)