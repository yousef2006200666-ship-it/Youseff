from flask import Flask, render_template_string

app = Flask(__name__)

nursing_data = {
    "summary": [
        "الأساسيات: العلامات الحيوية (Vital Signs) - الضغط الطبيعي 120/80 mmHg، النبض 60-100/دقيقة.",
        "التقييم الصحي: جمع البيانات الذاتية (Subjective) والموضوعية (Objective).",
        "علم الأدوية: Paracetamol مسكن ومخفض حرارة، الجرعة القصوى للبالغين 4g يومياً."
    ],
    "process": [
        "1. Assessment (التقييم الشامل)",
        "2. Diagnosis (التشخيص التمريضي - NANDA)",
        "3. Planning (تحديد الأهداف والخطط)",
        "4. Implementation (التطبيق والتدخل السريري)",
        "5. Evaluation (التقييم النهائي لمدى النجاح)"
    ],
    "cases": [
        {
            "id": 1,
            "case": "مريض عمره 52 سنة، يعاني من ضيق تنفس شديد، تورم بالقدمين، وارتفاع الضغط 165/95.",
            "options": ["عجز القلب (Heart Failure)", "التهاب الزائدة الدودية", "قرحة المعدة"],
            "correct": 0,
            "action": "رفع رأس السرير (Fowler's Position)، إعطاء أكسجين، ومراقبة السوائل."
        },
        {
            "id": 2,
            "case": "طفل عمره 6 سنوات، يعاني من إسهال مستمر، جفاف شديد، وانخفاض مرونة الجلد (Skin Turgor).",
            "options": ["هبوط السكر", "جفاف ناتج عن التهاب الأمعاء", "تسمم دوائي"],
            "correct": 1,
            "action": "بدء تعويض السوائل وريدياً (IV Fluids) ومراقبة العلامات الحيوية."
        }
    ]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ممرض البيان - Al-Bayan Nurse</title>
    <style>
        body { font-family: system-ui, sans-serif; background-color: #f4f7f6; padding: 20px; text-align: center; color: #333; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; }
        h1 { color: #2c3e50; font-size: 22px; }
        button { background-color: #27ae60; color: white; border: none; padding: 12px 18px; border-radius: 8px; font-size: 15px; cursor: pointer; margin: 5px; width: 100%; max-width: 300px; }
        button:hover { background-color: #219150; }
        .info-box { text-align: right; background: #eef9f5; padding: 15px; border-radius: 8px; margin-top: 10px; line-height: 1.6; }
    </style>
</head>
<body>
    <h1>🏥 تطبيق ممرض البيان 🏥</h1>
    <p>جامعة البيان - المرحلة الأولى والثانية</p>

    <div class="card">
        <button onclick="getSummary()">📚 ملخصات المنهج</button><br>
        <button onclick="getProcess()">🩺 العملية التمريضية (ADPIE)</button><br>
        <button onclick="getQuiz()">🎮 اختبار حالة سريرية</button>
    </div>

    <div class="card" id="display-area">
        <h3>اختر خياراً من الأعلى للبدء!</h3>
    </div>

    <script>
        const data = {{ data | tojson }};

        function getSummary() {
            let html = "<h3>📚 ملخصات المنهج:</h3><div class='info-box'><ul>";
            data.summary.forEach(item => { html += `<li>${item}</li>`; });
            html += "</ul></div>";
            document.getElementById('display-area').innerHTML = html;
        }

        function getProcess() {
            let html = "<h3>🩺 العملية التمريضية:</h3><div class='info-box'><ol>";
            data.process.forEach(item => { html += `<li>${item}</li>`; });
            html += "</ol></div>";
            document.getElementById('display-area').innerHTML = html;
        }

        function getQuiz() {
            const caseItem = data.cases[Math.floor(Math.random() * data.cases.length)];
            let html = `<h3>📋 حالة سريرية:</h3><p class='info-box'>${caseItem.case}</p><h4>ما هو التشخيص الصحيح؟</h4>`;
            caseItem.options.forEach((opt, idx) => {
                html += `<button onclick="checkAns(${idx}, ${caseItem.correct}, '${caseItem.action}')">${opt}</button><br>`;
            });
            document.getElementById('display-area').innerHTML = html;
        }

        function checkAns(selected, correct, action) {
            if(selected === correct) {
                alert("إجابة صحيحة وممتازة! 🎉\\n\\nالخطة والتدخل التمريضي: " + action);
            } else {
                alert("إجابة خاطئة، حاول مرة أخرى وركز على الأعراض!");
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, data=nursing_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
