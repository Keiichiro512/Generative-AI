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
def generate_compliment():
    try:
        # AIへの指示（プロンプト）を褒め言葉用に変更
        prompt = """
あなたは、人の素敵なところを見つけるのが得意な、心優しいカウンセラーです。
相手が本当に言われて嬉しい、心に響くような褒め言葉を1つだけ生成してください。

表面的なこと（例：「すごい！」「かわいいね」など）ではなく、相手の努力や内面、存在そのものを肯定するような、具体的で温かい言葉でお願いします。

以下に良い例をいくつか示します。このような方向性でお願いします。

例1：いつも周りをよく見て、細やかな気配りができるところ、本当に尊敬しています。
例2：〇〇さんがいるだけで、その場の雰囲気がパッと明るくなりますね。
例3：難しいことにも諦めずに挑戦し続けるその姿勢に、いつも元気をもらっています。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"褒め言葉生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)