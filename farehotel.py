import pandas as pd

l=[]
for i in range(1,288961):
	l.append(i)
df=pd.DataF frame({'Room_Id':l})
df.to_csv('abc.csv',index=False)