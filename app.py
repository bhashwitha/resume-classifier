from lib2to3.pgen2.pgen import PgenGrammar
from tkinter import PAGES
import streamlit as st
import docx2txt
import pdfplumber
import traceback
import matplotlib.pyplot as plt
import numpy as np
from predict import *


def r_pdf(file):
    try:
        at = ""
        with pdfplumber.open(file) as pdf:
            pg = pdf.pages
            for page in pg:
                at += page.extract_text()
        return at
    except Exception:
        st.warning('Unable to read PDF file')
        st.error(traceback.print_exc())
        return ""

def p_text(t_data):
    txt = c_text(t_data)
    res,df = pd_class(txt)
    st.markdown("""<hr style="height:5px;border:none;" /> """, unsafe_allow_html=True)
    st.subheader(" Resume suits for "+res[0]+" category !!")

def main():
    try:
        st.title('Resume Classification')
        r_t_area = st.text_area("Enter your Resume text data.")
        st.write('OR')
        r_f_upload = st.file_uploader("Upload Your Resume !",type=["pdf","docx","txt"])
        if st.button('Submit'):    
            if r_f_upload is not None:
                if r_f_upload.type=="text/plain":
                    txt = str(r_f_upload.read(),"utf-8")
                    p_text(txt)
                elif r_f_upload.type=="application/pdf":
                    text = r_pdf(r_f_upload)
                    p_text(text)
                else:
                    txt = docx2txt.process(r_f_upload)
                    p_text(txt)
            elif r_t_area is not None:
                p_text(r_t_area)
            st.markdown("""<hr " /> """, unsafe_allow_html=True)  
            col1, col2 = st.columns(2)
    except Exception:
        st.write(traceback.print_exc())

if __name__=="__main__":
    main()