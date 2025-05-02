import sys
from collections import deque

def resolver_caso(n: int, energia: int, robots: list[int], poderes: dict[int, int]) -> str:
    plataformas_seguras = {0, n} | {i for i in range(1, n) if i not in robots}
    
    visitado = [[False] * 101 for _ in range(n + 1)]
    padre = {}
    accion = {}
    
    cola = deque()
    cola.append((0, energia))
    visitado[0][energia] = True
    padre[(0, energia)] = None
    
    while cola:
        pos, en = cola.popleft()
        if pos == n:
            break
        
        for d, etiqueta in [(-1, "C-"), (1, "C+")]:
            nuevo = pos + d
            if 0 <= nuevo <= n and nuevo not in robots and not visitado[nuevo][en]:
                visitado[nuevo][en] = True
                padre[(nuevo, en)] = (pos, en)
                accion[(nuevo, en)] = etiqueta
                cola.append((nuevo, en))
                
        if pos in poderes:
            salto = poderes[pos]
            for d, etiqueta in [(-salto, "S-"), (salto, "S+")]:
                nuevo = pos + d
                if 0 <= nuevo <= n and nuevo not in robots and not visitado[nuevo][en]:
                    visitado[nuevo][en] = True
                    padre[(nuevo, en)] = (pos, en)
                    accion[(nuevo, en)] = etiqueta
                    cola.append((nuevo, en))
                    
        for destino in sorted(p for p in plataformas_seguras if p > pos):
            costo = destino - pos
            if en - costo < 0:
                break
            if not visitado[destino][en - costo]:
                visitado[destino][en - costo] = True
                padre[(destino, en - costo)] = (pos, en)
                accion[(destino, en - costo)] = f"T{costo}"
                cola.append((destino, en - costo))
                
        for destino in sorted((p for p in plataformas_seguras if p < pos), reverse=True):
            costo = pos - destino
            if en - costo < 0:
                break
            if not visitado[destino][en - costo]:
                visitado[destino][en - costo] = True
                padre[(destino, en - costo)] = (pos, en)
                accion[(destino, en - costo)] = f"T-{costo}"
                cola.append((destino, en - costo))
                
    estado_final = None
    for e in range(101):
        if visitado[n][e]:
            estado_final = (n, e)
            break
    if estado_final is None:
        return "NO SE PUEDE"
    
    camino = []
    actual = estado_final
    while padre[actual] is not None:
        camino.append(accion[actual])
        actual = padre[actual]
    camino.reverse()
    
    return f"{len(camino)} {' '.join(camino)}"

def main()->None:
    data = sys.stdin.read().strip().splitlines()
    idx = 0
    while idx < len(data) and data[idx].strip() == "":
        idx += 1
    t = int(data[idx].strip()); idx += 1
    for _ in range(t):
        while data [idx].strip() == "":
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
        print(resultado)
        
if __name__ == "__main__":
    main()