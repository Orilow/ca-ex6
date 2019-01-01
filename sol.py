import math
import numpy as np

with open('input.txt', 'r', encoding='utf-8') as f:
    temp = f.readline().split()
    N = int(temp[0])
    M = int(temp[1])
    RUSSIAN_ROOM = int(temp[2]) - 1
    MONEY = int(temp[3])

    doors = [[None, None] for _ in range(M)]
    for room in range(N):
        door_nums = f.readline().split()
        arr_len = int(door_nums[0])
        for num in range(1, arr_len + 1):
            door_num = int(door_nums[num]) - 1
            if doors[door_num][0] is None and doors[door_num][1] is None:
                doors[door_num][0] = room
            else:
                if doors[door_num][0] is None:
                    doors[door_num][0] = room
                else:
                    doors[door_num][1] = room

    door_price = ''.join(f.readlines()).split()

next_pseudo_node = N

for door in doors:
    if door[1] is None:
        door[1] = next_pseudo_node
        next_pseudo_node += 1

pseudo_N = next_pseudo_node
adj_matrix = np.array([[math.inf for _ in range(pseudo_N)] for _ in range(pseudo_N)])
for i in range(len(doors)):
    adj_matrix[doors[i][0]][doors[i][1]] = door_price[i]
    adj_matrix[doors[i][1]][doors[i][0]] = door_price[i]

exit_nodes = list(range(N, pseudo_N))


def dijkstra(nodes_count, start_node, matrix):
    valid = [True] * nodes_count
    weight = [math.inf] * nodes_count
    weight[start_node] = 0
    for _ in range(nodes_count):  # while all nodes are not marked
        min_weight = math.inf
        ID_min_weight = -1
        for i in range(len(weight)):  # find min distance edge to non-marked node
            if valid[i] and weight[i] < min_weight:
                min_weight = weight[i]
                ID_min_weight = i
        for i in range(nodes_count):
            if weight[ID_min_weight] + matrix[ID_min_weight][i] < weight[i]:
                weight[i] = weight[ID_min_weight] + matrix[ID_min_weight][i]
        valid[ID_min_weight] = False
    return weight


def get_min_exit_weight(weight):
    min_weight = math.inf
    for node in exit_nodes:
        if weight[node] <= MONEY and weight[node] < min_weight:
            min_weight = weight[node]
    if min_weight == math.inf:
        return -1
    return int(min_weight)


w = dijkstra(pseudo_N, RUSSIAN_ROOM, adj_matrix)
answer = get_min_exit_weight(w)

with open('output.txt', 'w', encoding='utf-8') as f:
    if answer == -1:
        f.write('N')
    else:
        f.write('Y\n{0}'.format(answer))
