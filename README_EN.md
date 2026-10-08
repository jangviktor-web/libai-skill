<div align="center">

<img width="120" src="docs/assets/logo.webp" alt="Li Bai Skill Logo: Li Bai raising a cup to the moon inside an azurite ring, with a gold cartouche reading 李白">

# LiBai-Skill · A Poet's Mind for AI Agents

**Inject the complete poetic system of Li Bai (701–762) into your AI agent**

`25 volumes` · `1,010 poems` · `14-dimension framework` · `58 annotated poems` · `16 image motifs` · `40 canonical guides` · `35 FAQs` · `4,337 lines of analysis`

[![GitHub Stars](https://img.shields.io/github/stars/jangviktor-web/libai-skill?style=for-the-badge&color=yellow&label=Stars)](https://github.com/jangviktor-web/libai-skill/stargazers)
[![Version](https://img.shields.io/badge/version-v1.1.0-blue?style=for-the-badge)](https://github.com/jangviktor-web/libai-skill/releases)
[![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-green?style=for-the-badge)](LICENSE)
[![Agent Skills Standard](https://img.shields.io/badge/Agent%20Skills%20Standard-Ready-orange?style=for-the-badge&logo=openai&logoColor=white)]()
[![Guide](https://img.shields.io/badge/guide-online-1E4C63?style=for-the-badge)](https://jangviktor-web.github.io/libai-skill/)

**🌐 [中文](https://github.com/jangviktor-web/libai-skill/blob/main/README.md) | [English](https://github.com/jangviktor-web/libai-skill/blob/main/README_EN.md)**

</div>

---

> "Clear water out of the lotus — natural, uncarved." — Li Bai
>
> He did not set out to write poems. He set out to restore the Odes.

### In one line

An **agent skill** that distils Li Bai's poetics, image system, judgement standards and voice into a role an AI can activate — for **Tang poetry appreciation, poetics commentary, source verification, and pastiche composition**. Two rules are hard-wired: **every quoted line must be greppable in the canon**, and **every pastiche must be labelled as not by Li Bai**.

**Trigger phrases**: `李白` / `Li Bai` / `Taibai` / `诗仙` / `Shixian` / `拟李白风格` / `write like Li Bai` / `将进酒` / `蜀道难` / `Tang poetry`

---

## Install

```bash
git clone https://github.com/jangviktor-web/libai-skill.git
cp -r libai-skill/libai ~/.claude/skills/libai/     # or your client's skills directory
```

The folder name is the registered name (`name: libai` in the frontmatter).

Or just tell your agent:

```text
Clone https://github.com/jangviktor-web/libai-skill and install the libai/ folder
into my local skills directory, then activate it.
```

- **Visual guide** (single file, zero dependencies): https://jangviktor-web.github.io/libai-skill/
- **Role rules**: [`libai/SKILL.md`](libai/SKILL.md) (316 lines)
- **Canon**: [`libai/modules/01_libai-shi-quanji.md`](libai/modules/01_libai-shi-quanji.md)

---

## What it does

| Capability | Coverage | Notes |
|:---|:---:|:---|
| Poetry appreciation | ✅ | Reads form through "qi precedes diction"; every claim backed by a verifiable line or a cited critique |
| **Six-step method** | ✅ | **qi → image → form → exaggeration → rupture → exhaustion — Li Bai's divergence from Du Fu** |
| Source verification | ✅ | Attribution, genre, textual variants; Ming/Qing edited wording is flagged as such |
| Pastiche composition | ✅ | Form first, then intent; **always labelled "AI in Li Bai's manner, not an original"** |
| Voice proxy | ✅ | Answers from Li Bai's stance; holds both sides of a tension instead of hagiography |
| Image motif bank | ✅ | 16 motifs (moon, wine, sword, roc, horse, cloud, rivers, mountains, immortals, dream, white hair, blue sky, solitude, autumn-frost-snow, flowers-spring, boat) with function and cited lines |
| Annotated canon | ✅ | 58 annotated poems (26 yuefu/gufeng + 32 regulated/quatrain) |
| Prosody | ✅ | Form definitions and statistics, yuefu knowledge, tone/parallel/rhyme rules, rhyme dictionary |
| Historical criticism | ✅ | Includes the detractors: Wang Anshi, Wang Shizhen, Zhao Yi |
| Ethics layer | ✅ | Wine, alchemy, and sword violence each have explicit handling rules and a fixed disclaimer template |

---

## The six-step method

```
qi (charge the air) → image (grasp a self-signifier) → form (emotion picks the metre)
                                                        ↓
exhaustion (one breath out) ← rupture (sense joins, words don't) ← excess (countable numbers for the uncountable)
```

Not "title, then plan" — **emotion first, image second, form last**. That is where Li Bai parts ways with Du Fu.

---

## What was distilled, and from what

### Primary source: a file that had to be rescued

The canon is a single user-supplied electronic edition of the *Collected Poems of Li Bai*:

| Stage | Operation | Result |
|---|---|---|
| Raw file | GB18030 encoded (mojibake when opened as UTF-8) | 159,246 characters · 18,340 lines |
| Detection | `detect_enc.py` / `check_enc.py` | Confirmed not UTF-8 |
| Conversion | `iconv` GB18030 → UTF-8 | Lossless |
| Simplification | `zhconv` | Unified script |
| Character hygiene | `clean_corpus.py` / `fix_pua.py` | **51 Private Use Area characters** cleared to replacement glyphs |
| Canon | `modules/01_libai-shi-quanji.md` | **25 volumes · 1,010 poems · 434 KB · 18,350 lines** |

### Four corrupted blocks, recovered in v1.1.0

Lines 2530–3202, 8273–8880, 9356–10118 and 13625–14233 (volumes 4, 12, 14, 20) were **GBK bytes decoded as EUC-JP**. After the inverse transform, 232 damaged characters and 198 corrupt readings (226 characters across 83 poems) were collated against the *Li Taibai Ji* and the *Quan Tangshi*. Three variant notes remain unresolved and are listed at the end of the canon file.

### Secondary sources

Chronology, friendships, and reception history (Yan Yu, Wang Shizhen, Zhao Yi, Meng Qi) come from web research, each cited in `references/`. A claim that cannot name its edition is not written.

### Methodology

Built with the pipeline from [`tcm-distiller`](https://github.com/jangviktor-web/tcm-distiller) — parallel sub-agents, quality gates, role-play validation, honest labelling, encoding hygiene, registration — with the physician-specific dimensions replaced by a **14-dimension literary framework**.

<details>
<summary><b>Repository layout</b></summary>

```
libai-skill/
├── README.md / README_EN.md
├── LICENSE                       # CC BY-SA 4.0
├── docs/                         # GitHub Pages guide (single file, no external deps)
└── libai/                        # the skill itself
    ├── SKILL.md                  # 316 lines: triggers, identity card, 7-part role rules,
    │                             #   retrieval router, six-step method, three quick-reference cards
    ├── CHANGELOG.md
    ├── modules/                  # 01 canon (1,010 poems) · 02 five poems outside this edition
    ├── references/               # 12 dimension analyses + missing-piece inventory + collation log
    ├── cases/                    # 58 annotated readings
    └── scripts/                  # 31 Python scripts: conversion, detection, collation, verification
```

`scripts/` is an audit trail, not engineering: it records every conversion, encoding check, collation and statistic. Intermediate reports were kept out of the repository.

</details>

---

## Why it does not invent lines

Seven output laws are written into `SKILL.md` rather than left to discretion: pastiche must be declared, quotations must carry a title and be greppable, commentary must cite evidence, suspect attributions must be footnoted, "absent from this edition" must never be inverted into "not written by Li Bai", nothing may be fabricated, and praise must be balanced with historical criticism.

Verification: 22 files pass a hard UTF-8 check, all 12 reference files are indexed with zero dead links, and an 8-question role-consistency test passes 8/8.

---

## Boundaries

> **Absent from this edition ≠ not written by Li Bai.**

Ci poetry, rhapsodies and prose prefaces are outside this poetry edition — that is editorial convention, not loss. Exactly five poems are absent and are supplied separately. The earlier claim of "18 missing masterpieces" is **withdrawn**: it was an artefact of the encoding damage.

---

## Ethics layer

| Area | Handling |
|:---|:---|
| Wine | Never romanticises drunkenness; Tang wine was a 6–15% fermented drink, distilled spirits arrived after the Yuan. Minors: health warning is mandatory |
| Alchemy | Elixir language is **poetic language, not instructions**. No recipe, dose, or method; always flagged as historical context, do not imitate |
| Sword violence | Marked as **literary rhetoric, not advocacy** |
| Real distress | The role steps out; signposting to professional help takes precedence |
| Endorsement | "Li Bai" never endorses products, assets or political positions |

---

## Changelog

#### v1.1.0 (2026-10-05) — Corpus repair and supplement
Recovered four encoding-damaged blocks, collated 232 damaged and 198 corrupt characters, promoted the canon to a complete 25-volume / 1,010-poem edition, added the five genuinely absent poems, corrected every "missing masterpiece" claim, and shipped the missing-piece inventory and collation log.

#### v1.0.0 (2026-10-04) — First distillation
14-dimension literary framework, 12 parallel research tracks (4,337 lines), `SKILL.md`, 58 annotated readings, quality gates.

---

## License

- Distilled framework and documentation: **[CC BY-SA 4.0](LICENSE)**
- Li Bai's poems: 8th-century works, **public domain**
- The electronic edition used as canon was user-supplied. The poems themselves are not under copyright, but a specific digital edition may carry editorial rights; this repository is for literary appreciation and scholarship. If you hold rights in that edition and want it credited or removed, please open an issue.
- This skill does not represent Li Bai's views. Pastiche is AI-authored, not original. It is not medical, legal or investment advice.

## Related

| Project | Relation |
|:---|:---|
| [`tcm-distiller`](https://github.com/jangviktor-web/tcm-distiller) | The distillation methodology itself |
| [`nihaixia`](https://github.com/jangviktor-web/nihaixia) | The same pipeline applied to a classical Chinese physician; the literary dimensions were migrated from its medical ones |

<p align="center"><sub>If this is useful, a star helps others find it.<br>Guide: <a href="https://jangviktor-web.github.io/libai-skill/">jangviktor-web.github.io/libai-skill</a></sub></p>
