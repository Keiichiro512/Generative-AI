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
def analyze_sentiment():
    try:
        data = request.get_json()
        if not data or 'text_to_analyze' not in data:
            return jsonify({'error': '分析対象の文章が指定されていません。'}), 400

        text_to_analyze = data['text_to_analyze']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、文章から感情を読み取ることを専門とする、高度なAIアシスタントです。
今から入力される文章を分析し、その文章が全体として「ポジティブ」「ネガティブ」「ニュートラル（中立）」のどれに分類されるかを判定してください。

【分析対象の文章】
{text_to_analyze}

判定結果に加えて、なぜそのように判断したのか、簡単な「分析の根拠」も示してください。

【出力フォーマット】
判定結果：(ポジティブ/ネガティブ/ニュートラルのいずれか)
分析の根拠：(なぜそのように判断したかを簡潔に説明)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"感情分析中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)