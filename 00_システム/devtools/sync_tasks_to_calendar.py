#!/usr/bin/env python3
import os
import re
import json
import subprocess
from datetime import datetime

# ==========================================
# 設定
# ==========================================
JOURNAL_DIR = "/Users/kasuyatooru/Product/2nd-Brain/05_日誌"
STATE_FILE = "/Users/kasuyatooru/.2ndbrain_calendar_sync.json"

# 追加先のカレンダー名 (AppleScriptで取得したカレンダー名のいずれか)
# "toru.kototama@gmail.com" はGoogleカレンダーと推測されます。
# または "粕谷　亨の予定" など。
CALENDAR_NAME = "toru.kototama@gmail.com"

# カレンダーに追加する際のプレフィックス (タスクだと分かりやすくするため)
EVENT_PREFIX = "📝 "

def get_today_file():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(JOURNAL_DIR, f"{today}.md")

def get_synced_tasks():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_synced_tasks(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def add_to_calendar(task_name):
    """AppleScriptを使ってMacの標準カレンダーアプリに終日予定として追加する"""
    event_title = f"{EVENT_PREFIX}{task_name}"
    
    # AppleScriptの文字列表現エスケープ
    event_title = event_title.replace('"', '\\"')
    
    applescript = f'''
    tell application "Calendar"
        try
            set targetCalendar to calendar "{CALENDAR_NAME}"
        on error
            -- 指定されたカレンダーが見つからない場合は最初のカレンダーを使用
            set targetCalendar to calendar 1
        end try
        
        tell targetCalendar
            -- 終日予定として今日のカレンダーに追加 (プライベート扱い)
            make new event with properties {{summary:"{event_title}", start date:(current date), end date:(current date), allday event:true}}
        end tell
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error adding task to calendar: {e.stderr.decode('utf-8') if e.stderr else e}")
        return False

def is_valid_task(task_text):
    """追加すべきタスクかどうかの判定"""
    if not task_text:
        return False
    # あからさまなプレースホルダや説明文は除外
    excludes = ["ここに溜まったタスクを、エージェントが振り分けます。", "コマンド"]
    for ex in excludes:
        if ex in task_text:
            return False
    return True

def sync_today_tasks():
    filepath = get_today_file()
    if not os.path.exists(filepath):
        print(f"Today's journal not found: {filepath}")
        return

    today_key = datetime.now().strftime("%Y-%m-%d")
    state = get_synced_tasks()
    
    if today_key not in state:
        state[today_key] = []
        
    synced_for_today = set(state[today_key])
    
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_syncs = []
    
    in_today_tasks_section = False
    
    for line in lines:
        # セクションの判定
        if "## ✅ Today's Tasks" in line or "## ✅ Today's Tasks (今日のタスク)" in line:
            in_today_tasks_section = True
            continue
        elif line.strip().startswith("## ") and in_today_tasks_section:
            # 次のH2セクションが来たらパース終了
            break
            
        if in_today_tasks_section:
            # `- [ ] Task`, `- [x] Task` の形式にマッチ
            match = re.search(r'^\s*-\s*\[[ xX/]\]\s+(.+)$', line)
            if match:
                task = match.group(1).strip()
                if is_valid_task(task) and task not in synced_for_today:
                    print(f"Syncing task to calendar: {task}")
                    if add_to_calendar(task):
                        new_syncs.append(task)
                        synced_for_today.add(task)
                    
    if new_syncs:
        state[today_key] = list(synced_for_today)
        save_synced_tasks(state)
        print(f"Successfully synced {len(new_syncs)} new tasks.")
    else:
        print("No new tasks to sync.")

if __name__ == "__main__":
    sync_today_tasks()
