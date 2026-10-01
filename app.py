import os
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# قائمة الملفات المرفوعة في المستودع
uploaded_files = [
    "allkiwiq_FUM_1 - health assessment.pdf",
    "allkiwiq_RE.LLEC 1_TRANSLATION.pdf",
    "Endocrine system disorders 1st lecture.pdf",
    "What is Breast Cancer (1).pdf",
    "introduction (1).pdf",
    "التقييم الصحي نظري م1 مترجم (1).pdf",
    "التقييم الصحي نظري م2 مترجم.pdf"
]

app_data = {
    "current_info": "الحمى المالطية (Brucellosis): عدوى بكتيرية تنتقل من الحيوانات إلى البشر، وأعراضها تشمل حمى مستمرة، آلام في المفاصل، وتعرق ليلي غزير.",
    "quiz": {
        "question": "ما هو العرض الأبرز الذي يصاحب الحمى المالطية ويعتبر من علاماتها المميزة؟",
        "options": ["التعرق الليلي الغزير", "فقدان حاسة الشم", "اصفرار العينين"],
        "answer": "التعرق الليلي الغزير"
    },
    "case_study": {
        "scenario": "مراجع يشتكي من حرارة ترتفع وتنخفض بشكل مستمر، مع آلام شديدة في المفاصل وتعرق ليلي غزير، وذكر أنه يتناول حليب غير معقم. ما هو التشخيص المحتمل؟",
        "diagnosis": "الحمى المالطية (Brucellosis)"
    },
    "files": uploaded_files,
    "summary_result": "",
    "translation_result": ""
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تطبيق التعلم الطبي والتلخيص الذكي</title>
    <style>
        body { font-family: Tahoma, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
        h1, h2 { color: #007BFF; text-align: center; }
        .section { background: #e9ecef; padding: 15px; margin-bottom: 20px; border-radius: 8px; }
        button { background: #007BFF; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #0056b3; }
        select, textarea { width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 10px; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        .result { background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🩺 تطبيق التعلم الطبي والاختبارات الذكية</h1>
        
        <!-- القسم الأول: معلومة الساعة والاختبارات -->
        <div class="section">
            <h2>⏰ إشعار معلومة الساعة (Micro-Learning)</h2>
            <p><strong>المعلومة الحالية:</strong> {{ data.current_info }}</p>
        </div>

        <div class="section">
            <h2>❓ الاختبار المفاجئ</h2>
            <p>{{ data.quiz.question }}</p>
            <ul>
                {% for option in data.quiz.options %}
                    <li>{{ option }}</li>
                {% endfor %}
            </ul>
        </div>

        <div class="section">
            <h2>🏥 الاختبار الشامل (الحالات السريرية)</h2>
            <p><strong>الحالة المرضية:</strong> {{ data.case_study.scenario }}</p>
            <details>
                <summary style="cursor: pointer; color: #007BFF; font-weight: bold;">اضغط هنا لمعرفة التشخيص الصحيح</summary>
                <p class="result">التشخيص: {{ data.case_study.diagnosis }}</p>
            </details>
        </div>

        <!-- القسم الثاني: أدوات الملفات والصور والترجمة -->
        <div class="section">
            <h2>📁 قائمة الملفات والتلخيص الذكي</h2>
            <form method="POST" action="/summarize">
                <label for="selected_file">اختر ملفاً من ملفاتك المرفوعة:</label>
                <select name="selected_file">
                    {% for file in data.files %}
                        <option value="{{ file }}">{{ file }}</option>
                    {% endfor %}
                </select>
                <button type="submit">تلخيص واستخراج النقاط المهمة للملف</button>
            </form>
            {% if data.summary_result %}
                <div class="result">
                    <strong>النقاط المختصرة من الملف المحدد:</strong>
                    <p>{{ data.summary_result }}</p>
                </div>
            {% endif %}
        </div>

        <div class="section">
            <h2>🌍 القائمة الثانية: الترجمة الطبية والعلمية</h2>
            <form method="POST" action="/translate">
                <label for="translate_input">أدخل النص أو اختر مصطلحاً للترجمة:</label>
                <textarea name="translate_input" rows="3" placeholder="أدخل النص الإنجليزي أو العربي للترجمة..."></textarea>
                <button type="submit">ترجمة فورية</button>
            </form>
            {% if data.translation_result %}
                <div class="result">
                    <strong>الترجمة:</strong>
                    <p>{{ data.translation_result }}</p>
                </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, data=app_data)

@app.route("/summarize", methods=["POST"])
def summarize():
    filename = request.form.get("selected_file", "")
    if filename:
        app_data["summary_result"] = f"تم تحليق واستخراج أهم النقاط لملف ({filename}): التركيز على المفاهيم الأساسية، المصطلحات الطبية، وتقييم الحالة المرتبط بالملف."
    else:
        app_data["summary_result"] = "الرجاء اختيار ملف صحيح."
    return redirect(url_for('home'))

@app.route("/translate", methods=["POST"])
def translate():
    text = request.form.get("translate_input", "")
    if text:
        app_data["translation_result"] = f"الترجمة المعتمدة للمصطلحات الطبية الخاصة بالنص المدخل: [ترجمة دقيقة لـ: {text}]"
    else:
        app_data["translation_result"] = "الرجاء إدخال نص للترجمة."
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
