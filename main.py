from enum import Enum
import re


class InputError(Exception):
    pass


class PlayType(Enum):
    SERVE = 1
    PASS = 2
    SET = 3
    ATTACK = 4
    BLOCK = 5
    DIG = 6


class PlayResult(Enum):
    LOSE = -1
    CONTINUE = 0
    WIN = 1


class Play:
    player_id: int
    play_type: PlayType
    play_quality: int

    def __init__(self, player_id):
        self.player_id = player_id

    def result(self) -> PlayResult:
        raise NotImplementedError()


class DecisivePlay(Play):
    play_quality = 0
    quality_bindings = {"p": 1, "l": -1}

    def __init__(self, player_id, quality):
        super().__init__(player_id)
        if quality:
            try:
                self.play_quality = self.quality_bindings[quality]
                return
            except KeyError:
                raise InputError(f"Invalid {self.play_type.name} quality: {quality}")

    def result(self):
        if self.play_quality == -1:
            return PlayResult.LOSE
        elif self.play_quality == 1:
            return PlayResult.WIN
        return PlayResult.CONTINUE


class Serve(DecisivePlay):
    play_type = PlayType.SERVE


class Pass(Play):
    play_type = PlayType.PASS
    play_quality: int
    quality_bindings = {"1": 1, "2": 2, "3": 3, "4": 0}

    def __init__(self, player_id, quality):
        super().__init__(player_id)
        if not quality:
            raise InputError("A pass must have a pass quality associated to it.")
        try:
            self.play_quality = self.quality_bindings[quality]
            return
        except KeyError:
            raise InputError(f"Invalid {self.play_type.name} quality: {quality}")

    def result(self):
        if self.play_quality == 0:
            return PlayResult.LOSE
        return PlayResult.CONTINUE


class Set(Play):
    play_type = PlayType.SET
    play_quality: int
    quality_bindings = {"l": -1}

    def __init__(self, player_id, quality):
        super().__init__(player_id)
        if quality:
            try:
                self.play_quality = self.quality_bindings[quality]
                return
            except KeyError:
                raise InputError(f"Invalid {self.play_type.name} quality: {quality}")

    def result(self):
        if self.play_quality == -1:
            return PlayResult.LOSE
        return PlayResult.CONTINUE


class Attack(DecisivePlay):
    play_type = PlayType.ATTACK


class Block(DecisivePlay):
    play_type = PlayType.BLOCK


class Dig(Play):
    play_type = PlayType.SET
    play_quality: int
    quality_bindings = {"l": -1}

    def __init__(self, player_id, quality):
        super().__init__(player_id)
        if quality:
            try:
                self.play_quality = self.quality_bindings[quality]
                return
            except KeyError:
                raise InputError(f"Invalid {self.play_type.name} quality: {quality}")

    def result(self):
        if self.play_quality == -1:
            return PlayResult.LOSE
        return PlayResult.CONTINUE


play_type_bindings = {
    "s": Serve,
    "a": Pass,
    "q": Set,
    "w": Attack,
    "e": Block,
    "r": Dig,
}


def play_of_string(play_string: str) -> Play:
    play_data = re.match(r"([1-4])(.)(\S*)", play_string)
    if play_data is None:
        raise InputError(f"Invalid play type '{play_string}'")
    try:
        play_class = play_type_bindings[play_data[2]]
    except KeyError:
        raise InputError(f"Invalid play type '{play_string}'")
    return play_class(int(play_data[1]), play_data[3])


class Game:
    players = {1: "1", 2: "2", 3: "3", 4: "4"}
    team_map = {"team1": [1, 2], "team2": [3, 4]}
    score = {"team1": 0, "team2": 0}
    point_list: list[list[Play]] = []
    current_point: list[Play] = []
    play_list: list[Play] = []

    def __init__(self):
        return

    def add_play(self, play_string):
        play = play_of_string(play_string)
        self.play_list.append(play)
        self.current_point.append(play)
        if play.result() is not PlayResult.CONTINUE:
            self.update_score()
        return

    def update_score(self):
        self.point_list.append((self.current_point.copy()))
        last_play = self.current_point[-1]
        self.current_point = []
        if last_play.result() is PlayResult.WIN:
            winning_team = self.find_team(last_play.player_id)
        else:
            winning_team = self.find_team(last_play.player_id, opposing=True)
        self.score[winning_team] += 1
        return

    def find_team(self, player_id, opposing=False):
        for k, v in self.team_map.items():
            if (player_id in v) ^ opposing:
                return k


intro_msg = "Welcome to the data entry system for volleyball!"


def main():
    print(intro_msg)
    game = Game()
    while True:
        play_text = input("Key the play and hit enter: ")
        try:
            game.add_play(play_text)
        except InputError as e:
            print(e)
            print("Try again.")


if __name__ == "__main__":
    main()


