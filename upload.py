import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import requests
import smtplib
import imghdr
from email.message import EmailMessage
from datetime import datetime as dt
# Authenticate and create Google Drive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
file_description=""
# Streamlit app
token='5360919649:AAGZgsx4IpU1SGe64v82Oj9fmjPMVOBakQU'
chat_id="-1001687356814"
def mail(mess):
    Sender_Email = "yashwanthbs1208@gmail.com"
    Reciever_Email = ["pragathimotors2016@gmail.com"]#,"htv6902@gmail.com","niruphombegowda1999@gmail.com",'nirupgowda1999@gmail.com']
    Password = "ofhqncekyefrrrxw"
    newMessage = EmailMessage()                         
    newMessage['Subject'] = f"Checkout, New Evidence added {dt.now().date()}" 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email                   
    newMessage.set_content(f"{mess}")
    # newMessage.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        
        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)

def telegram(filedescription,link):
    data={'chat_id':chat_id,
        'text':f"{filedescription}/n {link}"}
    telegram_msg = f'https://api.telegram.org/bot{token}/sendMessage'
    requests.post(telegram_msg,data)
def main():
    global file_description
    st.title("Pragathi Motors Evidence collector")

    # File upload section
    file_description = st.text_input("Enter Vehicle Number and Description")
    st.header("Upload File")
    file_types = ["mp4", "docx", "pdf","jpg","heic","jpeg"]
    file = st.file_uploader("Choose a file", type=file_types)
    if file is not None:
        file_id = save_file(file, file_description)
        share_link = get_share_link(file_id)
        if share_link:
            st.write("Shareable Link:")
            st.write(share_link)

# Save uploaded file to Google Drive and return the file ID
def save_file(file, description):
    file_name = file.name
    file_path = os.path.join(os.getcwd(), file_name)
    with open(file_path, 'wb') as f:
        f.write(file.read())

    gfile = drive.CreateFile({'title': file_name, 'description': description})
    gfile.SetContentFile(file_path)
    gfile.Upload()
    st.success("File uploaded successfully!, Check your email id for more details")
    return gfile['id']

# Get shareable link for file from Google Drive
def get_share_link(file_id):
    try:
        permission = drive.CreateFile({'id': file_id})
        permission.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'
        })
        link= f"https://drive.google.com/uc?id={file_id}"
        telegram(file_description,link)
        mess=f"{file_description} - {link}"
        mail(mess)
        return link
    except:
        st.error("Could not generate shareable link.")

if __name__ == "__main__":
    main()
    st.write("Developed by [yashtech.Inc](https://yashtech.xyz/)")
    # increment = st.button('Refresh')
    # if increment:
    #     count += 1
