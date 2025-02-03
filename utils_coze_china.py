import requests
import os
coze_token_china = os.getenv("COZE_TOKEN_CHINA")


# 创建一个会话，并获取会话id，后续所有对话都会加到会话里
def create_conversation_cn():
    url = "https://api.coze.cn/v1/conversation/create"  # 创建会话的请求地址
    headers = {
        "Authorization": f"Bearer {coze_token_china}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        # print("请求成功！")
        # print(response.json()) # 完整回复
        # created_at = response.json()["data"]["created_at"]
        conversation_id = response.json()["data"]["id"]
        return conversation_id
    else:
        return f"创建会话失败: {response.status_code}\n回复内容：{response.text}"


# 创建一个对话，并发送消息
def send_message_cn(conversation_id, bot_id, message):
    url="https://api.coze.cn/v3/chat"  # 创建对话请求地址-见文档“发起对话”
    params = {
        'conversation_id': conversation_id
    }
    headers = {
        "Authorization": f"Bearer {coze_token_china}",
        "Content-Type": "application/json"
    }
    payload = {
        "bot_id": bot_id,
        "user_id": "770515",  # 需要改成自己对应的user_id
        "stream": False,  # 是否流式输出
        "auto_save_history": True,
        "additional_messages": message
    }
    response = requests.post(url, headers=headers, params=params, json=payload)
    if response.json()["msg"] != "":
        print(response.json())
    else:
        chat_id = response.json()["data"]["id"]
        return chat_id

# 查看对话状态是in_progress还是completed
def get_chat_status_cn(conversation_id, chat_id):
    url = 'https://api.coze.cn/v3/chat/retrieve'  # 查看对话状态是否完成-见文档“查看对话详情”
    params = {
        'chat_id': chat_id,
        'conversation_id': conversation_id
    }
    headers = {
        'Authorization': f'Bearer {coze_token_china}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        # print(response.json())
        status = response.json()['data']['status']
        return status
    else:
        print(f"查看对话状态失败: {response.status_code}\n回复内容：{response.text}")

# 当对话状态为completed时，可获取回复消息
def get_reply_cn(conversation_id, chat_id):
    url = 'https://api.coze.cn/v3/chat/message/list'  # 获取回复请求地址-见文档“查看对话消息详情”
    params = {
        'chat_id': chat_id,
        'conversation_id': conversation_id
    }
    headers = {
        'Authorization': f'Bearer {coze_token_china}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, params=params)

    if response.status_code == 200:
        # print(response.json())
        answer_content = None
        for message in response.json()['data']:
            if message['type'] == 'answer':
                answer_content = message['content']
                break
        return answer_content
    else:
        print(f"获取消息失败: {response.status_code}\n回复内容：{response.text}")

# 一次对话，发送一次消息，获得一次回复。前面这一大堆都是为one_chat做准备的
def one_chat_cn(conversation_id, bot_id, message):
    chat_id = send_message_cn(conversation_id=conversation_id,
                           bot_id=bot_id,
                           message=message)
    # print(f"chat_id:{chat_id}")
    while True:
        status = get_chat_status_cn(conversation_id=conversation_id, chat_id=chat_id)
        # print(status)
        if status == "completed":
            break
        # time.sleep(0.1)
    answer_content = get_reply_cn(conversation_id=conversation_id, chat_id=chat_id)
    return answer_content

