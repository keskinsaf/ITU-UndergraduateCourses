import pandas as pd
import numpy as np
from numpy import linalg as LA
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier # randomforest
from sklearn.datasets import make_classification    # randomforest
import matplotlib.pyplot as plt
import random

def getBD(d_of_b, del_date):
    d_of_b  = del_date[:4] + d_of_b[4:]
    return d_of_b

def getMaxKey( clrs, cnames ):
    maxcolor = 0
    cname    = ""
    for i in cnames:
        if clrs[i] > maxcolor:
            maxcolor = clrs[i]
            cname = i
        #print( i + ":" + str(clrs[i]) )
    return cname

# lDate = last date, fDate = first date
def changeAge( lDate, fDate ):
    account_age = (((np.datetime64(lDate) - np.datetime64(fDate)) / np.timedelta64('1', 'D'))).astype(float) / 365.25
    return str(account_age)

def cleanTestData(x):
    data_dict   = {}
    colors      = {}
    colorsfromkey = {}
    colornames  = []
    color_index = 0
    data_index  = 0
    index   = 0
    size    = x.shape[0]
    totalctr= 0
    datectr = 0
    #print("Size:",size)
    empty_indexes = []
    color_indexes = []
    while(index < size):
        if x[index, 10] == '?':
            x[index, 10] = '1982-09-23'
            #size    -= 1
            #clear color
        if x[index,5] == '?':
            color_indexes.append(color_index)
        else:
            color_index += 1
            if x[index,5] in colors:
                colors[ x[index,5] ] += 1
            else:
                colors[ x[index,5] ] = 1
                colornames.append( x[index,5] )

        #clear dates
        if x[index,2] == '1990-12-31' or x[index,2] == '?':
            empty_indexes.append(data_index)
        else:
            diff = (((np.datetime64(x[index,2]) - np.datetime64(x[index,1]))
                / np.timedelta64('1', 'D'))).astype(int)
            totalctr+= diff
            datectr += 1

            # change creationDate with accountAge in days
            x[index, 12] = changeAge( x[index,2], x[index,12] )

            # change d_of_b with age
            x[index, 10] = changeAge( x[index, 2], x[index,10] )

            x[index,2] = str( int(diff) )

        data_dict[data_index] = x[index]
        index   += 1
        data_index += 1
    #print(x)
    del_dur = int(totalctr / datectr)
    #print("Delivery days in average: " +  str(del_dur))
    for i in empty_indexes:
        #print(del_dur)
        #x[i, 2] = str(del_dur)
        data_dict[i][2]  = (np.datetime64(data_dict[i][1]) + np.timedelta64(del_dur, 'D')).astype(str)
        #print( "oDate:" + data_dict[i][1], end='\t' )
        #print( "dDate:" + data_dict[i][2])
        data_dict[i][12] = changeAge( data_dict[i][2], data_dict[i][12] ) # creation day
        data_dict[i][10] = changeAge( data_dict[i][2], data_dict[i][10] ) # birthday
        data_dict[i][2]  = str(del_dur)

    # for color
    maxcolorname = getMaxKey( colors, colornames )
    for i in color_indexes:
        data_dict[i][5] = maxcolorname

    df = pd.DataFrame(data_dict).T.fillna(0)
    new_x = df.iloc[:,:].values
    new_x = np.delete( new_x, 1, 1 )    # orderDate
    return new_x

def cleanData(x):
    data_dict   = {}
    colors      = {}
    colorsfromkey = {}
    colornames  = []
    color_index = 0
    data_index  = 0
    index   = 0
    size    = x.shape[0]
    totalctr= 0
    datectr = 0
    #print("Size:",size)
    empty_indexes = []
    color_indexes = []
    while(index < size):
        date_of_birth = x[index].item(10)
        if date_of_birth == '?':
            #x = np.delete(x, (index), axis=0)
            #size    -= 1
            index += 1
        else:
            #clear color
            if x[index,5] == '?':
                color_indexes.append(color_index)
            else:
                color_index += 1
                if x[index,5] in colors:
                    colors[ x[index,5] ] += 1
                else:
                    colors[ x[index,5] ] = 1
                    colornames.append( x[index,5] )

            #clear dates
            if x[index,2] == '1990-12-31' or x[index,2] == '?':
                empty_indexes.append(data_index)
            else:
                diff = (((np.datetime64(x[index,2]) - np.datetime64(x[index,1]))
                    / np.timedelta64('1', 'D'))).astype(int)
                totalctr+= diff
                datectr += 1

                # change creationDate with accountAge in days
                x[index, 12] = changeAge( x[index,2], x[index,12] )

                # change d_of_b with age
                x[index, 10] = changeAge( x[index, 2], x[index,10] )

                x[index,2] = str( int(diff) )

            data_dict[data_index] = x[index]
            index   += 1
            data_index += 1
    #print(x)
    del_dur = int(totalctr / datectr)
    #print("Delivery days in average: " +  str(del_dur))
    for i in empty_indexes:
        #print(del_dur)
        #x[i, 2] = str(del_dur)
        data_dict[i][2]  = (np.datetime64(data_dict[i][1]) + np.timedelta64(del_dur, 'D')).astype(str)
        #print( "oDate:" + data_dict[i][1], end='\t' )
        #print( "dDate:" + data_dict[i][2])
        data_dict[i][12] = changeAge( data_dict[i][2], data_dict[i][12] ) # creation day
        data_dict[i][10] = changeAge( data_dict[i][2], data_dict[i][10] ) # birthday
        data_dict[i][2]  = str(del_dur)

    # for color
    maxcolorname = getMaxKey( colors, colornames )
    for i in color_indexes:
        data_dict[i][5] = maxcolorname

    df = pd.DataFrame(data_dict).T.fillna(0)
    new_x = df.iloc[:,:].values
    new_x = np.delete( new_x, 1, 1 )    # orderDate
    return new_x

