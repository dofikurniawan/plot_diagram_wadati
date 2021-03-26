import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import shutil
from sklearn.linear_model import LinearRegression
a=open('event6.pick','r')
b=a.readlines()
ambil_date=[]
c=[]
for i in range(len(b)-1):
    b[i]=b[i].split()
    for j in range(13):
        if j==6 :
            c.append(b[i][j:j+3])
time_p=[]
time_s=[]
for i in range(len(c)):
    temp_time=[]
    for j in range(4):
        if j==0:
            temp_time.append(int(c[i][j]))
        elif j==1:
            temp_time.append(int(c[i][1][0:2]))
        elif j==2:
            temp_time.append(int(c[i][1][2:4]))
        else:
            temp_time.append(float(c[i][2]))
    if i%2==0:
        time_p.append(temp_time)
    else:
        time_s.append(temp_time)
        
#mengolah data ke data frame
df1=pd.DataFrame(time_p)

sta=[]
for i in range(len(b)-1):
    if b[i][0]==b[i+1][0]:
        sta.append(b[i][0])
df2=pd.DataFrame(sta,columns=['Sta'])
tp_m=[]
tp=[]
ts=[]
for i in range(len(time_p)):
    tp_m.append(time_p[i][2])
    if  time_p[i][2]!=time_s[i][2]:
        tp.append(time_p[i][3])
            #ts.append(time_s[i][3]+60*(time_p[i][2]-time_s[i][2]))
        if time_p[i][2]>time_s[i][2]:
            ts.append(time_s[i][3]+60*(time_s[i][2]-time_p[i][2]+60))
        else:
            ts.append(time_s[i][3]+60*(time_s[i][2]-time_p[i][2]))
    else:
        tp.append(time_p[i][3])
        ts.append(time_s[i][3])

tp_fix=[]
ts_fix=[]
for i in range (len(tp_m)):
    tp_fix.append(tp[i]+(tp_m[i]-min(tp_m))*60)
    ts_fix.append(ts[i]+(tp_m[i]-min(tp_m))*60)
    if (tp_m[i]-min(tp_m))!=0:
        tp_m[i]=min(tp_m)
df2['tpm']=tp_m
tp_fix=pd.Series(tp_fix)
ts_fix=pd.Series(ts_fix)
ts=pd.Series(ts)
df2['tp']=tp_fix
df2['ts']=ts_fix
df2['ts-tp']=df2.ts-df2.tp
# regresi linear
model=LinearRegression()
dftp=df2['tp'].values.reshape(-1,1)
model.fit(dftp,df2.ts-tp)
y_pred=model.predict(dftp)
#Ploting Wadati Diagram
sns.set()
plt.figure(figsize=(12,10))
plt.scatter(df2.tp,df2.ts-tp)
plt.xlabel('tp(s)')
plt.ylabel('ts-tp(s)')
eventID='%d-%.2d-%.2d-%.2d' % (time_p[0][0],time_p[0][1],time_p[0][2],time_p[0][3]) 
plt.title("Date : %d , EventID: %s \n Vp/Vs=%1.3f \n" %(df1[0][0],eventID,1+model.coef_))
dftp=df2.tp.values.reshape(-1,1)
plt.plot(dftp,y_pred,'r')
for i, txt in enumerate(df2.Sta):
    plt.annotate(txt,(df2.tp[i],df2['ts-tp'][i]))
plt.savefig(eventID+'.png')
plt.show()
#mengcopy file output
shutil.copy('event6.pick',eventID+'.pick')
a.close()