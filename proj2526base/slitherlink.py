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


    def case_3_adjacent_0(self, cell: tuple) -> bool: #nao devia devolver None??
        """Verifica se a célula dada corresponde
        a um 3 com um 0 adjacente"""
        adjacent_cells = self.adjacent_cell(cell)
        for i in range(4):
            adj = adjacent_cells[i]  
            if adj!=None and self.get_cell_value(adj)==0: #tem uma célula adjacente com o valor 0
                self.fill_3_adjacent_0(cell, adj, i)
                return True
        return False
    
    def fill_3_diagonal_0(self, cell:tuple, cell0: tuple, pos0: int) -> None:
        self.deactivate_zero(cell0)
        edges=self.get_cell_edges(cell[0],cell[1]) #edges da celula 3
        #ativar as edges mais perto do 0
        self.activate_edge(edges[pos0]) 
        self.activate_edge(edges[(pos0 + 1)%4])

    def case_3_diagonal_0(self, cell: tuple) -> bool:
        """Verifica se a célula dada corresponde
        a um 3 com um 0 diagonal"""          
        diagonal_cells = self.diagonal_cell(cell)
        for i in range(4):
            diag = diagonal_cells[i]  
            if diag!=None and self.get_cell_value(diag)==0: #tem uma célula adjacente com o valor 0
                self.fill_3_diagonal_0(cell, diag, i)
                return True
        return False

    def case_3_adjacent_3 (self, cell: tuple) -> bool: 
        """Verifica se a célula dada corresponde
        a um 3 com um 3 adjacente"""
        adjacent_cells = self.adjacent_cell(cell) #células adjacentes à celula dada
        for i in range(4): #percorre as diferentes 4 opcões
            adj = adjacent_cells[i]
            if adj!=None and self.get_cell_value(adj)==3: #verifica que tem uma célula adjacente com valor 3
                self.fill_3_adjacent_3(cell, adj, i)
                return True
        return False

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
                self.fill_2_diagonal_double_3(cell, diag, i)
                return True
        return False
    

    def check_defined_cases(self) -> tuple:
        """Verifica se existem casos padrão de
        resolução, e devolve a célula onde ocorre"""
        pass

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

    def get_active_edges(self, row:int, column:int) -> int:
        """Devolve o número de arestas ativas"""
        return sum(1 for r, c in self.get_cell_edges(row, column) if self.board[r][c] == ACTIVE)

    def get_inactive_edges(self, row:int, column:int) -> int:
        """Devolve o número de arestas inativas"""
        return sum(1 for r,c in self.get_cell_edges(row,column) if self.board[r][c] == INACTIVE)

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
        # TODO
        pass


    def actions(self, state: SlitherlinkState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass


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
        # TODO
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
            if (board.case_3_adjacent_0((r,c))):
                continue
            elif (board.case_3_diagonal_0((r,c))):
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

