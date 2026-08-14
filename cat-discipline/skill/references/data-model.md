# 数据模型与算法

> 存储结构与关键逻辑。功能语义见 `features.md`。所有日期键一律用**本地时间**生成，避免 UTC 跨天错位。

## 1. 存储结构

单一 localStorage 键，值为如下 JSON：

```js
{
  habits: [
    {
      id: "k3x",            // 唯一 id
      name: "喝水 8 杯",
      icon: "💧",           // 可爱图标
      color: "#4fa8d5",     // 代表色（日历圆点用，天蓝色系）
      records: { "2026-08-14": true, ... }  // 打卡记录，按本地日期键
    }
  ],
  todos: [
    {
      id: "t9a",
      name: "写周报",
      date: "2026-08-14",   // 目标日期（仅 repeat.type==='none' 时用它定位）
      repeat: {             // 重复规则对象（不再是 boolean）
        type: "none",       // "none" | "daily" | "weekly" | "custom"
        weekdays: [],       // weekly：命中的周几 0=日..6=六
        dates: []           // custom：自选日期键列表 ["2026-08-14",...]
      },
      time: "09:00",        // 计划时间，可为 null
      done: false,          // 当日完成态（重复类跨天会重置）
      doneDate: null        // 完成日期键
    }
  ],
  settings: {
    notify: false,           // 桌面通知
    banner: true,            // 进入提醒横幅
    catName: "咪咪",
    theme: "skyblue",       // 预留多主题
    weekStart: "sun"         // "sun" | "mon"
  },
  lastOpen: "2026-08-14"     // 上次打开日，用于跨天重置
}
```

> `assets/template.html` 已对齐本结构（v2），含 `date`/`color`/`repeat` 对象 + v1 旧数据自动迁移（`migrateData`：把 `repeat:boolean` 转 `{type,weekdays,dates}`、补 `date`/`color`、从 v1 键 `cat_discipline_v1` 迁移到 `cat_discipline_v2`）。

## 2. 日期工具（必须用本地时间）

```js
// 本地日期键，避免 toISOString 的 UTC 错位
function dateKey(d){               // d: Date
  const y=d.getFullYear(), m=String(d.getMonth()+1).padStart(2,'0'), da=String(d.getDate()).padStart(2,'0');
  return `${y}-${m}-${da}`;
}
const todayKey=()=>dateKey(new Date());
function parseKey(k){const [y,m,d]=k.split('-').map(Number);return new Date(y,m-1,d);}
function addDays(k,n){const d=parseKey(k);d.setDate(d.getDate()+n);return dateKey(d);}
function isBefore(a,b){return parseKey(a)<parseKey(b);}   // a<b
function sameDay(a,b){return a===b;}
```

## 3. 关键算法

### 连续打卡 streak
```js
function streakOf(habit){
  let s=0; const rec=habit.records||{}; let k=todayKey();
  while(rec[k]){s++;k=addDays(k,-1);}
  return s;
}
```

### 跨天重置重复待办（daily/weekly/custom 统一逻辑）
```js
function dailyResetIfNeeded(){
  const t=todayKey();
  if(data.lastOpen!==t){
    data.todos.forEach(o=>{
      const r=o.repeat||{type:'none'};
      if(r.type!=='none' && o.done && o.doneDate!==t){o.done=false;o.doneDate=null;}
    });
    data.lastOpen=t; save();
  }
}
```
> 统一逻辑：所有重复类（daily/weekly/custom）待办，只要 `done` 且 `doneDate` 不是今天，就重置为未完成。下次命中日到来时自动变回待完成态。

### 某日有哪些待办（日历单元格 / 日详情用）
```js
function todoHitsDate(o,date){
  const r=o.repeat||{type:'none'};
  if(r.type==='daily')  return true;                                       // 每天都出现
  if(r.type==='weekly') return (r.weekdays||[]).includes(parseKey(date).getDay()); // 命中选中周几
  if(r.type==='custom') return (r.dates||[]).includes(date);              // 命中自选日期
  return o.date===date;                                                    // 单次：日期命中
}
function todosForDate(date){ return data.todos.filter(o=>todoHitsDate(o,date)); }
```

### 单元格综合状态（日历渲染核心）
```js
function calendarDayState(date){
  const t=todayKey();
  const habits=data.habits.map(h=>({h,done:!!(h.records||{})[date]}));
  const todos=todosForDate(date);
  const pending=todos.filter(o=>!o.done).length;
  const done=todos.filter(o=>o.done).length;
  const overdue=todos.filter(o=>!o.done && (o.repeat||{}).type==='none' && isBefore(o.date,t)).length;
  return { habits, habitDone:habits.filter(x=>x.done).length, habitTotal:habits.length,
           todoPending:pending, todoDone:done, todoOverdue:overdue, isToday:date===t };
}
```

### 月历矩阵（按周起始日）
```js
function monthMatrix(year,month,weekStart='sun'){
  const first=new Date(year,month,1);
  let offset=first.getDay();               // 0=日..6=六
  if(weekStart==='mon') offset=(offset+6)%7;
  const start=new Date(year,month,1-offset);
  const cells=[];
  for(let w=0;w<6;w++){
    const week=[];
    for(let d=0;d<7;d++){
      const cur=new Date(start); cur.setDate(start.getDate()+w*7+d);
      week.push({date:dateKey(cur), inMonth:cur.getMonth()===month, state:calendarDayState(dateKey(cur))});
    }
    cells.push(week);
  }
  return cells;                            // 6 行 × 7 列
}
```

## 4. 边界与约定

- **补打历史日**：允许在日详情给过去日期打卡（`records[历史键]=true`）；但 streak 只从今天向前连续计数，补打不直接续 streak（如需「补卡续 streak」需另设开关，默认关闭以免作弊）。
- **重复待办的「过期」**：daily/weekly/custom 待办只在命中日显示与提醒，不标过期；仅 `repeat.type==='none'` 且日期早于今天且未完成才标过期。
- **完成态语义**：单次（none）完成后永久 done；重复类（daily/weekly/custom）done 只代表「最近一次命中日完成了」，跨天（`doneDate !== today`）即重置。
- **导出/清空**：导出整份 data；清空需二次确认并重置为空结构（保留 settings）。
