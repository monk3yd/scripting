import os
import convertapi
import pandas as pd

from docxtpl import DocxTemplate
from pprint import pprint

def main():
    # --- Open csv and read all clients data
    df = pd.read_csv("BD - Protecciones.csv")[[
        "INGRESAR",
        "TIPO",
        "CORTE",
        "RECURRENTE",
        "CI",
        "ISAPRE",
        "RUT ISAPRE",
        "REP ISAPRE",
        "DOMICILIO ISAPRE",
        "FECHA CARTA",
        "PLAN",
        "ALZA",
        "PB",
        "PBR",
        "MES OBJECIÓN",
        # "TERMINADA",
    ]]

    # --- Filter df by column value == True
    df_filtered = df[df["INGRESAR"]]

    # --- df to list of dicts, each dict element in list is a different client's data
    # --- needs to be a different docs for each client
    clients_data_df = df_filtered.to_dict(orient="records")

    # --- Each dictionary element within this list represents a client ---
    for client_data in clients_data_df:
        # --- Each key of the client dictionary represents the jinja syntax used in the
        # --- word template.docx file as a placeholder.
        # --- Each value of the client dictionary represents the value that is going to
        # --- substitute the placeholder.
        context = {
            'CORTE': client_data['CORTE'],
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

        pprint(f"Creating {file_name}")

        # --- Open template docx file
        doc_template = DocxTemplate("template.docx")

        # --- Create new client's docx by parsing template 
        doc_template.render(context)

        # --- Save client's files (docx & pdf)
        file_name = f"C.A. DE {client_data['CORTE']} - {client_data['RECURRENTE']} con {client_data['ISAPRE']}"

        docx_file_path = f"docx_autoescrito/{file_name}.docx"
        doc_template.save(docx_file_path)

        # --- Converts docx into pdf API. Note: secrey key in scripting env
        secret_key = str(os.environ["convert_api_secret_key"])
        convertapi.api_secret = secret_key 

        pdf = convertapi.convert('pdf', {'File': docx_file_path})
        pdf_file_path = f"pdf_autoescrito/{file_name}.pdf"
        pdf.file.save(pdf_file_path)
        

if __name__ == "__main__":
    main()