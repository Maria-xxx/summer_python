---
name: cat-discipline-app
description: This skill should be used when building a cute/cat-themed personal self-discipline desktop app that marks habits AND todos clearly on a CALENDAR. Trigger on requests like "把待办和习惯标在日历上", "猫咪主题自律应用", "日历式习惯打卡+待办", "萌系自律效率工具", or any PC app uniting habit tracking, todo scheduling, and a clear month-calendar view with a cat/mascot aesthetic. It supplies a layered multi-file design spec (positioning, features, data model, build checklist, extensions) plus a single-file HTML scaffold — zero-install, localStorage, no backend.
agent_created: true
---

# Cat Discipline App

## Overview

Build a cute, cat-themed personal self-discipline desktop app with a **light sky-blue palette** whose **centerpiece is a month calendar** that clearly marks both habits (per-day check-in) and todos (scheduled by date), so the user sees their whole discipline life in one picture. Delivered as a single zero-install HTML file (localStorage, no backend). The adorable cat companion and instant positive feedback turn discipline into a low-pressure daily ritual.

## When To Use

- User wants a habit tracker + todo tool with a clear calendar view (mark both on the calendar).
- User wants a cute / cat / mascot-themed PC self-discipline app that runs by double-clicking a file.
- Requests mention 自律, 习惯打卡, 待办, 日历, 萌系/猫咪, 在日历上标出.

## File Map (progressive disclosure — read what you need)

| File | Contents | Read when |
|------|----------|-----------|
| `references/design.md` | Product positioning, target users, design principles, visual language | Confirming product direction & tone before building |
| `references/features.md` | Feature modules with the calendar as centerpiece + per-feature spec & acceptance | Defining scope, what to build, acceptance criteria |
| `references/data-model.md` | Storage schema + key algorithms (streak, recurrence, calendar-day state, overdue) | Implementing the data layer / calendar logic |
| `references/build-checklist.md` | Phased build checklist with checkboxes | Tracking progress; verify before delivery |
| `references/extensions.md` | Advanced / beyond-MVP paths | User asks for background reminders, sync, themes, etc. |
| `assets/template.html` | Complete single-file app: calendar main view + habits + todos (4 recurrence types: none/daily/weekly/custom) + stats + settings, light sky-blue theme, cat SVG mascot | Copy as starting point; customize visuals/features as needed |

## Build Workflow

1. **Confirm direction**: read `references/design.md` for positioning & visual language; align scope with the user.
2. **Define scope**: read `references/features.md`; the calendar main view (§1) is the centerpiece and must ship first. Negotiate any module cuts with the user.
3. **Copy template**: copy `assets/template.html` to the target workspace. It already ships the calendar main view + habits + todos (four recurrence types) + stats + settings + cat companion + sky-blue theme. Customize features/visuals as needed; reference `features.md` §1 and `data-model.md` for the design contract.
4. **Tweak data layer** per `references/data-model.md` if changing recurrence/streak/overdue semantics (template already implements `streakOf`, `dailyResetIfNeeded`, `todoHitsDate`/`todosForDate`, `calendarDayState`, `monthMatrix`, local date keys).
5. **Build features in phases** following `references/build-checklist.md` (scaffold → data → calendar → habits-on-calendar → todos-on-calendar → reminders → stats → personalization/data → polish).
6. **Validate**: extract the embedded `<script>` and run `node --check` after edits.
7. **Verify scope fit** against the checklist in `references/build-checklist.md` before delivering.

## Design Constraints

- Single self-contained HTML file: inline CSS + JS, no build step, no external dependencies.
- All data in `localStorage` under one key; provide JSON export + clear-all so the user stays in control.
- Calendar is the primary surface; habit and todo markers must be legible at a glance in a month cell.
- Instant feedback for every action (check-in animation, toast, live streak / calendar cell update).
- Use **local** date keys to avoid UTC off-by-one (see `references/data-model.md`).
- Responsive enough for basic viewing on smaller windows.
