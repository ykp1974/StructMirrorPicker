@echo off
chcp 65001 > nul
echo StructMirrorPicker GUI ビルド開始...

REM PyInstallerがなければインストール
pip show pyinstaller > nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstallerをインストールしています...
    pip install pyinstaller
)

REM EXEをビルド（コンソールなし、単一ファイル、アイコン付き）
python -m PyInstaller --onefile --windowed --name StructMirrorPickerGUI --icon icon.ico --add-data "icon.ico;." --add-data "396-600x600.png;." gui.py

if %errorlevel% equ 0 (
    echo.
    echo ビルド成功！
    echo dist\StructMirrorPickerGUI.exe が作成されました。
) else (
    echo.
    echo ビルドに失敗しました。エラーを確認してください。
)
pause
