import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # 这一行就是刚才漏掉的“介绍信”

# 配置你的 Gemini API Key
genai.configure(api_key="AIzaSyDvrYGOh0ZySu293XkJoga4mb4vaXoFIGE")
model = genai.GenerativeModel('gemini-1.5-flash')

@csrf_exempt
def upload_analyze(request):
    """
    让斤斤听懂文字、看懂图片的逻辑
    """
    if request.method == 'POST':
        user_input = ""
        img_data = None

        try:
            # 1. 判断是文字输入还是图片上传
            if request.content_type == 'application/json':
                body = json.loads(request.body)
                user_input = body.get('text', '')
            elif request.FILES.get('file'):
                img_file = request.FILES['file']
                img_data = img_file.read()
                user_input = "分析这张图里的食物"

            if not user_input and not img_data:
                return JsonResponse({"jinjin_comment": "你啥都不给，斤斤怎么算？", "calories": 0})

            # 2. 呼叫 Gemini
            prompt = f"你是毒舌减肥精算师'斤斤'。用户输入：{user_input}。请给出食物名、热量估算和吐槽。严格返回JSON: {{\"food_name\": \"...\", \"calories\": 0, \"jinjin_comment\": \"...\"}}"
            
            if img_data:
                response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': img_data}])
            else:
                response = model.generate_content(prompt)
            
            # 3. 处理并返回数据
            clean_text = response.text.replace('```json', '').replace('```', '').strip()
            ai_data = json.loads(clean_text)
            
            return JsonResponse({
                "jinjin_comment": ai_data.get('jinjin_comment'),
                "new_balance": 1500 - ai_data.get('calories', 0),
                "food_name": ai_data.get('food_name')
            })

        except Exception as e:
            return JsonResponse({"jinjin_comment": f"斤斤脑子乱了：{str(e)}", "new_balance": 1500})
            
    return JsonResponse({"error": "请使用 POST 请求"})
