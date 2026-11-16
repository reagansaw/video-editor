// 内容⑰ v2 · 另一个机位（IMG_4861，原生竖版 SDR）。正文、效果、字幕全部共用 t1711base.tsx
// 这支的原片时间码比 IMG_1711 晚约 0.3–0.5 秒，所以用 MAP 把「1711 的秒数」换算成「4861 的秒数」，
// 其余一律不改——两支的画面效果、字幕、音效因此完全一致。
import React from 'react';
import { T1711Body } from './t1711base';
import { mkEp, epFrames } from './kit';
import type { RFn } from './kit';
import FACE from '../suyenc-face-t4861.json';
import CUT from '../suyenc-t4861-subs.json';

const { ep, R } = mkEp('t4861', CUT as any, FACE);
export const framesT4861 = epFrames(CUT as any);

// [1711 起, 1711 止, 4861 起, 4861 止]，段内线性换算
const MAP: [number, number, number, number][] = [
  [146.96, 150.22, 147.20, 150.52], [151.10, 157.92, 151.36, 158.20],
  [10.96, 17.72, 11.52, 17.98], [23.10, 27.84, 23.36, 28.12],
  [51.86, 57.82, 52.04, 58.08], [60.64, 64.28, 60.92, 64.54],
  [121.16, 128.10, 121.42, 128.38], [129.52, 135.02, 129.78, 135.28],
  [104.94, 113.00, 105.22, 113.28], [254.52, 257.00, 254.78, 257.26],
  [265.14, 267.78, 265.46, 268.06],
];
const toThis = (t: number) => {
  const m = MAP.find(([a, b]) => t >= a - 0.4 && t <= b + 0.4);
  return m ? m[2] + ((t - m[0]) * (m[3] - m[2])) / (m[1] - m[0]) : t;
};
const R4861: RFn = (r, n) => R(toThis(r), n);

export const SuyenT4861: React.FC = () => <T1711Body ep={ep} R={R4861} hook="v1" wide />;
