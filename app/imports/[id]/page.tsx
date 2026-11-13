import { API_URL } from "@/lib/api";
import { Transaction } from "@/lib/transactions";

const SHRINK = "w-px whitespace-nowrap";

const headers = [
  { label: "Date", className: `text-left` },
  { label: "Merchant", className: `text-left ` },
  { label: "Category", className: `text-left ${SHRINK}` },
  { label: "Amount", className: `text-right` },
  { label: "Actions", className: `text-right ${SHRINK}` },
];

export default async function Import({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const res = await fetch(`${API_URL}/imports/${id}/transactions`, {
    cache: "no-store",
  });
  const transactions: Transaction[] = await res.json();
  return (
    <main className="max-w-5xl mx-auto w-full px-8 py-8">
      <table className="border border-neutral-800 bg-neutral-900 w-full border-collapse">
        <thead>
          <tr>
            {headers.map(({ label, className }) => (
              <th
                key={label}
                scope="col"
                className={`text-xs uppercase tracking-wider text-neutral-500 font-normal px-4 py-3 ${className}`}
              >
                {label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {transactions.map((t, id) => {
            return (
              <tr key={id} className="border-t border-neutral-80">
                <td className="whitespace-nowrap">{t.transaction_date}</td>
                <td>{t.merchant}</td>
                <td className="whitespace-nowrap">{t.bank_category}</td>
                <td className="whitespace-nowrap">{t.amount}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </main>
  );
}
