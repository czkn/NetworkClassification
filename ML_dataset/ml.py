import numpy as np
import sklearn.ensemble, sklearn.model_selection
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

def read_csv(file_path, has_header=True):
    with open(file_path) as f:
        if has_header: f.readline()
        data = []
        for line in f:
            line = line.strip().split(",")
            data.append([x for x in line])
    return data

####################################################
# Second Level models creator
####################################################
def Lv2modelsCreator(trainset, keyset, flimit):
    streamdict = defaultdict(list)
    models = defaultdict(list)
    dataset = zip(keyset, trainset)
    for row in dataset:
        streamdict[row[0]].append(row[1:44])
        randomforestmodel = RandomForestClassifier(n_estimators=10, n_jobs=10)

    for k in streamdict:
        perTLD = streamdict[k]
        #Full Feature set
        ktarget = np.array([x[0][flimit] for x in perTLD])
        ktrain = np.array([x[0][0:flimit] for x in perTLD])
        randomforestmodel.fit(ktrain, ktarget)
        s = pickle.dumps(randomforestmodel)
        models[k].append(s)
    return models

#############################################
# The Evaluation method
###############################################
def multiLevelEval(l2real, l2predict):
    total = 0
    partial = 0
    unknown = 0

    for i in range(0, len(l2real)):
        temp1 = tldextract.extract(l2real[i])
        temp2 = tldextract.extract(l2predict[i])
        realRD = temp1.domain + "." + temp1.suffix
        predictRD = temp2.domain + "." + temp2.suffix

        if l2real[i] == l2predict[i]:
            total=total+1.0

        elif realRD == predictRD:
            partial = partial + 1.0
    else:
        unknown = unknown + 1
    if realRD == "google.com" and predictRD == "gstatic.com":
        #partial=partial+1.0
        total = total + 1.0
    elif predictRD == "google.com" and realRD == "gstatic.com":
        #partial=partial+1.0
        total = total + 1.0

    print("[+] Partial : " + str(round(float(partial) / len(l2real),2)))
    print("[+] Full :" + str(round((float(total) / len(l2real)),2)))
    print("[+] Invalid :" + str(round((float(unknown) / len(l2real)),2)))
    return (float(total) / len(l2real))


#############################################
# Multi-Level Classification 
#############################################

#TODO: get this to work
def MultiLevelClassification(datasetfile, flimit):
    dataset=read_csv(datasetfile)
    result = []
    X = np.array([z[1:25] for z in dataset])
    y = np.array([z[0] for z in dataset])

    #TODO: need to filter out snis with few connections as with flat classification
    rf = RandomForestClassifier(n_estimators=250, n_jobs=10)
    kf = KFold(n_splits=10, shuffle=True)
    totalac = []
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        features = np.array([zp[0:flimit] for zp in X_train])
        features_test = np.array([zp[0:flimit] for zp in X_test])
        l2label = np.array([zp[flimit] for zp in X_test])
        Modles = Lv2modelsCreator(X_train, y_train, flimit)

        l2predict = []
        l2real = []

        streamdict = defaultdict(list)
        rf.fit(features, y_train)
        l1 = rf.predict(features_test)

        for i in range(0, len(l1)):
            streamdict[l1[i]].append(X_test[i])
        for k in streamdict:
            preTLD = streamdict[k]
            m = pickle.loads(Modles[k][0])
            feature = np.array([x[0:flimit] for x in preTLD])
            labels = np.array([x[flimit] for x in preTLD])
            l2 = m.predict(feature)
            l2predict = l2predict + l2.tolist()
            l2real = l2real + labels.tolist()
        totalac.append(multiLevelEval(l2real, l2predict))
        break

    return np.mean(totalac)
    
#############################################
# Flat Classification method
#############################################
def FlatClassification(datasetfile):
    dataset = read_csv(datasetfile)
    X = np.array([z[1:25] for z in dataset])
    y = np.array([z[0] for z in dataset])
    print( np.shape(X), np.shape(y))
    
    snis, counts = np.unique(y, return_counts=True)
    above_min_conns = list()

    MIN_CONNECTIONS = 100

    for i in range(len(counts)):
        if counts[i] > MIN_CONNECTIONS:
            above_min_conns.append(snis[i])

    indices = np.isin(y, above_min_conns)
    X = X[indices]
    y = y[indices]
    print (np.shape(X), np.shape(y))

    rf = RandomForestClassifier(n_estimators=250, n_jobs=10)
    kf = KFold(n_splits=10, shuffle=True)

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        rf.fit(X_train, y_train)
        l1 = rf.predict(X_test)
        print( accuracy_score(l1,y_test))

if __name__ == "__main__":
    FlatClassification("csvs/GCDay1stats.csv")
    MultiLevelClassification("csvs/GCDay1stats.csv",42)