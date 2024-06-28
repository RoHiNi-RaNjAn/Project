#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Example loaders.py
def process_file(file):
    import PyPDF2
    import docx

    if file.type == "text/plain":
        return file.getvalue().decode("utf-8")
    elif file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
        return pdf_text
    elif file.type in ["application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        doc = docx.Document(file)
        doc_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return doc_text
    else:
        return "Unsupported file type"

