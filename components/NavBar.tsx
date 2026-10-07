"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { label: "Overview", href: "/" },
  { label: "Transactions", href: "/transactions" },
  { label: "Savings & Goals", href: "/savings" },
  { label: "Upload CSV", href: "/upload" },
  { label: "Rules", href: "/rules" },
];

const chipClass = {
  lime: "border-lime-300/30 bg-lime-300/10 text-lime-300",
  sky: "border-sky-300/30 bg-sky-300/10 text-sky-300",
};

const linkClass = "px-3 py-1.5 text-sm uppercase tracking-wider";
const activeClass = "bg-lime-300 text-neutral-950";
const inactiveClass = "text-neutral-400 hover:text-white";

type NavBarProps = {
  month: string;
  people: { name: string; accent: keyof typeof chipClass }[];
};

export default function NavBar({ month, people }: NavBarProps) {
  const currPath = usePathname();
  return (
    <nav className="w-full border-b border-neutral-800">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-8 py-4">
        <div className="flex items-center gap-3">
          <span className="size-2 bg-lime-300" />
          <span className="text-sm font-bold uppercase tracking-wider text-lime-300">Budget</span>
          <span className="text-sm uppercase tracking-wider text-neutral-500">/ {month}</span>
          <span className="mx-2 h-4 w-px bg-neutral-700" />
          {people.map((p) => (
            <span key={p.name} className={`border px-2 py-0.5 font-mono text-xs ${chipClass[p.accent]}`}>
              {p.name}
            </span>
          ))}
        </div>
        <div className="flex items-center gap-2">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className={`${linkClass} ${currPath == l.href ? activeClass : inactiveClass}`}
            >
              {l.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
}
