"use client";
import { useUsers } from "@/components/UsersProvider";
import PersonalUploadCard from "./PersonalUploadCard";
import { Bank } from "@/lib/banks";

type UploadViewProps = {
  banks: Bank[];
};
export default function UploadView({ banks }: UploadViewProps) {
  const users = useUsers();
  return (
    <div className="grid grid-cols-2 gap-4">
      {users.map((user) => (
        <PersonalUploadCard
          key={user.name}
          name={user.name}
          accent={user.accent}
          banks={banks}
        />
      ))}
    </div>
  );
}
