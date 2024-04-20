import streamlit as st
import re


bot_msg_container_html_template = '''
<div style='padding: 10px; border-radius: 5px; margin-bottom: 10px; display: flex; justify-content: flex-start; gap:5px'>
        <img src="https://i.postimg.cc/J4PNyv7V/Marc-Louvion.png" style="max-height: 50px; max-width: 50px; border-radius: 50%; z-index:3; display: flex; justify-self: flex-start;">
    <div style="background-color: #F0F2F6; color:#262730; justify-content: center; border-radius: 8px; text-align: left; padding-top: 10px; padding-left: 25px; padding-bottom: 0px; padding-right: 20px;">
        $MSG
    </div>
</div>
'''

user_msg_container_html_template = '''
<div style='padding: 10px; border-radius: 5px; margin-bottom: 10px; display: flex; justify-content: flex-end; gap:5px'>
    <div style="width: auto; background-color: #F0F2F6; color:#262730; border-radius: 8px; padding-top: 10px; padding-left: 20px; padding-bottom: 10px; padding-right: 20px">
        $MSG
    </div>
        <img src="https://i.postimg.cc/xdFvvhbG/avatar-default.png" style="max-width: 50px; max-height: 50px; float: right; border-radius: 50%; z-index:3; display: flex; justify-self: flex-end;">   
</div>
'''

def render_article_preview(docs, tickers):
    message = f"<h5>Here are relevant articles for {tickers} that may answer your question. &nbsp; &nbsp;</h5>"
    message += "<div>"
    for d in docs:
        elipse = " ".join(d[2].split(" ")[:140])        
        message += f"<br><a href='{d[1]}'>{d[0]}</a></br>"
        message += f"<p>{elipse} ...</p>"
        message += "<br>"
    message += "</div>"
    return message

def render_earnings_summary(ticker, summary):
    transcript_title = summary["transcript_title"]
    message = f"<h5>Here is summary for {ticker} {transcript_title} </h5>"
    message += "<div>"
    body =  re.sub(r'^-', r'*  ', summary["summary"])
    body =  re.sub(r'\$', r'\\$', body)
    message += f"<p>{body}</p>"
    message += "</div>"
    return message

def render_chat(**kwargs):
    """
    Handles is_user 
    """
    if kwargs["is_user"]:
        st.write(
            user_msg_container_html_template.replace("$MSG", kwargs["message"]),
            unsafe_allow_html=True)
    else:
        st.write(
            bot_msg_container_html_template.replace("$MSG", kwargs["message"]),
            unsafe_allow_html=True)

    if "figs" in kwargs:
        for f in kwargs["figs"]:
            st.plotly_chart(f, use_container_width=True)

