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
def generate_character_profile():
    try:
        data = request.get_json()
        if not data or 'features' not in data:
            return jsonify({'error': 'キャラクターの特徴が指定されていません。'}), 400

        features = data['features']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、世界的な人気を誇るゲームのキャラクターデザイナーです。
今から指定する「特徴」を持つ、魅力的でユニークなキャラクターの設定を創作してください。

【キャラクターの特徴】
{features}

設定は、プレイヤーや読者がキャラクターに愛着を持てるように、以下の要素を具体的に記述してください。

【出力フォーマット】
名前：(キャラクターの名前)
年齢：(キャラクターの年齢)
性格：(キャラクターの性格を簡潔に)
外見：(髪型、服装、持ち物などの特徴)
特技：(キャラクターが得意なこと)
悩み・弱点：(キャラクターが抱える悩みや弱点)
決め台詞：「(キャラクターが言いそうなセリフ)」
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"キャラクター設定生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)