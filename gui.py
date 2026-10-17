import sys
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk

import StructMirrorPicker


def resource_path(name):
    """--onefile 展開時は sys._MEIPASS、通常実行時はスクリプトと同じフォルダを返す"""
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


class RedirectText:
    """標準出力をTkinterのテキストウィジェットにリダイレクトするクラス"""

    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.after(0, self._insert, string)

    def flush(self):
        pass

    def _insert(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)


class StructMirrorPickerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("StructMirrorPicker GUI")
        self.root.geometry("700x540")
        try:
            self.root.iconbitmap(resource_path("icon.ico"))
        except Exception:
            pass
        self.create_widgets()

    def create_widgets(self):
        frame_top = tk.LabelFrame(self.root, text=" 実行設定 ", padx=10, pady=10)
        frame_top.pack(fill="x", padx=10, pady=10)

        # 入力パス
        tk.Label(frame_top, text="入力フォルダ:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.entry_path = tk.Entry(frame_top, width=50)
        self.entry_path.grid(row=0, column=1, padx=5, pady=5)
        self.entry_path.insert(0, StructMirrorPicker.load_last_path())
        tk.Button(
            frame_top, text="参照...", command=self.browse_input_path
        ).grid(row=0, column=2, padx=5, pady=5)

        # 出力パス
        tk.Label(frame_top, text="出力フォルダ:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.entry_output = tk.Entry(frame_top, width=50)
        self.entry_output.grid(row=1, column=1, padx=5, pady=5)
        saved_output = StructMirrorPicker.load_last_output_path()
        default_output = saved_output or StructMirrorPicker.compute_output_path(
            StructMirrorPicker.load_last_path()
        )
        self.entry_output.insert(0, default_output)
        tk.Button(
            frame_top, text="参照...", command=self.browse_output_path
        ).grid(row=1, column=2, padx=5, pady=5)

        # favicon画像を参照ボタン右側に表示（2行分にまたがる）
        try:
            img = Image.open(resource_path("396-600x600.png")).convert("RGBA")
            img = img.resize((80, 80), Image.LANCZOS)
            self._favicon = ImageTk.PhotoImage(img)
            tk.Label(frame_top, image=self._favicon).grid(
                row=0, column=3, rowspan=2, padx=15, pady=5
            )
        except Exception:
            pass

        self.btn_run = tk.Button(
            self.root,
            text="処理を実行",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.start_process,
            padx=20,
            pady=5,
        )
        self.btn_run.pack(pady=5)

        frame_log = tk.LabelFrame(self.root, text=" 実行ログ ", padx=10, pady=10)
        frame_log.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_area = scrolledtext.ScrolledText(
            frame_log, wrap=tk.WORD, state="normal", font=("Consolas", 10)
        )
        self.log_area.pack(fill="both", expand=True)

        sys.stdout = RedirectText(self.log_area)
        sys.stderr = RedirectText(self.log_area)

    def browse_input_path(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.entry_path.delete(0, tk.END)
            self.entry_path.insert(0, dir_path)

    def browse_output_path(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.entry_output.delete(0, tk.END)
            self.entry_output.insert(0, dir_path)

    def start_process(self):
        input_path = self.entry_path.get()
        output_path = self.entry_output.get()

        if not input_path:
            messagebox.showwarning("警告", "入力フォルダを選択してください。")
            return

        StructMirrorPicker.save_config(input_path, output_path)
        self.btn_run.config(state="disabled")
        self.log_area.delete("1.0", tk.END)

        threading.Thread(
            target=self.run_task, args=(input_path, output_path or None), daemon=True
        ).start()

    def run_task(self, input_path, output_path):
        try:
            print(f"--- 処理開始 ---")
            print(f"  入力: {input_path}")
            effective_output = output_path or StructMirrorPicker.compute_output_path(input_path)
            print(f"  出力: {effective_output}")
            StructMirrorPicker.process_directories(input_path, output_path=output_path)
            print("処理が正常に完了しました。")
        except Exception as e:
            print(f"[エラー] {e}")
        finally:
            print("--- 処理終了 ---")
            self.root.after(0, lambda: self.btn_run.config(state="normal"))


if __name__ == "__main__":
    root = tk.Tk()
    app = StructMirrorPickerGUI(root)
    root.mainloop()
