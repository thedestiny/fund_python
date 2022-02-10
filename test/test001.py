data_list = """
123
346
"""
dd_list = []
for nd in data_list.split("\n"):

    if nd:
        dd_list.append(nd)

print(",".join(dd_list))

tmp = "\",\"".join(dd_list)
print("\"" + tmp + "\"")
