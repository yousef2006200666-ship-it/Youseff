from flask import Flask, render_template_string, jsonify, request
import random

app = Flask(__name__)

# بنك الأسئلة الشامل لمنهج جامعة البيان (المرحلة الأولى والثانية)
QUIZ_BANK = [
    {
        "id": 1,
        "category": "أساسيات التمريض - العلامات الحيوية",
        "question": "ما هو المدى الطبيعي لمعدل نبضات القلب لدى البالغين في حالة الراحة؟",
        "options": ["40 - 60 نبضة/دقيقة", "60 - 100 نبضة/دقيقة", "100 - 120 نبضة/دقيقة", "120 - 140 نبضة/دقيقة"],
        "answer": "60 - 100 نبضة/دقيقة",
        "explanation": "المعدل الطبيعي للنبض لدى البالغين هو 60-100 نبضة/دقيقة (Normal Resting Heart Rate)."
    },
    {
        "id": 2,
        "category": "العملية التمريضية (ADPIE)",
        "question": "أي من الخطوات التالية تُعتبر الخطوة الأولى في العملية التمريضية؟",
        "options": ["التشخيص (Diagnosis)", "التقييم (Assessment)", "التخطيط (Planning)", "التنفيذ (Implementation)"],
        "answer": "التقييم (Assessment)",
        "explanation": "تبدأ العملية التمريضية دائماً بجمع البيانات الذاتية والموضوعية عبر التقييم (Assessment)."
    },
    {
        "id": 3,
        "category": "تمريض البالغين - الجهاز التنفسي",
        "question": "مريض يعاني من صعوبة بالغة في التنفس (Dyspnea)، ما هو الوضع السريري الأفضل لوضعه فيه؟",
        "options": ["وضع الاستلقاء (Supine)", "وضع فورلر العالي (High Fowler's)", "وضع تريندلينبرغ (Trendelenburg)", "وضع الخدج (Prone)"],
        "answer": "وضع فورلر العالي (High Fowler's)",
        "explanation": "وضع High Fowler's يساعد على تمدد الرئتين وتسهيل عملية التنفس."
    },
    {
        "id": 4,
        "category": "علم الأدوية (Pharmacology)",
        "question": "ما هو الدواء الأول المستخدم عادةً في إسعاف حالات انخفاض السكر الحاد مع فقدان الوعي؟",
        "options": ["Insulin", "IV Dextrose 50%", "Metformin", "Aspirin"],
        "answer": "IV Dextrose 50%",
        "explanation": "يتم إعطاء الجلوكوز الوريدي المركّز فوراً لرفع نسبة السكر في الدم وإيقاف الغيبوبة."
    },
    {
        "id": 5,
        "category": "أساسيات التمريض - إعطاء الحقن",
        "question": "ما هي الزاوية الصحيحة لإعطاء الحقن العضلية (Intramuscular - IM)؟",
        "options": ["15 درجة", "45 درجة", "90 درجة", "25 درجة"],
        "answer": "90 درجة",
        "explanation": "الحقن العضلية تُعطى بزاوية قائمة 90 درجة لضمان وصول الدواء للنسيج العضلي."
    }
]

