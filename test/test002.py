
data_list = """
ddd
"""

for nd in data_list.split("\n"):
    if nd and nd.strip():
        print("\"{}\",".format(nd))