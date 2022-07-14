# What does this script do?
It parses a template docx file (template.docx) using jinja2.

# How?
By using Pandas it reads and filters a csv containing all the clients data.
It outputs a Pandas' dataframe(clients_data_df), that is a list of dicts

- Each dictionary element within this list represents a client,
- Each key of the client dictionary represents the jinja syntax used in the word template.docx file as a placeholder.
- Each value of the client dictinary represents the value that is going to substitute the placeholder.

Renders template...

Create new personalized client's docx and save it

Connect to convertapi
Takes the just created docx file, converts it into a pdf file and save it


