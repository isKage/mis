import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from web_utils.kimi import kimi_chat


@csrf_exempt
def chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            message = data.get("message")
            if message:
                reply = kimi_chat(message)
                return JsonResponse({"reply": reply})
            else:
                return JsonResponse({"reply": "我没有收到消息！"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"reply": "无效的请求！"}, status=400)
    return JsonResponse({"reply": "请求方式错误！"}, status=400)
