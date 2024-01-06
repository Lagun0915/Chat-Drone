import gradio as gr
import time
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import os

from Web_Mic import Web_Mic_Controler
mic = Web_Mic_Controler()

from API_Key import CHAT_GPT
os.environ['OPENAI_API_KEY']=CHAT_GPT()
llm = ChatOpenAI(temperature=1.0, model='gpt-4')
additional_input_info = "너는 이제부터 작은 편의점에서 물건을 찾는걸 도와주는 챗봇이야."
history = []

def respond(msg, chat_history):
    history_langchain_format = []

    history_langchain_format.append(SystemMessage(content= additional_input_info))
    for human, ai in history:
            history_langchain_format.append(HumanMessage(content=human))
            history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=msg))
    bot_message = llm(history_langchain_format).content
    
    history.append((msg, bot_message))
    
    chat_history.append((msg, bot_message))
    return "", chat_history

def bnt1_click():
    mic.start()
    return None

def bnt2_click(chat_history):
    mic.stop()
    time.sleep(1)
    
    msg = mic.speech_to_text()
    
    _, chat_history = respond(msg, chat_history)
    
    return None, chat_history

def bnt3_click(message, chat_history):
    bot_message = "상품을 추천하겠습니다! 현재 상황을 설명해주세요!"
    chat_history.append((None, bot_message))
    return None, chat_history

def bnt4_click(message, chat_history):
    bot_message = "상품을 찾아드리겠습니다! 원하시는 상품을 입력해주세요!"
    chat_history.append((None, bot_message))
    return None, chat_history

with gr.Blocks() as app:
    gr.Markdown("Chat-Drone")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="원하시는 것을 입력하세요!")

    with gr.Row():
        btn1 = gr.Button("🔴녹음시작")
        btn2 = gr.Button("⬛녹음종료")
    with gr.Row():
        btn3 = gr.Button("📌상품추천")
        btn4 = gr.Button("🔍상품찾기")

    btn1.click(fn=bnt1_click, inputs=[], outputs=[msg])
    btn2.click(fn=bnt2_click, inputs=[chatbot], outputs=[msg, chatbot])
    btn3.click(fn=bnt3_click, inputs=[msg, chatbot], outputs=[msg, chatbot])
    btn4.click(fn=bnt4_click, inputs=[msg, chatbot], outputs=[msg, chatbot])

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

app.launch()