"use client";
import AmountCard from "@/components/AmountCard";
import PersonalCard from "@/components/PersonalCard";
import { useUsers } from "@/components/UsersProvider";

export default function Dashboard() {
  const users = useUsers();
  return (
    <div>
      <main className="mx-auto w-full max-w-6xl px-8 py-8 space-y-6">
        <div className="grid grid-cols-3 gap-4 ">
          <AmountCard title="Household Income" amount={2390.09} />
          <AmountCard title="Household Expenses" amount={12000.09} />
          <AmountCard title="Net Saved" amount={10000000.09} />
        </div>
        <div className="grid grid-cols-2 gap-4">
          {users.map((user) => (
            <PersonalCard
              key={user.name}
              name={user.name}
              income={user.income}
              expenses={user.expenses}
              percent={Math.round((user.expenses / user.income) * 100)}
              accent={user.accent}
            />
          ))}
        </div>
        <div className="grid grid-cols-2">
          <div>Spending Category</div>
          <div>Monthly Spend</div>
        </div>
      </main>
    </div>
  );
}
