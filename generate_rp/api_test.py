import convertapi

# ENDPOINT = "https://v2.convertapi.com/convert/docx/to/pdf?StoreFile=true"
convertapi.api_secret = ""

file_name = "C.A. DE LA SERENA - MANUEL ABARCA MEZA con BANMÉDICA"
file_docx_path = f"docx_autoescrito/{file_name}.docx"
result = convertapi.convert('pdf', {'File': file_docx_path})
result.file.save(f"pdf_autoescrito/{file_name}.pdf")
