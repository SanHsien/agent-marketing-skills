# 產品 Skill 規格（本 fork 摘要）

完整寫作指引以上游歷史中的 `AGENTS.md` 與 [Agent Skills 規格](https://agentskills.io/specification.md) 為準。本檔只鎖定本 fork 驗收會檢查的契約，避免把產品文件翻成繁體。

## 目錄

```text
skills/<skill-name>/
├── SKILL.md        # 必填；主指令，建議 <500 行
├── references/     # 可選；按需載入
├── scripts/        # 可選
├── assets/         # 可選
└── evals/          # 上游評測樣本
```

`name` 必須與目錄名完全相同。

## Frontmatter

```yaml
---
name: skill-name
description: What this skill does and when to use it. Include trigger phrases.
---
```

| 欄位 | 必填 | 限制 |
|---|---|---|
| `name` | 是 | 1–64 字元，小寫 `a-z`、數字、連字號。不可開頭／結尾為連字號，不可連續 `--`，必須等於目錄名 |
| `description` | 是 | 1–1024 字元；寫清做什麼、何時觸發 |
| `license` | 否 | 預設 MIT |
| `metadata` | 否 | `version` 放這裡，不要放成 top-level `version` |

## 寫作邊界

- 產品語言維持英文。
- 不要在 `SKILL.md` 加入 Claude Code 專用的 `` !`command` ``；那會讓其他宿主看到字面字串。
- 提及工具時給選項而非唯一答案，通過「對調測試」。規則見 `tools/PARTNERS.md`。
- 不提交憑證或客戶資料。

本 fork 的 `tools/validate_skills.py` 檢查：每個 `skills/*/` 都有 `SKILL.md`、frontmatter 存在、`name` 符合目錄與格式、`description` 長度合法。警告（缺 trigger 用語、超過 500 行）不會讓 gate 失敗。
