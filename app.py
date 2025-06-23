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
def generate_special_move():
    try:
        # AIへの指示（プロンプト）を必殺技用に変更
        prompt = """
あなたは、世界中のRPGや漫画に登場する、最高にかっこいい技を名付ける「詠唱師」です。
「炎属性」の剣技、魔法、または体術の必殺技の名前を、厨二病っぽく、かつ独創的で力強い響きのものを1つだけ生成してください。

技の名前だけでなく、どのような技かの簡単な説明（例：灼熱の炎を纏った剣で敵を十文字に切り裂く）も添えてください。

フォーマットは必ず以下のようにしてください。

【技名】：(ここに技名)
【説明】：(ここに技の説明)

例：
【技名】：インフェルノ・カタストロフィ
【説明】：すべてを焼き尽くす煉獄の炎を召喚し、敵一体に絶大なダメージを与える究極魔法。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"必殺技生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)