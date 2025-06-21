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
def generate_menu():
    try:
        data = request.get_json()
        if not data or 'ingredients' not in data:
            return jsonify({'error': '材料が指定されていません。'}), 400

        ingredients = data['ingredients']

        # AIへの指示を、料理名と簡単な手順を尋ねるように変更
        prompt = f"""
以下の冷蔵庫の中にある食材を使って作れる、美味しくて現実的な家庭料理のメニューを1つだけ提案してください。
メニュー名だけでなく、作るための簡単な手順も3ステップ程度で教えてください。

【冷蔵庫の中身】
{ingredients}

【出力フォーマット】
料理名：(ここに料理名)

簡単な作り方：
1. (手順1)
2. (手順2)
3. (手順3)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"献立生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)