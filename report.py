import pandas as pd

df = pd.read_csv("data/wordpress.csv", encoding="utf-8-sig")

print("=== 最初の5行 ===")
print(df.head())

print()
print(f"全件数: {len(df)} 件")

print()
print("=== 深刻度ごとの件数 ===")
print(df["深刻度"].value_counts())

print()
print(f"平均スコア: {df['スコア'].mean():.1f}")
print(f"最高スコア: {df['スコア'].max()}")