import AmountCard from "@/components/AmountCard"

export default function Dashboard() {
  return (
    <div>
      <nav>Nav Bar</nav>
      <main>
        <div className="grid grid-cols-3">
          <AmountCard title="Household Income" amount={2390.09}/>
          <div>Household Expenses</div>
          <div>Net Saved</div>
        </div>
        <div className="grid grid-cols-2">
          <div>Sienna</div>
          <div>Nikita</div>
        </div>
        <div className="grid grid-cols-2">
          <div>Spending Category</div>
          <div>Monthly Spend</div>
        </div>
      </main>
    </div>

  );
}
