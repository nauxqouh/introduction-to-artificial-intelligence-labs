import queue
import matplotlib.pyplot as plt

# getting heuristics from file
def getHeuristics():
    heuristics = {}
    f = open("heuristics.txt")
    for i in f.readlines():
        node_heuristic_val = i.split()
        heuristics[node_heuristic_val[0]] = int(node_heuristic_val[1])

    return heuristics

def getCity():
    city = {}
    citiesCode = {}
    f = open("cities.txt")
    j = 1
    for i in f.readlines():
        node_city_val = i.split()
        city[node_city_val[0]] = [int(node_city_val[1]), int(node_city_val[2])]

        citiesCode[j] = node_city_val[0]
        j += 1

    return city, citiesCode

def createGraph():
    graph = {}
    file = open("citiesGraph.txt")
    for i in file.readlines():
        node_val = i.split()

        if node_val[0] in graph and node_val[1] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})

            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})

        elif node_val[0] in graph:
            c = graph.get(node_val[0])
            c.append([node_val[1], node_val[2]])
            graph.update({node_val[0]: c})

            graph[node_val[1]] = [[node_val[0], node_val[2]]]

        elif node_val[1] in graph:
            c = graph.get(node_val[1])
            c.append([node_val[0], node_val[2]])
            graph.update({node_val[1]: c})

            graph[node_val[0]] = [[node_val[1], node_val[2]]]

        else:
            graph[node_val[0]] = [[node_val[1], node_val[2]]]
            graph[node_val[1]] = [[node_val[0], node_val[2]]]
                                  
    return graph

def GBFS(startNode, heuristics, graph, goalNode):
    # priorityQueue to hold nodes to explore, sorted by heuristic value
    # visited is a list of nodes to keep track of visited nodes
    priorityQueue = queue.PriorityQueue()
    priorityQueue.put((heuristics[startNode], startNode))
    visited = set()
    
    path = []

    while priorityQueue.empty() == False:
        current = priorityQueue.get() [1]
        path.append(current)
        
        if current == goalNode:
            return path

        visited.add(current)
        for i in graph[current]:
            if i[0] not in visited:
                priorityQueue.put((heuristics[i[0]], i[0]))
    return None

def Astar(startNode, heuristics, graph, goalNode):
    # open_list is a list of nodes which have been visited, but not expanded
    # close_list is a list of nodes which have been expanded
    open_list = set([startNode])
    close_list = set([])
    
    # g contains current distances from start_node to all other nodes
    g = {}
    g[startNode] = 0
    
    # parent contains parent of all nodes
    parent = {}
    parent[startNode] = None
    
    path_found = False
    while open_list:
        current_node = None
        
        # find a node with the lowest f
        for node in open_list:
            if current_node == None or g[node] + heuristics[node] < g[current_node] + heuristics[current_node]:
                current_node = node
        
        # open_list is empty
        if current_node == None:
            raise Exception("No way Exception")
        
        # if current node is goal node, then reconstruction the path from it to the start_node
        if current_node == goalNode:
            path_found = True
            break

        # for all childs of current node
        for i in graph[current_node]:
            node = i[0]
            weight = int(i[1])
            # if child not in open list and close list, then add it into open list, save g and parent of it
            if node not in open_list and node not in close_list:
                open_list.add(node)
                g[node] = g[current_node] + weight
                parent[node] = current_node
            else: # if child have already existed in open list or close list, then calculate new g from start node to it
                new_g = g[current_node] + weight
                # update g, parent if new g is smaller than the value before
                if new_g < g[node]:
                    g[node] = new_g
                    parent[node] = current_node

                    # update node from close list
                    if node in close_list:
                        close_list.remove(node)
                        open_list.add(node)
        
        open_list.remove(current_node)
        close_list.add(current_node)
    
    path = []
    if path_found:
        end = goalNode
        path.append(end)
        while parent[end] is not None:
            path.append(parent[end])
            end = parent[end]
        path.reverse()
    return path     

def drawMap(city, gbfs, astar, graphmax):
    for i, j in city.items():
        plt.plot(j[0], j[1], "ro")
        plt.annotate(i, (j[0] + 5, j[1]))

        for k in graph[i]:
            n = city[k[0]]
            plt.plot([j[0], n[0]], [j[1], n[1]], "gray")

    for i in range(len(gbfs)):
        try:
            first = city[gbfs[i]]
            secend = city[gbfs[i+1]]

            plt.plot([first[0], secend[0]], [first[1], secend[1]], "green")
        except:
            continue

    for i in range(len(astar)):
        try:
            first = city[astar[i]]
            secend = city[astar[i+1]]

            plt.plot([first[0], secend[0]], [first[1], secend[1]], "blue")
        except:
            continue

    plt.errorbar(1, 1, label="GBFS", color="green")
    plt.errorbar(1, 1, label="ASTAR", color="blue")
    plt.legend(loc="lower left")

    plt.show()

if __name__ == "__main__":
    heuristic = getHeuristics()
    graph = createGraph()
    city, citiesCode = getCity()

    for i, j in citiesCode.items():
        print(i, j)

    while True:
        inputCode1 = int(input("Nhập đỉnh bắt đầu: "))
        inputCode2 = int(input("Nhập đỉnh kết thúc: "))

        if inputCode1 == 0 or inputCode2 == 0:
            break

        startCity = citiesCode[inputCode1]
        endCity = citiesCode[inputCode2]

        gbfs = GBFS(startCity, heuristic, graph, endCity)
        astar = Astar(startCity, heuristic, graph, endCity)
        print("GBFS => ", gbfs)
        print("ASTAR => ", astar)

        drawMap(city, gbfs, astar, graph)
