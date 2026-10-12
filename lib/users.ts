import type { Accent } from "./accents";

export type User = {
  name: string;
  accent: Accent;
  income: number;
  expenses: number;
};
