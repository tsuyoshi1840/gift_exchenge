
import random

# 参加者リスト
participants = []

# 名前の登録
while True:
    name = input("参加者の名前（終了する場合はEnter）： ")

    if name == "":
        break

    participants.append(name)

# 人数チェック
if len(participants) < 2 or len(participants) % 2 != 0:
    print("参加者は2人以上の偶数にしてください。")

else:
    print("\n抽選を開始します！")

    # 全員が交換するまで繰り返す
    while len(participants) > 0:

        input("\nEnterキーで次のペアを抽選： ")

        # 2人をランダムに選択
        pair = random.sample(participants, 2)

        print(f"\n今回のペア：{pair[0]} ＆ {pair[1]}")

        # 選出された2人をリストから削除
        for name in pair:
            participants.remove(name)

    print("\n全員のプレゼント交換が終了しました！")

import random

# 参加者リスト
participants = []

# 名前の登録
while True:
    name = input("参加者の名前（終了する場合はEnter）： ")

    if name == "":
        break

    participants.append(name)

# 人数チェック
if len(participants) < 2 or len(participants) % 2 != 0:
    print("参加者は2人以上の偶数にしてください。")

else:
    print("\n抽選を開始します！")

    # 全員が交換するまで繰り返す
    while len(participants) > 0:

        input("\nEnterキーで次のペアを抽選： ")

        # 2人をランダムに選択
        pair = random.sample(participants, 2)

        print(f"\n今回のペア：{pair[0]} ＆ {pair[1]}")

        # 選出された2人をリストから削除
        for name in pair:
            participants.remove(name)

    print("\n全員のプレゼント交換が終了しました！")
