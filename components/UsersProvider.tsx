"use client";
import { useContext, createContext } from "react";

type User = {
  name: string;
  accent: "lime" | "sky";
  income: number;
  expenses: number;
};

const UsersContext = createContext<User[]>([]);

export default function UsersProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const users: User[] = [
    { name: "Sienna", accent: "lime", income: 3000, expenses: 2000 },
    { name: "Nikita", accent: "sky", income: 5000, expenses: 1000 },
  ];

  return (
    <UsersContext.Provider value={users}>{children}</UsersContext.Provider>
  );
}
export const useUsers = () => useContext(UsersContext);
