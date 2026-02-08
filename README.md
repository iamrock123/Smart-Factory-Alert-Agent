# Anomaly Alert AI Agent

這是一個基於 Python 與 UV 管理的異常偵測 AI 代理專案。
專案包含資料生成、異常偵測（規則與機器學習），以及基於 Ollama (LLM) 的智慧分析代理。

## 專案結構

- `data_generator.py`: 生成測試用的 `data/test_data.csv`，包含約 20% 的異常數據。
- `anomaly_detector.py`: 實作異常偵測邏輯。
    - **規則偵測**: 檢查溫度、壓力、震動是否超出設定範圍 (區分 Warning/Critical)。
- `agent.py`: 整合 `anomaly_detector` 與 `langchain-ollama`。
    - 針對偵測到的異常，讀取 `config/knowledge_base.md` 提供 LLM 支援的綜合診斷報告。
- `data/`: 存放 CSV 數據檔 (`test_data.csv`, `sensor_data.csv`).
- `config/`: 存放設定檔 (`knowledge_base.md`).
- `pyproject.toml`: 專案依賴設定（由 `uv` 管理）。

## 安裝與執行

### 前置需求
1. 安裝 [uv](https://github.com/astral-sh/uv)。
2. 安裝並啟動 [Ollama](https://ollama.com/) (預設模型 `gemma3:4b` 或 `llama3`)。
   ```bash
   ollama serve
   ollama pull gemma3:4b
   ```

### 步驟

1. **初始化與安裝依賴**
   ```bash
   uv sync
   ```

2. **生成數據**
   ```bash
   uv run python test_data_generator.py --rows 20
   ```
   這會產生 `data/test_data.csv`。

3. **執行異常偵測 (單獨測試)**
   ```bash
   uv run python anomaly_detector.py
   ```
   這會顯示規則偵測結果摘要。

4. **執行 AI Agent**
   ```bash
   uv run python agent.py --model Qwen3:4b
   ```
   預設使用 `Qwen3:4b` 並讀取 `data/test_data.csv`。Agent 會提供一份綜合診斷報告。
   也可以使用 `uv run python agent.py --help` 查看說明。

## 異常定義

- **Temperature**: Normal 45–50°C (Abnormal >52 or <43)
- **Pressure**: Normal 1.00–1.05 (Abnormal >1.08 or <0.97)
- **Vibration**: Normal 0.02–0.04 (Abnormal >0.07)
