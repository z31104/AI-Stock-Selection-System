# AI Stock Selection System

AI 智慧股票選股與投資配置系統

## 技術架構

- Python
- Flask
- SQLite
- Pandas
- Matplotlib
- Redis
- Docker
- Pytest

## 功能

### 股票查詢

- 台股資料抓取
- MA5 / MA20
- RSI
- KD

### 新聞分析

- 新聞趨勢分析
- 新聞分數
- AI分析

### 投資配置

- 本金配置
- 產業分散
- 停損停利建議

### 回測系統

- 歷史回測
- 報酬率分析
- 資產曲線

### 模擬投資

- 模擬買進
- 模擬獲利

### AI選股

- 綜合評分排序
- 推薦股票

## Redis Cache

避免重複呼叫 TWSE API

## Docker

啟動：

docker compose up -d

## 測試

python -m pytest