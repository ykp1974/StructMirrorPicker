import os
import shutil
import flet as ft

# 処理ロジックを関数化
def process_directories(root_path, replace_dirnm="OutP"):
    # 移動元の親ディレクトリ名を特定
    base_dir = os.path.dirname(root_path)
    target_path = os.path.join(base_dir, replace_dirnm)
    
    mylist = []
    fPathList = []

    def recursive_file_check(path):
        if os.path.isdir(path):
            files = os.listdir(path)
            files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
            # 直下ファイルのみリストアップ（既存ロジック踏襲）
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

# Flet GUI定義
def main(page: ft.Page):
    page.title = "StructMirrorPicker"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # 初期値
    default_path = r"C:\wk\yamag2\x\.metadata"
     
    path_input = ft.TextField(label="ROOT_PATH", value=default_path, width=500)
    status_text = ft.Text("")

    def start_process(e):
        try:
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