from pprint import pprint
import pandas as pd
from docxtpl import DocxTemplate

def main():
    # Open csv and read all clients data
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

    # Filter df by INGRESAR column value
    df_filtered = df[df["INGRESAR"]]

    # df to list of dicts, each element is list needs to be a different docs
    clients_data_df = df_filtered.to_dict(orient="records")

    # Open docx document
    doc_template = DocxTemplate("template.docx")

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

        pprint(context)
        doc_template.render(context)

        # Save client own doc
        doc_template.save(f"docx_autoescrito/C.A. DE {client_data['CORTE']} - {client_data['RECURRENTE']} con {client_data['ISAPRE']}.docx")
    

        

if __name__ == "__main__":
    main()