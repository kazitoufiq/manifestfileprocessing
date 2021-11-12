import re
import json
import pandas as pd

FILE_NAME= "outputV4.manifest"
METADATAKEY="labellingjobname-metadata"

f = open(FILE_NAME, "r")

'''
dict_empty ={}

for x in f:
  convertedDict = json.loads(x)
  class_label = convertedDict.get(METADATAKEY).get('class-map')
  dict_empty.update(class_label) # finaly creates a dict with unique values 

print(len(dict_empty))

f.close()
'''

list_empty =[]
for x in f:
  convertedDict = json.loads(x)
  class_label = convertedDict.get(METADATAKEY).get('class-map')
  list_empty.append(class_label)


df =pd.DataFrame(list_empty)
df.count() #count non-empty values in each columns of the dataframe
#print(df) 
f.close()

df_cnt = df.count().to_frame(name='Count') #series to dataframe with column name
df_count_all = df_cnt.rename_axis('class_id').reset_index() #index as new column

df_temp = df.fillna(method='ffill') # forward fill
df_temp = df_temp.fillna(method='bfill') #backfill
df_class_label = df_temp.head(1).T #transpose
df_class_label.rename( columns={0 :'class_label'}, inplace=True )
df_class_id = df_class_label.rename_axis('class_id').reset_index()

df_stats = pd.merge(df_count_all,df_class_id,on='class_id')
count_column = df_stats.pop('Count') #to rearrange column
df_stats.insert(2,count_column.name,count_column)

df_stats.to_csv("df_stats.csv", index=False)

