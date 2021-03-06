from rdflib import Dataset

import constants as c, main as m, save as s

ds = Dataset()
ds.bind(c.PREFIX, c.ONT)
ds.bind('dbo', c.DBO)
ds.bind('dbr', c.DBR)
ds.bind('dbp', c.DBP)
ds.bind('foaf', c.FOAF)

graph = ds.graph(c.ONT)

ds, graph = m.convert_mep(c.DATA_MEP, ds, graph)

s.save_json(c.DICT_MEPS, m.dict_mep)
s.save_json(c.DICT_PARTIES, m.dict_party)

ds, graph = m.convert_dossier(c.DATA_DOSSIER, ds, graph)

ds, graph = m.convert_votes(c.DATA_VOTES, ds, graph)

s.save_dataset(c.DATA_OUTPUT, ds)
