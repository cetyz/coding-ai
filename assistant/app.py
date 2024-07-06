import streamlit as st
from PIL import Image
 
from agents import *
 
# Initialize agents OUTSIDE the main Streamlit app flow
if 'github_cleaner_agent' not in st.session_state:
    st.session_state.github_cleaner_agent = GithubCleanerAgent()

 
# Page configuration
st.set_page_config(page_title='Coding Assistant', page_icon='🤓', layout='wide', initial_sidebar_state='auto')
background_dark_image = Image.open('images\\background_dark.png')
 
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
 
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 


# welcome_page_title = "Welcome to the SMB Gen AI Center"
# smb_gemini_chatbot_title = 'SMB Gemini Chatbot'
 
# selected_interface = st.session_state.get("selected_interface", welcome_page_title)
 
# with st.sidebar:
#     st.image(background_dark_image)
#     st.title('SMB Gemini Chatbot')
#     st.subheader('Gemini for SMB')
#     st.divider() # add some spacing
 
#     if st.button('SMB Gemini Chatbot'):
#         st.session_state['selected_interface'] = 'SMB Gemini Chatbot'
#     st.caption('The main interface for our Gemini Chatbot')
 
#     st.divider()
 
# st.title(selected_interface)
 
# if selected_interface == welcome_page_title:
#     # Welcome page content
#     st.write('Welcome to the Gen AI Center for SMB Google Ads.')
#     st.image(image3)
#     st.divider()
 
#     st.subheader('Getting Started')
#     st.markdown(
#         """
#         Select a tool on the left sidebar to begin.
#         """
#     )
 
# elif selected_interface == smb_gemini_chatbot_title:
#     st.subheader('SMB Gemini Chatbot')
 
#     analyst_agent = st.session_state.analyst_agent
 
#     # Initialize chat history in session state
#     if 'gemini_chatbot_messages' not in st.session_state:
#         st.session_state.gemini_chatbot_messages = []
 
#     for message in st.session_state.gemini_chatbot_messages:
#         with st.chat_message(message['role']):
#             st.markdown(message['content'])
 
#     prompt = st.chat_input('Your message')
#     if prompt:
#         st.session_state.gemini_chatbot_messages.append({'role': 'user', 'content': prompt})
#         with st.chat_message('user'):
#             st.markdown(prompt)
#         response = analyst_agent.invoke(prompt)
#         st.session_state.gemini_chatbot_messages.append({'role': 'assistant', 'content': response['output']})
#         with st.chat_message('assistant'):
#             st.markdown(response['output'])