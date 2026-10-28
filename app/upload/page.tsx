import UploadView from "@/components/UploadView";
import { Bank } from "@/lib/banks";
import { connection } from "next/server";
import { API_URL } from "@/lib/api";

export default async function Upload() {
  await connection();
  const res = await fetch(`${API_URL}/banks`);
  if (!res.ok) {
    throw new Error(`Failed to fetch banks: ${res.status}`);
  }
  const banks: Bank[] = await res.json();
  return (
    <main className="flex flex-col gap-5 mx-auto w-full max-w-6xl px-8 py-8">
      <div className="border border-neutral-800 bg-neutral-900 p-5 flex flex-col gap-4">
        <div>CSV UPLOAD</div>
        <p>
          Upload a bank or card export for each household member. Transactions
          are imported into the shared ledger and tagged by person. Your CSV
          should include date, description, and amount columns (any header names
          work).
        </p>
      </div>
      <UploadView banks={banks} />
      <div></div>
      <div></div>
    </main>
  );
}