# بنك الحالات السريرية (Clinical Cases)
CLINICAL_CASES = [
    {
        "id": 1,
        "title": "حالة مريض: ألم في الصدر (Chest Pain)",
        "scenario": "حضر مريض يبلغ من العمر 55 عاماً إلى الطوارئ يعاني من ألم ضاغط حاد في منتصف الصدر يمتد إلى الذراع الأيسر، مع تعرق بارد وضيق في التنفس.",
        "question": "بناءً على التقييم السريري أعلاه، ما هو التدخل التمريضي الأولي الفوري؟",
        "options": [
            "إعطاء مسكن ألم خفيف وترك المريض يرتاح",
            "وضع المريض على الأكسجين، قياس العلامات الحيوية، وإجراء تخطيط القلب (ECG) فوراً",
            "طلب قياس السكر في الدم فقط",
            "تشجيع المريض على المشي لتقليل التوتر"
        ],
        "answer": "وضع المريض على الأكسجين، قياس العلامات الحيوية، وإجراء تخطيط القلب (ECG) فوراً",
        "explanation": "الأعراض تشير إلى احتمال الذبحة الصدرية أو الجلطة القلبية (MI)، وتستدعي التخطيط والأكسجين الفوري."
    },
    {
        "id": 2,
        "title": "حالة مريض: ارتفاع حرارة وجفاف (Fever & Dehydration)",
        "scenario": "طفل يبلغ من العمر 4 سنوات يعاني من إسهال مستمر لمدة يومين، مع حرارة 39.2°C، وجفاف في اللسان وانخفاض في مرونة الجلد (Decreased Skin Turgor).",
        "question": "ما هو التشخيص التمريضي (Nursing Diagnosis) الأولوية لهذه الحالة؟",
        "options": [
            "نقص حجم السوائل (Fluid Volume Deficit)",
            "اضطراب نمط النوم (Disturbed Sleep Pattern)",
            "خطر التلوث (Risk for Infection)",
            "ضعف الحركة (Impaired Physical Mobility)"
        ],
        "answer": "نقص حجم السوائل (Fluid Volume Deficit)",
        "explanation": "أعراض جفاف اللسان وقلة مرونة الجلد مع الإسهال تؤكد نقص حجم السوائل كأولوية قصوى."
    }
]

