import csv
from datetime import date, datetime

CSV_FILE = "investors.csv"
TODAY = date.today()


def load_investors():
    with open(CSV_FILE, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def status_counts(investors):
    counts = {}
    for inv in investors:
        status = inv["ステータス"]
        counts[status] = counts.get(status, 0) + 1
    return counts


def approved_total(investors):
    total = sum(
        int(inv["出資可能額（万円）"])
        for inv in investors
        if inv["ステータス"] == "承認済"
    )
    return total


def stale_contacts(investors, days=90):
    result = []
    for inv in investors:
        last = datetime.strptime(inv["最終コンタクト日"], "%Y-%m-%d").date()
        if (TODAY - last).days >= days:
            result.append((inv["投資家名"], inv["最終コンタクト日"], (TODAY - last).days))
    return result


def main():
    investors = load_investors()

    print("=" * 40)
    print("1. ステータス別 投資家数")
    print("=" * 40)
    for status, count in status_counts(investors).items():
        print(f"  {status}: {count}名")

    print()
    print("=" * 40)
    print("2. 承認済み投資家の出資可能額合計")
    print("=" * 40)
    total = approved_total(investors)
    print(f"  {total:,} 万円（{total / 10000:.1f} 億円）")

    print()
    print("=" * 40)
    print("3. 最終コンタクトから90日以上経過している投資家")
    print("=" * 40)
    stale = stale_contacts(investors)
    if stale:
        for name, last_date, elapsed in stale:
            print(f"  {name}（最終コンタクト: {last_date} / {elapsed}日経過）")
    else:
        print("  該当者なし")


if __name__ == "__main__":
    main()
