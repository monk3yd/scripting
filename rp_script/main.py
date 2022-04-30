import pandas as pd
from docxtpl import DocxTemplate

def main():
    # Open csv and read all cases
    df = pd.read_csv("BD - Protecciones.csv")[[
        # "TERMINADA",
        "CORTE",
        "RECURRENTE",
        "CI",
        "ISAPRE",
        "RUT ISAPRE",
        "REP ISAPRE",
        "DOMICILIO ISAPRE",
        "FECHA CARTA/FUN",
        "PLAN",
        "% ALZA",
        "PB",
        "PBR",
        "MES OBJECIÓN"
    ]]

    # Clean df --- extract NAPB only
    df_filtered = df.dropna(subset=["FECHA CARTA/FUN"])

    # df to list of dicts, each element is list needs to be a different docs
    clients_data_df = df_filtered.to_dict(orient="records")

    # Open docx document
    # doc_template = docx.Document("MODELO RECURSO ALZA PRECIO BASE 2022.docx")
    doc_template = DocxTemplate("template.docx")
    for client_data in clients_data_df:
        print(client_data)
        context = {
            'CORTE': client_data['CORTE'],
            'RECURRENTE': client_data['RECURRENTE'],
            'CI': client_data['CI'],
            'ISAPRE': client_data['ISAPRE'],
            'RUT_ISAPRE': client_data['RUT ISAPRE'],
            'REP_ISAPRE': client_data['REP ISAPRE'],
            'DOMICILIO_ISAPRE': client_data['DOMICILIO ISAPRE'],
            'PLAN': client_data['PLAN'],
            'ALZA': client_data['% ALZA'],  # TODO fix 
            'FECHA_CARTA': client_data['FECHA CARTA/FUN'],  # TODO fix
            'PB': client_data['PB'],
            'PBR': client_data['PBR'],
            'MES_OBJECIÓN': client_data["MES OBJECIÓN"]  # TODO fix
        }
        doc_template.render(context)

        # Save client own doc
        doc_template.save(f"C.A. DE {client_data['CORTE']} - {client_data['RECURRENTE']} con {client_data['ISAPRE']}.docx")
        

if __name__ == "__main__":
    main()