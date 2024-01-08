import pygame
import sys
from pygame.locals import *
from collections import defaultdict

# Initializing the Graph Class
class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def addNode(self, value):
        self.nodes.add(value)

    def addEdge(self, fromNode, toNode, distance):
        self.edges[fromNode].append(toNode)
        self.distances[(fromNode, toNode)] = distance

# Implementing Dijkstra's Algorithm
def dijkstra(graph, initial):
    visited = {initial: {"cost": 0, "neighbor": None}}
    path = defaultdict(list)

    nodes = set(graph.nodes)

    while nodes:
        minNode = None
        for node in nodes:
            if node in visited:
                if minNode is None:
                    minNode = node
                elif visited[node]["cost"] < visited[minNode]["cost"]:
                    minNode = node
        if minNode is None:
            break

        nodes.remove(minNode)
        currentCost = visited[minNode]["cost"]

        for neighbor in graph.edges[minNode]:
            weight = currentCost + graph.distances[(minNode, neighbor)]
            if neighbor not in visited or weight < visited[neighbor]["cost"]:
                visited[neighbor] = {"cost": weight, "neighbor": minNode}
                path[neighbor].append(minNode)

    return visited, path

# Pygame Initialization
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
NODE_RADIUS = 25
FONT_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a window
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Dijkstra Visualization")

# Function to draw the graph
def draw_graph(graph):
    screen.fill(WHITE)

    for node in graph.nodes:
        pygame.draw.circle(screen, BLACK, node_positions[node], NODE_RADIUS)
        font = pygame.font.Font(None, FONT_SIZE)
        text = font.render(node , True, WHITE)
        # text_rect = text.get_rect(center=(node_positions[0], node_positions[1]))
        screen.blit(text, (node_positions[node][0] - len(node) * 5, node_positions[node][1] - FONT_SIZE / 2))

    for edge, distance in graph.distances.items():
        pygame.draw.line(screen, BLACK, node_positions[edge[0]], node_positions[edge[1]], 2)
        text = font.render(str(distance), True, BLACK)
        text_rect = text.get_rect(center=((node_positions[edge[0]][0] + node_positions[edge[1]][0]) / 2,
                                          (node_positions[edge[0]][1] + node_positions[edge[1]][1]) / 2))
        screen.blit(text, text_rect)

# Function to draw the path
def draw_path(path, start, end):
    current = end
    while current != start:
        pygame.draw.line(screen, (0, 255, 0), node_positions[current], node_positions[path[current][0]], 4)
        current = path[current][0]

# Function to draw the routing table
def draw_routing_table(visited):
    text_surface = font.render("Routing Table", True, BLACK)
    screen.blit(text_surface, (WIDTH - 150, 20))
    y_position = 50

    for node, info in visited.items():
        text = font.render(f"{node}: Cost = {info['cost']}, Neighbor = {info['neighbor']}", True, BLACK)
        screen.blit(text, (WIDTH - 150, y_position))
        y_position += 30

# Main loop
font = pygame.font.Font(None, FONT_SIZE)

# User input for graph
node_positions = {}
num_nodes = int(input("Enter the number of nodes: "))
for i in range(num_nodes):
    node_name = input(f"Enter the name of node {i + 1}: ")
    x = int(input("Enter the x-coordinate: "))
    y = int(input("Enter the y-coordinate: "))
    node_positions[node_name] = (x, y)

customGraph = Graph()
for node in node_positions:
    customGraph.addNode(node)

num_edges = int(input("Enter the number of edges: "))
for i in range(num_edges):
    from_node = input(f"Enter the starting node for edge {i + 1}: ")
    to_node = input(f"Enter the ending node for edge {i + 1}: ")
    distance = int(input("Enter the distance/cost: "))
    customGraph.addEdge(from_node, to_node, distance)

start_node = input("Enter the starting node for Dijkstra's algorithm: ")
end_node = input("Enter the ending node for Dijkstra's algorithm: ")
visited, path = dijkstra(customGraph, start_node)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    draw_graph(customGraph)
    draw_path(path, start_node, end_node)
    draw_routing_table(visited)

    pygame.display.flip()

pygame.quit()
sys.exit()