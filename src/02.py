def play_with_guessed_rules():
    points_rps = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
    points_game = {"defeat": 0, "draw": 3, "win": 6}
    game_results = {("A", "X"): "draw",
                    ("A", "Y"): "win",
                    ("A", "Z"): "defeat",
                    ("B", "X"): "defeat",
                    ("B", "Y"): "draw",
                    ("B", "Z"): "win",
                    ("C", "X"): "win",
                    ("C", "Y"): "defeat",
                    ("C", "Z"): "draw",
                    }

    i = 0
    my_points = 0
    opponents_points = 0

    with open("../dat/02") as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break

            i += 1
            game = tuple(line.split())
            opponents_points += points_rps[game[0]]
            my_points += points_rps[game[1]]
            opponents_points += 6 - points_game[game_results[game]]
            my_points += points_game[game_results[game]]
            print("Round {}: {}".format(i, game_results[game]))

    print("Final points: {}-{}".format(my_points, opponents_points))


def play_with_true_rules():
    points_rps = {"A": 1, "B": 2, "C": 3}
    points_game = {"X": 0, "Y": 3, "Z": 6}
    my_choice = {("A", "X"): "C",
                 ("A", "Y"): "A",
                 ("A", "Z"): "B",
                 ("B", "X"): "A",
                 ("B", "Y"): "B",
                 ("B", "Z"): "C",
                 ("C", "X"): "B",
                 ("C", "Y"): "C",
                 ("C", "Z"): "A",
                 }
    result = {"X": "defeat", "Y": "draw", "Z": "win"}

    i = 0
    my_points = 0
    opponents_points = 0

    with open("../dat/02") as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break

            i += 1
            game = tuple(line.split())
            opponents_points += points_rps[game[0]]
            my_points += points_game[game[1]]
            opponents_points += 6 - points_game[game[1]]
            my_points += points_rps[my_choice[game]]
            print("Round {}: {}".format(i, result[game[1]]))

    print("Final points: {}-{}".format(my_points, opponents_points))


if __name__ == "__main__":
    play_with_true_rules()
