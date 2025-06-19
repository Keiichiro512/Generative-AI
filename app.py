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
def generate_tweet_idea():
    try:
        # AIへの指示（プロンプト）を「ツイートアイデア」用に変更
        prompt = """
あなたは人気のテック系インフルエンサーです。
「プログラミング学習」をテーマにした、多くの人に「いいね」や「リポスト」をしてもらえそうな、面白くて役立つツイートのアイデアを1つだけ生成してください。

フォーマットは必ず以下のようにしてください。

【ツイート案】
(ここに140字程度のツイート本文)

【ハッシュタグ案】
#プログラミング学習 #駆け出しエンジニアと繋がりたい
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ツイートアイデア生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)