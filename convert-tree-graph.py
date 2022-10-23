import re
import json
import html

with open('out.txt', 'r') as theFile:
    dotGraph = theFile.readlines()

modGraph = []
for line in dotGraph:

    # lines starting with integer only
    if len(re.findall(r"^[0-9]+", line)) > 0:
        modGraph.append(line)

nodeMaps = []
nodeDesc = []

# divide lines by type
for line in modGraph:
    if len(re.findall(r"[0-9]+", line)) == 2 or "labeldistance" in line:
        nodeMaps.append(line)
    else:
        nodeDesc.append(line)

# rename nodes
for y, node in enumerate(nodeMaps):
    node = node.split('->')
    if '[' in node[1]:
        node[1] = node[1].split('[')[0]
    for n, i in enumerate(node):
        reString = r"^" + re.escape(i.strip().replace(';', ''))
        
        for x in nodeDesc:
            if len(re.findall(reString, x)) > 0:
                node[n] = x
                break
        nodeMaps[y] = node

# format labelled nodes
for n, node in enumerate(nodeMaps):
    for y, part in enumerate(node):
        # extract integer id
        numId = ' '.join(part.split(' ')[:1])
        label = ' '.join(part.split(' ')[1:])
        numId = html.escape(numId)
        label = html.escape(label)
        label = label.replace('\\n', '<br>').replace("label=",'').replace("entropy=", "entropy:").replace("samples=", "samples:")
        replString = '<label for="{numId}">{label}</label><input id="{numId}" type="checkbox"'.format(numId = numId, label = numId)
        node[y] = replString
    nodeMaps[n] = node

# nest lists
nodeDict = {}
for relation in nodeMaps:
    if relation[0] in nodeDict.keys():
        nodeDict[relation[0]].append(relation[1])
    else:
        nodeDict[relation[0]] = [relation[1]]

# nested dictionary
layer = 0
def iterdict(d):
    for k,v in d.items():        
        for n, i in enumerate(v):
            if isinstance(k, dict):
                if i in d.keys():
                    if v[n] in k.keys():
                        d[k][v[n]].append(d[i])
                    else:
                        d.update({k: {v[n] : [[d[i]]]}})
                    if isinstance(d[k][v[n]], dict):
                        iterdict(d[k][v[n]])
            else:
                d.update({k: {v[n] : []}})
                d[k][v[n]].append(d[i])
            if isinstance(d[k][v[n]], dict):
                iterdict(d[k][v[n]])
    return(d)

nodeDict = iterdict(nodeDict)
print(json.dumps(nodeDict, indent = 4))


# nested dict to html
def convHtml(file, d):
    if isinstance(d, dict):
        file.write("<ul>\n")
        for k,v in d.items():
            file.write("<ul>\n")
            file.write('<span class="more">&hellip;</span>')
            file.write("<li>\n")
            file.write(k)

            for i in v:
                convHtml(file, i)

        file.write("</ul>\n")

    else:
        
        print('\n')

        print(d)
        if isinstance(d, str):
            file.write("<li>" + d + "</li>")

        else:
            for i in d:

                file.write("<li>" + d[n] + "</li>")
                convHtml(file, d[n])
                
            


with open('out.html', 'w') as the_file:
    convHtml(the_file, nodeDict)




