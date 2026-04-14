import os
import sys

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")


def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(notes))


def list_notes(notes):
    if not notes:
        print("メモがありません。")
        return
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")


def add_note(notes):
    text = input("メモを入力してください: ").strip()
    if text:
        notes.append(text)
        save_notes(notes)
        print("メモを追加しました。")
    else:
        print("空のメモは追加できません。")


def delete_note(notes):
    list_notes(notes)
    if not notes:
        return
    try:
        num = int(input("削除するメモの番号を入力してください: "))
        if 1 <= num <= len(notes):
            removed = notes.pop(num - 1)
            save_notes(notes)
            print(f"削除しました: {removed}")
        else:
            print("無効な番号です。")
    except ValueError:
        print("数字を入力してください。")


def main():
    notes = load_notes()
    while True:
        print("\n--- メモ帳 ---")
        print("1. メモ一覧")
        print("2. メモを追加")
        print("3. メモを削除")
        print("4. 終了")
        choice = input("選択してください (1-4): ").strip()

        if choice == "1":
            list_notes(notes)
        elif choice == "2":
            add_note(notes)
        elif choice == "3":
            delete_note(notes)
        elif choice == "4":
            print("終了します。")
            sys.exit(0)
        else:
            print("1〜4の数字を入力してください。")


if __name__ == "__main__":
    main()
