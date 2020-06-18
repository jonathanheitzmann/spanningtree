import random

graphfile = open ('graph.txt', 'rt').read()
lineList = graphfile.split('\n')
nodes = {}

for singelLine in lineList:

    singelLine = singelLine.strip()

    #Node wird hinzugefügt
    if '=' in singelLine:
        nodeName, nodeID = singelLine.split('=')
        nodeName = nodeName.strip()
        nodeID = int(nodeID.replace(';','').strip())
        skipNode = True
        try:
            n = nodes[nodeName]
        except:
            skipNode = False
        for node in nodes:
            print(node)
            if nodes[node]['nodeID'] == nodeID:
                skipNode = True
        if skipNode == False:
            nodes[nodeName] = {'nodeID': nodeID, 'root': nodeName, 'cost': 0, 'nextHop': nodeName, 'msgCnt': 0, 'neighbourscost': {}}

    #Kosten zwischen zwei Nodes werden hinzugefügt
    if '-' in singelLine and ':' in singelLine:
        linkedNodes, cost = singelLine.split(':')
        node1, node2 = linkedNodes.split('-')
        cost = int(cost.replace(';','').strip())
        node1 = node1.strip()
        node2 = node2.strip()
        if node1 != node2:
            nodes[node1]['neighbourscost'][node2] = cost
            nodes[node2]['neighbourscost'][node1] = cost

maxCount = False
while maxCount == False:
    
    transmitterNode = random.choice(list(nodes))

    nodes[transmitterNode]['msgCnt']=nodes[transmitterNode]['msgCnt'] + 1
        
    receiverList = list(nodes[transmitterNode]['neighbourscost'])

    for receiverNode in receiverList:

        transmitterRoot = nodes[transmitterNode]['root']
        receiverRoot = nodes[receiverNode]['root']

        #die ID der jeweiligen Root wird verglichen die receiverNode übernimmt das Root mit der kleineren ID
        if nodes[transmitterRoot]['nodeID'] < nodes[receiverRoot]['nodeID']:
            nodes[receiverNode]['root'] = nodes[transmitterNode]['root']
            nodes[receiverNode]['cost'] = nodes[transmitterNode]['cost']+nodes[receiverNode]['neighbourscost'][transmitterNode]
            nodes[receiverNode]['nextHop'] = transmitterNode

        #Wenn die ID der jeweiligen Root gleich ist wird überprüft ob die kosten über die receiverNode günstiger sind
        if nodes[transmitterNode]['root'] == nodes[receiverNode]['root'] and nodes[receiverNode]['cost'] > nodes[transmitterNode]['cost']+nodes[receiverNode]['neighbourscost'][transmitterNode]:
            nodes[receiverNode]['cost'] = nodes[transmitterNode]['cost']+nodes[receiverNode]['neighbourscost'][transmitterNode]
            nodes[receiverNode]['nextHop'] = transmitterNode
    
    #maxCount bleibt True wenn alle Nodes mindestens 3 mal die Anzahl von Nodes aufgerufen wurden
    maxCount = True
    for node in nodes:
        if nodes[node]['msgCnt'] < len(nodes)*3:
            maxCount = False


rootName = nodes[transmitterNode]['root']

otuput = "Spanning-Tree {\n\n    Root: "+rootName+";\n"
for nodeName in nodes:
    if nodeName is not rootName:
        otuput = otuput+"    "+nodeName+" - "+nodes[nodeName]['nextHop']+";\n"
otuput = otuput + "}"
file = open("result.txt", "w")
file.write(otuput)
file.close()