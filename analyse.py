import pymongo
import numpy as np

client = pymongo.MongoClient()
db = client['MyAPP']
col = db['sj']

raw_datas = list(col.find())

datas = np.array([(x['Name'], x['DownloadCount']) for x in sorted(raw_datas, key=lambda i:i['DownloadCount'], reverse=True)])

print(datas[:30])