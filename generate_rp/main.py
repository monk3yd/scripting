import pandas as pd

from pathlib import Path
from utils import parse_and_save, gdrive_authenticate, download_gsheet


def main():
    # --- Connect to Google Drive (Authentication) & Download gsheet ---
    service = gdrive_authenticate()
    gsheets = download_gsheet(service)  # csv or df?

    gdf = pd.DataFrame(gsheets)

    # First row as header
    gdf = gdf.rename(columns=gdf.iloc[0]).loc[1:]

    # Save backup csv
    gdf.to_csv("Protecciones.csv", index=False)

    # --- Manage Database ---
    # --- Open csv and read all clients data
    df = pd.read_csv("Protecciones.csv")[[
        "ID",
        "INGRESAR",
        "TIPO",
        "CORTE",
        "PREFIX",
        "GENDER",
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
    clients_data_list = df_filtered.to_dict(orient="records")

    # --- File Generator ---
    # --- Parse template & Save docx & pdf files ---
    parse_and_save(clients_data_list, Path("templates/template.docx"))


if __name__ == "__main__":
    main()
