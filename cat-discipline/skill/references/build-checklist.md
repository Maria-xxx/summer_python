# 分阶段构建清单

> 按阶段实现，每阶段勾选后再进下一阶段。功能语义见 `features.md`，算法见 `data-model.md`。

## Phase 0 · 脚手架
- [ ] 复制 `assets/template.html` 到工作区为 `index.html`
- [ ] 确认 template 已含：日历主视图、习惯打卡、待办（四类重复）、设置、猫咪 SVG、导出/清空
- [ ] 确认 v1→v2 旧数据迁移（`migrateData`）生效：`repeat:boolean` → `{type,weekdays,dates}`、补 `date`/`color`、从 v1 键迁到 v2 键

## Phase 1 · 数据层
- [ ] 本地日期工具（`dateKey`/`addDays`/`isBefore`，**勿用 `toISOString`** 防 UTC 错位）
- [ ] `streakOf`、`dailyResetIfNeeded`、`todoHitsDate`/`todosForDate`、`calendarDayState`、`monthMatrix`
- [ ] 启动时调用 `dailyResetIfNeeded()`

## Phase 2 · 日历主视图（核心 · template 已实现）
- [x] 月历网格渲染（6×7，周起始可配）
- [x] 今天高亮、选中日区分、翻月导航 +「今天」回跳
- [x] 单元格习惯圆点（≤4 逐个显示，>4 显示 n/m）+ 待办徽标（全完成绿/有未完成橙/过期红）
- [x] 有活动日淡蓝底色、空日中性白；图例
- [x] 点击某日下钻日详情面板（补打习惯 / 完成待办 / 快速新增到指定日）

## Phase 3 · 习惯落到日历
- [ ] 习惯增删（分配 icon + color）
- [ ] 日详情面板里一键打卡/取消（含历史日补打）
- [ ] streak 正确；单元格随打卡即时更新
- [ ] 习惯列表页（次要）：streak + 最近 7 天迷你日历

## Phase 4 · 待办落到日历（template 已实现四类重复）
- [x] 添加待办指定 `date`（默认今天）+ 计划时间
- [x] 四类重复：不重复 / 每天 / 每周几（多选） / 自选日期（chips 多选）
- [x] `todoHitsDate` 命中判定；日历单元格计数正确
- [x] 完成/取消；过期高亮（仅 none 类）；跨天重置（daily/weekly/custom 统一）
- [x] 日详情里完成切换 + 快速新增到指定日（单次）
- [x] 待办列表页「今日 / 全部」切换

## Phase 5 · 提醒
- [ ] 进入横幅列出今日未完成（开关）
- [ ] 桌面通知授权流程 + 打开应用时弹通知
- [ ] 过期/今日待办在日历可见（兜底）

## Phase 6 · 统计
- [ ] 累计打卡、最长连击、今日/本月完成率
- [ ] 热力图（与日历同日期键）
- [ ] 各习惯 streak 排行 + 本月覆盖率

## Phase 7 · 个性化与数据
- [ ] 猫咪命名、撸猫互动（开心/日常表情切换）
- [ ] 导出 JSON、清空（二次确认）

## Phase 8 · 打磨与校验
- [ ] 提取 `<script>` 跑 `node --check`
- [ ] 小窗口响应式抽查
- [ ] 对照本清单逐项核对
