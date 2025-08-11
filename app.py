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
def generate_domain_names():
    try:
        data = request.get_json()
        if not data or 'service_name' not in data:
            return jsonify({'error': 'サービス名が指定されていません。'}), 400

        service_name = data['service_name']

        # AIへの指示（プロンプト）
        prompt = f"""
あなたは、スタートアップのブランディングとドメイン名の選定を専門とする、経験豊富なマーケターです。
今から指定する「サービス名」のコンセプトに合った、覚えやすく、タイプしやすく、利用可能（空いている）可能性が高いドメイン名を5つ提案してください。

【サービス名】
{service_name}

提案するドメイン名は、.com / .jp / .net / .io / .app などの人気のトップレベルドメインを使い、クリエイティブな単語の組み合わせや、短縮形なども含めてください。
それぞれのドメイン名に、なぜそれが良いかの簡単な「選定理由」も添えてください。

【出力フォーマット】
1. (ドメイン名1)
   理由：(なぜこのドメイン名が良いかの簡単な説明)
2. (ドメイン名2)
   理由：(なぜこのドメイン名が良いかの簡単な説明)
3. (ドメイン名3)
   理由：(なぜこのドメイン名が良いかの簡単な説明)
4. (ドメイン名4)
   理由：(なぜこのドメイン名が良いかの簡単な説明)
5. (ドメイン名5)
   理由：(なぜこのドメイン名が良いかの簡単な説明)
"""
        
        response = model.generate_content(prompt)
        
        formatted_response = response.text.strip()

        return jsonify({'result': formatted_response})

    except Exception as e:
        print(f"ドメイン名生成中にエラー: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)