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
def generate_video_idea():
    try:
        # AIへの指示（プロンプト）
        prompt = """
あなたは、TikTokのトレンドを熟知した、バズる動画を生み出すプロのコンテンツクリエイターです。
今、若者の間で流行しそうな、ダンス以外の面白いショート動画のネタを1つ提案してください。

提案する際は、誰でも簡単に真似できて、視聴者が思わず「いいね」や「シェア」をしたくなるような、具体的な企画内容にしてください。

【出力フォーマット】
ネタのタイトル：(キャッチーなタイトル)
内容：(動画の具体的な内容と流れを説明)
バズるポイント：(なぜこの動画が流行りそうかの簡単な解説)
おすすめBGM：(動画に合いそうなBGMの雰囲気や曲名)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ショート動画ネタ生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)