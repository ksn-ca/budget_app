type AmountCardProps = {
    title: string;
    amount: number;
};

export default function AmountCard(cardProps: AmountCardProps) {
    return (
        <>
            <div>{cardProps.title}</div>
            <div>${cardProps.amount}</div>
        </>
    )
}