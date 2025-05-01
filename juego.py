import sys
from collections import deque
from typing import Optional, Dict, List, Tuple

sys.setrecursionlimit

def resolver_caso(n: int, energia: int, robots: list[int], poderes: dict[int, int]) -> Optional[List[str]]:
    bloqueada = [False] * (n + 2)
    for r in robots:
        if 1 <= r <= n:
            bloqueada[r] = True
    salto = poderes
    
    padre = list(range(n + 2))
    
    def encontrar(x) -> int:
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x
    def union(a, b) -> None:
        padre[encontrar(a)] = encontrar(b)
    for i in range(1, n + 1):
        if bloqueada[i]:
            union(i, i + 1)
    max_energy = [-1] * (n + 1)
    parent: Dict[Tuple[int, int], Tuple[Optional[int], Optional[int], Optional[str]]] = {}
    
    dq = deque([(0, energia)])
    max_energy[0] = energia
    parent[(0, energia)] = (None, None, None)
    
    while dq:
        pos, e = dq.popleft()
        for mov, etiqueta in [(pos+1, 'C+'), (pos-1, 'C-')]:
            if 0 <= mov <= n and not bloqueada[mov] and max_energy[mov] < e:
                max_energy[mov] = e
                parent[(mov, e)] = (pos, e, etiqueta)
                union(mov, mov + 1)
                if mov == n:
                    return reconstruir(n, e, parent)
                dq.append((mov, e))
        k = salto.get(pos)
        if k:
            for mov, etiqueta in [(pos + k, 'S+'), (pos - k, 'S-')]:
                if 0 <= mov <= n and not bloqueada[mov] and max_energy[mov] < e:
                    max_energy[mov] = e
                    parent[(mov, e)] = (pos, e, etiqueta)
                    union(mov, mov + 1)
                    if mov == n:
                        return reconstruir(n, e, parent)
                    dq.append((mov, e))
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
            etiqueta = f"T{j - pos}"
            if max_energy[j] < ne:
                max_energy[j] = ne
                parent[(j, ne)] = (pos, e, etiqueta)
                union(j, j + 1)
                if j == n:
                    return reconstruir(n, ne, parent)
                dq.append((j, ne))
            else:
                union(j, j + 1)
            j = encontrar(j + 1)
    return None

def reconstruir(destino: int, energia_final:int, padre: Dict[Tuple[int, int], Tuple[Optional[int], Optional[int], Optional[str]]]) -> list[str]:
    acciones = []
    nodo = (destino, energia_final)
    while True:
        prev = padre[nodo]
        if prev[0] is None:
            break
        acciones.append(prev[2])
        nodo = (prev[0], prev[1])
    acciones.reverse()
    return acciones

def main() -> None:
    t_line = sys.stdin.readline()
    while t_line.strip() == "":
        t_line = sys.stdin.readline()
    t = int(t_line)
    for _ in range(t):
        line = sys.stdin.readline()
        while line.strip() == "":
            line = sys.stdin.readline()
        n, energia = map(int, line.strip().split())
        line = sys.stdin.readline()
        while line.strip() == "":
            line = sys.stdin.readline()
        robots = list(map(int, line.strip().split())) if line.strip() else []
        line = sys.stdin.readline()
        while line.strip() == "":
            line = sys.stdin.readline()
        token_line = list(map(int, line.strip().split())) if line.strip() else []
        poderes = {(token_line[i]): (token_line[i + 1]) for i in range(0, len(token_line), 2)}
        resultado = resolver_caso(n, energia, robots, poderes)
        if resultado is None:
            print("No hay solución")
        else:
            print(len(resultado), *resultado)
if __name__ == "__main__":
    main()