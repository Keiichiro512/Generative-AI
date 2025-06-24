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
def generate_story_starter():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、世界中の子供たちを虜にする物語を紡ぎ出す、有名な童話作家です。
「むかしむかし、あるところに…」から自然に続く、読者の想像力を掻き立てるような、不思議で魅力的な物語の冒頭を、たった1文だけ創作してください。

ありきたりな内容ではなく、少しだけ意外性のある、続きが気になるような一文をお願いします。

良い例：
・むかしむかし、あるところに、自分の影と喧嘩別れしてしまった、ひとりぼっちの王様がいました。
・むかしむかし、あるところに、空から降ってくる星を食べて生きている、小さなドラゴンが住んでいました。
・むかしむかし、あるところに、全ての嘘が本当になってしまう、不思議な泉が湧いていました。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"物語の冒頭生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)