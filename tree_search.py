import sys
import Queue as q

import collections
lines=[]
graph={}
out = open("output.txt", "w")
OrderedGraph = collections.OrderedDict({})
def bfs(start,end,fuel,alpha_graph):
    nopath_flag=0
    reserve = fuel
    explored = set()
    parent={}
    path=[]
    openset = collections.deque()#openset implementated as a queue in bfs
    openset.append(start)
    while openset:
        current = openset.popleft()
        explored.add(current)
        nopath_flag=0
        # if current == end:
        #     while current!=start and fuel<0:
        #         current=parent[current]
        #     out.write(current)
        #     return
        for child_node in alpha_graph[current].keys():
            if(nopath_flag):
                break
            print alpha_graph[current].keys()
            if child_node not in explored and child_node not in openset:
                if child_node != end:
                    parent[child_node] = current
                    openset.append(child_node)
                    #openset = list(child_node)+openset
                else:
                    while fuel>0:
                        fuel-=alpha_graph[child_node][current]
                        if(fuel<0):
                            fuel=reserve
                            nopath_flag=1
                            del path[:]
                            break
                        if current==start:
                            break
                        path.append(current)
                        child_node=current
                        current = parent[current]
                    if nopath_flag==0 and current==start:
                        out.write(start+"-")
                        for i in reversed(path):
                            out.write(i+"-")
                        out.write(end)
                        out.write(" ")
                        out.write(str(fuel))
                        return
    if(nopath_flag):
        out.write("No Path")



def dfs(start,end,fuel,alpha_graph):



   openset, explored =[start],set([]) #openset is implemented as a stack in dfs
   parent = {}
   reserve = fuel
   fuel_used = 0
   path=[]
   count=1
   for nodes in alpha_graph.keys():
        alpha_graph[nodes] = collections.OrderedDict(sorted(alpha_graph[nodes].items(), reverse = True))
   while openset:
        vertex = openset.pop()
        explored.add(vertex)
        nopath_flag=0
        if vertex == end:
            while vertex!=start and fuel > 0:
                temp=parent[vertex]
                fuel -= alpha_graph[temp][vertex]
                if (fuel < 0):
                    fuel = reserve
                    nopath_flag = 1
                    del path[:]
                    break
                if vertex == start:
                    break
                path.append(vertex)
                #child_node = vertex
                vertex = parent[vertex]
            # out.write(vertex)
            if nopath_flag == 0 and vertex == start:
                out.write(start + "-")
                for i in reversed(path):
                    out.write(i)
                    if count<len(path):
                        out.write("-")
                        count+=1
                out.write(" ")
                out.write(str(fuel))
                return
        c = alpha_graph[vertex].keys()
        c.sort()
        print c
        temp_2 = []
        for child_node in c:
            #alpha_graph[vertex][child_node] = collections.OrderedDict(sorted(alpha_graph[vertex][child_node].items(), reverse=True))
            if child_node not in explored:
                #openset.append(child_node)
                temp_2.append(child_node)
                # openset = list(child_node)+openset
                print "openset: ", openset
                parent[child_node] = vertex
            openset += sorted(temp_2, reverse=True)

   if(nopath_flag or len(openset)==0):
        out.write("No Path")


import heapq

