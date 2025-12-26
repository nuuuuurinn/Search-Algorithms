import heapq

def read_input(filename = "input.txt"):
    with open(filename, "r") as f:
        line = f.readline().strip()
    M_left, C_left, M_right, C_right, boat, *model = line.split(",")
    return (int(M_left), int(C_left), int(M_right), int(C_right), boat.strip())

def conditions(state):
    M_left, C_left, M_right, C_right, boat = state
    if (M_left < 0 or M_left > 3) or (C_left < 0 or C_left > 3) or (M_right < 0 or M_right > 3) or (C_right < 0 or C_right > 3): 
        return False
    if (M_left > 0 and C_left > M_left) or (M_right > 0 and C_right > M_right): 
        return False
    return True

def get_successors(state):
    M_left, C_left, M_right, C_right, boat = state
    moves = [(1,0), (2,0), (0,1), (0,2), (1,1)]
    successors = []
    if boat == 'L':
        for m, c in moves:
            newstate = (M_left - m, C_left - c, M_right + m, C_right + c, 'R')
            if conditions(newstate):
                successors.append((newstate, (m, c)))
    else:
        for m, c in moves:
            newstate = (M_left + m, C_left + c, M_right - m, C_right - c, 'L')
            if conditions(newstate): 
                successors.append((newstate, (m, c)))
    return successors

def h1(state):
    M_left, C_left, M_right, C_right, boat = state
    return 2 * M_left + C_left

def h2(state):
    M_left, C_left, M_right, C_right, boat = state
    return (2 * M_left + C_left + 2) // 3

def a_star(initial, h):
    goal = (0, 0, 3, 3, 'R')
    fringe = []
    heapq.heappush(fringe, (h(initial), 0, initial, [initial])) #(f = h), path cost so far, current state, [path so far]
    visited = set()
    expansions = 0
    while fringe:
        f, g, state, path = heapq.heappop(fringe)
        if state[:4] == goal[:4]:
            return path, g, expansions
        if state in visited:
            continue
        visited.add(state)
        expansions += 1
        for succ, action in get_successors(state):
            if succ not in visited:
                cost = g + 2 * action[0] + 1 * action[1]
                new_f = cost + h(succ)
                heapq.heappush(fringe, (new_f, cost, succ, path + [succ]))
    return [], 0, expansions

if __name__=="__main__":
    init = read_input()

    path, cost, expansions = a_star(init, h1)
    print("The solution of Q3.1 (Heuristic 1) is:")
    print("Solution Path:", path)
    print(f"Total cost = {cost}")
    print(f"Number of node expansions = {expansions}")

    path, cost, expansions = a_star(init, h2)
    print("The solution of Q3.1 (Heuristic 2) is:")
    print("Solution Path:", path)
    print(f"Total cost = {cost}")
    print(f"Number of node expansions = {expansions}")