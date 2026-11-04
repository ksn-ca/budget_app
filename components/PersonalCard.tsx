import { accents, type Accent } from "@/lib/accents";
import { formatMoney, type Money } from "@/lib/money";

type PersonalCardProps = {
    name: string,
    income: Money,
    expenses: Money,
    percent: number,
    accent: Accent
}

export default function PersonalCard(personalProps: PersonalCardProps) {
    const clamped = Math.min(Math.max(personalProps.percent, 0), 100);
    const accent = accents[personalProps.accent];
    return (
        <div className={`border ${accent.borderSubtle} bg-neutral-900 px-8 py-6`}>
            <div className="flex items-center gap-3 text-lg font-semibold">
                <span className={`size-2.5 ${accent.bg}`} />
                {personalProps.name}
            </div>
            <div className="mt-6 grid grid-cols-2 gap-4">
                <div>
                    <div className="text-sm uppercase tracking-wider text-neutral-400">Income</div>
                    <div className={`mt-1 font-mono text-2xl font-semibold ${accent.text}`}>{formatMoney(personalProps.income)}</div>
                </div>
                <div>
                    <div className="text-sm uppercase tracking-wider text-neutral-400">Expenses</div>
                    <div className="mt-1 font-mono text-2xl font-semibold text-white">{formatMoney(personalProps.expenses)}</div>
                </div>
            </div>
            <div className="mt-6">
                <div className="h-1 w-full bg-neutral-800">
                    <div className={`h-full ${accent.bg}`} style={{ width: `${clamped}%` }} />
                </div>
                <div className="mt-2 font-mono text-sm text-neutral-400">{personalProps.percent}% of income spent</div>
            </div>
        </div>
    )
}