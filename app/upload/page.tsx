"use client";
import PersonalUploadCard from "@/components/PersonalUploadCard";
import { useUsers } from "@/components/UsersProvider";

export default function Upload() {
  const users = useUsers();
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
      <div className="grid grid-cols-2 gap-4">
        {users.map((user) => (
          <PersonalUploadCard
            key={user.name}
            name={user.name}
            accent={user.accent}
          />
        ))}
      </div>
      <div></div>
      <div></div>
    </main>
  );
}
