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

print()
print("=== 対応が必要な脆弱性 (CRITICAL・HIGH) ===")
urgent = df[(df["深刻度"] == "CRITICAL") | (df["深刻度"] == "HIGH")]
urgent = urgent.sort_values("スコア", ascending=False)
print(urgent[["CVE番号", "公開日", "深刻度", "スコア"]])
print(f"→ {len(urgent)} 件")

summary = df["深刻度"].value_counts().reset_index()
summary.columns = ["深刻度", "件数"]

with pd.ExcelWriter("report.xlsx") as writer:
    summary.to_excel(writer, sheet_name="サマリー", index=False)
    urgent.to_excel(writer, sheet_name="要対応", index=False)
    df.to_excel(writer, sheet_name="全件", index=False)

print()
print("📊 report.xlsx を作成しました")