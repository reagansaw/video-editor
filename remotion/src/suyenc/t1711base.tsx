// 内容⑰ 中国报华耀奖 2026 得奖访问 · 四个钩子版共用的正文（赛马：v1 / A / B / D）
// 正文都一样：不要一直讲 → 80 年企业跌跌撞撞 / 屹立不倒（B-roll 荣誉墙）→ 玄学每 20 年一运、80 年四运
// → 九运离火 2024–2043（罗盘）→ 把包袱抛开往前看 → 正能量要落实 → 布局、破局 → Don't just talk, do it
// 钩子只差开头那一段，时间一律写 R(原片秒)，所以同一份正文四版通用
import React from 'react';
import { Hero, Cutaway, HandCircle, Seal, Flash, TopBanner, LuopanRing, Chip, Sfx } from '../SuyenContent';
import type { Cam, Ep } from '../SuyenContent';
import { EpShell, subsR, mkYAt, YearStrip } from './kit';
import type { RFn } from './kit';

export type HookId = 'v1' | 'a' | 'b' | 'd';

// 正文字幕（四版都有这些段）
const BASE_SUBS: [string, number, number][] = [
  ['两个字，就是落实', 146.96, 150.22],
  ['不要再讲了', 151.10, 152.52], ['不要一直讲，没有行动', 152.52, 155.30], ['所以你必须讲行动', 155.30, 157.92],
  ['所以你想想', 10.96, 11.90], ['80 年的企业一路走来', 11.90, 14.40], ['肯定是经历风风雨雨、跌跌撞撞', 14.40, 17.72],
  ['而你可以想想', 23.10, 24.20], ['经历过的风雨依然到了今天', 24.20, 26.40], ['屹立不倒', 26.40, 27.84],
  ['你看从玄学的角度', 51.86, 53.78], ['每 20 年转运一次', 53.78, 55.30], ['十年河东、十年河西', 55.30, 57.82],
  ['你看 80 年就经历了四运', 60.64, 62.64], ['四个运转', 62.64, 64.28],
  ['来到了九运 2024 年到 2043 年', 121.16, 124.40], ['就是离火九运', 124.40, 126.18], ['九运讲的就是能量磁场', 126.18, 128.10],
  ['把过去的包袱抛开', 129.52, 131.62], ['一定要往前看', 131.62, 133.64], ['这个就是秘诀', 133.64, 135.02],
  ['要时时刻刻保持这个正能量', 104.94, 107.60], ['正能量不仅仅是口说', 107.60, 110.42], ['而是你必须要把它落实下来', 110.42, 113.00],
  ['布局，然后就可以破局', 254.52, 257.00],
  ['Don’t just talk', 265.14, 266.56], ['Do it', 266.56, 267.78],
];

// 各版钩子多出来的那一段字幕
const HOOK_SUBS: Record<HookId, [string, number, number][]> = {
  v1: [],
  a: [],
  b: [['80 年哦？', 6.76, 8.10], ['人生有多少个 80 年？', 8.10, 10.28]],
  d: [['当你去到了高点', 84.42, 86.24], ['它就会跌落来低点', 86.24, 87.88], ['它就会走下坡', 87.88, 89.00]],
};

