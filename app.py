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
def generate_debate_topic():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、世界中のあらゆる対立を知り尽くした、議論の専門家です。
誰もが一度は考えたことがあり、どちらの立場にも正義があるような、白熱した議論を呼ぶ「究極の二択」のお題を1つ生成してください。

お題は、「きのこの山 vs たけのこの里」のように、食べ物やライフスタイルに関する、身近で面白いテーマが望ましいです。
政治や宗教など、深刻すぎるテーマは避けてください。

【出力フォーマット】
(究極の二択のお題、例：犬派 vs 猫派)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ディベートお題生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)