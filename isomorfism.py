import time
from collections import defaultdict
from itertools import permutations
import random 

def is_regular(graph):
    degrees = [sum(row) for row in graph]
    return len(set(degrees)) == 1

def naive_isomorphism_check(adj1, adj2, max_attempts=1000):
    n = len(adj1)
    if n > 10: 
        return None
    
    for _ in range(max_attempts):
        perm = list(range(n))
        random.shuffle(perm)
        
        is_isom = True
        for i in range(n):
            for j in range(n):
                if adj1[i][j] != adj2[perm[i]][perm[j]]:
                    is_isom = False
                    break
            if not is_isom:
                break
        if is_isom:
            return True
    return False

def enhanced_color_refinement(adj1, adj2):
    n = len(adj1)
    
    if sum(sum(row) for row in adj1) != sum(sum(row) for row in adj2):
        return False
    
    degree_sequence1 = sorted(sum(row) for row in adj1)
    degree_sequence2 = sorted(sum(row) for row in adj2)
    if degree_sequence1 != degree_sequence2:
        return False
    
    if n <= 10:
        result = naive_isomorphism_check(adj1, adj2)
        if result is not None:
            return result
    
    if is_regular(adj1) and is_regular(adj2):
        return naive_isomorphism_check(adj1, adj2) if n <= 8 else False
    
    color1 = [sum(row) for row in adj1]
    color2 = [sum(row) for row in adj2]
    
    for _ in range(2 * n):
        color_map = {}
        new_color = 0
        
        new_color1 = []
        for v in range(n):
            neighbors = tuple(sorted(color1[u] for u in range(n) if adj1[v][u]))
            key = (color1[v], neighbors)
            if key not in color_map:
                color_map[key] = new_color
                new_color += 1
            new_color1.append(color_map[key])
        
        new_color2 = []
        for v in range(n):
            neighbors = tuple(sorted(color2[u] for u in range(n) if adj2[v][u]))
            key = (color2[v], neighbors)
            if key not in color_map:
                return False
            new_color2.append(color_map[key])
        
        if sorted(new_color1) != sorted(new_color2):
            return False
            
        if color1 == new_color1 and color2 == new_color2:
            break
            
        color1, color2 = new_color1, new_color2
    
    if n <= 15:
        return naive_isomorphism_check(adj1, adj2) or False
    
    return True

def process_graph_pairs(graphs):
    if not graphs:
        return
    
    print("|V| +++/--- CPU time")
    for idx, (n, adj1, adj2) in enumerate(graphs, 1):
        start_time = time.time()
        is_isomorphic = enhanced_color_refinement(adj1, adj2)
        elapsed_time = time.time() - start_time
        
        result = "+++" if is_isomorphic else "---"
        print(f"{idx}) n = {n} {result} {elapsed_time:.6f}")

def read_graphs(filename):
    """Lê os pares de grafos do arquivo"""
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        print("Certifique-se que o arquivo está no mesmo diretório do script.")
        return []
    
    graphs = []
    i = 0
    while i < len(lines):
        try:
            n = int(lines[i])
            i += 1
            
            adj1 = []
            for _ in range(n):
                adj1.append([int(x) for x in lines[i]])
                i += 1
            
            adj2 = []
            for _ in range(n):
                adj2.append([int(x) for x in lines[i]])
                i += 1
            
            graphs.append((n, adj1, adj2))
        except (IndexError, ValueError) as e:
            print(f"Erro ao processar linha {i+1}: {e}")
            break
    
    return graphs

def enhanced_color_refinement(adj1, adj2):
    """Implementa o algoritmo Color Refinement para verificar isomorfismo"""
    n = len(adj1)
    
    if sum(sum(row) for row in adj1) != sum(sum(row) for row in adj2):
        return False
    
    color1 = [sum(row) for row in adj1]
    color2 = [sum(row) for row in adj2]
    
    if sorted(color1) != sorted(color2):
        return False
    
    max_iter = 2 * n  
    
    for _ in range(max_iter):
        color_map = {}
        new_color = 0
        
        new_color1 = []
        for v in range(n):
            neighbors = tuple(sorted(color1[u] for u in range(n) if adj1[v][u]))
            key = (color1[v], neighbors)
            
            if key not in color_map:
                color_map[key] = new_color
                new_color += 1
            new_color1.append(color_map[key])
        
        new_color2 = []
        for v in range(n):
            neighbors = tuple(sorted(color2[u] for u in range(n) if adj2[v][u]))
            key = (color2[v], neighbors)
            
            if key not in color_map:
                return False
            new_color2.append(color_map[key])
        
        if sorted(new_color1) != sorted(new_color2):
            return False
            
        if color1 == new_color1 and color2 == new_color2:
            break
            
        color1, color2 = new_color1, new_color2
    
    return True

def process_graph_pairs(graphs):
    """Processa todos os pares de grafos e imprime os resultados"""
    if not graphs:
        return
    
    print("|V| +++/--- CPU time")
    for idx, (n, adj1, adj2) in enumerate(graphs, 1):
        start_time = time.time()
        is_isomorphic = enhanced_color_refinement(adj1, adj2)
        elapsed_time = time.time() - start_time
        
        result = "+++" if is_isomorphic else "---"
        print(f"{idx}) n = {n} {result} {elapsed_time:.6f}")

def main():
    filename = "instancias_isomorfismo.txt"
    
    graphs = read_graphs(filename)
    
    if graphs:
        process_graph_pairs(graphs)
    else:
        print("Nenhum grafo foi processado.")

if __name__ == "__main__":
    main()