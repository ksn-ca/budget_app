const accents = {
    lime: { square: "bg-lime-300", text: "text-lime-300", fill: "bg-lime-300", border: "border-lime-300/20" },
    sky: { square: "bg-sky-300", text: "text-sky-300", fill: "bg-sky-300", border: "border-sky-300/20" },
};

const currency = new Intl.NumberFormat("en-CA", { style: "currency", currency: "CAD" });

type PersonalCardProps = {
    name: string,
    income: number,
    expenses: number,
    percent: number,
    accent: keyof typeof accents
}

export default function PersonalCard(personalProps: PersonalCardProps) {
    const clamped = Math.min(Math.max(personalProps.percent, 0), 100);
    const accent = accents[personalProps.accent];
    return (
        <div className={`border ${accent.border} bg-neutral-900 px-8 py-6`}>
            <div className="flex items-center gap-3 text-lg font-semibold">
                <span className={`size-2.5 ${accent.square}`} />
                {personalProps.name}
            </div>
            <div className="mt-6 grid grid-cols-2 gap-4">
                <div>
                    <div className="text-sm uppercase tracking-wider text-neutral-400">Income</div>
                    <div className={`mt-1 font-mono text-2xl font-semibold ${accent.text}`}>{currency.format(personalProps.income)}</div>
                </div>
                <div>
                    <div className="text-sm uppercase tracking-wider text-neutral-400">Expenses</div>
                    <div className="mt-1 font-mono text-2xl font-semibold text-white">{currency.format(personalProps.expenses)}</div>
                </div>
            </div>
            <div className="mt-6">
                <div className="h-1 w-full bg-neutral-800">
                    <div className={`h-full ${accent.fill}`} style={{ width: `${clamped}%` }} />
                </div>
                <div className="mt-2 font-mono text-sm text-neutral-400">{personalProps.percent}% of income spent</div>
            </div>
        </div>
    )
}