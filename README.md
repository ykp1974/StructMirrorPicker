### 1. .exe化
前回の方法（コマンドプロンプトからの起動）は、**「プログラミング用の環境」**で実行するものでした。今回作成するアプリは**「Windowsの一般ユーザーが使うアプリ」**にしたいですよね。

アプリをダウンロードしてきた方が、コマンドプロンプトを開かずにダブルクリックで起動できるように、**「実行ファイル (.exe)」**に変換（ビルド）します。

#### 手順1: 環境構築 (初回のみ)
まず、Fletでアプリを配布するために必要な「包装ツール」をインストールします。Pythonがインストールされている環境（C:\wk\yamag2\venv...）で、以下のコマンドを1回だけ実行してください。

```bash
pip install flet pyinstaller
```

#### 手順2: 実行ファイル化 (ビルド)
次に、先ほどの`StructMirrorPicker.py`を「実行ファイル（exe）」に変換します。コマンドプロンプト（またはPowerShell）を開き、以下のコマンドを実行してください。

```bash
flet pack StructMirrorPicker.py --name StructMirrorPicker --onefile
```

##### アイコン付きで作成する場合
```bash
flet pack StructMirrorPicker.py --name StructMirrorPicker --onefile --icon=path/to/icon.ico
```
* Windowsでアイコン付きで作成する場合、Icon.icoはexeと同じフォルダに入れておく必要があります。
* Linuxの場合、--iconの引数にpngファイルを指定することでアイコン付きで作成できます。

**【解説】**
*   `flet pack` : Fletアプリを実行ファイルにまとめるコマンドです。
*   `StructMirrorPicker.py` : 元のPythonファイル名を指定しています。
*   `--name StructMirrorPicker` : 完成品のファイル名を「StructMirrorPicker.exe」に設定します。
*   `--onefile` : すべてを1つのファイルにまとめます（推奨）。

#### 手順3: アプリの確認
ビルドが成功すると、先ほどの`StructMirrorPicker.py`と同じ階層に`dist`というフォルダができているはずです。その中にある`StructMirrorPicker.exe`をダブルクリックすると、ウィンドウが立ち上がり、先ほどまで使っていた操作画面（テキストボックスとボタン）が表示されるはずです。



.\venv\Scripts\Activate.ps1

python -m PyInstaller --onefile --windowed --name StructMirrorPickerGUI --icon icon.ico --add-data "icon.ico;." gui.py

python -m PyInstaller --onefile --windowed --name StructMirrorPickerGUI --icon icon.ico --add-data "icon.ico;." --add-data "396-600x600.png;." gui.py
