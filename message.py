import json
from azure_prompt import azure1_system_prompt, azure2_system_prompt

def coze_image_and_question(question, image_id): # 见coze开发文档-对话-发起对话
    content = [{"type": "text","text": question},
        {"type": "image","file_id": image_id}]

    message = [{"role": "user",
                "content_type": "object_string",
                "content": json.dumps(content),
                }]
    return message

def coze_url_and_question(question,image_url):
    content = [{"type": "text", "text": question},
               {"type": "file", "file_url": image_url}]

    message = [{"role": "user",
                "content_type": "object_string",
                "content": json.dumps(content),
                }]
    return message


def coze_single_message(content, role="user", content_type="text"):
    message = [{"role": role,
                "content": content,
                "content_type": content_type
                }]
    return message


def coze_reflection_bot(question, solution, extra_info="", role="user", content_type="text"):
    content = f"题目：{question}\n\n不完全正确的解题思路：{solution}"
    if extra_info !="":
        content += f"\n\n补充信息：{extra_info}"
    message = [{"role": role,
                "content": content,
                "content_type": content_type
                }]
    return message


def azure1_message(question,solution):
    message = [
        {
            "role":"system",
            "content":[{
                "type":"text",
                "text": azure1_system_prompt

            }]
        },
        {
            "role":"user",
            "content":[{
                "type":"text",
                "text":f"题目：{question}\n\n解题思路：{solution}"
            }]
        }
    ]
    return message


def azure2_message(question,solution,answer):
    message = [
        {
            "role":"system",
            "content":[{
                "type":"text",
                "text": azure2_system_prompt
            }]
        },
        {
            "role":"user",
            "content":[{
                "type":"text",
                "text":f"题目：{question}\n\n解答过程:{solution}\n\n解析：{answer}"
            }]
        }
    ]
    return message
