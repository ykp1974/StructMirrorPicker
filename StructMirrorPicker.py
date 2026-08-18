import os
import shutil
import json
import flet as ft

# 設定ファイルのパス
CONFIG_FILE = "config.json"

def load_last_path():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("last_path", r"\\Ypci5\I\CDDVD\DVD\r18\DLtmp3")
        except:
            pass
    return r"\\Ypci5\I\CDDVD\DVD\r18\DLtmp3"

def save_last_path(path):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"last_path": path}, f)

def process_directories(root_path, replace_dirnm="OutP"):
    # ... (前回の process_directories ロジックと同じ) ...
    base_dir = os.path.dirname(root_path)
    target_path = os.path.join(base_dir, replace_dirnm)
    
    mylist = []
    fPathList = []

    def recursive_file_check(path):
        if os.path.isdir(path):
            files = os.listdir(path)
            files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
            for file in files_file[:1]:
                fPathList.append(os.path.join(path, file))
            for file in files:
                full_path = os.path.join(path, file)
                if os.path.isdir(full_path):
                    mylist.append(full_path)
                    recursive_file_check(full_path)

    recursive_file_check(root_path)
    for mylst in mylist:
        new_path = mylst.replace(root_path, os.path.join(target_path, os.path.basename(root_path)))
        os.makedirs(new_path, exist_ok=True)
    for f in fPathList:
        dest = f.replace(root_path, os.path.join(target_path, os.path.basename(root_path)))
        shutil.move(f, dest)

def main(page: ft.Page):
    page.title = "StructMirrorPicker"
    
    # 前回起動時のパスを読み込み
    saved_path = load_last_path()
    
    path_input = ft.TextField(label="ROOT_PATH", value=saved_path, width=500)
    status_text = ft.Text("")

    def start_process(e):
        try:
            # 実行時にパスを保存
            save_last_path(path_input.value)
            
            status_text.value = "処理中..."
            page.update()
            
            process_directories(path_input.value)
            
            status_text.value = "完了しました！"
            page.dialog = ft.AlertDialog(title=ft.Text("完了"), content=ft.Text("ファイルの移動が完了しました。"))
            page.dialog.open = True
        except Exception as ex:
            status_text.value = f"エラー: {str(ex)}"
        page.update()

    page.add(
        ft.Text("ディレクトリ構造ミラーリングツール", size=20, weight="bold"),
        path_input,
        ft.ElevatedButton("実行開始", on_click=start_process),
        status_text
    )

ft.app(target=main)