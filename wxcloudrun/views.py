@csrf_exempt
def upload_analyze(request):
    # 逻辑：不管是文字还是图片，最终都变成一段 Prompt 给 Gemini
    user_input = ""
    img_data = None

    if request.method == 'POST':
        # 1. 检查是不是文字输入
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            user_input = data.get('text', '')
        
        # 2. 检查是不是图片上传
        if request.FILES.get('file'):
            img_file = request.FILES['file']
            img_data = img_file.read()
            user_input = "分析这张图里的食物"

        # 3. 呼叫 Gemini
        prompt = f"你是毒舌减肥精算师'斤斤'。用户说/发了：{user_input}。请给出热量估算和吐槽。返回JSON。"
        
        if img_data:
            response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': img_data}])
        else:
            response = model.generate_content(prompt)
            
        return JsonResponse(json.loads(response.text))
