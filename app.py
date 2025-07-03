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
def generate_pun():
    try:
        data = request.get_json()
        if not data or 'keyword' not in data:
            return jsonify({'error': 'キーワードが指定されていません。'}), 400

        keyword = data['keyword']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、日本一のダジャレ職人です。どんな言葉でも、面白くてくだらないダジャレに変換することができます。
今から指定する「キーワード」を使って、誰が聞いても思わず脱力してしまうような、面白いダジャレを1つ創作してください。

【キーワード】
{keyword}

ただの語呂合わせだけでなく、意外な状況設定やストーリーを少し加えると、より面白いダジャレになります。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ダジャレ生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)