import dash_interactive_graphviz
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier 
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import pygraphviz
import dash_bootstrap_components as dbc

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


clf = DecisionTreeClassifier()

clf.fit(X_train, y_train)
fig, axes = plt.subplots(nrows = 1,ncols = 1, figsize = (3,3), dpi=300)

y_preds = clf.predict(X_test)

print('Accuracy: ', accuracy_score(y_test, y_preds))
accuracy = accuracy_score(y_test, y_preds)

dot_data = tree.export_graphviz(clf, out_file='out.txt', feature_names=X_train.columns, class_names = clf.classes_)

app = dash.Dash(__name__)

with open('out.txt', 'r') as the_file:
  initial_dot_source = the_file.read()

app.layout = html.Div(
    [
        html.Div(
            dash_interactive_graphviz.DashInteractiveGraphviz(id="gv"),
            style=dict(flexGrow=1, position="relative"),
        ),
        html.Div(
          [
          html.H2("Accuracy Level"),
          html.H3(accuracy),
          ]
        ),
        html.Div([
        html.Div(
            [
                dbc.Label("Choose the Features to Include"),
                dbc.Checkbox(
                        id="color-checkbox",
                        label="Color-Values",
                        value=False),
                dbc.Checkbox(
                        id="prop-checkbox",
                        label="Prop-Values",
                        value=False),
                dbc.Checkbox(
                        id="ratio-checkbox",
                        label="Ratio-Values",
                        value=False),
                    ],
                ),
                html.P(id="standalone-radio-check-output"),
    ]
        ),
        html.Div(
            [
                html.H3("Selected element"),
                html.Div(id="selected"),
                html.H3("Dot Source"),
                dcc.Textarea(
                    id="input",
                    value=initial_dot_source,
                    style=dict(flexGrow=1, position="relative"),
                ),
                html.H3("Engine"),
                dcc.Dropdown(
                    id="engine",
                    value="dot",
                    options=[
                        dict(label=engine, value=engine)
                        for engine in [
                            "dot",
                            "fdp",
                            "neato",
                            "circo",
                            "osage",
                            "patchwork",
                            "twopi",
                        ]
                    ],
                ),
                
            ],
            style=dict(display="flex", flexDirection="column"),
        ),
    ],
    style=dict(position="absolute", height="100%", width="100%", display="flex"),
)

@app.callback(
    Output("standalone-radio-check-output", "children"),
    [
        Input("color-checkbox", "value"),
        Input("prop-checkbox", "value"),
        Input("ratio-checkbox", "value"),
    ],
)

@app.callback(
    [Output("gv", "dot_source"), Output("gv", "engine")],
    [Input("input", "value"), Input("engine", "value")],
    
)
def display_output(value, engine):
    return value, engine


@app.callback(Output("selected", "children"), [Input("gv", "selected")])
def show_selected(value):
    return html.Div(value)


if __name__ == "__main__":
    app.run_server(debug=True)