def changeToInt( x, colnumber, olddict ):
    ctr = 0
    key_dict = olddict
    if key_dict == {}:
        ctr = 0
    else:
        key_max = max(key_dict.keys(), key=(lambda k: key_dict[k]))
        ctr = key_dict[key_max] + 1

    size    = x.shape[0]
    for i in range(size):
        if x[i][colnumber] in key_dict:
            x[i][colnumber] = key_dict[str(x[i][colnumber])]
        else:
            key_dict[ x[i][colnumber] ] = ctr
            x[i][colnumber] = str(ctr)
            ctr += 1
    #print(key_dict)
    return (x, key_dict)

df = pd.read_csv(
    filepath_or_buffer='../blg-454e-term-project-competition/train.txt',
    header=None,
    sep=',',dtype='str')

df.dropna(how="all", inplace=True) # drops the empty line at file-end

features    = df.iloc[0, :].values          # reading columns
df.columns  = features                       # columns
X           = df.iloc[1:,0:14].values    # for only 100 items
#Y           = df.iloc[1:,14].values      # for only 100 items


X = cleanData(X)
X,statemap = changeToInt(X, 10,{})
X,salutmap = changeToInt(X, 8, {})
X,colormap = changeToInt(X, 4, {})
#delDurCalc(X)
features[10] = 'age'
features[12] = 'accountAge'
features[1] = 'deldur'

X = np.delete( X, 10, 1 )# state
X = np.delete( X, 7, 1 ) # customerID
X = np.delete( X, 3, 1 ) # size
X = np.delete( X, 0, 1 ) # orderitemID
X = np.delete( X, 0, 1 ) # deldur
X = X.astype(float)

for i in range(2,13):   # delDate
    features[i] = features[i+1]

for i in range(3,13):   # size
    features[i] = features[i+1]
features = features[1:12] # orderitemID
# 11 with return
for i in range(8,10):   # birtdday (age)
    features[i] = features[i+1]
# 10 with return
for i in range(5,9):    # customerID
    features[i] = features[i+1]
# 9 with return
features = features[1:9] # deldur
# 8 with return
finalf = pd.DataFrame(X)
finalf.columns = features
finalf.to_csv("XandRETURN.csv", index=False)

# use sklearn
# model
Y   = X[:, 7].astype(int)
traindata = X[:, :7]

# clf = tree.DecisionTreeClassifier()
# clf = clf.fit(traindata, Y)
#print("Model trained.")

clf = RandomForestClassifier()
clf = clf.fit(traindata, Y)
print("Data is trained.")

#test data
tf = pd.read_csv(
    filepath_or_buffer='../blg-454e-term-project-competition/test.txt',
    header=None,
    sep=',',dtype='str')

tf.dropna(how="all", inplace=True)

features    = tf.iloc[0, :].values      # reading columns
tf.columns  = features                  # columns
T           = tf.iloc[1:,0:13].values   # for only 100 items

T = cleanTestData(T)
T, t_statemap = changeToInt(T, 10, statemap)
T, t_salutmap = changeToInt(T, 8,  salutmap)
T, t_colormap = changeToInt(T, 4,  colormap)

T = np.delete( T, 10, 1 )# state
T = np.delete( T, 7, 1 ) # customerID
T = np.delete( T, 3, 1 ) # size
T = np.delete( T, 0, 1 ) # orderitemID
T = np.delete( T, 0, 1 ) # deldur
T = T.astype(float)

# testf = pd.DataFrame(T)
# testf.index = testf.index + 1
# testf.to_csv("CLEANTestData.csv", index=True)

pr = clf.predict_proba(T)
pr = pr[:,1]
prediction = pd.DataFrame(pr)
prediction.index = prediction.index + 1
prediction.to_csv("randForPrediction.txt", header = ['orderItemID,returnShipment'], index=True)
