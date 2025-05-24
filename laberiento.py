from collections import deque

def find_shortest_path_inverted(maze):
    rows = len(maze)
    cols = len(maze[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)

    if maze[start[0]][start[1]] == 0 or maze[end[0]][end[1]] == 0:
        return [["X" for _ in row] for row in maze]

    queue = deque([(start, [start])])
    visited = {start}
    parent = {start: None}

    while queue:
        current, path = queue.popleft()
        if current == end:
            shortest_path = path
            result_maze = [["X" for _ in range(cols)] for _ in range(rows)]
            for r, c in shortest_path:
                result_maze[r][c] = "S"
            for r in range(rows):
                for c in range(cols):
                    if result_maze[r][c] != "S":
                        result_maze[r][c] = "."
            return result_maze

        r, c = current
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1 and (nr, nc) not in visited:
                visited.add((nr, nc))
                parent[(nr, nc)] = current
                queue.append(((nr, nc), path + [(nr, nc)]))

    result_maze = [["X" for _ in range(cols)] for _ in range(rows)]
    return result_maze

M = [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1]
]

E_maze = [
    [1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 0, 0, 1],
    [0, 1, 1, 1, 1]
]

M_maze = [
    [1, 1, 1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 1]
]

H_maze = [
    [1, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]
]

mazes = {"M(1)": M, "Easy_maze(2)": E_maze, "Medium_maze(3)": M_maze, "Hard_maze (4)": H_maze}

for name, maze in mazes.items():
    solution = find_shortest_path_inverted(maze)
    print(f"S = Camino que SÍ se puede tomar. \nSolucion para el laberiento {name}:")
    for row in solution:
        print(" ".join(row))
    print()