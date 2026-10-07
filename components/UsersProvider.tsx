"use client";
import { useContext, createContext } from "react";

type User = { name: string; accent: "lime" | "sky" };

const UsersContext = createContext<User[]>([]);

export default function UsersProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const users: User[] = [
    { name: "Sienna", accent: "lime" },
    { name: "Nikita", accent: "sky" },
  ];

  return (
    <UsersContext.Provider value={users}>{children}</UsersContext.Provider>
  );
}
export const useUsers = () => useContext(UsersContext);
