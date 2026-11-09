import pandas as pd
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, PatternFill

SEVERITY_ORDER = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "未評価"]

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

summary = df["深刻度"].value_counts().reindex(SEVERITY_ORDER, fill_value=0).reset_index()
summary.columns = ["深刻度", "件数"]

COLUMN_WIDTHS = {
    "サマリー": {"A": 15, "B": 10},
    "要対応": {"A": 18, "B": 12, "C": 12, "D": 8, "E": 80, "F": 50},
     "全件": {"A": 18, "B": 12, "C": 12, "D": 8, "E": 80, "F": 50},
}

with pd.ExcelWriter("report.xlsx") as writer:
    summary.to_excel(writer, sheet_name="サマリー", index=False)
    urgent.to_excel(writer, sheet_name="要対応", index=False)
    df.to_excel(writer, sheet_name="全件", index=False)

    for sheet_name, ws in writer.sheets.items():
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="1F4E78")

        for column, width in COLUMN_WIDTHS[sheet_name].items():
            ws.column_dimensions[column].width = width

        ws.freeze_panes = "A2"

    ws = writer.sheets["サマリー"]
    chart = BarChart()
    chart.title = "深刻度ごとの件数"
    chart.y_axis.title = "件数"

    data = Reference(ws, min_col=2, min_row=1, max_row=len(summary) + 1)
    categories = Reference(ws, min_col=1, min_row=2, max_row=len(summary) + 1)

    chart.add_data(data, titles_from_data=True)
    chart.set_categories(categories)
    ws.add_chart(chart, "D2")
    
print()
print("📊 report.xlsx を作成しました")