import heapq
import sys


class Node:
    """
    Třída reprezentující stavy lahvý po jednotlivých přelitích, tudíž i vrcholy grafu.
    """
    def __init__(self, bottles, state, cost, transfers):
        self.bottles = bottles  # objemy nádob
        self.state = state  # aktuální stav nádob
        self.cost = cost  # celková doba přelití
        self.transfers = transfers  # počet přelití

    def __lt__(self, other):
        # potřebujeme porovnávat uzly podle ceny pro heapq
        return self.cost < other.cost


def create_nodes(first_node):
    """
    Řídící metoda tvorby nodes, využívající principu průchodu do šířky.
    """
    queue = [first_node]
    heapq.heapify(queue)
    nodes = [first_node]
    states = set()
    states.add(tuple(first_node.state))
    maximum = first_node.bottles[-1]
    while queue:
        if (len(set([numbers for tpl in states for numbers in tpl]))) == maximum+1:
            return nodes
        node = heapq.heappop(queue)
        # print("next", node.state, node.cost,)
        for i, state in enumerate(node.state):
            if state != 0:
                for j in range(len(node.state)):
                    if i != j and node.state[j] != node.bottles[j]:
                        new_node = pour(node, i, j)
                        if tuple(new_node.state) not in states:
                            states.add(tuple(new_node.state))
                            heapq.heappush(queue, new_node)
                            nodes.append(new_node)
                            # print("added")
    return nodes


def pour(node, from_index, to_index):
    """
    Metoda provadějící přelití z lahve do lahve a tudíž i vytvoření new_node.
    """
    # print(from_index, to_index)
    pour_amount = min([node.state[from_index], (node.bottles[to_index] - node.state[to_index])])
    new_cost = node.cost + pour_amount
    new_transfers = node.transfers + 1
    new_state = list(node.state)
    new_state[from_index] -= pour_amount
    new_state[to_index] += pour_amount
    # print(new_state, new_cost)
    return Node(node.bottles, new_state, new_cost, new_transfers)


def nodes_process(nodes, max_vol):
    """
    Z nalezených nodes najde nejkratší cesty k jednotlivým objemům.
    """
    costs = [float('inf')] * (max_vol+1)
    transfers = [float('inf')] * (max_vol+1)
    for node in nodes:
        for i in range(1, max_vol+1):
            if i in node.state and node.cost <= costs[i]:
                costs[i] = node.cost
                if node.cost == costs[i]:
                    transfers[i] = min([transfers[i], node.transfers])
                else:
                    transfers[i] = node.transfers
    return costs, transfers


def print_output(costs, transfers):
    """
    Vypíše vyžadovaný output ze získaných nejkradších cesty k jednotlivím objemům.
    """
    for i in range(1, len(costs)):
        print(i, end=" ")
        if costs[i] < float('inf'):
            print(costs[i], transfers[i])
        else:
            print()


def main():
    """
    Hlavní řídící funkce programu a funkce načítající vstupy.
    """
    # odsud zakomentovat pro spuštění bez sys.stdin
    max_volumes = []
    amount = 0
    for i, line in enumerate(sys.stdin):
        if i == 0:
            amount = int(line.strip().replace("\n", ""))
        if i != 0 and i <= amount:
            max_volumes.append(int(line.strip().replace("\n", "")))
    # zde zkonči zakomentování, odkomentuj max volumes
    # max_volumes = [10, 78, 106, 200]
    max_volumes.sort()
    start_volume = ([0] * (len(max_volumes) - 1)) + [max_volumes[-1]]
    first_node = Node(max_volumes, start_volume, 0, 0)
    nodes = create_nodes(first_node)
    costs, transfers = nodes_process(nodes, max_volumes[-1])
    print_output(costs, transfers)


if __name__ == "__main__":
    main()
