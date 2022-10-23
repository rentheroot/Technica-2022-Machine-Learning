from sklearn import tree
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import pygraphviz

df = pd.read_pickle('df4.pkl')
df2 = pd.DataFrame()
for i in ['color0c', 'color1c', 'color2c', 'color3c', 'color4c']:
    print(i)
    # expand df lists into its own dataframe
    rgbVals = df[i].apply(pd.Series)

    # rename each variable is tags
    rgbVals = rgbVals.rename(columns = lambda x : i + '_' + str(x))
    df2 = pd.concat([df2, rgbVals], axis=1)
df3 = pd.DataFrame(df.filter(['Item', 'Ratio', 'color0p', 'color1p', 'color2p', 'color3p', 'color4p'], axis=1))

# combine dataframe
df = pd.concat([df3, df2], axis=1)

X = df.filter(['Ratio', 'color0c', 'color1c', 'color2c', 'color3c', 'color4c', 'color0p', 'color1p', 'color2p', 'color3p', 'color4p'], axis=1)
y = df.filter(['Item'], axis =1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)


clf = DecisionTreeClassifier(criterion='entropy')

clf.fit(X_train, y_train)
fig, axes = plt.subplots(nrows = 1,ncols = 1, figsize = (3,3), dpi=300)

y_preds = clf.predict(X_test)

print('Accuracy: ', accuracy_score(y_test, y_preds))

tree.plot_tree(clf,
               feature_names = df.columns, 
               class_names=np.unique(y).astype('str'),
               filled = True)
plt.show()
dot_data = tree.export_graphviz(clf, out_file='out.txt')

