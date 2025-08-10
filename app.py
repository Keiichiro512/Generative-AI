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
def generate_recipe():
    try:
        data = request.get_json()
        if not data or 'ingredients' not in data:
            return jsonify({'error': '食材が指定されていません。'}), 400

        ingredients = data['ingredients']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、世界中の料理に精通し、意外な食材の組み合わせで人々を驚かせるのが得意な、創造力豊かな料理人です。
今から指定する「主な食材」を使って、家庭でも作れる、少し珍しくて美味しい料理のレシピを1つ考案してください。

【主な食材】
{ingredients}

レシピは、以下のフォーマットで、誰でも作れるように分かりやすく記述してください。

【出力フォーマット】
料理名：(独創的で美味しそうな料理名)

材料（2人分）：
　・(材料リスト)

作り方：
　1. (手順1)
　2. (手順2)
　3. (手順3)

この料理のポイント：(美味しさの秘訣や、珍しい組み合わせの理由など)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"レシピ生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)