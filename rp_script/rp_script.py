import re
import docx
import pprint
import pandas as pd

# Open csv and read all cases
df = pd.read_csv("BD - Protecciones.csv")[
    "TERMINADA",
    "CORTE",
    "RECURRENTE",
    "CI",
    "FECHA CARTA/FUN",
    "ISAPRE",
    "PLAN",
    "% ALZA",
    "PB",
    "PBR",
    "MES OBJECIÓN"
    ]

# Clean df --- extract NAPB only
df_filtered = df.dropna(subset=["FECHA CARTA/FUN"])
print(df_filtered)

exit()
# Open document
doc = docx.Document("MODELO RECURSO ALZA PRECIO BASE 2022.docx")
regex = re.compile("<<(.*?)>>")

replace_str = "This is a test string"

# Iterate through all paragraphs in doc
for paragraph in doc.paragraphs:
    paragraph_replace_text(paragraph, regex, replace_str)
    pprint.pprint(list(r.text for r in paragraph.runs))
   
# Thanks to @scanny for this function, you can find it at https://github.com/python-openxml/python-docx/issues/30#issuecomment-879593691
def paragraph_replace_text(paragraph, regex, replace_str):
    """Return `paragraph` after replacing all matches for `regex` with `replace_str`.

    `regex` is a compiled regular expression prepared with `re.compile(pattern)`
    according to the Python library documentation for the `re` module.
    """

    # --- a paragraph may contain more than one match, loop until all are replaced ---
    while True:
        text = paragraph.text
        match = regex.search(text)
        if not match:
            break


        # --- when there's a match, we need to modify run.text for each run that
        # --- contains any part of the match-string.
        runs = iter(paragraph.runs)
        start, end = match.start(), match.end()

        # --- Skip over any leading runs that do not contain the match ---
        for run in runs:
            run_len = len(run.text)
            if start < run_len:
                break
        start, end  = start - run_len, end - run_len

        # --- Match starts somewhere in the current run. Replace match-str prefix
        # --- ocurring in this run with entire replacement str.
        run_text = run.text
        run_len = len(run_text)
        run.text = "%s%s%s" % (run_text[:start], replace_str, run_text[end:])
        end -= run_len  # --- note this is run-len before replacement ---

        # --- Remove any suffix of match word that occurs in following runs. Note that
        # --- such a suffix will always begin at the first character of the run. Also
        # --- note a suffix can span one or more entire following runs.
        for run in runs:  # --- next and remaining runs, uses same iterator ---
            if end <= 0:
                break
            run_text = run.text
            run_len = len(run_text)
            run.text = run_text[end:]
            end -= run_len

    # --- optionally get rid of any "spanned" runs that are now empty. This
    # --- could potentially delete things like inline pictures, so use your judgement.
    # for run in paragraph.runs:
    #     if run.text == "":
    #         r = run._r
    #         r.getparent().remove(r)

    return paragraph
 


if __name__ == "__main__":
    main()
