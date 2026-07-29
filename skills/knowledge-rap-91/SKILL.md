---
name: knowledge-rap-91
description: 将任意中文知识文案固定制作成 91 BPM、4/4、十六分音符卡字的快嘴知识说唱，并产出人声、完整伴奏、计划逐字时间、字幕卡点和短视频时间线建议。用于用户提供科普、商业、历史、数学、方法论、观点对比或其他知识文案，并要求“唱出来”“做成知识说唱”“按固定快嘴节奏跑文案”“生成有伴奏的节奏口播”，或在短视频工作流中稳定复用同一 flow、编曲方向与时间基准时。主题不限，不应把任何测试文案当作默认内容。
---

# 91 BPM 知识说唱

把新文案约束到同一套节奏、flow、编曲和验收标准。固定的是音乐语言与生产规则，不复制未经授权的真人身份音色。

## 必读资源

开始编排前完整阅读 [references/rhythm-contract.md](references/rhythm-contract.md)。不要凭感觉修改其中的硬参数。

## 工作流

1. 接收任意主题的中文知识文案；保留事实含义，先去除不需要演唱的说明文字。不得沿用上一次任务的主题、人物、专有名词或歌词。
2. 运行节奏规划脚本：

```bash
python3 scripts/plan_rap_timing.py input.txt --out timing.json --srt timing.srt
```

3. 阅读脚本摘要。若平均每行超过 2 小节、连续 24 个槽位没有停顿，或结论未落在小节末尾，先重排断句，不要直接生成。
4. 根据文案选择解释、清单、故事或对比结构，再按以下节奏骨架组织：
   - 0–2 小节：一句冲突或问题钩子。
   - 2–8 小节：第一层解释、事实或方法。
   - 45%–65%：二次钩子、反转或“注意到”。
   - 后半：深入解释、案例、对比或更优解。
   - 最后 2–4 小节：结论；最后一个关键词落在强拍。
5. 只提交一次音乐生成；接受服务自动返回的候选，不用重复点击换取更多版本。
6. 从完整候选中优先选择：前奏最短、普通话最清晰、长音最少、鼓点最稳定的一版。
7. 下载并核验真实音频时长和可播放性。不要把生成前的计划时间当成实际逐字时间。
8. 需要字幕或画面卡点时，对最终音频做转写/强制对齐，再用实际时间替换 `timing.json` 的计划时间。
9. 需要可编辑视频时，调用 ChatCut/短视频工作流，把最终混音、字幕和画面卡点写入时间线；背景音乐与人声已经混合的成品不要再叠加第二条人声。

## 固定生成提示

在音乐生成服务的 style/prompt 字段使用以下英文提示；只替换内容主题，不改节奏参数：

```text
Mandarin Chinese knowledge rap, exactly 91 BPM, 4/4, rapid sixteenth-note syllable flow, most Chinese characters about 0.16 seconds, clipped punchy male spoken rap, semi-spoken semi-sung, low pitch range, strong downbeats, short 0.12 to 0.20 second pauses, high-energy educational short-video delivery, hard boom bap kick and snare, crisp hi-hats, modern trap sub bass, dark cinematic synths, vocals very clear and forward, catchy hypnotic hook, no long notes, no slow singing, no long intro, no ad-libs, no improvised lyrics, no instrumental breaks
```

歌词分段标签优先使用：

```text
[Intro - spoken count-in]
[Hook - fast rhythmic rap]
[Verse - rapid fire]
[Verse - clipped syllables]
[Bridge - tension build]
[Contrast - call and response]
[Final - strong cadence]
```

只在原文确实存在双方对比时使用 `[Contrast]`；普通解释类文案不要强行改成对决。

## 生成路径

- 已登录 Suno 且用户要求用 Suno：通过浏览器使用 Advanced/Write，填写歌词、固定提示和标题，确认不是 Instrumental，再生成。
- 用户需要人声与伴奏分轨：分别生成 91 BPM 纯伴奏和匿名男声说唱，按计划时间对齐；不要把含人声的整曲当背景再次叠加。
- 用户要求 ChatCut 成片：加载对应 ChatCut voice/music/import/verification/export Skills，导入最终音频并按实际时长放置。
- 当前服务不能稳定唱准中文：先交付计划节奏稿和可试听样片，明确实际字时需以最终转写为准，不虚构“逐字精确同步”。

## 验收门

成品必须同时满足：

- BPM 目标 91；允许整体分析值 90–92。
- 4/4；主句以十六分音符推进。
- 普通汉字计划时长约 0.165 秒；多数实际字长应在 0.12–0.20 秒。
- 每 1–2 小节至少出现一次可感知停顿或重音变化。
- 前奏不超过 2 秒，除非用户明确要音乐开场。
- 人声清晰靠前，不能被鼓和低音遮盖。
- 无慢歌腔、连续长音、无关即兴词或长器乐间奏。
- 完整覆盖用户文案，不悄悄漏句或改写事实。
- 最终文件已实际解码验证，而非只凭网页显示“完成”。

若任何一项失败，指出具体失败项并只修复该项；不要擅自改变整套节奏。

## 音色与权利

只复用匿名声线、节奏、断句和编曲特征。用户提供自有声音或明确授权证明时才进行身份音色克隆；否则生成“相近但不可识别为特定真人”的男声。第三方免费音乐服务可能不授予商业使用权，交付时明确提示其授权状态。
