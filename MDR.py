class Player:
    def __init__(self, name, start_pos):
        self.name = name
        self.position = start_pos
        self.mp = 5
        self.last_seen = None  # 最後に相手を見た位置
        self.track_turns = 0  # エンシスマキシマが有効なターン数

    def move(self, board, direction, distance=1):
        directions = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        dx, dy = directions[direction]
        for _ in range(distance):
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
                self.position = (new_x, new_y)
            else:
                break

    def cast_spell(self, spell, target):
        global game_over
        outcome = ""
        if spell == "Lapis":
            if self.mp >= 3:
                affected_area = [(self.position[0], self.position[1]),
                                 (self.position[0], max(0, self.position[1]-1)),
                                 (self.position[0], min(len(board)-1, self.position[1]+1)),
                                 (max(0, self.position[0]-1), self.position[1]),
                                 (min(len(board)-1, self.position[0]+1), self.position[1])]
                if target.position in affected_area:
                    game_over = True
                    outcome = f"{self.name} wins with Lapis!"
                self.mp -= 3
        elif spell == "Beam":
            if self.mp >= 6:
                beam_path = [(self.position[0] + i * dx, self.position[1] + i * dy)
                             for i in range(1, 4) for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]
                             if 0 <= self.position[0] + i * dx < len(board) and 0 <= self.position[1] + i * dy < len(board)]
                if target.position in beam_path:
                    game_over = True
                    outcome = f"{self.name} wins with Beam!"
                self.mp -= 6
        elif spell == "Meteor":
            if self.mp >= 12 and self.position != target.position:
                meteor_area = [(target.position[0] + dx, target.position[1] + dy)
                               for dx in range(-1, 2) for dy in range(-1, 2)
                               if 0 <= target.position[0] + dx < len(board) and 0 <= target.position[1] + dy < len(board)]
                if target.position in meteor_area:
                    game_over = True
                    outcome = f"{self.name} wins with Meteor!"
                self.mp -= 12
        elif spell == "Invest":
            if self.mp >= 1:
                outcome = f"{target.name}'s MP is {target.mp}"
                self.mp -= 1
        elif spell == "Encis":
            if self.mp >= 3:
                self.last_seen = target.position
                outcome = f"{target.name} is at {self.last_seen}"
                self.mp -= 3
        elif spell == "EncisMaxima":
            if self.mp >= 7:
                self.track_turns = 3
                outcome = f"{target.name}'s location will be tracked for 3 turns"
                self.mp -= 7
        return outcome

    def rest(self):
        self.mp = min(self.mp + 3, 15)

def game_loop():
    board_size = 6
    board = [[None for _ in range(board_size)] for _ in range(board_size)]
    player_red = Player("Red", (0, 0))
    player_blue = Player("Blue", (board_size - 1, board_size - 1))
    global game_over
    game_over = False

    while not game_over:
        for player in [player_red, player_blue]:
            other_player = player_blue if player == player_red else player_red
            if player.track_turns > 0:
                print(f"{other_player.name} is located at {other_player.position} for {player.track_turns} more turns")
                player.track_turns -= 1
            print(f"{player.name}'s turn. MP: {player.mp}")
            action = input(f"Choose action (move, cast, rest): ").strip()
            if action == "move":
                direction = input("Enter direction (up, down, left, right): ").strip()
                distance = int(input("Enter distance (1, 2, 3, 4 for Mubi, MubiRa, MubiGa respectively): "))
                player.move(board, direction, distance)
            elif action == "cast":
                spell = input("Enter spell (Lapis, Beam, Meteor, Invest, Encis, EncisMaxima): ").strip()
                result = player.cast_spell(spell, other_player)
                if result:
                    print(result)
            elif action == "rest":
                player.rest()
                print(f"{player.name} rests and now has {player.mp} MP")
            print(f"{player.name}'s position: {player.position}, MP: {player.mp}")

            if game_over:
                break

game_loop()
