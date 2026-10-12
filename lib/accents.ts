export type Accent = "lime" | "sky";

export const accents: Record<
  Accent,
  {
    bg: string;
    text: string;
    border: string;
    borderSubtle: string;
    focusBorder: string;
    tint: string;
  }
> = {
  lime: {
    bg: "bg-lime-300",
    text: "text-lime-300",
    border: "border-lime-300",
    borderSubtle: "border-lime-300/20",
    focusBorder: "focus:border-lime-300",
    tint: "border-lime-300/30 bg-lime-300/10 text-lime-300",
  },
  sky: {
    bg: "bg-sky-300",
    text: "text-sky-300",
    border: "border-sky-300",
    borderSubtle: "border-sky-300/20",
    focusBorder: "focus:border-sky-300",
    tint: "border-sky-300/30 bg-sky-300/10 text-sky-300",
  },
};
