import type { Accent } from "./accents";
import type { Money } from "./money";

export type User = {
  name: string;
  accent: Accent;
  income: Money;
  expenses: Money;
  percent_spent: number;
};
