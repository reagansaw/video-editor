// 内容⑰ 华耀奖 2026 · 钩子版 a（正文共用 t1711base.tsx）
import React from 'react';
import { mkEp, epFrames } from './kit';
import { T1711Body } from './t1711base';
import FACE from '../suyenc-face-t1711a.json';
import CUT from '../suyenc-t1711a-subs.json';

const { ep, R } = mkEp('t1711a', CUT as any, FACE);
export const framesT1711A = epFrames(CUT as any);
export const SuyenT1711A: React.FC = () => <T1711Body ep={ep} R={R} hook="a" />;
