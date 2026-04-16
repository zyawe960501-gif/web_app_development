---
name: commit
description: 提交程式碼變更。用於階段性任務完成後，總結開發內容並產生符合規範的 Git Commit Message，最後執行 commit。
---

# Commit Skill — 版本控制提交

這個 skill 會引導 AI agent 檢查目前專案的變更、產生適當且符合規範的 Git Commit Message，並將變更提交到版本控制系統。

## When to use this skill

- 完成一個階段性任務（如：完成某個頁面、修正某個 Bug）
- 準備將目前進度封裝為一個版本時
- 在進行下一個重大的改動之前

## How to use it

### 步驟一：檢查專案變更狀態

```text
請幫我檢查專案目前有哪些變更。
請執行 `git status` 了解修改了哪些檔案，如果有需要，可以執行 `git diff` 或是 `git diff --staged` 來詳細了解變更內容。
看完後請列出這些變更的摘要。
```

### 步驟二：產生 Commit Message 並請使用者確認

```text
請根據變更內容，幫我草擬一段符合 Conventional Commits 規範的 Commit Message。
格式要求：
1. `<type>(<scope>): <subject>`
   - `type` 選項包含：feat, fix, refactor, docs, style, test, chore
   - `subject` 請使用簡明扼要的描述
2. 如果修改內容較多，請換行後補充 `body` 說明為什麼這樣修改，以及改了什麼。

請列出你草擬的訊息，並問我是否可以執行 `git add .` 與 `git commit`？
```

### 步驟三：執行提交

```text
當我同意後，請幫我執行 `git add .`。
接著使用你剛剛草擬的訊息來執行 `git commit -m "訊息"`。
完成後請顯示提交的結果（`git log -1`）。
```

## 注意事項

- 如果專案尚未初始化 Git，請先詢問是否要執行 `git init`。
- 切勿在未經使用者同意的情況下直接執行提交指令。
- 確保不要提交不想追蹤的檔案（需要確認是否有正確的 `.gitignore`）。
