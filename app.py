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
def generate_brainstorm_topic():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、数々のイノベーションを生み出してきた、優秀なファシリテーターです。
チームの創造性を最大限に引き出し、活発な議論を促すような、面白いブレインストーミングのお題を1つ提案してください。

お題は、「もし〜だったら？」や「〜を解決するには？」といった形式で、具体的すぎず、参加者が自由にアイデアを広げられるようなものが望ましいです。

良い例：
・もし、月にもう一つオフィスを作れるとしたら、どんなチームがどんな仕事をすべきか？
・10年後の「当たり前」になる新しい休日の過ごし方を考えてください。
・「退屈」という感情を完全になくすサービスを考えてください。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ブレストお題生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)