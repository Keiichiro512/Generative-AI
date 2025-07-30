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
def generate_event_plan():
    try:
        data = request.get_json()
        if not data or 'event_theme' not in data:
            return jsonify({'error': 'イベントのテーマが指定されていません。'}), 400

        event_theme = data['event_theme']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、数々のイベントを成功させてきた、創造力豊かなイベントプランナーです。
今から指定する「イベントのテーマ」に沿って、参加者が楽しめる、ユニークで具体的な企画案を1つ作成してください。

【イベントのテーマ】
{event_theme}

企画案は、幹事がそのまま使えるように、以下の要素を含んだ形式でお願いします。

【出力フォーマット】
イベント名案：(キャッチーなイベント名)
コンセプト：(イベントの目的や目指す雰囲気)
開催時期の目安：(テーマに合った季節や時期)
主なコンテンツ案：
　・(イベントの中心となる催し物を箇条書きで2〜3個)
参加を促す一言：(参加したくなるような、キャッチーな誘い文句)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"イベント企画案生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)