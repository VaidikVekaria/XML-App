from tkinter import *
import tkinter
import customtkinter
import pandas as pd
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image, ImageTk
import sys
from pathlib import Path
import os
import io, base64


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# system Settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


## Ensures that the file is downloaded only once. And we ask the user to upload a new CSV File
def fileDownload():
    global fileStatus
    if fileStatus:
        convert()
    else:
        statusLabel.configure(text = "Error: " + 'This file has already been converted. Please upload a new CSV file.', text_color = "red", font = ("Sanskrit Text", 14, "bold"))
    
    fileStatus=False

def uploadFile():
    global fileStatus
    fileStatus = True
    try:
        filePath = filedialog.askopenfilename( filetypes=[("CSV Files", "*.csv")])
        global df
        df = (pd.read_csv(str(filePath), encoding='utf-8'))
        statusLabel.configure(text = "Successfully Uploaded: {}".format(str(filePath)), text_color = "lightblue",font = ("Sanskrit Text", 13, "bold"))
        
    except Exception as error:
        statusLabel.configure(text = "Error: " + str(error), text_color = "red")
    
def convert():
    
    try: 
        global file_id
        xml_content = '<?xml version="1.0" encoding="UTF-8" ?>\n'
        xml_content += '<FEEDBACK VERSION="200701" COMMENT="XML-Importfile for mod/feedback">\n'
        xml_content += '    <ITEMS>\n'

        item_id = 1008

        for index, row in df.iterrows():
            new_item = '        <ITEM TYPE="numeric" REQUIRED="0">\n'
            new_item += '            <ITEMID><![CDATA[{}]]></ITEMID>\n'.format(item_id)
            new_item += '            <ITEMTEXT><![CDATA[{} {}]]></ITEMTEXT>\n'.format(row[list(df.columns)[0]], row[list(df.columns)[1]] )
            new_item += '            <ITEMLABEL><![CDATA[]]></ITEMLABEL>\n'
            new_item += '            <PRESENTATION><![CDATA[0|3]]></PRESENTATION>\n'
            new_item += '            <OPTIONS><![CDATA[]]></OPTIONS>\n'
            new_item += '            <DEPENDITEM><![CDATA[0]]></DEPENDITEM>\n'
            new_item += '            <DEPENDVALUE><![CDATA[]]></DEPENDVALUE>\n'
            new_item += '        </ITEM>\n'
            xml_content += new_item
            item_id += 1

        xml_content += '    </ITEMS>\n'
        xml_content += '</FEEDBACK>\n'

        # Save the XML file
        if file_id == 0:
            with open(os.path.join(os.path.expanduser('~'),'Downloads','output.xml'), 'w') as f:
                f.write(xml_content)
        else: 
            #'output({}).xml'.format(file_id)
            with open(os.path.join(os.path.expanduser('~'), 'Downloads','output({}).xml'.format(file_id)), 'w') as f:
                f.write(xml_content)
        
        file_id += 1
        statusLabel.configure(text = "Download Complete! Please check your Downloads folder.", text_color = 'lightgreen' )
    
    except Exception as error:

        statusLabel.configure(text = "Error: " + str(error), text_color = "red")

# app frame
app = customtkinter.CTk()
app.title("LA&PS eServices Office")
app.geometry("720x680")  # width x height
app.resizable(False, False)  # prevent resizing

# adding UI
W1 = customtkinter.CTkLabel(app, text="eClass Feedback Activity",
                                 font=("Georgia Pro", 25, "bold"), text_color = 'white' )
W1.pack(pady=(70, 20))

# Laps Logo

logo_b64 = '''
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
'''

#Decode the PNG data & "wrap" it into a file-like object
fh = io.BytesIO(base64.b64decode(logo_b64))

#Create a PIL image from the PNG data
img = Image.open(fh, mode='r')
photo = ImageTk.PhotoImage(image=img)
image_label = customtkinter.CTkLabel(app, image = photo, text = '')
image_label.pack(padx = 10, pady=10)


# logo = customtkinter.CTkImage(dark_image = Image.open(resource_path('C:\\Users\\vaidi\\Documents\\XML_Project_1.1\\logo2.png')),size = (195,195))
# C:\\Users\\vaidi\\Documents\\XML_Project_1.1\\
# logo = tkinter.PhotoImage(file=resource_path('logo2.png'), master=app ).subsample(2,2)
# image_label = customtkinter.CTkLabel(app, image = logo, text = '')
# image_label.pack(padx = 10, pady=10)

welcome = customtkinter.CTkLabel(app, text="Convert CSV to XML",
                                 font=("Georgia Pro", 21, "bold"), text_color = 'white' )
welcome.pack(pady=(20, 20))


# File upload button
fileStatus = True
upload = customtkinter.CTkButton(app, text = "Upload CSV", command = uploadFile, font=("Montserrat", 16, "bold") )
upload.pack(padx=10, pady=10)

# Upload Status button
statusLabel = customtkinter.CTkLabel(app, text="", font=("Sanskrit Text", 15),wraplength=650, justify = "center")
statusLabel.pack()

# Convert Button
file_id = 0
download = customtkinter.CTkButton(app, text="Download XML", command= fileDownload,
                                   fg_color=("white", "green"), hover_color="darkgreen",
                                   font=("Montserrat", 17, "bold"))
download.pack(padx=10, pady=20)

# Run app
app.mainloop()
