import json
import os
import shutil

# 設定ファイルのパス
CONFIG_FILE = "config.json"


def load_config():
  if os.path.exists(CONFIG_FILE):
    try:
      with open(CONFIG_FILE, "r") as f:
        return json.load(f)
    except:
      pass
  return {}


def load_last_path():
  return load_config().get("last_path", r"\\ypci5u\drv_i\CDDVD\DVD\r18\DLtmp3")


def load_last_output_path():
  return load_config().get("last_output_path", "")


def save_config(input_path, output_path):
  with open(CONFIG_FILE, "w") as f:
    json.dump({"last_path": input_path, "last_output_path": output_path}, f)


def save_last_path(path):
  cfg = load_config()
  cfg["last_path"] = path
  with open(CONFIG_FILE, "w") as f:
    json.dump(cfg, f)


def compute_output_path(root_path, replace_dirnm="OutP"):
  """入力パスの親フォルダ + replace_dirnm のフルパスを返す"""
  return os.path.join(os.path.dirname(root_path), replace_dirnm)


def process_directories(root_path, output_path=None, replace_dirnm="OutP"):
  if output_path:
    target_path = output_path
  else:
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
    new_path = mylst.replace(
        root_path, os.path.join(target_path, os.path.basename(root_path))
    )
    os.makedirs(new_path, exist_ok=True)
  for f in fPathList:
    dest = f.replace(
        root_path, os.path.join(target_path, os.path.basename(root_path))
    )
    shutil.move(f, dest)


if __name__ == "__main__":
  import flet as ft

  def main(page: ft.Page):
    page.title = "StructMirrorPicker"

    saved_path = load_last_path()

    path_input = ft.TextField(label="ROOT_PATH", value=saved_path, width=400)
    status_text = ft.Text("")

    def get_directory_result(e: ft.FilePickerResultEvent):
      if e.path:
        path_input.value = e.path
        path_input.update()

    folder_picker = ft.FilePicker(on_result=get_directory_result)
    page.overlay.append(folder_picker)

    def start_process(e):
      try:
        save_last_path(path_input.value)
        status_text.value = "処理中..."
        page.update()

        process_directories(path_input.value)

        status_text.value = "完了しました！"
        page.dialog = ft.AlertDialog(
            title=ft.Text("完了"),
            content=ft.Text("ファイルの移動が完了しました。"),
        )
        page.dialog.open = True
      except Exception as ex:
        status_text.value = f"エラー: {str(ex)}"
      page.update()

    page.add(
        ft.Text("ディレクトリ構造ミラーリングツール", size=20, weight="bold"),
        ft.Row(
            [
                path_input,
                ft.ElevatedButton(
                    "参照...",
                    on_click=lambda _: folder_picker.get_directory_path(),
                ),
            ]
        ),
        ft.ElevatedButton("実行開始", on_click=start_process),
        status_text,
    )

  ft.app(target=main)
