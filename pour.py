import heapq
import sys
import time


class Node:
    """
    Třída reprezentující stavy lahví po jednotlivých přelitích, tudíž i vrcholy grafu.
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
    # Vytvoření prioritní fronty
    queue = [first_node]
    heapq.heapify(queue)
    # Vytvoření knihovny nalezených stavů
    states = {tuple(first_node.state): [first_node.cost, 0]}
    # Vytvoření listu cen a transfers pro všechny objemy
    max_vol = first_node.bottles[-1]
    costs = [float('inf')] * (max_vol+1)
    transfers = [float('inf')] * (max_vol+1)
    costs[max_vol] = 0
    transfers[max_vol] = 0
    # Vytvoření setu všech nenalezených objemů
    nums = set(range(1, max_vol+1))
    while queue:
        node = heapq.heappop(queue)
        # Porovnání nalezených objemů s nejnižšími dosavadními hodnotamy
        node_state = tuple(node.state)
        for volume in node_state:
            if node.cost < costs[volume]:
                costs[volume] = node.cost
                transfers[volume] = node.transfers
            elif node.cost == costs[volume]:
                transfers[volume] = min([transfers[volume], node.transfers])
        # Kontrola zda byly nalezeny všechny objemy v ceně nižší než prohledávaný node
        nums -= set(node.state)
        if len(set(nums)) == 0 and min(costs) < node.cost:
            return costs, transfers
        # Vytvoření nových nodes pomocí přelití
        for i, state in enumerate(node.state):
            if state != 0:
                for j in range(len(node.state)):
                    if i != j and node.state[j] != node.bottles[j]:
                        new_node = pour(node, i, j)
                        new_state = tuple(new_node.state)
                        # Kontrola zda je nový stav nový, nebo lépe hodnocený než stav jemu odpovídající
                        if new_state not in states or (new_node.cost, new_node.transfers) < tuple(states[new_state]):
                            states[new_state] = [new_node.cost, new_node.transfers]
                            heapq.heappush(queue, new_node)

    return costs, transfers


def pour(node, from_index, to_index):
    """
    Metoda provadějící přelití z lahve do lahve a tudíž i vytvoření new_node.
    """
    pour_amount = min([node.state[from_index], (node.bottles[to_index] - node.state[to_index])])
    new_cost = node.cost + pour_amount
    new_transfers = node.transfers + 1
    new_state = list(node.state)
    new_state[from_index] -= pour_amount
    new_state[to_index] += pour_amount
    return Node(node.bottles, new_state, new_cost, new_transfers)


def print_output(costs, transfers):
    """
    Vypíše vyžadovaný output ze získaných nejkratších cest k jednotlivím objemům.
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
    """
    max_volumes = [78, 75, 199, 106]
    max_volumes.sort()
    start_volume = ([0] * (len(max_volumes) - 1)) + [max_volumes[-1]]
    first_node = Node(max_volumes, start_volume, 0, 0)
    costs, transfers = create_nodes(first_node)
    print_output(costs, transfers)


if __name__ == "__main__":
    start = time.time()
    main()
    print(time.time() - start)
