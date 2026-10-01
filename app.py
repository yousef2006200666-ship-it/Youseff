from flask import Flask, render_template_string, jsonify, request
import random
import json
import os

app = Flask(__name__)

# تحميل قاعدة البيانات الضخمة الخارجية إذا وجدت، أو استخدام بنك افتراضي
DB_FILE = "nursing_database.json"

def load_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # بنك افتراضي أولي لحين إنشاء الملف الشامل
        return {
            "nursing_info": [
                {"id": 1, "topic": "العلامات الحيوية - ضغط الدم", "info": "المعدل الطبيعي 120/80 مم زئبق."}
            ],
            "quiz_bank": [
                {
                    "id": 1,
                    "category": "أساسيات التمريض",
                    "question": "ما هو المعدل الطبيعي لنبض البالغين؟",
                    "options": ["40-60", "60-100", "100-120", "120-140"],
                    "answer": "60-100",
                    "explanation": "المعدل الطبيعي للنبض هو 60-100 نبضة/دقيقة."
                }
            ],
            "clinical_cases": [],
            "flashcards": []
        }

db_data = load_database()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تطبيق ممرض البيان - النسخة الموسعة</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 15px; }
        .card { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-bottom: 15px; text-align: center; }
        h1 { color: #2c3e50; font-size: 22px; margin-bottom: 5px; }
        .subtitle { color: #7f8c8d; font-size: 14px; margin-bottom: 15px; }
        .score-board { background: #2c3e50; color: #fff; padding: 10px; border-radius: 8px; margin-bottom: 15px; font-weight: bold; }
        .btn { display: block; width: 100%; padding: 12px; margin: 8px 0; background-color: #27ae60; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; font-weight: bold; }
        .btn-info { background-color: #16a085; }
        .btn-secondary { background-color: #2980b9; }
        .option-btn { background-color: #ecf0f1; color: #2c3e50; text-align: right; border: 1px solid #bdc3c7; }
        .explanation { background-color: #e8f8f5; border-right: 4px solid #1abc9c; padding: 10px; margin-top: 10px; text-align: right; border-radius: 4px; }
        .info-card { background-color: #eaf2f8; border-right: 4px solid #2980b9; padding: 12px; margin: 8px 0; text-align: right; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🏥 تطبيق ممرض البيان (قاعدة البيانات الضخمة) 🏥</h1>
        <div class="subtitle">جاهز لاستيعاب آلاف الأسئلة والمعلومات</div>
        
        <div class="score-board">
            🏆 النقاط (XP): <span id="xp">0</span> | المستوى: <span id="level">ممرض مبتدئ 🩺</span>
        </div>

        <button class="btn btn-info" onclick="loadNursingInfo()">💡 تصفح بنك المعلومات الضخم</button>
        <button class="btn" onclick="loadRandomQuiz()">🎲 اختبار من بنك الأسئلة الشامل</button>
    </div>

    <div id="content-area" class="card" style="display:none;"></div>

    <script>
        let xp = 0;
        function addXP(points) {
            xp += points;
            document.getElementById('xp').innerText = xp;
        }

        function loadNursingInfo() {
            fetch('/api/info')
                .then(res => res.json())
                .then(data => {
                    let area = document.getElementById('content-area');
                    area.style.display = 'block';
                    let html = `<h3>💡 بنك المعلومات (المجموع الكلي: ${data.length} معلومة)</h3>`;
                    // عرض عينة أو البحث لتجنب تعليق المتصفح إذا كانت العناصر بالآلاف
                    data.slice(0, 50).forEach(item => {
                        html += `<div class="info-card"><b>📌 ${item.topic}:</b><br>${item.info}</div>`;
                    });
                    if(data.length > 50) {
                        html += `<p style="color:#e67e22;">... ويوجد المزيد من المعلومات المسجلة في القاعدة.</p>`;
                    }
                    area.innerHTML = html;
                });
        }

        function loadRandomQuiz() {
            fetch('/api/quiz/random')
                .then(res => res.json())
                .then(data => {
                    let area = document.getElementById('content-area');
                    area.style.display = 'block';
                    let html = `<h3>${data.question}</h3>`;
                    data.options.forEach(opt => {
                        html += `<button class="btn option-btn" onclick="checkAnswer('${opt}', '${data.answer}', '${data.explanation}')">${opt}</button>`;
                    });
                    html += `<div id="ans-result"></div>`;
                    area.innerHTML = html;
                });
        }

        function checkAnswer(selected, correct, explanation) {
            let resDiv = document.getElementById('ans-result');
            if(selected === correct) {
                resDiv.innerHTML = `<div class="explanation" style="border-color:#27ae60;">✅ <b>إجابة صحيحة! (+10 XP)</b><br>${explanation}</div>`;
                addXP(10);
            } else {
                resDiv.innerHTML = `<div class="explanation" style="border-color:#e74c3c;">❌ <b>إجابة خاطئة.</b> الصحيحة هي: ${correct}<br>${explanation}</div>`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/info')
def get_info():
    data = load_database()
    return jsonify(data.get("nursing_info", []))

@app.route('/api/quiz/random')
def get_random_quiz():
    data = load_database()
    quiz_list = data.get("quiz_bank", [])
    quiz = random.choice(quiz_list)
    options = quiz['options'].copy()
    random.shuffle(options)
    return jsonify({
        "category": quiz.get('category', 'عام'),
        "question": quiz['question'],
        "options": options,
        "answer": quiz['answer'],
        "explanation": quiz['explanation']
    })

if __name__ == '__main__':
    app.run(debug=True)
