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
def generate_lyrics_chorus():
    try:
        data = request.get_json()
        if not data or 'theme' not in data:
            return jsonify({'error': 'テーマが指定されていません。'}), 400

        theme = data['theme']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、数々のヒット曲を生み出してきた、プロの作詞家です。
今から指定する「テーマ」に沿って、聴く人の心に響く、J-POPの歌のサビ（一番盛り上がる部分）の歌詞を作成してください。

【テーマ】
{theme}

作成する歌詞は、情景が目に浮かぶような具体的な言葉を使い、共感を呼ぶような感情表現を盛り込んでください。
4行から8行程度の、覚えやすい構成でお願いします。
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"作詞中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)