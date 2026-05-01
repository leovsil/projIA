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
        if column < 2 * self.ncolumns - 1:
            adjacent_cells.append((row, column + 2))
        if row < 2 * self.nrows - 1:
            adjacent_cells.append((row + 2, column))
        if column > 1:
            adjacent_cells.append((row, column - 2))

        return adjacent_cells

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

    def output_board(self) -> str:
        """Devolve o output da board"""
        output = ""
        for i in range(1, 2*self.nrows+1, 2):
            for j in range(1, 2*self.ncolumns+1, 2):
                edges = self.get_cell_edges(i,j)
                for edge in edges:
                    r,c = edge
                    output += "1" if self.board[r][c] == ACTIVE else "0"
                if j != 2*self.ncolumns:
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



test = Board.parse_instance()
print(test.output_board())



