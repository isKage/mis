# -*- coding: utf-8 -*-
from openai import OpenAI
from django.conf import settings

import os
import django

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
             "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。"
                        "你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。"
                        "现在你作为一个文章总结助手，删除读取文章内容，尤其是markdown格式的内容，并返回对内容的简要总结。"},
            {"role": "user", "content": asked}
        ],
        temperature=0.3,
    )

    return completion.choices[0].message.content


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
