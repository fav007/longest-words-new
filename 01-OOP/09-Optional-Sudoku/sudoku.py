# pylint: disable=missing-docstring

class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid

    def is_valid(self):
        for i in range(9):
            if len(set([self.grid[i][j] for j in range(9)])) != 9 :
                return False
            if len(set([self.grid[j][i] for j in range(9)])) != 9 :
                return False
        for u in range(0,9,3):
            for v in range(0,9,3):
                if len(set([self.grid[i][j] for i in range(u,u+3) for j in range(v,v+3) ]))!=9:
                    return False
        return True
        
                
                
        
        
