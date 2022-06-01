import os
import pandas as pd

from pathlib import Path
# from robot import SeleniumBot
from utils import parse_and_save
from pprint import pprint


def main():
    # --- Manage Database ---  # TODO make func
    # --- Open csv and read all clients data
    df = pd.read_csv("BD - Protecciones.csv")[[
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
    parse_and_save(clients_data_list, Path("template.docx"))

    # pprint('''
    #     All files generated...
    #     Starting upload...
    # ''')

    # --- Robot ---
    # URL = "https://oficinajudicialvirtual.pjud.cl/home/index.php"
    # RUT = os.environ["rut"]
    # PASSWD = os.environ["passwd"]

    # robot = SeleniumBot(url=URL)
    # robot.login(rut=RUT, passwd=PASSWD)
    # robot.goto_ingreso_dda_escrito()
    # robot.fill_forms(clients_data_df)


if __name__ == "__main__":
    main()