def ucs2(start, end, fuel, alpha_graph):
    openset = []
    nopath_flag = 0
    reserve = fuel
    explored = set()
    parent = {}
    path = []
    path_cost = {}
    count=1
    heapq.heappush(openset, (0, start))
    check_open=[]

    while openset:
        weight, current = heapq.heappop(openset)
        explored.add(current)
        nopath_flag = 0
        path_cost.update({current:weight})
        if current == end:
            while current!=start and fuel > 0:
                temp = parent[current]
                fuel -= alpha_graph[temp][current]
                if (fuel < 0):
                    fuel = reserve
                    nopath_flag = 1
                    del path[:]
                    break
                if current == start:
                    break
                path.append(current)
                child_node = current
                current = parent[current]
            if nopath_flag == 0 and current == start:
                out.write(start + "-")
                for i in reversed(path):
                    out.write(i)
                    if count<len(path):
                        out.write("-")
                        count+=1

                out.write(" ")
                out.write(str(fuel))
                return
        for child_node in alpha_graph[current].keys():
            if (nopath_flag):
                break
            print alpha_graph[current].keys()
            for i in openset:
                check_open.append(i[1])
            print "hey", check_open
            if child_node not in explored and child_node not in check_open:
                if child_node != end:
                    parent[child_node] = current
                    weight = path_cost[current]+alpha_graph[current][child_node]
                    path_cost.update({child_node : weight})
                    #heapq.heappush(openset, (alpha_graph[current][child_node], child_node))
                    heapq.heappush(openset, (path_cost[child_node], child_node))
                else:
                    while fuel > 0:
                        fuel -= alpha_graph[child_node][current]
                        if (fuel < 0):
                            fuel = reserve
                            nopath_flag = 1
                            del path[:]
                            break
                        if current == start:
                            break
                        path.append(current)
                        child_node = current
                        current = parent[current]
                    if nopath_flag == 0 and current == start:
                        out.write(start + "-")
                        for i in reversed(path):
                            out.write(i + "-")
                        out.write(end)
                        out.write(" ")
                        out.write(str(fuel))
                        return
    if (nopath_flag):
        out.write("No Path")


def ucs(start,end,fuel,alpha_graph):
    #import Queue as q
    openset = q.PriorityQueue()# openset implementated as a priority queue in ucs
    nopath_flag = 0
    reserve = fuel
    explored = set()
    parent = {}
    path = []
    openset.put(start)
    while openset:
        current = openset.get()
        explored.add(current)
        nopath_flag = 0
        # if current == end:
        #     while current != start and fuel < 0:
        #         current = parent[current]
        #     out.write(current)
        #     return
        for child_node in alpha_graph[current].keys():
            if (nopath_flag):
                break
            print alpha_graph[current].keys()
            if child_node not in explored:
                if child_node != end:
                    parent[child_node] = current
                    openset.put(child_node)
                else:
                    while fuel > 0:
                        fuel -= alpha_graph[child_node][current]
                        if (fuel < 0):
                            fuel = reserve
                            nopath_flag = 1
                            del path[:]
                            break
                        if current == start:
                            break
                        path.append(current)
                        child_node = current
                        current = parent[current]
                    if nopath_flag == 0 and current == start:
                        out.write(start + "-")
                        for i in reversed(path):
                            out.write(i + "-")
                        out.write(end)
                        out.write(" ")
                        out.write(str(fuel))
                        return
    if (nopath_flag):
        out.write("No Path")


#out = open("output.txt", "w")

with open(sys.argv[2]) as input:
#with open("input") as input:
    line_count = 0
    lines.extend(input.read().splitlines())
    for line in lines:
        if line_count == 0:
            SEARCH = line
        elif line_count == 1:
            #FUEL = int(input.readline())
            FUEL = int(line)
        elif line_count == 2:
            SOURCE = line
        elif line_count == 3:
            DESTINATION = line
        else:
            line = line.strip()
            start = line.split(":")[0]
            OrderedGraph[start] = collections.OrderedDict({})
            list_nodes = line.split(":")[1]
            nodes = list_nodes.split(",")
            for node in nodes:
                node_name = node.split("-")[0].strip()
                node_fuel = int(node.split("-")[1])
                OrderedGraph[start][node_name] = node_fuel
            alpha_Graph = collections.OrderedDict(sorted(OrderedGraph.items()))
            for t in OrderedGraph.keys():
                alpha_Graph[t] = collections.OrderedDict(sorted(OrderedGraph[t].items()))
        line_count+=1
    if SEARCH == "BFS":
        bfs(SOURCE,DESTINATION,FUEL,alpha_Graph)
    elif SEARCH == "DFS":
        dfs(SOURCE,DESTINATION,FUEL,alpha_Graph)
    elif SEARCH =="UCS":
        ucs2(SOURCE,DESTINATION,FUEL,alpha_Graph)
    out.close()