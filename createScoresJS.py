from dataclasses import dataclass
import csv
import os

from comments import comments


@dataclass
class Game:
    party_pack: int
    game_name: str
    total_score: int
    avg_score: float

    def set_comment(self):
        self.comment = comments.get(self.game_name)
        return self

    def get_comment(self):
        return f', comment: "{self.comment}"' if self.comment else ""

    def formatted(self):
        return (
            f'  {{ partyPack: {self.party_pack}, game: "{self.game_name}", '
            + f"totalScore: {self.total_score}, avgScore: {self.avg_score}"
            + f"{self.get_comment()} }},\n"
        )


def write_js_arr(name, items, file):
    file.write(f"const {name} = [\n")
    for item in items:
        file.write(item)
    file.write(f"];\nexport default {name};")


score_data = "scoredata.csv"
scores = "scores.js"
temp_file = "tmp_" + scores


with open(score_data, "r") as f:
    score_data_reader = csv.DictReader(f)
    games = (Game(*row.values()).set_comment() for row in score_data_reader)

    with open(temp_file, "w") as f:
        write_js_arr("scores", (game.formatted() for game in games), f)

os.replace(temp_file, scores)
