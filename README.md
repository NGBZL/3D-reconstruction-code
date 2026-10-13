# 3D-reconstruction-code

三维重建项目的**代码 + 任务（Issue）仓库**。

看板代码在另一个仓库：[NGBZL/3Dcooperate](https://github.com/NGBZL/3Dcooperate)
—— 那边只存放看板自己的代码，本仓库负责「写代码」和「记任务」。

## 这个仓库放什么

| 内容 | 说明 |
|------|------|
| 项目代码 | 分支、提交、Pull Request 都在这里 |
| 任务（Issue） | 看板上的每张卡片 = 本仓库的一个 Issue，看板从这里同步 |
| Agent 代码审核 | `.github/workflows/agent-review.yml` + `agent/`：push 之后自动审核，过审就关闭关联 Issue |

## 任务（Issue）怎么写

标题就是任务名；**正文第一行**写负责人代号：

```
**负责人**: 小明
```

> ⚠️ 仓库是公开的，里面只用**代号**（小明 / 小红 / 小刚 / 小丽 / 小强 / 小美），
> 不要写真实姓名。真名只存在各人本机的 `assignees.local.json`（已被 `.gitignore` 忽略），
> 由看板界面负责翻译成姓名显示。

* 状态用标签表示：`todo` / `doing` / `done`（看板会自动创建并同步这些标签）
* `done` 只能由 Agent 审核通过后写入：人工在看板上也拖不进 Done 列，进来之后也拖不出去

## 提交（commit）怎么关联任务

提交信息里带上关联的 Issue 编号，Agent 就会审核这次 push：

```bash
git commit -m "fix: 修正点云配准的边界判断 #12"
git push origin main
```

* 审核通过 → Agent 评论审核报告 + 打 `done` 标签 + 关闭 Issue → 看板同步后任务进 Done 列
* 审核不通过 → 只留评语，Issue 保持打开，看板上能看到「审核不通过」徽章
* 提交信息里**没有** Issue 编号时，Agent 只跑离线自检，不调用大模型（不花 token）

## 需要在仓库里配置的 Secret

`Settings → Secrets and variables → Actions`：

| 名称 | 必填 | 说明 |
|------|------|------|
| `LLM_API_KEY` | ✅ | 大模型 API Key，不配则 Agent 无法审核 |
| `LLM_API_URL` | 可选 | 默认 `https://api.deepseek.com/v1/chat/completions` |
| `LLM_MODEL` | 可选 | 默认 `deepseek-chat` |

`GITHUB_TOKEN` 由 GitHub Actions 自动注入，不需要自己配。

## 本地自检（不消耗 API）

```bash
pip install requests
python -m agent.selftest        # 离线自检：正则、JSON 解析、降级、审核流程
python tools/check_names.py     # 推送前检查有没有真实姓名漏进 Git
```

`.githooks/pre-commit` 是可选的钩子，想让它在提交前自动跑一遍姓名检查：

```bash
git config core.hooksPath .githooks
```
