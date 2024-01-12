
test = """
'Dengue virus'
'Ebola virus'
'Encephalomyocarditis virus'
'Enterovirus 71'
'Epstein-Barr Virus'
'H7N9 influenza virus'
'Hepatitis B virus'
'Hepatitis C virus'
'Human Bocavirus 1'
'Human cytomegalovirus'
'Human immunodeficiency virus type 1'
'Human rhinovirus'
'Human T-lymphotropic virus type 1'
'Influenza A virus'
Kaposi's sarcoma-associated herpesvirus
'Lymphocytic choriomeningitis mammarenavirus'
'Measles virus'
Rhinovirus
'Rift Valley fever virus'
'Sendai virus'
'Severe acute respiratory syndrome coronavirus 2'
'West Nile virus'
'Zika virus'
"""

tmp = """update diff set NAME = replace(NAME, "{}","")"""

for nd in test.split("\n"):
    cnt = nd.replace("'","").strip()
    if cnt:
      print(tmp.format("files/" + cnt + "/"))