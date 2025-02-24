# uv 101
Author: Jack Liu  
last updated: 2025/02/24


## install uv
* On macOS and Linux 
    ```shell
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
* On Windows
    ```shell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
    > 理論上會安裝到 `C:\Users\<使用者名稱>\.local\bin`，並自動設置環境變設  
* check uv installed
    ```shell
    uv -V
    uv --version
    ```

## install python
* 查看 python 版本清單
    ```shell
    uv python list
    ```
* 查看已安裝 python 版本
    ```shell
    uv python list --only-installed
    ```
* 安裝最新的穩定版本
    ```shell
    uv python install
    ```
* 安裝指定版本
    ```shell
    uv python install 3.13
    ```
* 解除安裝指定版本
    ```shell
    uv python uninstall 3.13
    ```

## init project
* **init a basic project**
    ```shell
    uv init [PATH]
    ```
* **Init package**
    ```shell
    uv init --package [PATH]
    ```
* **Init Library**
    ```shell
    uv init --package [PATH]
    ```
<!-- > **src layout vs flat layout** layouthttps://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/ -->

<!-- * **pyproject.toml**
    專案的 **meta data**定義如何構建、管理和安裝 package
    * 管理依賴 (dependency)
    * 指定虛擬環境和 Python 版本 (venv) -->

## venv
* 使用已安裝的最新版
    ```shell
    uv venv
    ```
* 使用指定版本
    ```shell
    uv venv --python 3.13
    ```

## dependencies
* 查看目前環境已安裝 package
    ```shell
    uv pip list
    ```
* 安裝 package
    ```shell
    uv add <package>
    ```
    the pip interface
    ```shell
    uv pip install <package>
    ```
    * **Q: What's the difference using pip insterface?**  
        * **uv pip install**: only install dependency, **do not** update pyproject.toml and uv.lock
        * **uv add**: not only install dependency, but also update pyproject.toml and uv.lock
    * **pyproject.toml**
        1. 定義專案的基本資訊，例如名稱、版本、依賴項等。
        2. 主要用於描述專案的需求，而不包含具體的鎖定版本。
        3. 依賴管理工具（如 poetry, uv）會根據這個檔案來解析並安裝對應的套件。
    * **uv.lock**
        1. 是 uv 這個 Python 套件管理工具使用的鎖定檔案。
        2. 鎖定專案的所有依賴及其確切版本，以確保在不同環境下安裝時獲得相同的結果。
        3. 類似於 poetry.lock 或 requirements.txt（但更精確），可用來確保可重現的安裝環境。
* Version Constraints
    * specific version
    ```shell
    uv add cowsay==6.1
    ```
    * specific version range
    ```shell
    uv add "cowsay>=5.0,<=6.1"
    ```
* Source Constraints
    * from git
    ```shell
    uv add git+https://github.com/encode/httpx
    ```
    如果使用自定的 source，`pyproject.toml` 會記錄額外資訊
    ```toml
    [tool.uv.sources]
    httpx = { git = "https://github.com/encode/httpx" }
    ```
    * specific git tag
    ```shell
    uv add git+https://github.com/encode/httpx --tag 0.28.1
    ```
    * specific git branch
    ```shell
    uv add git+https://github.com/encode/httpx --branch master
    ```
    * 可編輯套件 (Editable packages)
    ```shell
    uv add --editable <package_dir>
    ```
* remove dependency
    ```shell
    uv remove package
    ```
    the pip insterface
    ```shell
    uv pip uninstall package
    ```
* group
    * develop group
    ```shell
    uv add --dev pytest
    # uv add --group dev pytest
    ```
    * other group
    ```shell
    uv add --dev pytest
    uv add --group web flask
    ``` 
    ```toml
    [dependency-groups]
    dev = [
        "pytest>=8.3.4",
    ]
    web = [
        "flask>=3.1.0",
    ]
    ```
    移除時 group dependency 時也須須帶上 group option

    ```shell
    uv remove --group dev flask
    ```
## uv run
Before running, it will create venv (if not exists)

* run python file
    ```shell
    uv run 
    ```
* run python (interactive shell)
    ```shell
    uv run python
    ```
* run python (with command)
    ```shell
    uv run python -c "import lab2; lab2.main()"
    ```
* run with external dependency
    ```shell
    uv run --with httpx==0.26.0 python -c "import httpx; print(httpx.__version__)"
    ```
    the dependency will be installed automatically (in cache)
* run with entry point
    * set entry point in pyproject.toml
    ```toml
    [project.scripts]
    lab2 = "lab2:main"
    ```
    * run with entry point
    ```shell
    uv run lab2
    ```

## lock
* 解析 pyproject.toml 生成 uv.lock
    ```shell
    uv.lock
    ```
* 僅檢查 uv.lock，不更新
    ```shell
    uv pip freeze > requirements.txt
    ```
* 允許升級 dependency
    ```shell
    uv lock --upgrade
    ```
* 輸出為 requirements.txt
    ```shell
    uv export --format requirements-txt > requirements.txt
    ```
* 輸出為 requirements.txt (pip interface)
    ```shell
    uv pip freeze > requirements.txt
    ```

## sync
1. uv venv: create venv (if not exists)
2. uv lock: generate uv.lock (from pyproject.toml)
3. uv pip: install dependencies (from uv.lock)

* sync (default include dev group)
    ```shell
    uv sync
    ```
* to include other groups
    ```shell
    uv sync --group web --group dev 
    ```

## build
* 打包 package 為 source, wheel
    ```shell
    uv build
    ```
* 在打包時加入 extra 選項 (修改 pyproject.toml)
    ```toml
    [project.optional-dependencies]
    dev = ["pytest>=8.3.4"]
    web = ["requests>=2.32.3"]
    ```


### requirements.txt --> pyproject.toml

從 pip + requirements.txt 轉換成 uv + pyproject.toml

* 解析原本的 requirements.txt，產出帶有詳細版本訊息的版本
    ```shell
    uv pip compile requirements.txt --universal --output-file requirements.txt
    ```

* 安裝套件 同時更新 pyproject.toml
    ```shell
    uv add -r requirements.txt
    uv add --requirements requirements.txt
    ```