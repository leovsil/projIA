#!/usr/bin/env python3
# slitherlink.py: Template para implementação do projeto de Inteligência Artificial 2025/2026.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import random, copy
from sys import stdin
from collections import defaultdict

import utils
from utils import *

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

UNKNOWN = -1
INACTIVE = 0
ACTIVE = 1

DOT = None
CORNER = None

TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

TOP_RIGHT = 0
BOTTOM_RIGHT = 1
BOTTOM_LEFT = 2
TOP_LEFT = 3


class SlitherlinkState:
    state_id = 0


    def __init__(self, board):
        self.board = board
        self.id = SlitherlinkState.state_id
        SlitherlinkState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de Slitherlink."""
    def __init__(self, nrows:int, ncolumns:int, board:list):
        self.nrows = nrows
        self.ncolumns = ncolumns
        self.board = board

    def adjacent_cell(self, cell:tuple) -> list:
        """Devolve uma lista das células que fazem
        fronteira com a célula enviada no argumento"""
        adjacent_cells = []
        row, column = cell

        #top right bottom left
        if row > 1:
            adjacent_cells.append((row - 2, column))
        else:
            adjacent_cells.append(None)

        if column < 2 * self.ncolumns - 1:
            adjacent_cells.append((row, column + 2))
        else:
            adjacent_cells.append(None)

        if row < 2 * self.nrows - 1:
            adjacent_cells.append((row + 2, column))
        else:
            adjacent_cells.append(None)

        if column > 1:
            adjacent_cells.append((row, column - 2))
        else:
            adjacent_cells.append(None)

        return adjacent_cells

    def diagonal_cell(self, cell:tuple) -> list:
        """Devolve uma lista das células na diagonal
        da célula enviada no argumento"""
        diagonal_cells = []
        row,column = cell

        #Top-Right Bottom-Right Bottom-Left Top-Left
        if (self.is_in_board((row-2,column+2))):
            diagonal_cells.append((row-2,column+2))
        else:
            diagonal_cells.append(None)
        
        if (self.is_in_board((row+2,column+2))):
            diagonal_cells.append((row+2,column+2))
        else:
            diagonal_cells.append(None)

        if (self.is_in_board((row+2,column-2))):
            diagonal_cells.append((row+2,column-2))
        else:
            diagonal_cells.append(None)

        if (self.is_in_board((row-2,column-2))):
            diagonal_cells.append((row-2,column-2))
        else:
            diagonal_cells.append(None)

        return diagonal_cells
    
    def is_in_board(self, cell_or_edge: tuple) -> bool: #check
        r,c = cell_or_edge
        if r < 0 or r > 2 * self.nrows:
            return False
        if c < 0 or c > 2 * self.ncolumns:
            return False
        return True

    def activate_edge(self, edge: tuple) -> None:
        if (not self.is_in_board(edge)):
            return
        r,c = edge
        self.board[r][c] = ACTIVE

    def deactivate_edge(self, edge:tuple) -> None:
        if (not self.is_in_board(edge)):
            return
        r,c = edge
        self.board[r][c] = INACTIVE

    def deactivate_zero(self, cell:tuple) -> None:
        if (not self.is_in_board(cell)):
            return
        for edge in self.get_cell_edges(cell[0],cell[1]):
            self.deactivate_edge(edge)

    def activate_corner(self, cell:tuple, corner_pos: int):
        r,c = cell
        if (corner_pos == TOP_RIGHT):
            self.activate_edge((r-1,c))
            self.activate_edge((r,c+1))

        elif (corner_pos == BOTTOM_RIGHT):
            self.activate_edge((r,c+1))
            self.activate_edge((r+1,c))

        elif (corner_pos == BOTTOM_LEFT):
            self.activate_edge((r+1,c))
            self.activate_edge((r,c-1))

        elif (corner_pos == TOP_LEFT):
            self.activate_edge((r,c-1))
            self.activate_edge((r-1,c))

    def deactivate_corner(self, cell:tuple, corner_pos: int):
        r,c = cell
        if (corner_pos == TOP_RIGHT):
            self.deactivate_edge((r-1,c))
            self.deactivate_edge((r,c+1))

        elif (corner_pos == BOTTOM_RIGHT):
            self.deactivate_edge((r,c+1))
            self.deactivate_edge((r+1,c))

        elif (corner_pos == BOTTOM_LEFT):
            self.deactivate_edge((r+1,c))
            self.deactivate_edge((r,c-1))

        elif (corner_pos == TOP_LEFT):
            self.deactivate_edge((r,c-1))
            self.deactivate_edge((r-1,c))

    def activate_corner_2(self, cell: tuple, corner_pos: int):
        r, c = cell

        if corner_pos == TOP_LEFT:
            self.activate_edge((r - 1, c + 2))
            self.activate_edge((r + 2, c - 1))

        elif corner_pos == TOP_RIGHT:
            self.activate_edge((r - 1, c - 2))
            self.activate_edge((r + 2, c + 1))

        elif corner_pos == BOTTOM_LEFT:
            self.activate_edge((r + 1, c + 2))
            self.activate_edge((r - 2, c - 1))

        elif corner_pos == BOTTOM_RIGHT:
            self.activate_edge((r + 1, c - 2))
            self.activate_edge((r - 2, c + 1))
            
    #Defined cases
    def fill_3_adjacent_0(self, cell:tuple, cell0:tuple, pos0:int) -> None: #pos0 é a inidce da posicao da celula 0
        self.deactivate_zero(cell0) #desativa todas as arestas da célula 0
        edges=self.get_cell_edges(cell[0],cell[1]) #edges da celula 3
        for i in range(4):
            if i != pos0:
                self.activate_edge(edges[i]) #ativar as edges que nao estao em contacto com o 0 (mesmo indice da posiçao)

        print(f"pos0: {pos0} ")
        if (pos0 == TOP or pos0 == BOTTOM): #se o 0 estiver em cima ou em baixo
            row = (cell[0] + cell0[0]) // 2 #row da aresta entre o 3 e o 0
            column = cell[1]
            print(f"row,column: ({row},{column})")
            self.activate_edge((row,column-2))
            self.activate_edge((row,column+2))

        elif (pos0 == RIGHT or pos0 == LEFT):
            column = (cell[1] + cell0[1]) // 2
            row = cell[1]
            self.activate_edge((row+2,column))
            self.activate_edge((row-2,column))

    
    def fill_3_diagonal_0(self, cell:tuple, cell0: tuple, pos0: int) -> None:
        self.deactivate_zero(cell0)
        edges=self.get_cell_edges(cell[0],cell[1]) #edges da celula 3
        #ativar as edges mais perto do 0
        self.activate_edge(edges[pos0]) 
        self.activate_edge(edges[(pos0 + 1)%4])

    def case_3_diagonal(self, cell: tuple) -> bool:
        """Verifica se a célula dada corresponde
        a um 3 com um 0 diagonal"""          
        diagonal_cells = self.diagonal_cell(cell)
        for i in range(4):
            diag = diagonal_cells[i]  
            if diag!=None and self.get_cell_value(diag)==0: #tem uma célula adjacente com o valor 0
                self.fill_3_diagonal_0(cell, diag, i)
                return True
            if diag!=None and self.get_cell_value(diag)==3: #tem uma célula adjacente com o valor 3
                self.fill_3_diagonal_3(cell, diag, i)
                return True
        return False
    
    
    def case_3_adjacent(self, cell: tuple) -> bool: 
        """Verifica se a célula dada corresponde
        a um 3 com um 0 adjacente e 3 adjacente"""
        adjacent_cells = self.adjacent_cell(cell) #células adjacentes à celula dada
        for i in range(4): #percorre as diferentes 4 opções
            adj = adjacent_cells[i]  
            if adj!=None and self.get_cell_value(adj)==0: #tem uma célula adjacente com o valor 0
                self.fill_3_adjacent_0(cell, adj, i)
                return True
            if adj!=None and self.get_cell_value(adj)==3: #verifica que tem uma célula adjacente com valor 3
                self.fill_3_adjacent_3(cell, adj, i)
                return True
        return False
    
    
    def fill_3_adjacent_3(self, cell: tuple, cell3: tuple, pos3: int) -> None:
        edges = self.get_cell_edges(cell[0], cell[1])
        edges_cell3 = self.get_cell_edges(cell3[0], cell3[1])

        shared_edge = edges[pos3]
        self.activate_edge(shared_edge)

        self.activate_edge(edges[(pos3 + 2) % 4])#aresta exterior da célula atual
        self.activate_edge(edges_cell3[pos3])# Aresta exterior da célula adjacente

        r, c = shared_edge
        if pos3 == RIGHT or pos3 == LEFT:
            self.deactivate_edge((r - 2, c))
            self.deactivate_edge((r + 2, c))

        elif pos3 == TOP or pos3 == BOTTOM:
            self.deactivate_edge((r, c - 2))
            self.deactivate_edge((r, c + 2))

    
    
    def fill_3_diagonal_3(self, cell: tuple, cell3: tuple, pos3: int) -> None: #usar o activate corner 
        dot = ((cell[0] + cell3[0]) // 2, (cell[1] + cell3[1]) // 2)
        #print(dot)
        edges = self.get_cell_edges(cell[0], cell[1])
        edges_cell3 = self.get_cell_edges(cell3[0], cell3[1])

        edges_dot = self.get_cell_edges(dot[0], dot[1])
        #print(edges_dot)
        for i in edges:
            if i not in edges_dot:
                self.activate_edge(i)
        for i in edges_cell3:
            if i not in edges_dot:
                self.activate_edge(i)

    def fill_2_diagonal_double_3 (self, diag:tuple, other_diag:tuple, posDiag:int):
        if (posDiag == TOP_RIGHT):
            self.activate_corner(diag, TOP_RIGHT)
            self.activate_corner(other_diag, BOTTOM_LEFT)
        elif (posDiag == BOTTOM_RIGHT):
            self.activate_corner(diag, BOTTOM_RIGHT)
            self.activate_corner(other_diag, TOP_LEFT)

    def case_2_diagonal_double_3 (self, cell:tuple) -> bool:
        """Verifica se a célula dada corresponde
        a um 2 com dois 3 numa das diagonais"""          
        diagonal_cells = self.diagonal_cell(cell)
        for i in range(2):
            diag = diagonal_cells[i] 
            other_diag = diagonal_cells[i + 2]
            if diag!=None and other_diag!=None and self.get_cell_value(diag)==3 and self.get_cell_value(other_diag)==3:
                self.fill_2_diagonal_double_3(diag, other_diag, i)
                return True
        return False
    
    
    def case_corner(self, cell: tuple) -> bool:
        """Verifica se a célula está num canto do tabuleiro.
        Se for 3, ativa o canto.
        Se for 2, aplica o caso do 2 no canto.
        Se for 1, desativa o canto.
        """

        cell_value = self.get_cell_value(cell)
        adjacent_cells = self.adjacent_cell(cell)

        position = None

        if adjacent_cells[TOP] is None and adjacent_cells[LEFT] is None:
            position = TOP_LEFT

        elif adjacent_cells[TOP] is None and adjacent_cells[RIGHT] is None:
            position = TOP_RIGHT

        elif adjacent_cells[BOTTOM] is None and adjacent_cells[RIGHT] is None:
            position = BOTTOM_RIGHT

        elif adjacent_cells[BOTTOM] is None and adjacent_cells[LEFT] is None:
            position = BOTTOM_LEFT

        # Se não está num canto, não faz nada
        if position is None:
            return False

        if cell_value == 3:
            self.activate_corner(cell, position)
            return True

        elif cell_value == 2:
            self.activate_corner_2(cell, position)
            return True

        elif cell_value == 1:
            self.deactivate_corner(cell, position)
            return True
        
        return False
    

    def check_defined_cases(self) -> None:
        """Verifica se existem casos padrão de
        resolução, e devolve a célula onde ocorre"""
        for r in range(1, 2*self.nrows, 2):
            for c in range(1, 2*self.ncolumns, 2):
                val = self.get_cell_value((r,c))
                if val == 3:
                    if (self.case_3_adjacent_0((r,c))):
                        continue
                    elif (self.case_3_diagonal_0((r,c))):
                        continue
                    elif (self.case_3_adjacent_3((r,c))):
                        continue
                    elif (self.case_3_diagonal_3((r,c))):
                        continue
                    elif(self.case_corner_3((r,c))):
                        continue
                elif val == 2:
                    if (self.case_2_diagonal_double_3((r,c))):
                        continue
                elif val == 0:
                    self.deactivate_zero((r,c))

    def get_cell_value(self, cell:tuple) -> int:
        r,c = cell
        return self.board[r][c]

    def get_cell_edges(self, row:int, column:int) -> list:
        """Devolve as arestas da célula enviada no argumento"""
        return [
            (row - 1, column),  # top
            (row, column + 1),  # right
            (row + 1, column),  # bottom
            (row, column - 1),  # left
        ]

    def get_cell_active_edges(self, row:int, column:int):
        """Devolve as arestas ativas da célula ou ponto enviado"""
        active_edges = []
        #Top Right Bottom Left
        if row > 1 and self.get_cell_value((row-1,column)) == ACTIVE:
            active_edges.append((row - 1, column))

        if column < 2 * self.ncolumns - 1 and self.get_cell_value((row, column + 1)) == ACTIVE:
            active_edges.append((row, column + 1))

        if row < 2 * self.nrows - 1 and self.get_cell_value((row + 1, column)) == ACTIVE:
            active_edges.append((row + 1, column))

        if column > 1 and self.get_cell_value((row, column - 1)) == ACTIVE:
            active_edges.append((row, column - 1))

        return active_edges

    def get_cell_active_edges_amount(self, row:int, column:int) -> int:
        """Devolve o número de arestas ativas"""
        return sum(1 for r, c in self.get_cell_edges(row, column) if self.board[r][c] == ACTIVE)

    def get_cell_inactive_edges_amount(self, row:int, column:int) -> int:
        """Devolve o número de arestas inativas"""
        return sum(1 for r,c in self.get_cell_edges(row,column) if self.board[r][c] == INACTIVE)

    def get_amount_of_active_edges(self) -> int:
        """Devolve o número total de arestas
        ativas no tabuleiro"""
        active_edges = 0
        for r in range(0, 2*self.nrows + 1):
            start_idx = (r%2 + 1)%2
            for c in range(start_idx, 2*self.ncolumns + 1, 2):
                if self.get_cell_value((r,c)) == ACTIVE:
                    active_edges+=1
        return active_edges

    def get_active_edges(self) -> list:
        """Devolve uma lista que contém as arestas
        ativas do tabuleiro"""
        active_edges= []
        for r in range(0, 2*self.nrows + 1):
            start_idx = (r%2 + 1)%2
            for c in range(start_idx, 2*self.ncolumns + 1, 2):
                if self.get_cell_value((r,c)) == ACTIVE:
                    active_edges.append((r,c))
        return active_edges

    def get_unknown_edges(self) -> list:
        """Devolve uma lista que contém as arestas
        indecididas do tabuleiro"""
        unknown_edges= []
        for r in range(0, 2*self.nrows + 1):
            start_idx = (r%2 + 1)%2
            for c in range(start_idx, 2*self.ncolumns + 1, 2):
                if self.get_cell_value((r,c)) == UNKNOWN:
                    unknown_edges.append((r,c))
        return unknown_edges
    
    def valid_dots(self)->bool:
        for r in range(0, 2*self.nrows + 1, 2):
            for c in range(0, 2*self.ncolumns + 1,2):
                active_edges = self.get_cell_active_edges_amount(r,c)
                if active_edges not in (0,2) :
                    return False
        return True
    
    def is_edge_vertical(self, edge:tuple) -> bool:
        return edge[0]%2

    def get_next_edge_and_dot(self, edge:tuple, previous_dot: tuple = None) -> tuple:
        r,c = edge
        if self.is_edge_vertical(edge):
            edge_dots = [(r-1,c),(r+1,c)]
        else:
            edge_dots = [(r,c-1),(r,c+1)]

        if previous_dot == None or previous_dot == edge_dots[0]:
            next_idx = 1
        else:
            next_idx = 0

        next_dot = edge_dots[next_idx]
        #Aqui podemos assumir que o ponto tem exatamente duas active edges
        for cell_edge in self.get_cell_active_edges(*next_dot):
            if edge != cell_edge:
                return cell_edge, next_dot

    def check_loop(self) -> bool:
        active_edges = self.get_active_edges()
        if not active_edges:
            return False
        first_edge = active_edges[0]
        current_edge = first_edge
        previous_dot = None
        processed_edges = 1
        while True:
            current_edge, previous_dot = self.get_next_edge_and_dot(current_edge, previous_dot)
            if current_edge == first_edge:
                break
            processed_edges+=1
        return processed_edges == len(active_edges)

    def valid_clues(self) -> bool:
        for r in range(1, 2*board.nrows, 2):
            for c in range(1, 2*board.ncolumns, 2):
                cell = self.get_cell_value((r,c))
                if cell!=DOT and self.get_cell_active_edges_amount(r,c) != cell:
                    return False
        return True

    def output_board(self) -> str:
        """Devolve o output da board"""
        output = ""
        for i in range(1, 2*self.nrows+1, 2):
            for j in range(1, 2*self.ncolumns+1, 2):
                edges = self.get_cell_edges(i,j)
                for edge in edges:
                    r,c = edge
                    output += "1" if self.board[r][c] == ACTIVE else "0"
                if j != 2*self.ncolumns-1:
                    output += '\t'
            output += '\n'
        return output
    
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        data = stdin.read().strip()
        rows = data.split('\n')
        board = [row.split() for row in rows]
        nrows = len(board)
        ncolumns = len(board[0])
        final_board = []
        current_row = 0

        for i in range(nrows):
            final_board.append([])
            for j in range(ncolumns):
                final_board[current_row].append(CORNER)
                final_board[current_row].append(UNKNOWN)
            final_board[current_row].append(CORNER)
            current_row+=1
            final_board.append([])
            for j in range(ncolumns):
                final_board[current_row].append(UNKNOWN)
                clue = board[i][j]
                final_board[current_row].append(DOT if clue == '.' else int(clue))
            final_board[current_row].append(UNKNOWN)
            current_row+=1

        final_board.append([])
        for j in range(ncolumns):
            final_board[current_row].append(CORNER)
            final_board[current_row].append(UNKNOWN)
        final_board[current_row].append(CORNER)

        return Board(nrows, ncolumns, final_board)
    
    # TODO: outros metodos da classe

class Slitherlink(Problem):
    def __init__(self, board: Board, gui=None):
        """O construtor especifica o estado inicial."""
        pass


    def actions(self, state: SlitherlinkState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        return state.board.get_unknown_edges()

    def result(self, state: SlitherlinkState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: SlitherlinkState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        return state.board.valid_dots() and state.board.check_loop() and state.board.valid_clues()
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass



board = Board.parse_instance()

print(f"Board {board.nrows}x{board.ncolumns}")

print("Clues:")
for r in range(1, 2*board.nrows, 2):
    row_clues = [str(board.board[r][c]) for c in range(1, 2*board.ncolumns, 2)]
    print("  " + " ".join(row_clues))

board.activate_edge((0, 1))
print(f"\nArestas ativas em célula (1,1): {board.get_active_edges(1, 1)}")

print("\nOutput board:")
print(board.output_board())

for r in range(1, 2*board.nrows, 2):
    for c in range(1, 2*board.ncolumns, 2):
        val = board.get_cell_value((r,c))
        if val == 3:
            if (board.case_3_adjacent((r,c))):
                continue
            elif (board.case_3_diagonal((r,c))):
                continue
            elif(board.case_corner((r,c))):
                continue
        elif val == 2:
            if (board.case_2_diagonal_double_3((r,c))):
                continue
            if (board.case_corner((r,c))):
                continue
        elif val == 1:
            if (board.case_corner((r,c))):
                continue
        elif val == 0:
            board.deactivate_zero((r,c))


print("\nOutput board:")
print(board.output_board())

print("\nBoard state:")
edge_h = {-1: '?', 0: 'x', 1: '-'}
edge_v = {-1: '?', 0: 'x', 1: '|'}

for r in range(2 * board.nrows + 1):
    row_str = ""
    for c in range(2 * board.ncolumns + 1):
        val = board.board[r][c]
        if r % 2 == 0 and c % 2 == 0:   # canto
            row_str += '+'
        elif r % 2 == 0:                  # aresta horizontal
            row_str += edge_h.get(val, '?') * 3
        elif c % 2 == 0:                  # aresta vertical
            row_str += edge_v.get(val, '?')
        else:                             # célula
            row_str += f' {val if val is not None else "."} '
    print(row_str)

print(board.get_unknown_edges())