from transformers import pipeline
import torch
import torch.nn.functional as F

from transformers import AutoTokenizer, AutoModelForMaskedLM

# tokenizer = AutoTokenizer.from_pretrained("albert-base-v1")
#
# model = AutoModelForMaskedLM.from_pretrained("albert-base-v1")

from transformers import AlbertTokenizer, AlbertModel
tokenizer = AlbertTokenizer.from_pretrained('albert-base-v1')
model = AlbertModel.from_pretrained("albert-base-v1")
text = "Replace me by any text you'd like."
encoded_input = tokenizer(text, return_tensors='pt')
output = model(**encoded_input)

classifier = pipeline("sentiment-analysis")
res = classifier("slavery is being abolished across the country")
print(res)

import mysql.connector
from config import host, user, passwd, database_name, path_to_tickers_set


try:
    db = mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        passwd=passwd,
        database=database_name
    )
    my_cursor = db.cursor()
except Exception as e:
    print(e)
else:
    for ticker in new_tickers:
        my_cursor.execute('ALTER TABLE stockMarketPrices ADD COLUMN `{ticker}` FLOAT'.format(ticker=ticker))
    my_cursor.close()