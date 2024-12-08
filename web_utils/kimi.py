# -*- coding: utf-8 -*-
import os
import django
from openai import OpenAI
from django.conf import settings
from django.http import HttpRequest
from web.models import Preference
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mis.settings")  # 替换 your_project 为你的项目名称
django.setup()  # 初始化 Django 环境

client = OpenAI(
    api_key=settings.KIMI_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)


def conclusion(content):
    asked = "情对下面的内容进行简要的总结" + content
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是MIS网站助手"
                        "现在你作为一个文章总结助手，删除读取文章内容，尤其是markdown格式的内容，并返回对内容的简要总结。"},
            {"role": "user", "content": asked}
        ],
        temperature=0.3,
    )

    return completion.choices[0].message.content


def kimi_chat(content):
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是MIS网站助手。"
                        "现在你作为这个网站的AI助手，能力是回答用户发出的提问，同时能够与用户正常沟通。"
                        "网站的功能是为客户提供一个学习、交流的平台，平台上有许多公开的学习资源，用户可以自己创建话题、小组，并与其他用户一同讨论。"
             },
            {"role": "user", "content": content}
        ],
        temperature=0.3,
    )

    return completion.choices[0].message.content


def partner(user_name):
    preferences = Preference.objects.all()

    preference_str = ""
    for preference in preferences:
        # 构建每个用户的偏好信息，以“人名：字段1，字段2”的格式拼接
        preference_str += f"{preference.userid.username}: " \
                          f"学号{preference.student_id}，" \
                          f"专业{preference.major}，" \
                          f"宿舍区{preference.dorm_area}，" \
                          f"偏好建筑{preference.preferred_building}，" \
                          f"偏好学科{preference.preferred_subject}，" \
                          f"偏好话题{preference.preferred_topic}，" \
                          f"附加偏好{preference.additional_preferences}；"

    # 在生成的字符串中加入当前用户的名字和所有用户的偏好信息
    content = f"直接给出相似性最高的3人，简短分析（不超过200字），当前用户是: {user_name}，所有用户是: {preference_str}。不包含自己{user_name}"

    # 调用 AI 完成模型获取推荐结果
    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {"role": "system",
             "content": "你是MIS网站助手。现在你作为这个网站的AI助手，要求是根据我提供的一组数据，按照相似性为当前用户推荐前三名相似的用户名"},
            {"role": "user",
             "content": content}
        ],
        temperature=0.3,
    )

    ans = completion.choices[0].message.content
    return ans


if __name__ == '__main__':
    content = ("# 数学分析自习搭子## 目标- 共同学习数学分析，夯实基础。"
               "- 解决疑难问题，相互讨论。- 提高学习效率，培养逻辑思维。"
               "---## 学习计划### 第一阶段：基础复习- **复习内容**："
               "函数、极限与连续- **时间安排**：1周- **具体任务**：- "
               "梳理课本概念和定理（每天2小时）。- 完成课后基础习题（每天至少5题）。"
               "### 第二阶段：重点突- **重点内容**：- 导数与微分- 微分中值定理及其应用-"
               " **时间安排**：2周- **具体任务**：- 结合习题掌握核心定理的证明过程。- "
               "熟练解决课本例题并尝试拓展题目。### 第三阶段：专题研讨- **专题方向**：- "
               "无穷级数收敛性判别方法- 函数列一致收敛- **时间安排**：2周- **具体任务**："
               "- 各自准备专题内容，进行讨论与分享。- 针对性解决疑难问题。---"
               "## 规则1. **按时学习**：每次约定时间后，务必准时到场。2. **独立思考**："
               "每人需提前完成自习任务，带着问题来讨论。3. **分工合作**：共同完成总结笔记，"
               "轮流主讲不同内容。---## 联系方式- 微信群：xx- 学习资料共享：xx云盘链接---"
               "## 温馨提示- 勤学多思，重在坚持。- 遇到困难不要害怕，搭子们是最坚实的后盾。"
               "- 让我们一起进步，努力搞定数学分析！")
    conclusions = conclusion(content=content)
    print(conclusions)
    # preferences = Preference.objects.all()
    # print(preferences)
