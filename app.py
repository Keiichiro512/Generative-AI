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
def generate_trip_plan():
    try:
        data = request.get_json()
        if not data or 'trip_request' not in data:
            return jsonify({'error': '旅行の要望が指定されていません。'}), 400

        trip_request = data['trip_request']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、日本中の観光地に詳しい、経験豊富な旅行プランナーです。
今から指定する「旅行の要望」に沿って、読んだ人がワクワクするような、具体的で実現可能な旅行プランを1つ作成してください。

【旅行の要望】
{trip_request}

プランは、タイムスケジュールが分かるように、以下の要素を含んだ形式でお願いします。

【出力フォーマット】
旅行のテーマ：(プランにキャッチーな名前を付ける)

【1日目】
午前：(具体的なアクティビティや場所)
昼食：(おすすめの食事やレストラン)
午後：(具体的なアクティビティや場所)
宿泊：(おすすめの宿泊施設エリアや種類)

【2日目】
午前：(具体的なアクティビティや場所)
昼食：(おすすめの食事やレストラン)
午後：(具体的なアクティビティや場所)

プランのポイント：(この旅行プランの魅力や楽しむコツ)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"旅行プラン生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)