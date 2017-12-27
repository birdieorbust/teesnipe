import pandas as pd
import numpy as np
import time

def clean_table(dataframe):
	#READ TEST TABLE
	#table=pd.read_csv("data/test_table.csv")
	dataframe['Holes']=dataframe['Holes'].astype('object')
	#GET SUNRISE AND SUNSET TIME
	#sunrise=dataframe['Holes'][dataframe['Holes'].str.contains("Sunrise")==True]
	#sunrise=time.strptime(sunrise[0].strip('Sunrise '),'%I:%M %p')
	#REMOVE ROWS TO LEAVE TEE TIMES ONLY
	dataframe = dataframe[dataframe['Holes'].str.contains("Sunset|Sunrise")==False]
	dataframe.columns = [c.replace(' ', '_') for c in dataframe.columns]
	dataframe.columns = [c.replace('._', '_') for c in dataframe.columns]
	
	#BOOKED STATUS 1=booked, 0=not booked, 9=not bookable
	print(dataframe.dtypes)
	dataframe['Holes']=dataframe.Holes.apply(lambda x: 1 if 'Booked' in x else 0)
	print(dataframe)
	#RESERVEd FOR BACKNINE i.e. reservedforbacknine=1
	return dataframe