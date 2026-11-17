import json
from pathlib import Path
from random_generator import create_generator


# 参加者のシャッフル・ペア作成
# 乱数を使って参加者をシャッフルし、2人ずつ組にする。

def create_pairs(participants, generator):
    if len(participants) < 2 or len(participants) % 2 != 0:
        raise ValueError("参加者は2人以上の偶数で登録してください。")

    participants = participants.copy()

    # Fisher–Yates法によるシャッフル
    for i in range(len(participants) - 1, 0, -1):
        j = generator() % (i + 1)
        participants[i], participants[j] = participants[j], participants[i]

    pairs = []

    for i in range(0, len(participants), 2):
        pair = participants[i:i + 2]
        pairs.append(pair)

    return pairs


if __name__ == "__main__":
    # JSONファイルの読み込み
    json_path = Path(__file__).with_name("participants.json")

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 参加者データを変数に格納
    participants = data.get("participants", [])

    # 乱数生成器を作成
    generator = create_generator(12345)

    # ペアを作成
    pairs = create_pairs(participants, generator)

    print(pairs)