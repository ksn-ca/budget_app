"use client";

import { createContext, useCallback, useContext, useState } from "react";
import ToastItem from "./ToastItem";
import type { ShowToast, Toast } from "@/lib/toast";

const ToastContext = createContext<ShowToast>(() => {});

export default function ToastProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const showToast = useCallback((messages: string[], type: Toast["type"]) => {
    const toast: Toast = { id: crypto.randomUUID(), messages, type };
    setToasts((prev) => [...prev, toast]);
  }, []);

  const dismiss = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={showToast}>
      {children}
      <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm">
        {toasts.map((toast) => (
          <ToastItem key={toast.id} toast={toast} onDismiss={dismiss} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}
export const useToast = () => useContext(ToastContext);
