import AmountCard from "@/components/AmountCard";
import PersonalCard from "@/components/PersonalCard";

export default function Dashboard() {
  return (
    <div>
      <main className="mx-auto w-full max-w-6xl px-8 py-8 space-y-6">
        <div className="grid grid-cols-3 gap-4 ">
          <AmountCard title="Household Income" amount={2390.09} />
          <AmountCard title="Household Expenses" amount={12000.09} />
          <AmountCard title="Net Saved" amount={10000000.09} />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <PersonalCard
            name="Sienna"
            income={5000}
            expenses={3000}
            percent={Math.round((3000 / 5000) * 100)}
            accent="lime"
          />
          <PersonalCard
            name="Nikita"
            income={10000}
            expenses={5000}
            percent={Math.round((5000 / 10000) * 100)}
            accent="sky"
          />
        </div>
        <div className="grid grid-cols-2">
          <div>Spending Category</div>
          <div>Monthly Spend</div>
        </div>
      </main>
    </div>
  );
}
