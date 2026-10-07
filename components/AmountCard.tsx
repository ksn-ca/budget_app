type AmountCardProps = {
    title: string;
    amount: number;
};
const currency = new Intl.NumberFormat("en-CA", { style: "currency", currency: "CAD" });

export default function AmountCard(cardProps: AmountCardProps) {
    return (
        <div className="border border-neutral-800 bg-neutral-900 px-8 py-6">
            <div className="text-sm uppercase tracking-wider text-neutral-400">{cardProps.title}</div>
            <div className="mt-2 font-mono text-4xl font-semibold text-lime-300">{currency.format(cardProps.amount)}</div>
        </div>
    )
}