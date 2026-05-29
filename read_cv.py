import zipfile
import xml.etree.ElementTree as ET

def read_docx(file_path):
    try:
        with zipfile.ZipFile(file_path) as docx:
            xml_content = docx.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            # Retrieve all text nodes
            paragraphs = []
            for child in root.iter():
                if child.tag.endswith('p'):
                    p_text = []
                    for node in child.iter():
                        if node.tag.endswith('t') and node.text:
                            p_text.append(node.text)
                    if p_text:
                        paragraphs.append("".join(p_text))
            
            return "\n\n".join(paragraphs)
    except Exception as e:
        return f"Error reading docx: {e}"

cv_text = read_docx("C:/Users/Dave/Desktop/David_Fisher_PurtyCV.docx")
with open("M:/Projects/Revenant-Relay/cv_extracted.txt", "w", encoding="utf-8") as f:
    f.write(cv_text)
print("Extracted CV successfully using native python zipfile/xml!")