export const T1711Body: React.FC<{ ep: Ep; R: RFn; hook: HookId }> = ({ ep, R, hook }) => {
  const CUTT = ep.dur;
  const subs = subsR(R, [...HOOK_SUBS[hook], ...BASE_SUBS] as any);
  const shakes = [R(153.84), R(26.40), R(124.40), R(266.56)];
  const cam: Cam = {
    hits: [0.05, R(148.40), R(153.84), R(26.40), R(55.30), R(62.64), R(124.40), R(131.62), R(104.94), R(254.52), R(266.56)],
    pushes: [[R(110.42), R(113.00), 1.05], [R(265.14), R(267.78), 1.06]],
  };
  // 顶部标题条：钩子讲完才上（各版的第一段不一样）
  const bannerAt = hook === 'b' ? R(10.96) : hook === 'd' ? R(146.96) : hook === 'a' ? R(146.96) : R(151.10);
  return (
    <EpShell ep={ep} subs={subs} cam={cam} shakes={shakes}
      behind={<>
        {hook === 'b' && <Hero text="80 年？" at={R(7.20)} until={R(10.28)} x={540} y={430} size={250} tone="cream" anim="呐喊声波" />}
        {hook === 'd' && <Hero text="走下坡" at={R(87.88)} until={R(89.00)} x={540} y={430} size={240} tone="navy" anim="呐喊声波" shake={[R(87.88)]} />}
        <Hero text="落实" at={R(148.40)} until={R(150.22)} x={540} y={430} size={280} tone="rose" anim="呐喊声波" shake={[R(148.40)]} />
        <Hero text="没有行动" at={R(153.84)} until={R(155.30)} x={540} y={420} size={190} tone="navy" anim="呐喊声波" shake={[R(153.84)]} />
        {hook !== 'b' && <Hero text="80 年" at={R(11.90)} until={R(14.40)} x={520} y={400} size={240} tone="cream" />}
        <Hero text="四个运转" at={R(62.64)} until={R(64.28)} x={540} y={420} size={200} tone="cream" anim="呐喊声波" />
        <LuopanRing from={R(126.18)} to={R(128.10)} lock={R(127.6)} cx={540} cy={560} r={430} />
        <Hero text="九运 · 离火" at={R(124.40)} until={R(126.18)} x={540} y={420} size={170} tone="rose" anim="呐喊声波" shake={[R(124.40)]} />
        <Hero text="往前看" at={R(131.62)} until={R(133.64)} x={540} y={430} size={220} tone="rose" anim="呐喊声波" />
        <Hero text="正能量" at={R(104.94)} until={R(107.60)} x={540} y={420} size={230} tone="cream" anim="呐喊声波" />
        <Hero text="Do it" at={R(266.56)} until={R(267.78)} x={540} y={430} size={240} tone="rose" anim="呐喊声波" shake={[R(266.56)]} />
      </>}
      yAt={mkYAt([[R(51.86), R(64.28)], [R(121.16), R(128.10)]], [[R(11.90), R(17.00)]])}
      sfx={<>
        {hook === 'b' && <Sfx at={R(7.20)} s="综艺悬疑不对劲" />}
        {hook === 'd' && <Sfx at={R(87.88)} s="猛然一惊" />}
        <Sfx at={R(148.40)} s="综艺咚" /><Sfx at={R(151.10)} s="扫光" /><Sfx at={R(153.84)} s="故障音效" /><Sfx at={R(155.30)} s="咚" />
        <Sfx at={R(11.90)} s="回忆-刷一下" /><Sfx at={R(17.00)} s="拍照声2" /><Sfx at={R(26.40)} s="猛然一惊" />
        <Sfx at={R(51.86)} s="扫光音效4" /><Sfx at={R(55.30)} s="叮" /><Sfx at={R(62.64)} s="综艺咚" />
        <Sfx at={R(121.16)} s="扫光" /><Sfx at={R(124.40)} s="综艺咚" /><Sfx at={R(127.60)} s="叮" />
        <Sfx at={R(129.52)} s="纸张抖动声" /><Sfx at={R(131.62)} s="亮一下" />
        <Sfx at={R(104.94)} s="扫光" /><Sfx at={R(110.42)} s="叮" />
        <Sfx at={R(254.52)} s="综艺咚" /><Sfx at={R(255.6)} s="综艺咚" /><Sfx at={R(266.56)} s="咚咚重音心头震" vol={0.4} />
      </>}>
      <TopBanner at={bannerAt} until={CUTT} kicker="林舒苑老师 · 中国报华耀奖 2026" title="2027 两个字：落实" />
      <Flash at={R(148.40)} k={0.4} /><Flash at={R(124.40)} k={0.3} />
      {/* 全片唯一的 B-roll：她走过中国报荣誉墙（IMG_1699） */}
      <Cutaway ep={ep} src="award_wall" from={R(11.90)} to={R(17.00)} pipTopAt={R(12.3)} />
      <Seal text="屹立不倒" at={R(26.40)} until={R(27.84)} x={190} y={760} size={190} />
      <YearStrip at={R(60.64)} until={R(64.28)} y={880} title="80 年 · 四个运转"
        items={[{ year: '1944', word: '一运', at: R(60.9) }, { year: '1964', word: '二运', at: R(61.6) }, { year: '1984', word: '三运', at: R(62.3) }, { year: '2004', word: '四运', at: R(63.0), up: 1 }]} />
      <Chip text="2024 – 2043" at={R(121.16)} until={R(124.40)} x={620} y={1240} tone="navy" size={52} />
      <HandCircle ep={ep} at={R(133.64)} until={R(135.02)} label="秘诀" labelAt={R(133.9)} />
      <Seal text="布局" at={R(254.52)} until={R(257.00)} x={190} y={820} size={180} />
      <Seal text="破局" at={R(255.80)} until={R(257.00)} x={190} y={1060} size={180} rot={4} />
    </EpShell>
  );
};
