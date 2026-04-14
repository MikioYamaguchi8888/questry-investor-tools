import csv
import json
import os
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

INVESTORS_CSV   = "investors.csv"
FUNDS_JSON      = "funds.json"
TEMPLATE_MD     = "report_template.md"
OUTPUT_DIR      = "reports"


def load_investors():
    """investors.csv を {名前: 行データ} の辞書で返す"""
    with open(INVESTORS_CSV, encoding="utf-8") as f:
        return {row["投資家名"]: row for row in csv.DictReader(f)}


def load_funds():
    with open(FUNDS_JSON, encoding="utf-8") as f:
        return json.load(f)


def load_template():
    with open(TEMPLATE_MD, encoding="utf-8") as f:
        return f.read()


def progress_text(fund):
    """調達進捗をテキストで表現する"""
    target  = fund["ターゲット金額（万円）"]
    current = fund["現在調達額（万円）"]
    pct     = round(current / target * 100, 1)
    return f"調達額 {current:,}万円 / 目標 {target:,}万円（達成率 {pct}%）・ステータス：{fund['ステータス']}"


def estimate_dividend_date(fund):
    """案件の投資期間をもとに配当予定日を概算する（今月 + 投資期間）"""
    months   = fund["投資期間（月）"]
    base     = date.today().replace(day=1)
    div_date = base + relativedelta(months=months)
    return div_date.strftime("%Y年%m月末")


def render(template, variables):
    """{{キー}} を variables の値で置換する"""
    result = template
    for key, value in variables.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    investors = load_investors()
    funds     = load_funds()
    template  = load_template()
    today_str = date.today().strftime("%Y年%m月%d日")
    yyyymm    = date.today().strftime("%Y%m")

    count = 0
    for fund in funds:
        for inv_entry in fund["投資家リスト"]:
            name   = inv_entry["名前"]
            amount = inv_entry["出資額（万円）"]

            # investors.csv に存在すれば IRR 実績として利回り目標を使用
            # （実データでは実績値に差し替える）
            irr = fund["利回り目標（%）"]

            variables = {
                "投資家名":    name,
                "案件名":      fund["案件名"],
                "出資額":      f"{amount:,}",
                "期間":        f"{fund['投資期間（月）']}ヶ月",
                "現在の進捗":  progress_text(fund),
                "配当予定日":  estimate_dividend_date(fund),
                "IRR実績":     irr,
                "発行日":      today_str,
            }

            content   = render(template, variables)
            filename  = f"{name}_レポート_{yyyymm}.md"
            filepath  = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

            count += 1
            print(f"  作成: {filename}")

    print(f"\n{count}名分のレポートを生成しました（出力先: {OUTPUT_DIR}/）")


if __name__ == "__main__":
    main()
