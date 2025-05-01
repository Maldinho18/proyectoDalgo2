import sys
from collections import deque
from typing import Optional, Dict, List, Tuple

def resolver_caso(n: int, energia: int, robots: list[int], poderes: Dict[int, int]) -> Optional[List[str]]:
    bloqueada = [False] * (n + 2)
    for r in robots:
        if 1 <= r <= n:
            bloqueada[r] = True
    
    padre = list(range(n + 2))
    
    def encontrar(x: int) -> int:
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x
    
    def union(a: int, b: int) -> None:
        pa, pb = encontrar(a), encontrar(b)
        if pa != pb:
            padre[pa] = pb
    for i in range(1, n + 1):
        if bloqueada[i]:
            union(i, i + 1)
    start = (0, energia)
    dq = deque([start])
    visited = set([start])
    parent_state: Dict[Tuple[int, int], Tuple[int, int, str]] = {}
    
    while dq:
        pos, e = dq.popleft()
        for mov, tag in ((pos + 1, 'C+'), (pos - 1, 'C-')):
            if 1 <= mov <= n and not bloqueada[mov]:
                nxt = (mov,e)
                if nxt not in visited:
                    visited.add(nxt)
                    parent_state[nxt] = (pos, e, tag)
                    dq.append(nxt)
                    if mov == n:
                        return reconstruir(n, e, parent_state)
                    dq.append(nxt)
        if pos in poderes:
            k = poderes[pos]
            for mov, tag in ((pos + k, 'S+'), (pos - k, 'S-')):
                if 1 <= mov <= n and not bloqueada[mov]:
                    nxt = (mov,e)
                    if nxt not in visited:
                        visited.add(nxt)
                        parent_state[nxt] = (pos, e, tag)
                        dq.append(nxt)
                        if mov == n:
                            return reconstruir(n, e, parent_state)
                        dq.append(nxt)
        low, high = max(1, pos - e), min(n, pos + e)
        j = encontrar(low)
        while j <= high:
            if j == pos:
                union(j, j + 1)
                j = encontrar(j)
                continue
            dist = abs(j - pos)
            ne = e - dist
            if ne < 0:
                break
            nxt = (j, ne)
            if nxt not in visited:
                visited.add(nxt)
                parent_state[nxt] = (pos, e, f"T{j - pos}")
                if j == n:
                    return reconstruir(n, ne, parent_state)
                dq.append(nxt)
            union(j, j + 1)
            j = encontrar(j)
    return None

def reconstruir(destino: int, energia_final:int, padre: Dict[Tuple[int, int], Tuple[int, int, str]]) -> list[str]:
    acciones: List[str] = []
    nodo = (destino, energia_final)
    while nodo in padre:
        ppos, pe, tag = padre[nodo]
        acciones.append(tag)
        nodo = (ppos, pe)
    acciones.reverse()
    return acciones

def main() -> None:
    data = sys.stdin.read().strip().splitlines()
    idx = 0
    while idx < len(data) and data[idx].strip() == "":
        idx += 1
    t = int(data[idx].strip()); idx += 1
    for _ in range(t):
        while data[idx].strip() == "":
            idx += 1
        n, energia = map(int, data[idx].split()); idx += 1
        while data[idx].strip() == "":
            idx += 1
        robots = list(map(int, data[idx].split())) if data[idx].strip() else []
        idx += 1
        while data[idx].strip() == "":
            idx += 1
        token_line = list(map(int, data[idx].split())) if data[idx].strip() else []
        idx += 1
        poderes = {(token_line[i]): (token_line[i + 1]) for i in range(0, len(token_line), 2)}
        resultado = resolver_caso(n, energia, robots, poderes)
        if resultado is None:
            print("No hay solución")
        else:
            print(len(resultado), *resultado)
            
if __name__ == "__main__":
    main()