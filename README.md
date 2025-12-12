# MF4 Operations - 車載計測ファイル変換・閲覧アプリケーション

[English](#english) | [日本語](#japanese)

---

## <a name="english"></a>English

### Overview

**MF4 Operations** is a fast and lightweight application for handling MF4, MDF, and DAT measurement files commonly used in automotive development and testing. It provides functionality equivalent to measurement device converters like INCA, with an intuitive graphical interface for data preview, channel selection, CSV export, and visualization.

### Features

- **Multi-format Support**: Load and process MF4, MDF, and DAT files
- **Data Preview**: Browse and preview measurement data with channel information
- **Channel Selection**: Search and select specific channels/labels with history tracking
- **CSV Export**: Convert measurement data to CSV format with optional resampling
- **Data Visualization**: Plot channel data using lightweight graphing library
- **Variable Refresh Rate**: Support for data resampling at custom rates
- **User Settings**: Automatic saving of preferences and label selection history
- **Encoding Support**: Robust handling of various character encodings
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Standalone Executable**: No Python installation required for end users

### Installation

#### Option 1: Run from Source

1. Install Python 3.8 or higher
2. Clone this repository:
   ```bash
   git clone https://github.com/sdrdx4100/mf4_operations.git
   cd mf4_operations
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python -m mf4_operations.main
   ```

#### Option 2: Use Pre-built Executable

Download the latest release from the [Releases](https://github.com/sdrdx4100/mf4_operations/releases) page and run the executable directly.

### Usage

1. **Open File**: Click "File" → "Open File..." or use the "Open File..." button to load a measurement file
2. **Browse Channels**: View available channels in the right panel
3. **Search Channels**: Use the search box to filter channels by name
4. **Select Channels**: Click channels to select them (Ctrl+Click for multiple selections)
5. **Configure Resampling**: Set the resample rate in seconds (0.0 for no resampling)
6. **Export to CSV**: Click "Export Selected to CSV..." to save selected channels
7. **Plot Data**: Click "Plot Selected Channels" to visualize the data
8. **History**: The application remembers your previous channel selections per file

### Technical Details

#### Dependencies

- **asammdf**: For reading MF4/MDF files (industry-standard library)
- **pandas**: For data manipulation and CSV export
- **matplotlib**: For data visualization
- **tkinter**: For the graphical user interface (included with Python)

#### User Settings Location

Settings and history are stored in:
- Windows: `C:\Users\<username>\.mf4_operations\`
- Linux/Mac: `~/.mf4_operations/`

Files:
- `settings.json`: Application preferences
- `label_history.json`: Channel selection history

### Building Executable

To build a standalone executable:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   pyinstaller build_exe.spec
   ```
3. Find the executable in the `dist/` directory

See `build_instructions.txt` for detailed build instructions.

### Development

#### Project Structure

```
mf4_operations/
├── mf4_operations/          # Main package
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Entry point
│   ├── gui.py               # GUI application
│   ├── file_handler.py      # File I/O operations
│   ├── settings_manager.py  # Settings and history
│   └── plotter.py           # Data visualization
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── build_exe.spec           # PyInstaller configuration
└── README.md                # This file
```

#### Key Modules

- **file_handler.py**: Handles loading MF4/MDF/DAT files, channel extraction, data retrieval, and CSV export
- **settings_manager.py**: Manages user preferences and channel selection history
- **gui.py**: Main GUI application with Tkinter
- **plotter.py**: Plotting functionality using matplotlib

### License

This project is open source. Please refer to the LICENSE file for details.

### Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/sdrdx4100/mf4_operations).

---

## <a name="japanese"></a>日本語

### 概要

**MF4 Operations** は、自動車開発・試験で広く使用されるMF4、MDF、DATの計測ファイルを扱うための高速で軽量なアプリケーションです。INCAなどの計測器付属コンバーターと同等の機能を提供し、直感的なグラフィカルインターフェースでデータプレビュー、チャネル選択、CSV変換、可視化が行えます。

### 機能

- **複数形式対応**: MF4、MDF、DATファイルの読み込みと処理
- **データプレビュー**: チャネル情報付きで計測データを閲覧・プレビュー
- **チャネル選択**: 検索機能と履歴追跡による特定チャネル/ラベルの選択
- **CSV変換**: オプションのリサンプリング機能付きでCSV形式に変換
- **データ可視化**: 軽量なグラフライブラリでチャネルデータをプロット
- **可変リフレッシュレート**: カスタムレートでのデータリサンプリング対応
- **ユーザー設定**: 環境設定とラベル選択履歴の自動保存
- **エンコーディング対応**: 各種文字コードを堅牢に処理
- **クロスプラットフォーム**: Windows、Linux、macOSで動作
- **スタンドアロン実行可能ファイル**: エンドユーザーにPythonインストール不要

### インストール

#### 方法1: ソースコードから実行

1. Python 3.8以上をインストール
2. このリポジトリをクローン:
   ```bash
   git clone https://github.com/sdrdx4100/mf4_operations.git
   cd mf4_operations
   ```
3. 依存関係をインストール:
   ```bash
   pip install -r requirements.txt
   ```
4. アプリケーションを実行:
   ```bash
   python -m mf4_operations.main
   ```

#### 方法2: ビルド済み実行可能ファイルを使用

[Releases](https://github.com/sdrdx4100/mf4_operations/releases)ページから最新リリースをダウンロードして、実行可能ファイルを直接実行してください。

### 使用方法

1. **ファイルを開く**: 「File」→「Open File...」をクリック、または「Open File...」ボタンで計測ファイルを読み込み
2. **チャネルを閲覧**: 右パネルで利用可能なチャネルを表示
3. **チャネルを検索**: 検索ボックスでチャネル名によるフィルタリング
4. **チャネルを選択**: チャネルをクリックして選択（Ctrl+クリックで複数選択）
5. **リサンプリング設定**: リサンプルレートを秒単位で設定（0.0はリサンプリングなし）
6. **CSV変換**: 「Export Selected to CSV...」をクリックして選択チャネルを保存
7. **データをプロット**: 「Plot Selected Channels」をクリックしてデータを可視化
8. **履歴機能**: アプリケーションがファイルごとに以前のチャネル選択を記憶

### 技術詳細

#### 依存関係

- **asammdf**: MF4/MDFファイル読み込み用（業界標準ライブラリ）
- **pandas**: データ操作とCSV変換用
- **matplotlib**: データ可視化用
- **tkinter**: グラフィカルユーザーインターフェース用（Python付属）

#### ユーザー設定の保存場所

設定と履歴は以下に保存されます:
- Windows: `C:\Users\<ユーザー名>\.mf4_operations\`
- Linux/Mac: `~/.mf4_operations/`

ファイル:
- `settings.json`: アプリケーション環境設定
- `label_history.json`: チャネル選択履歴

### 実行可能ファイルのビルド

スタンドアロン実行可能ファイルをビルドする方法:

1. PyInstallerをインストール:
   ```bash
   pip install pyinstaller
   ```
2. 実行可能ファイルをビルド:
   ```bash
   pyinstaller build_exe.spec
   ```
3. `dist/`ディレクトリ内に実行可能ファイルが生成されます

詳細なビルド手順は`build_instructions.txt`を参照してください。

### 開発

#### プロジェクト構造

```
mf4_operations/
├── mf4_operations/          # メインパッケージ
│   ├── __init__.py          # パッケージ初期化
│   ├── main.py              # エントリーポイント
│   ├── gui.py               # GUIアプリケーション
│   ├── file_handler.py      # ファイルI/O操作
│   ├── settings_manager.py  # 設定と履歴
│   └── plotter.py           # データ可視化
├── requirements.txt         # Python依存関係
├── setup.py                 # パッケージセットアップ
├── build_exe.spec           # PyInstaller設定
└── README.md                # このファイル
```

#### 主要モジュール

- **file_handler.py**: MF4/MDF/DATファイルの読み込み、チャネル抽出、データ取得、CSV変換を処理
- **settings_manager.py**: ユーザー環境設定とチャネル選択履歴を管理
- **gui.py**: Tkinterを使用したメインGUIアプリケーション
- **plotter.py**: matplotlibを使用したプロット機能

### ライセンス

このプロジェクトはオープンソースです。詳細はLICENSEファイルを参照してください。

### サポート

問題、質問、貢献については、[GitHubリポジトリ](https://github.com/sdrdx4100/mf4_operations)をご覧ください。