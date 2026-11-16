// 内容⑰ 华耀奖 2026 · v1 落实 · 60fps 版（剪片／抠像／脸轨迹都是 60fps，正文共用 t1711base.tsx）
import React from 'react';
import { T1711Body } from './t1711base';
import { mkEp } from './kit';
import FACE from '../suyenc-face-t171160.json';
import CUT from '../suyenc-t171160-subs.json';

const { ep, R } = mkEp('t171160', CUT as any, FACE);
export const framesT171160 = Math.round((CUT as any).dur * 60);
export const SuyenT171160: React.FC = () => <T1711Body ep={ep} R={R} hook="v1" fps={60} />;
