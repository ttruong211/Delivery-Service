import sys
from graph import Graph, Vertex
from priority_queue import PriorityQueue
from collections import deque


class DeliveryService:
    def __init__(self) -> None:
        """
        Constructor of the Delivery Service class
        """
        self.city_map = None
        self.MST = None

    def buildMap(self, filename: str) -> None:
        # initialize new graph of map
        self.city_map = Graph()

        # open filename and create lists 
        with open(filename, 'r') as file:
            for line in file:
                node1, node2, cost = map(int, line.strip().split('|'))
                # add vertices and edges
                self.city_map.addEdge(node1, node2, cost)

    def isWithinServiceRange(self, restaurant: int, user: int, threshold: int) -> bool:
        # return False if the user node does exit
        if user not in self.city_map.vertList:
            return False

        # initialize new lists for visited vertex
        visited = []
        # create a deque starting at the user node
        queue = deque([(user, 0)])

        while queue:
            # remove current node from deque
            current_node, cost = queue.popleft()

            # skip node that exceed the threshold
            if cost > threshold:
                continue
            # return True if the user is within service range of restaurant
            if current_node == restaurant:
                return True
            # add vertex visited to list
            visited.append(current_node)

            for nextNode in self.city_map.getVertex(current_node).getConnections():
                if nextNode.getId() not in visited:
                    # get new cost
                    nextCost = cost + \
                        self.city_map.getVertex(
                            current_node).getWeight(nextNode)
                    # add new node to deque
                    queue.append((nextNode.getId(), nextCost))

        return False

    def buildMST(self, restaurant: int) -> None:
        # initialize a priority queue
        pq = PriorityQueue()
        # initialize a new graph for the Minimum Spanning Tree
        self.MST = Graph()
        # get vertex from restaurant
        v = self.city_map.getVertex(restaurant)
        # set distance of the restaurant vertext to 0
        v.setDistance(0)
        # build the priority queue with vertex distances
        pq.buildHeap([(v.getDistance(), v) for v in self.city_map])
        # initialize new lists for visited vertex
        visited = []
        while not pq.isEmpty():
            currentVert = pq.delMin()
            if currentVert not in visited:
                visited.append(currentVert)
                # add edges to the MST based on the current vertex's predecessor
                if currentVert.getPred() is not None:
                    pred = currentVert.getPred()
                    self.MST.addEdge(currentVert.getId(),
                                     pred.getId(), currentVert.getWeight(pred))
                # update distance in prioity queue
                for nextVert in currentVert.getConnections():
                    newCost = currentVert.getWeight(nextVert)
                    # update vertex if it's in the priority queue and a shorter path is found
                    if nextVert in pq and newCost < nextVert.getDistance():
                        nextVert.setPred(currentVert)
                        nextVert.setDistance(newCost)
                        pq.decreaseKey(nextVert, newCost)

    
    def minimalDeliveryTime(self, restaurant: int, user: int) -> int:
        # perform DFS 
        def dfs(current_node:int, target_node:int, visited:list[int]): 
            visited.append(current_node) 
            if target_node == current_node:
                return visited
            
            v = self.MST.getVertex(current_node)
            for nextVert in v.getConnections():
                if nextVert.getId() not in visited:
                    path = dfs(nextVert.getId(), target_node, visited)
                    if path:
                        return path

            visited.pop()
            return None
        
        # return -1 if either node does not exit 
        if restaurant not in self.MST.vertList or user not in self.MST.vertList:
            return -1

        # find the shortest path from restaurant to user
        visited_path = dfs(restaurant, user, [])  

        if visited_path:
        # initialize time as 0 
            time = 0 

            for i in range(len(visited_path) - 1): 
                # get total of minimal time from user and restaurant 
                time += self.MST.getVertex(visited_path[i]).getWeight(self.MST.getVertex(visited_path[i + 1])) 
        
            return time 
        return -1 
            
    
    def findDeliveryPath(self, restaurant: int, user: int) -> str:
        # return "INVALID" if either nodes do not exit 
        if restaurant not in self.city_map.vertList or user not in self.city_map.vertList:
            return "INVALID"
        
        # initialize a priority queue for Dijkstra's algorithm 
        pq = PriorityQueue()
        for vertex in self.city_map:
            # set distance to infinity
            vertex.setDistance(float('inf'))
            # set predecessor to None
            vertex.setPred(None)

        # get vertex from restaurant
        v = self.city_map.getVertex(restaurant)
        # set distance of the restaurant vertext to 0
        v.setDistance(0)
    
        pq.buildHeap([(v.getDistance(), v) for v in self.city_map])

        # initialize new lists for visited vertex
        visited = []  

        # perform Dijkstra's algorithm 
        while not pq.isEmpty():
            currentVert = pq.delMin() 
            if currentVert not in visited: 
                visited.append(currentVert) # add if not on the visited list 
                for nextVert in currentVert.getConnections():
                    newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)
                    if newDist < nextVert.getDistance():
                        nextVert.setDistance(newDist)
                        nextVert.setPred(currentVert)
                        pq.decreaseKey(nextVert, newDist)

        
        # build the path as a sequence of node IDs connected by arrows
        path_str = []
        current = user 
        while current != restaurant:
            path_str.insert(0, str(current))
            current = self.city_map.getVertex(current).getPred().getId()

        path_str.insert(0, str(restaurant))
        path = ""
        
        for node_id in path_str:
            path += f"{node_id} -> "
        
        path_result = path.rstrip(" -> ") 

        # calculate total time  
        visited_path = list(map(int, path_result.split("->"))) # list of nodes path removing "->"  

        # initialize time as 0
        time = 0

        for i in range(len(visited_path) - 1):
            # check if vertices do exit or do not exit  
            if self.city_map.getVertex(visited_path[i]) and self.city_map.getVertex(visited_path[i + 1]) is not None:
                time += self.city_map.getVertex(visited_path[i]).getWeight(self.city_map.getVertex(visited_path[i + 1]))

        if path_result:
            return f"{path_result} ({time})"
        
        return "INVALID"


    def findDeliveryPathWithDelay(self, restaurant: int, user: int, delay_info: dict[int, int]) -> str:
    
        path_result = self.findDeliveryPath(restaurant, user)

        if path_result == "INVALID":
            return "INVALID"

        # calculate total time with having traffic delays

        path_parts = path_result.split(" (")
        path_result = path_parts[0]
        path_elements = path_result.replace(" ", "").split("->") 
        # list of nodes path removing "->" and time 
        visited_path = [int(element) for element in path_elements] 

        # initialize time as 0
        time = 0

        for i in range(len(visited_path) - 1):
            # check if vertices exist
            if self.city_map.getVertex(visited_path[i]) and self.city_map.getVertex(visited_path[i + 1]) is not None:
                # add weight and traffic delay 
                time += (self.city_map.getVertex(visited_path[i]).getWeight(self.city_map.getVertex(visited_path[i + 1])) 
                         + delay_info.get(visited_path[i + 1], 0) 
            )

        return f"{path_result} ({time})"

    @staticmethod
    def nodeEdgeWeight(v):
        return sum([w for w in v.connectedTo.values()])

    @staticmethod
    def totalEdgeWeight(g):
        return sum([DeliveryService.nodeEdgeWeight(v) for v in g]) // 2

    @staticmethod
    def checkMST(g):
        for v in g:
            v.color = 'white'

        for v in g:
            if v.color == 'white' and not DeliveryService.DFS(g, v):
                return 'Your MST contains circles'
        return 'MST'

    @staticmethod
    def DFS(g, v):
        v.color = 'gray'
        for nextVertex in v.getConnections():
            if nextVertex.color == 'white':
                if not DeliveryService.DFS(g, nextVertex):
                    return False
            elif nextVertex.color == 'black':
                return False
        v.color = 'black'

        return True


