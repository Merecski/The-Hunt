
class Board:
    def __init__(self, axis):
        self.axis = axis
        self.view_dist = 2
        self.gui = {
            None:'_|',
            'ai':'R|',
            'usr':'H|',
            'kill':'X|',
            'w':'^',
            'a':'<',
            's':'v',
            'd':'>'
        }

    def generate(self):
        return

    def print(self, positions, window):
        window.clear()
        window.border()
        board = []
        board_str = []
        for y in range(self.axis[0]):
            board.append([None] * self.axis[0])
        for player, pos in positions.items():
            board[pos[0]][pos[1]] = player
        for y in board:
            board_str.append(''.join(self.gui[x] for x in y))

        index = 1
        for line in board_str:
            window.addstr(index, 2, line)
            index += 1
        window.refresh()
        return

    def printShort(self, positions, window):
        window.clear()
        window.border()

        origin = positions['usr']
        start = [max(0, origin[0] - self.view_dist), \
                 max(0, origin[1] - self.view_dist)]
        end = [min(self.axis[0], origin[0] + self.view_dist) + 1, \
               min(self.axis[1], origin[1] + self.view_dist) + 1]

        board = []
        for y in range(self.axis[0]):
            board.append([None] * self.axis[0])
        for player, pos in positions.items():
            board[pos[0]][pos[1]] = player
        board_short = board[start[0]:end[0]]
        for index in range(len(board_short)):
            board_short[index] = board_short[index][start[1]:end[1]]

        board_str = []
        for y in board_short:
            board_str.append(''.join(self.gui[x] for x in y))
        index = 1
        for line in board_str:
            window.addstr(index + 4, 8, line)
            index += 1
        window.refresh()
        return
