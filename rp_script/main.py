import os
import pandas as pd

from pprint import pprint
from robot import SeleniumBot
from utils import parse_and_save


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
    clients_data_df = df_filtered.to_dict(orient="records")

    # --- Parse template & Save docx & pdf files ---
    # parse_and_save(clients_data_df)

    # pprint('''
    #     All files generated...
    #     Starting upload...
    # ''')

    # --- Robot ---
    URL = "https://oficinajudicialvirtual.pjud.cl/home/index.php"
    RUT = os.environ["rut"]
    PASSWD = os.environ["passwd"]

    pprint("Connecting to robot...")

    robot = SeleniumBot(url=URL)
    robot.login(rut=RUT, passwd=PASSWD)
    robot.goto_ingreso_dda_escrito()
    robot.fill_forms()  # Pass in data


if __name__ == "__main__":
    main()
