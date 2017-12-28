import pandas as pd
import numpy as np
import time

def clean_table(dataframe):
	#READ TEST TABLE
	#dataframe=pd.read_csv("data/test_table.csv")
	dataframe=dataframe.reset_index()
	dataframe['Holes']=dataframe['Holes'].astype('object')
	#GET SUNRISE AND SUNSET TIME
	#sunrise=dataframe['Holes'][dataframe['Holes'].str.contains("Sunrise")==True]
	#sunrise=time.strptime(sunrise[0].strip('Sunrise '),'%I:%M %p')
	#REMOVE ROWS TO LEAVE TEE TIMES ONLY
	#dataframe = dataframe[dataframe['Holes'].str.contains("Sunset|Sunrise")==False]
	dataframe.columns = [c.replace(' ', '_') for c in dataframe.columns]
	dataframe.columns = [c.replace('._', '_') for c in dataframe.columns]
	
	#BOOKED STATUS 1=booked, 0=not booked, 9=not bookable
	#print(dataframe.dtypes)
	#dataframe['Book']=dataframe.Holes.apply(lambda x: 1 if 'Booked' in x else 0)
	#dataframe.isbooked=np.where(dataframe.Book.str.contains("Booked",na=False),1,0)
	#dataframe.to_csv("data/test_table.csv")
	#numberofcurrentplayers
	subset=dataframe[['Player_1','Player_2','Player_3','Player_4']]
	subset=subset.replace('.','')
	players=subset.count(axis=1)
	dataframe['players']=players
	#print(dataframe)

	return dataframe