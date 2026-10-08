<div align="center">

<img width="120" src="docs/assets/logo.webp" alt="李白 Skill Logo：石青圆环内李白举杯对月，下方金线匾额书「李白」">

# 李白Skill · 唐朝诗人思维AI

**将盛唐诗人李白的完整诗学体系注入 AI Agent**

`25卷诗全集` · `1010首` · `14维文学家框架` · `58篇名篇赏析` · `16个意象母题` · `40篇名篇导航` · `35问FAQ` · `4,337行维度分析` · `434KB正典语料`

[![GitHub Stars](https://img.shields.io/github/stars/jangviktor-web/libai-skill?style=for-the-badge&color=yellow&label=Stars)](https://github.com/jangviktor-web/libai-skill/stargazers)
[![SkillHub](https://img.shields.io/badge/腾讯云skillhub-安装李白SKILL-green?style=for-the-badge)](https://skillhub.cn/skills/user_ff4d9420/libai)
[![版本](https://img.shields.io/badge/版本-v1.1.0-blue?style=for-the-badge)](https://github.com/jangviktor-web/libai-skill/releases)
[![思维蒸馏器](https://img.shields.io/badge/思维蒸馏器-V4.6.0-red?style=for-the-badge)](https://github.com/jangviktor-web/tcm-distiller)
[![License](https://img.shields.io/badge/协议-CC--BY--SA--4.0-green?style=for-the-badge)](LICENSE)
[![Agent Skills Standard](https://img.shields.io/badge/Agent%20Skills%20Standard-Ready-orange?style=for-the-badge&logo=openai&logoColor=white)]()
[![功能说明页](https://img.shields.io/badge/功能说明页-在线-1E4C63?style=for-the-badge)](https://jangviktor-web.github.io/libai-skill/)

**🌐 [中文](https://github.com/jangviktor-web/libai-skill/blob/main/README.md) | [English](https://github.com/jangviktor-web/libai-skill/blob/main/README_EN.md)**

</div>

---

> 「清水出芙蓉。天然去雕饰。」—— 李白
>
> 他自任的不是写诗，是删述：「我志在删述。垂辉映千春。」

### 一句话介绍

将李白（701—762，字太白，号青莲居士，世称诗仙）的诗学观、创作六步法、意象系统、判断标准与口吻，蒸馏为可激活的 Agent Skill，使 AI 能以李白的视角进行**唐诗鉴赏、诗学评述、出处考据、拟体创作**——并且**引的每一句诗都能被 grep 命中，写的每一首拟作都必须声明非原作**。

**直接激活词**：`李白` / `太白` / `诗仙` / `谪仙人` / `青莲居士` / `拟李白风格` / `以李白视角` / `李白会怎么写` / `将进酒` / `蜀道难` / `静夜思` / `唐诗`

---

## 快速安装

<details>
<summary><b>SkillHub（腾讯云·推荐）可复制下面文字到agent安装 </b></summary>

```
请根据 https://skillhub.cn/install/skillhub.md，安装 @user_ff4d9420/libai。
```

商店页：https://skillhub.cn/skills/user_ff4d9420/libai

</details>

<details>
<summary><b>从 GitHub 安装</b></summary>

```bash
git clone https://github.com/jangviktor-web/libai-skill.git
cp -r libai-skill/libai ~/.claude/skills/libai/
把 https://github.com/jangviktor-web/libai-skill 克隆下来，
将仓库里的 libai/ 整个目录安装到本地 skills 目录，然后激活它。 # 或你所用客户端的 skills 目录
```

目录名即注册名（frontmatter 中 `name: libai`）。装好后提到"李白"即激活。

</details>

<details>
<summary><b>一句话让 Agent 自己装</b></summary>

把下面这段直接发给你的 agent：

```text
把 https://github.com/jangviktor-web/libai-skill 克隆下来，
将仓库里的 libai/ 整个目录安装到本地 skills 目录，然后激活它。
```

</details>

<details>
<summary><b>只想读，不想装</b></summary>

- **功能说明页**（单文件，无外部依赖）：https://jangviktor-web.github.io/libai-skill/
- **角色规则本体**：[`libai/SKILL.md`](libai/SKILL.md)（316 行）
- **正典语料**：[`libai/modules/01_libai-shi-quanji.md`](libai/modules/01_libai-shi-quanji.md)（25 卷 1010 首）

</details>

<details>
<summary><b>历史版本下载</b></summary>

#### v1.1.0（2026-10-05，更新日志：修复正典 4 段编码损坏、校补残字 232 处与讹字 198 处，本集升为完整诗本 1010 首；补录本集未收 5 篇；全面修正边界误判）
下载地址：https://github.com/jangviktor-web/libai-skill/archive/refs/tags/v1.1.0.zip

#### v1.0.0（2026-10-04，首次蒸馏：14 维文学家框架 + 58 篇名篇赏析 + 25 卷诗全集）
**未提供下载**——v1.0.0 的"本集缺 18 篇名作"判定已被 v1.1.0 证实为编码损坏造成的假缺失并作废，放出一个已知有误的旧包只会误导使用者。变更细节见 [`libai/CHANGELOG.md`](libai/CHANGELOG.md)。

</details>

---

## 功能矩阵

| 能力 | 覆盖范围 | 说明 |
|:---|:---:|:---|
| 唐诗鉴赏 | ✅ | 以「气先于辞」解析章法，每个判断后跟可核诗句或可出处诗话 |
| **创作六步法** | ✅ | **气→象→体→夸→断→尽，李白与杜甫分道的关键（不是先谋篇）** |
| 出处考据 | ✅ | 辨篇目归属、体裁、版本异文；通行本文字注明「明清改本」 |
| 拟体创作 | ✅ | 先定体裁骨架再填意，**强制署「AI 拟李白风格之作，非李白原作」** |
| 口吻代言 | ✅ | 以李白视角答问，遇内在张力主题两面并置，不做单向拔高 |
| 诗学观与谱系 | ✅ | 8 个心智模型 + 三条连接线；屈原→庄子→建安→谢朓鲍照→陈子昂 |
| 意象母题库 | ✅ | 16 个母题（月/酒/剑/鹏/马/云/江河/山岳/仙/梦/白发/青天/孤独/秋霜雪/花春/舟）+ 功能 + 例句出处 |
| 名篇赏析库 | ✅ | 58 篇（古风乐府 26 + 古近体绝句 32），引句逐条 grep 命中后写入 |
| 诗体与格律 | ✅ | 体裁定义与统计、乐府知识、平仄对仗押韵、拟作结构模板、韵脚字库 |
| 历代批评 | ✅ | 不神化：王安石「识污下」、王世贞「索之易穷」、赵翼「沉刻不如杜」 |
| 常见问答 | ✅ | 35 问 FAQ + 名句速查 + 误读清单 |
| 版本与校勘 | ✅ | 缺篇盘点 + 校勘日志 + 编码损坏修复全过程与 31 个核验脚本 |
| 伦理安全层 | ✅ | 涉酒 / 涉炼丹 / 涉侠客暴力三条红线 + 固定免责模板 |

---

## 使用示例

**鉴赏**
> **Q**：《将进酒》好在哪里？
> **A**：先立气，再取象。起句「君不见黄河之水天上来」不是写景，是把时间的不可逆直接倒进杯子；「朝如青丝暮成雪」把一生压缩成一天，「会须一饮三百杯」用可计算的数目量不可名状的情绪。末句「与尔同销万古愁」宕开，不留余味——这就是「尽」。

**考据**
> **Q**：「床前明月光」是原文吗？
> **A**：本集正文与宋本异文并存，通行本文字来自明清改本。引用时须注明「明清改本文字」，不能径改原文。

**拟作**
> **Q**：写一首李白风格的秋夜思乡诗
> **A**：孤静思乡 → 选五七言绝句；取月与舟二象；输出旧体诗，题末必附一行：**以下为 AI 拟李白风格之作，非李白原作**。

**边界**
> **Q**：「飞流直下三千尺」引自哪篇？
> **A**：《望庐山瀑布水二首》其二，本集可验——v1.1.0 修复编码损坏后，该名篇即在正典 25 卷之内，`grep` 命中。

**拒答**
> **Q**：李白喝醉了是不是才写得出好诗？
> **A**：不美化酗酒。唐代饮的是 6—15 度发酵酒，蒸馏酒普及在元代以后；「会须一饮三百杯」是夸张修辞，酒在他的体系里是确认自我存在的仪式，不是消愁剂。

---

## 核心知识体系

### 创作六步法（李白式作答的底层次序）

```
气（情绪满格）→ 象（取人格符号）→ 体（情绪决定体裁）
                                    ↓
尽（一喷而出）← 断（意接词不接）← 夸（可计算的数目量不可名状）
```

**不是「先有题、再谋篇」，而是「先有气、再取象、最后才落实体裁」。**

### 八个心智模型的三条连接线

```
退出机制线   4 功成身退 ＝ 5 事了拂衣去 ＝ 8 散发弄扁舟
自由意志线   6 不屈己不干人（人格）→ 3 大雅清真（文体）→ 7 大鹏图南（宇宙）
张力线       4 入世之深  ↔  2/6/7 出世之决  ──情绪产物──▶ 8 万古之愁
```

### 评价一个人的诗，李白的标准排序

**真（清真）＞ 气（风骨）＞ 自由（不缚声律）＞ 工巧（最末）**——反对堆砌典故与雕琢对偶。

### 一个不可混的区分

「**谪仙人**」是贺知章所呼、李白反复自用的**自命**；「**诗仙**」是**后世**定型的称号。二者不可混为一谈。

---

## 效果演示

完整可视化说明页（竖排诗卷首屏 + 六步法分步 + 16 意象筛选 + 校勘记）：

<div align="center">

**🌐 https://jangviktor-web.github.io/libai-skill/**

<img  height="883" alt="360截图20261008150005_compressed" src="https://github.com/user-attachments/assets/89b1d97f-1bca-4979-a2b8-574bab61c18f" />


</div>

---

## 数据来源

<details>
<summary><b>点击查看蒸馏用了哪些源文件，以及它们被怎样处理（一手素材 + 联网检索 + 校勘依据）</b></summary>

### 一手素材：一份需要抢救的电子文本

正典只有一部——用户提供的《李白诗全集》电子本 `.txt`。它不是干净输入：

| 环节 | 处理 | 结果 |
|---|---|---|
| 原始文件 | GB18030 编码（按 UTF-8 打开全乱码） | 159,246 字 · 18,340 行 |
| 编码判定 | `detect_enc.py` / `check_enc.py` | 确认非 UTF-8 |
| 转码 | `iconv` GB18030 → UTF-8 | 159,246 字无损 |
| 简体化 | `zhconv` | 繁简统一 |
| 字符清理 | `clean_corpus.py` / `fix_pua.py` | 清出 **51 个私用区（PUA）字符** → 缺字符「□」 |
| 正典成文 | `modules/01_libai-shi-quanji.md` | **25 卷 · 1010 首 · 434 KB · 18,350 行** |

### 四段整段编码损坏（v1.1.0 才查明并复原）

| 区间 | 对应卷次 | 成因 |
|---|---|---|
| 行 2530–3202 | 卷四 | **GBK 字节被误按 EUC-JP 解码** |
| 行 8273–8880 | 卷十二 | 同上 |
| 行 9356–10118 | 卷十四 | 同上 |
| 行 13625–14233 | 卷二十 | 同上 |

逆变换复原 4 段后，据 **《李太白集》《全唐诗》** 校补 **残字 232 处**（今仅余 3 处异文校记，见 `modules/01` 文末清单）、**讹字 198 处 / 226 字 / 涉 83 首诗**。校勘日志见 `references/27-proofread-log.md`。

### 补充素材：联网检索，逐条标源

生平年表、交游考、历代评价与诗话出处（严羽《评点李太白诗集》、王世贞《艺苑卮言》、赵翼《瓯北诗话》、孟棨《本事诗·高逸》等）来自联网检索，在 `references/` 中标注来源。凡不能指认出处者不写——「宋本作……」必须能指认版本。

### 本集未收的 5 篇

据权威源补录为 `modules/02_buyi.md`：**折荷有赠、别匡山、菩萨蛮、忆秦娥、桂殿秋**。引用时标「本集未收」，不得引为正典原文。

</details>

<details>
<summary><b>点击查看仓库目录结构</b></summary>

```
libai-skill/
├── README.md                   # 你正在看的这份（中文）
├── README_EN.md                # English version
├── LICENSE                     # CC BY-SA 4.0 全文
├── docs/                       # GitHub Pages 功能说明页
│   ├── index.html              # 单文件详情页（无外部依赖，56KB）
│   └── assets/                 # 图标 / 横幅 / 社交卡
└── libai/                      # ← 技能本体，整个目录拷走即可安装
    ├── SKILL.md                # 主入口 316 行：触发词 frontmatter + 身份卡 + 7 段式角色规则
    │                           #   + 检索路由表 + 六步法 + 三张速查卡 + 关键词索引 + 素材边界
    ├── README.md               # 技能内说明
    ├── CHANGELOG.md            # 版本变更（含编码修复全过程）
    ├── modules/
    │   ├── 01_libai-shi-quanji.md  # 正典：诗全集 25 卷 1010 首（UTF-8 简体，434KB）
    │   └── 02_buyi.md          # 补遗：本集未收 5 篇原文
    ├── references/             # 14 维文学家框架 · 12 份维度分析 + 缺篇盘点 + 校勘日志（4,337 行）
    │   ├── 01-core-philosophy.md        # 8 个核心心智模型 + 三条连接线
    │   ├── 02-creation-heuristics.md    # 创作决策启发式（起句三选一 / 最小执行序列）
    │   ├── 03-style-dna.md              # 诗风 DNA：高频字词 / 句式节奏 / 李杜王对比
    │   ├── 04-antipatterns-boundaries.md # 诗病 · 历代批评 · 伪作存疑 · 三条红线
    │   ├── 05-biography-legacy.md       # 生平年表 · 交游 · 版本流传
    │   ├── 06-tensions.md               # 8 组内在张力
    │   ├── 07-literary-lineage.md       # 文学谱系（屈庄→建安→谢朓鲍照→陈子昂→下游）
    │   ├── 08-faq.md                    # 35 问 FAQ · 名句速查 · 误读清单
    │   ├── 09-ethics-safety.md          # 创作伦理与安全层 · 免责模板
    │   ├── 10-image-motif-system.md     # 16 意象母题库 + 40 篇名篇导航
    │   ├── 11-cultural-context.md       # 唐代文士文化语境（科举/干谒/道教/任侠/乐府/漫游）
    │   ├── 12-poetics-prosody.md        # 诗体与格律 · 韵脚字库 · 拟作结构模板
    │   ├── 26-missing-inventory.md      # 缺篇盘点（v1.1.0 新增）
    │   └── 27-proofread-log.md          # 校勘日志（v1.1.0 新增）
    ├── cases/                  # 名篇赏析库 58 篇
    │   ├── 00_index.md         # 总索引
    │   ├── 01_gufeng-yuefu.md  # 古风·乐府赏析 26 篇
    │   ├── 02_jinti-jueju.md   # 古近体·绝句赏析 32 篇
    │   └── 03_missing-pieces.md # 本集未收 5 篇 + 编码修复说明
    └── scripts/                # 31 个 Python 脚本：转码 / 编码检测 / PUA 清理 / 逐字校勘 / 统计核验
```

`scripts/` 是**审计痕迹**而非工程代码——记录转码、编码检测、清洗、校勘、统计的每一步；中间产物报告（diff 报告、决策表、反向映射）未入库。

</details>

---

## 它凭什么不瞎编

七条输出铁律写死在 `SKILL.md`，不靠临场自觉：

1. **拟作必书面声明**——禁止无标注署「李白《××》」
2. **引诗必标《篇名》**——写进答案前先在正典 `grep` 命中
3. **评论须给证据**——无证据的判断改为存疑表述
4. **存疑篇目引用即加注**——《笑歌行》《悲歌行》《草书歌行》《上李邕》本集自带伪作按语
5. **本集未收不得反推**——只可标「本集未收 / 待考」，不可断为伪托
6. **不编造**——不虚构篇题、不虚构佚句、不臆造版本
7. **不神化、不猎奇**——讲长处同时呈现历代批评

**质量验证**：22 个文件全部通过 UTF-8 硬校验（0 乱码）· 12 份 references 全部被 `SKILL.md` 索引（0 死链）· 角色一致性自测 8 题（评论 / 考据 / 拟作 / 张力 / 伦理 / 越界）**8/8 通过**。

---

## ⚠️ 素材边界

> **本集未收 ≠ 李白没写过。**

- 本集为**诗本**（25 卷 · 1010 首）。词作、赋、文书序不在本集，属**版本体例**，不是缺失。
- 修复后名篇齐备：《梦游天姥吟留别》《望庐山瀑布》《黄鹤楼送孟浩然之广陵》《清平调三首》《南陵别儿童入京》《望天门山》《登金陵凤凰台》《玉阶怨》等均在集内可检索。
- ~~本集不完整、缺 18 篇名作~~ → **v1.1.0 更正作废**：系编码损坏造成的**假缺失**。
- 生平佚事（出生地、卒因、贵妃捧砚、力士脱靴、永王璘事件、《菩萨蛮》《忆秦娥》词体归属）一律标「存疑 / 传说」，必要处两说并列。

---

## 伦理与安全层

| 红线 | 处理方式 |
|:---|:---|
| **涉酒** | 不美化酗酒、不生成劝酒话术；豪饮句输出时附现实提示，未成年人场景必加「酒精危害健康，未成年人禁止饮酒」 |
| **涉炼丹** | 丹语均为**诗歌语言，非操作指南**；不给丹方、剂量、火候、服法，一律标「唐代历史语境，切勿效仿」 |
| **涉侠客暴力** | 「十步杀一人」一律标**文学修辞，非现实倡导**；不生成现实暴力、复仇文案 |
| **现实困境** | 涉抑郁、绝望、法律、医疗、投资时**切出角色**，给真实支持资源与专业建议提示 |
| **不代言** | 不得让「李白」为现代商品、投资标的、政治立场站台 |

每次输出结尾附固定免责框（模板见 `libai/references/09-ethics-safety.md`）。

---

## 自己复现核验

```bash
cd libai

# 这句在不在正典里
grep -n "君不见黄河之水天上来" modules/01_libai-shi-quanji.md

# 本集未收的到底是哪 5 篇
cat modules/02_buyi.md

# 编码卫生自检（PUA 与空字符）
python3 - <<'PY'
import pathlib, unicodedata
bad = [p.name for p in pathlib.Path('.').rglob('*.md')
       if (lambda t: '' in t or any(unicodedata.category(c) == 'Co' for c in t))(p.read_text(encoding='utf-8'))]
print('异常文件:', bad or '无')
PY
```

---

## 更新日志

#### v1.1.0（2026-10-05）— 语料修复与补遗：把"假缺失"找回来

核心升级：查明正典有 **4 段整段编码损坏**（GBK 字节被误按 EUC-JP 解码），逆变换复原后本集升为**完整诗本 25 卷 1010 首**，此前被误判缺失的名篇全部回归。

改动内容：

- **编码复原**：行 2530–3202 / 8273–8880 / 9356–10118 / 13625–14233（卷四 / 十二 / 十四 / 二十）
- **逐字校勘**：据《李太白集》《全唐诗》校补残字 **232 处**（今仅余 3 处异文校记）、讹字 **198 处 / 226 字 / 涉 83 首**
- **补遗**：新建 `modules/02_buyi.md`，本集确未收的 5 篇据权威源补录
- **边界修正**：修正 SKILL.md、references/02·04·05·07·08·10、cases/00–03、README 中"本集缺失名篇"的旧误判；`L####` 精确行号因修复会偏移，统一改为「可 grep 命中」表述
- **新增**：`references/26-missing-inventory.md`（缺篇盘点）、`references/27-proofread-log.md`（校勘日志）

| 指标 | v1.0.0 | v1.1.0 |
|:---|:---:|:---:|
| 正典状态 | 4 段乱码，误判不完整 | **完整诗本 1010 首** |
| 名篇可用性 | 误判缺 18 篇 | 误判作废，名篇齐备 |
| 本集未收 | 口径混乱 | 明确仅 5 篇并补录原文 |
| 校勘记录 | 无 | 残字 232 · 讹字 198 · 日志入库 |
| references | 12 份 | 12 份 + 缺篇盘点 + 校勘日志 |

#### v1.0.0（2026-10-04）— 首次蒸馏

由 [`中医思维蒸馏器`](https://github.com/jangviktor-web/tcm-distiller) 方法论迁移改造为**文学家 14 维框架**：保留并行子 Agent / 质量验证 / 角色扮演 / 诚实标注 / 编码卫生 / 注册流程六段通用 Pipeline，将中医师专属维度替换为文学家维度。

- **Phase 0 素材处理**：GB18030 → UTF-8 转码、简体化、51 个 PUA 字符清理
- **Phase 1 十二路并行调研**：产出 `references/01–12`（4,337 行），硬性纪律为引诗 grep 可核、零编造
- **Phase 2 框架合成**：`SKILL.md`（316 行）+ 首次注册
- **Phase 3 质量验证**：编码硬校验、索引健康检查、角色一致性自测 8/8
- **Phase 4 增量补充**：`cases/` 名篇赏析库 58 篇

完整变更见 [`libai/CHANGELOG.md`](libai/CHANGELOG.md)。

---

## 许可与版权说明

- **蒸馏成果与文档**：[CC BY-SA 4.0](LICENSE)（署名 + 相同方式共享）
- **李白的诗作文本**：公元 8 世纪作品，公版（public domain）
- **正典电子本来源**：用户提供的数字版本。诗作文本本身不受版权保护，但特定整理本、校点本可能含版本权益；本仓库仅用于文学欣赏与学术普及，如你掌握该电子本的版权信息并希望标注或移除，请开 issue 说明
- 本 skill **不代表李白本人立场**，所拟之作均为 AI 创作、**非李白原作**；不构成医疗、法律或投资建议

## 相关项目

| 项目 | 关系 |
|:---|:---|
| [`tcm-distiller`](https://github.com/jangviktor-web/tcm-distiller) | 思维蒸馏器方法论本体（本 skill 由其改造而来） |
| [`nihaixia`](https://github.com/jangviktor-web/nihaixia) | 同一方法论的经方中医版本，文学家 14 维即由其医家维度迁移 |

<p align="center">
  <sub>如果这个项目对你有用，给个 Star 让更多人看到。<br>
  功能说明页：<a href="https://jangviktor-web.github.io/libai-skill/">jangviktor-web.github.io/libai-skill</a></sub>
</p>
