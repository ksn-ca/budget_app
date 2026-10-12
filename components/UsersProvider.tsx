"use client";
import { useContext, createContext } from "react";
import type { User } from "@/lib/users";

const UsersContext = createContext<User[]>([]);

export default function UsersProvider({
  children,
  users,
}: {
  children: React.ReactNode;
  users: User[];
}) {
  return (
    <UsersContext.Provider value={users}>{children}</UsersContext.Provider>
  );
}
export const useUsers = () => useContext(UsersContext);
