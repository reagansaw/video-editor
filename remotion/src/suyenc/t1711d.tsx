// 内容⑰ 华耀奖 2026 · 钩子版 d（正文共用 t1711base.tsx）
import React from 'react';
import { mkEp, epFrames } from './kit';
import { T1711Body } from './t1711base';
import FACE from '../suyenc-face-t1711d.json';
import CUT from '../suyenc-t1711d-subs.json';

const { ep, R } = mkEp('t1711d', CUT as any, FACE);
export const framesT1711D = epFrames(CUT as any);
export const SuyenT1711D: React.FC = () => <T1711Body ep={ep} R={R} hook="d" />;
