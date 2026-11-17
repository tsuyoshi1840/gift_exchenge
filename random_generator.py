# Mulberry32の実装
# シード値を受け取り、疑似乱数を生成するアルゴリズム。
# ★疑似乱数とは
# ランダムに見える数列を計算によって生成する仕組み。
# 同じシード値と同じ計算手順なら、同じ数列が再現される。
# ★シード値（初期値）
# 乱数生成の出発点となる数値。
# ★内部状態の変化
# 初期値：12345
#   ↓ 計算
# 内部状態：別の数値
#   ↓ 計算
# 内部状態：さらに別の数値
#   ↓ 計算
# 内部状態：また別の数値

# 1 byte = 8 bit
# 32 bit = 4 byte
# 32ビットで表現できる組み合わせは2の32乗通り。
# 0から数えるため、最大値は2の32乗 - 1。
# 2の32乗     = 4294967296
# 2の32乗 - 1 = 4294967295
# 0x は16進数を表す接頭辞。
# 16進数1桁は2進数4桁に相当する。
# FFFFFFFF はFが8桁なので、合計32ビット。
# ★0x6D2B79F5 はMulberry32で使用する固定定数。
# 16進数で8桁、32ビットの値。
# 10進数では1831565813
# 2進数：
# 0110 1101 0010 1011 0111 1001 1111 0101

# この定数を加算することで内部状態を進める。
# 奇数を32ビットの範囲で加算し続けると、
# すべての32ビット状態を一巡する。
import secrets

seed = secrets.randbits(32)
# print(seed)

MASK = 0xFFFFFFFF


def create_generator(seed):

    def generate():
        nonlocal seed

        seed = (seed + 0x6D2B79F5) & MASK

        value = seed
        value = ((value ^ (value >> 15)) * (value | 1)) & MASK
        value = (value ^ ((value + ((value ^ (value >> 7)) * (value | 61))) & MASK)) & MASK
        value = (value ^ (value >> 14)) & MASK

        return value & MASK

    return generate


generator = create_generator(seed)
