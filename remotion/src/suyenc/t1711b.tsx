// 内容⑰ 华耀奖 2026 · 钩子版 b（正文共用 t1711base.tsx）
import React from 'react';
import { mkEp, epFrames } from './kit';
import { T1711Body } from './t1711base';
import FACE from '../suyenc-face-t1711b.json';
import CUT from '../suyenc-t1711b-subs.json';

const { ep, R } = mkEp('t1711b', CUT as any, FACE);
export const framesT1711B = epFrames(CUT as any);
export const SuyenT1711B: React.FC = () => <T1711Body ep={ep} R={R} hook="b" />;
