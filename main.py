import streamlit as st
from utils_coze import one_chat,upload_image,create_conversation
from utils_coze_china import one_chat_cn,create_conversation_cn
from message import coze_image_and_question, coze_single_message, coze_reflection_bot, azure1_message, azure2_message
from utils_azure import azure_generate_json
# 创建会话
conv = create_conversation()
conv_cn = create_conversation_cn()

# 一些子固定变量
agent1_id = "7414836197388386309"
agent2_gpt = "7415515938361311237"
agent2_db = "7422120337678532658"
doubao_agent3 = "7422120337678581810"

# 管理会话状态和变量
if "input_question" not in st.session_state:
    st.session_state["input_question"] = ""
if "image" not in st.session_state:
    st.session_state["image"] = None
if "file_id" not in st.session_state:  #
    st.session_state["file_id"] = None  #
if "whole_question" not in st.session_state:
    st.session_state["whole_question"] = ""  # 完整题干
if "extra_info" not in st.session_state:
    st.session_state["extra_info"] = ""  # 解题思路补充信息

if "solution" not in st.session_state:
    st.session_state["solution"] = ""
if "solution_replica" not in st.session_state:
    st.session_state["solution_replica"] = ""

if "reflection" not in st.session_state:
    st.session_state["reflection"] = ""

if "answer" not in st.session_state:
    st.session_state["answer"] = ""  # 本项目中answer指解析
if "answer_suggestion" not in st.session_state:
    st.session_state["answer_suggestion"] = ""  # answer_suggestion指对解析的修改建议

# 标题
st.title("高中生物选择题解析生成")

# 题目
st.header("题目")
input_question = st.text_area("请输入选择题", st.session_state["input_question"])
if input_question:
    st.session_state["input_question"] = input_question
uploaded_file = st.file_uploader("题目配图(如有)", type=["jpg", "jpeg", "png"]) # 上传图片
if uploaded_file:
    st.session_state["image"] = uploaded_file
    # 展示图片
    st.image(st.session_state["image"], caption='上传的图像', width=300)

submit0 = st.button("生成image_id↓")
if st.session_state["image"] and submit0:
    file_id = upload_image(st.session_state["image"])  #
    st.session_state["file_id"] = file_id  #
st.write(st.session_state["file_id"])


# 用agent1生成图片阐释
submit1 = st.button("完整题干↓")
if submit1 and st.session_state["input_question"]:
    if st.session_state["file_id"] is not None:
        with st.spinner(("AI正在读图中...")):
            to_agent1_message = coze_image_and_question(question=st.session_state["input_question"],
                                                        image_id=st.session_state["file_id"])
            image_explanation = one_chat(conversation_id=conv,
                                         bot_id=agent1_id,
                                         message=to_agent1_message)
            st.session_state["whole_question"] = "题目："+st.session_state["input_question"]+"\n\n配图阐释："+image_explanation
        st.success("已生成")
    else:
        st.session_state["whole_question"] = "题目：" + st.session_state["input_question"]
st.write(st.session_state["whole_question"])



# 解题思路
st.header("解题思路")

tab_db,tab_gpt = st.tabs(["豆包function call","chatgpt-4o",])

with tab_db:
   submit_solve_db = st.button("豆包生成解题思路↓")
   if submit_solve_db and st.session_state["whole_question"] != "":
       with st.spinner(("AI正在做题中...")):
           to_db_message = coze_single_message(content=st.session_state["whole_question"])
           solution = one_chat_cn(conversation_id=conv_cn,
                               bot_id=agent2_db,
                               message=to_db_message)
       st.success("已生成")
       st.session_state["solution"] = solution
   st.write(st.session_state["solution"])


with tab_gpt:
    submit_solve_gpt = st.button("chatgpt4o生成解题思路↓")
    if submit_solve_gpt and st.session_state["whole_question"]!="":
        with st.spinner(("AI正在做题中...")):
            to_gpt_message = coze_single_message(content=st.session_state["whole_question"])
            solution = one_chat(conversation_id=conv,
                                bot_id=agent2_gpt,
                                message=to_gpt_message)
        st.success("已生成")
        st.session_state["solution"] = solution
    st.write(st.session_state["solution"])


submit2_2 = st.button("解题思路纠正↓")
extra_info = st.text_area("如需纠错，将补充信息写在这里", st.session_state["extra_info"])
if submit2_2:
    with st.spinner(("解题思路迭代ing...")):
        to_agent3_message = coze_reflection_bot(question=st.session_state["whole_question"],
                                                solution=st.session_state["solution"],
                                                extra_info=st.session_state["extra_info"])
        ## doubao_agent3
        reflection = one_chat_cn(conversation_id=conv_cn,
                              bot_id=doubao_agent3,
                              message=to_agent3_message)

        st.session_state["reflection"] = reflection
    st.success("已生成")
st.caption("Agent反思改进")
st.write(st.session_state["reflection"])

# 解析
st.header("解析")

st.session_state["solution_replica"] = st.session_state["solution"]

input_solution = st.text_area("请输入解题过程", st.session_state["solution_replica"])
if input_solution:
    st.session_state["solution_replica"] = input_solution


submit3 = st.button("解析↓")

if submit3 and st.session_state["whole_question"] != "" and st.session_state["solution_replica"] != "":
    with st.spinner(("AI正在编写解析...")):
        azure1_message = azure1_message(question=st.session_state["whole_question"],
                                        solution=st.session_state["solution_replica"])
        azure1_json = azure_generate_json(message=azure1_message)
        azure1_content = azure1_json["content"]
    st.success("已生成")
    st.session_state["answer"] = azure1_content
st.write(st.session_state["answer"])

submit3_2 = st.button("解析评估↓")

if submit3_2 and st.session_state["answer"]!="":
    with st.spinner(("解析评估ing...")):
        azure2_message = azure2_message(question=st.session_state["whole_question"],
                                        solution=st.session_state["solution_replica"],
                                        answer=st.session_state["answer"])
        azure2_json = azure_generate_json(message=azure2_message)
        azure2_content = azure2_json["content"]
        st.session_state["answer_suggestion"] = azure2_content
    st.success("已完成")
st.caption("提修改建议")
st.write(st.session_state["answer_suggestion"])
