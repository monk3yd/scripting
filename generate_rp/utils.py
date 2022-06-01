import os
import convertapi

from docxtpl import DocxTemplate


def parse_and_save(clients_data: list, template_path: str):
    # --- Each dictionary element within this list represents a client ---
    for client_data in clients_data:
        # --- Each key of the client dictionary represents the jinja syntax used in the
        # --- word template.docx file as a placeholder.
        # --- Each value of the client dictionary represents the value that is going to
        # --- substitute the placeholder.
        print(f"Generate context variables for...{client_data['RECURRENTE']}")
        context = {
            'CORTE': client_data['CORTE'],
            'PREFIX': client_data['PREFIX'],
            'GENDER': client_data['GENDER'],
            'RECURRENTE': client_data['RECURRENTE'],
            'CI': client_data['CI'],
            'ISAPRE': client_data['ISAPRE'],
            'RUT_ISAPRE': client_data['RUT ISAPRE'],
            'REP_ISAPRE': client_data['REP ISAPRE'],
            'DOMICILIO_ISAPRE': client_data['DOMICILIO ISAPRE'],
            'PLAN': client_data['PLAN'],
            'ALZA': client_data['ALZA'],
            'FECHA_CARTA': client_data['FECHA CARTA'],
            'PB': client_data['PB'],
            'PBR': client_data['PBR'],
            'MES_OBJECIÓN': client_data["MES OBJECIÓN"]
        }
        # --- Converts docx into pdf API. Note: secrey key in conda scripting env
        convertapi.api_secret = os.getenv("SECRET_KEY")

        # --- Open template docx file
        print("Open docx template...")
        doc_template = DocxTemplate(template_path)

        # --- Create new client's docx by parsing template
        print("Render template and replace with context variables...")
        doc_template.render(context)

        # --- Save client's files (docx & pdf)
        file_name = f"ID {client_data['ID']} - C.A. DE {client_data['CORTE']} - {client_data['RECURRENTE']} con {client_data['ISAPRE']}"

        print(f"Saving {file_name} in DOCX...")
        docx_file_path = f"docx_autoescrito/{file_name}.docx"
        doc_template.save(docx_file_path)

        print(f"Saving {file_name} in PDF...")
        pdf = convertapi.convert('pdf', {'File': docx_file_path})
        pdf_file_path = f"pdf_autoescrito/{file_name}.pdf"
        pdf.file.save(pdf_file_path)

    print("Success script run.")
    return 0
