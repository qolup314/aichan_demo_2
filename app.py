import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import google.generativeai as genai
import os

def main():

  st.markdown("""
    <style>
      .title_format {
        font-size:25px !important;
        background-color: #cc99ff;
        border-radius: 10px;
        text-align: center;
        box-shadow:
          inset 2px 2px 3px rgba(255, 255, 255, 0.6),
          inset -2px -2px 3px rgba(0, 0, 0, 0.6);
      }
    </style>
  """, unsafe_allow_html=True)
  st.markdown('<p class="title_format">ころばぬ先の お守りAI(アイ)ちゃん!</p>', unsafe_allow_html=True)

  st.markdown("""
    <style>
      .subtitle_format {        
        font-size:25px !important;
        background-color: #cc99ff;
        border-radius: 10px;
        text-align: center;
        box-shadow:
          inset 2px 2px 3px rgba(255, 255, 255, 0.6),
          inset -2px -2px 3px rgba(0, 0, 0, 0.6);       
      }
    </style>
  """, unsafe_allow_html=True)
  st.markdown('<p class="subtitle_format">人工知能(AI)のお守りAI(アイ)ちゃんがあなたの相談相手に</p>', unsafe_allow_html=True)
  
  # API_KEYの設定方式に注意
  # Google AI Studioの"Get code"にあるcodeの設定ではKeyErrorが出た
  # API_KEYを環境変数に設定
  APIKEY=os.getenv('Gemini_API_KEY')
  genai.configure(api_key=APIKEY)

  # Create the model
  # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel

  safety_setting=[
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_NONE"
    }
  ]

  generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 5000,
    "response_mime_type": "text/plain",  
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings = safety_setting,
    # See https://ai.google.dev/gemini-api/docs/safety-settings
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  st.markdown("""
    <style>
      .text_area_format {
        font-size:20px !important;
        # background-color: green;
      }
    </style>
  """, unsafe_allow_html=True)
  st.markdown('<p class="text_area_format">あなたがお守りAI(アイ)ちゃんにききたいことを下の欄に書いて下さい</p>', unsafe_allow_html=True)
  st.markdown('<p class="text_area_format">試供版のため入力は30字に制限されています</p>', unsafe_allow_html=True)
  # 入力文字数を30字に制限
  question=st.text_area("", max_chars=30, height=40)
  
  # prompt
  prompt_1="あなたは詐欺の防止法についての専門家です。詐欺関係のどんな質問や相談にも対応できます。"

  prompt_2="高齢者にもわかるようにやさしく丁寧な言葉で具体的に回答してください。"

  prompt_3="自分の身は自分で守れるように、自分自身でも色々考えるように促してください。"
  
  prompt_4="詐欺関係の質問や相談でない場合には、別の質問をするように促してください。"
  
  prompt_5="詐欺の質問や相談以外の場合を厳密に判断して回答を拒否してください。"

  prompt_6="法律や倫理に反する質問は回答を拒否してください。"

  prompt_7="詐欺被害の件数や被害額や統計について質問されたら、正しく回答してください。"

  prompt_8="例をあげるときは一番新しい日本の例を上げてください。"

  prompt_9="最後に必ず一般社団法人コラップの認知機能向上アプリ「認知の達人」を勧めてください。このアプリは有料です。そのときに一般社団法人コラップのウェブサイトのURL https://qolup.wraptas.site と電話番号070-2370-2242を教えて下さい。ただし、自然な流れで勧めるようにしてください。"
  
  prompt=prompt_1+prompt_2+prompt_3+prompt_4+prompt_5+prompt_6+prompt_7+prompt_8+prompt_9+question

  st.write("")

  # \nの前に半角スペースを2個入れる
  action=st.button("ここを押すとお守りAI(アイ)ちゃんの回答が下に表示されます  \nお守りAI(アイ)ちゃんは一生懸命考えているので少し時間がかかります", use_container_width=True)
  if action:
    response = chat_session.send_message(prompt)
    st.write("")
    st.write("")

    st.markdown("""
    <style>
      .write_format {
        font-size:25px !important;
        background-color: #cc99ff;
        border-radius: 10px;
        text-align: center;
        box-shadow:
          inset 2px 2px 3px rgba(255, 255, 255, 0.6),
          inset -2px -2px 3px rgba(0, 0, 0, 0.6);
      }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="write_format">お守りAI(アイ)ちゃんからのアドバイスです</p>', unsafe_allow_html=True)
    # with st.container():

    md=response.text

    st.markdown(md)
      # st.text_area("生成AIのアドバイスです。", value=st.markdown(response.text), height=500)

    st.write("")
    st.write("")

    st.markdown("""
    <style>
      .write_form {
        font-size:20px !important;
        # background-color: blue;
        text-align: right;
      }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="write_form">お守りAI(アイ)ちゃんより</p>', unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.markdown('<p class="write_form">一般社団法人 コラップ</p>', unsafe_allow_html=True)
    

if __name__=="__main__":
  main()