# بطاقات المصطلحات التمريضية (Flashcards)
FLASHCARDS = [
    {"term": "NPO", "meaning": "Nil Per Os - لا شيء عن طريق الفم (Nulla Per Os)"},
    {"term": "PRN", "meaning": "Pro Re Nata - عند الحاجة"},
    {"term": "Stat", "meaning": "Statim - فوراً / على العجل"},
    {"term": "BP", "meaning": "Blood Pressure - ضغط الدم"},
    {"term": "HR", "meaning": "Heart Rate - معدل ضربات القلب"},
    {"term": "IM", "meaning": "Intramuscular - داخل العضلة"},
    {"term": "IV", "meaning": "Intravenous - داخل الوريد"}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تطبيق ممرض البيان</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 15px; }
        .card { background: #fff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-bottom: 15px; text-align: center; }
        h1 { color: #2c3e50; font-size: 22px; margin-bottom: 5px; }
        .subtitle { color: #7f8c8d; font-size: 14px; margin-bottom: 15px; }
        .score-board { background: #2c3e50; color: #fff; padding: 10px; border-radius: 8px; margin-bottom: 15px; font-weight: bold; }
        .btn { display: block; width: 100%; padding: 12px; margin: 8px 0; background-color: #27ae60; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; font-weight: bold; transition: 0.2s; }
        .btn:hover { opacity: 0.9; }
        .btn-secondary { background-color: #2980b9; }
        .btn-purple { background-color: #8e44ad; }
        .btn-orange { background-color: #e67e22; }
        .option-btn { background-color: #ecf0f1; color: #2c3e50; text-align: right; border: 1px solid #bdc3c7; }
        .explanation { background-color: #e8f8f5; border-right: 4px solid #1abc9c; padding: 10px; margin-top: 10px; text-align: right; border-radius: 4px; }
        .badge { background-color: #e74c3c; color: white; padding: 3px 8px; border-radius: 12px; font-size: 12px; float: left; }
        input { width: 90%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 6px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🏥 تطبيق ممرض البيان 🏥</h1>
        <div class="subtitle">جامعة البيان - المرحلة الأولى والثانية</div>
        
        <div class="score-board">
            🏆 النقاط (XP): <span id="xp">0</span> | المستوى: <span id="level">ممرض مبتدئ 🩺</span>
        </div>

        <button class="btn" onclick="loadRandomQuiz()">🎲 اختبار أسئلة متجددة</button>
        <button class="btn btn-secondary" onclick="loadClinicalCase()">🩺 حالات سريرية تفاعلية</button>
        <button class="btn btn-orange" onclick="loadDoseCalculator()">🧮 حاسبة الجرعات التمريضية</button>
        <button class="btn btn-purple" onclick="loadFlashcards()">📚 بطاقات المصطلحات السريعة</button>
    </div>

    <div id="content-area" class="card" style="display:none;"></div>

    <script>
        let xp = 0;

        function addXP(points) {
            xp += points;
            document.getElementById('xp').innerText = xp;
            if (xp >= 50) {
                document.getElementById('level').innerText = 'ممرض متمكن 💉';
            } if (xp >= 100) {
                document.getElementById('level').innerText = 'رئيس تمريض 🎓';
            }
        }

        function loadRandomQuiz() {
            fetch('/api/quiz/random')
                .then(res => res.json())
                .then(data => {
                    let area = document.getElementById('content-area');
                    area.style.display = 'block';
                    let html = `<span class="badge">${data.category}</span><h3>${data.question}</h3>`;
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
                resDiv.innerHTML = `<div class="explanation" style="border-color:#e74c3c;">❌ <b>إجابة خاطئة.</b> الإجابة الصحيحة هي: ${correct}<br>${explanation}</div>`;
            }
        }

        function loadClinicalCase() {
            fetch('/api/clinical/random')
                .then(res => res.json())
                .then(data => {
                    let area = document.getElementById('content-area');
                    area.style.display = 'block';
                    let html = `<h3>${data.title}</h3><p style="text-align:right; background:#f9f9f9; padding:10px; border-radius:6px;">${data.scenario}</p><h4>${data.question}</h4>`;
                    data.options.forEach(opt => {
                        html += `<button class="btn option-btn" onclick="checkAnswer('${opt}', '${data.answer}', '${data.explanation}')">${opt}</button>`;
                    });
                    html += `<div id="ans-result"></div>`;
                    area.innerHTML = html;
                });
        }

        function loadDoseCalculator() {
            let area = document.getElementById('content-area');
            area.style.display = 'block';
            area.innerHTML = `
                <h3>🧮 حاسبة قطرات المغذي (IV Drip Rate)</h3>
                <p>احسب عدد القطرات/دقيقة لربط المغذي للمريض:</p>
                <input type="number" id="volume" placeholder="حجم المغذي (مل)">
                <input type="number" id="hours" placeholder="عدد الساعات">
                <input type="number" id="factor" placeholder="عامل القطرة (عادة 15 أو 20)">
                <button class="btn" onclick="calculateDrip()">احسب الجرعة</button>
                <div id="calc-result"></div>
            `;
        }

        function calculateDrip() {
            let v = parseFloat(document.getElementById('volume').value);
            let h = parseFloat(document.getElementById('hours').value);
            let f = parseFloat(document.getElementById('factor').value);
            if (v && h && f) {
                let rate = Math.round((v * f) / (h * 60));
                document.getElementById('calc-result').innerHTML = `<div class="explanation">💧 معدل التقطير المطلوب: <b>${rate} قطرة/دقيقة</b></div>`;
            } else {
                alert('يرجى ملء جميع الحقول بصورة صحيحة!');
            }
        }

        function loadFlashcards() {
            fetch('/api/flashcards')
                .then(res => res.json())
                .then(cards => {
                    let area = document.getElementById('content-area');
                    area.style.display = 'block';
                    let html = `<h3>📚 بطاقات المصطلحات السريعة</h3>`;
                    cards.forEach(c => {
                        html += `<div style="background:#edf2f7; padding:10px; margin:5px 0; border-radius:6px; text-align:right;"><b>${c.term}:</b> ${c.meaning}</div>`;
                    });
                    area.innerHTML = html;
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/quiz/random')
def get_random_quiz():
    quiz = random.choice(QUIZ_BANK)
    options = quiz['options'].copy()
    random.shuffle(options)
    return jsonify({
        "category": quiz['category'],
        "question": quiz['question'],
        "options": options,
        "answer": quiz['answer'],
        "explanation": quiz['explanation']
    })

@app.route('/api/clinical/random')
def get_random_clinical():
    case = random.choice(CLINICAL_CASES)
    options = case['options'].copy()
    random.shuffle(options)
    return jsonify({
        "title": case['title'],
        "scenario": case['scenario'],
        "question": case['question'],
        "options": options,
        "answer": case['answer'],
        "explanation": case['explanation']
    })

@app.route('/api/flashcards')
def get_flashcards():
    return jsonify(FLASHCARDS)

if __name__ == '__main__':
    app.run(debug=True)
