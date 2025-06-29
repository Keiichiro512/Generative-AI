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
def generate_workout_menu():
    try:
        data = request.get_json()
        if not data or 'part' not in data:
            return jsonify({'error': '部位が指定されていません。'}), 400

        part = data['part']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、経験豊富なパーソナルトレーナーです。
クライアントからリクエストのあった「鍛えたい体の部位」に合わせて、自宅でもできる効果的な筋トレメニューを1つ提案してください。

【鍛えたい部位】
{part}

提案には、具体的な「種目名」「セット数」「レップ数（回数）」、そしてそれぞれの種目の簡単な「ポイント」を含めてください。

【出力フォーマット】
今日のメニュー：【{part}の日】

■ 種目名：(ここに種目名)
・セット数：3セット
・レップ数：10〜12回
・ポイント：(ここに簡単なコツや注意点)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"筋トレメニュー生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)