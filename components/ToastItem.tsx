import type { Toast } from "@/lib/toast";
import { useEffect } from "react";

const roleByType: Record<Toast["type"], string> = {
  error: "alert",
  success: "status",
};

const styleByType: Record<Toast["type"], string> = {
  error: "border-red-500/50",
  success: "border-lime-300/50",
};

export default function ToastItem({
  toast,
  onDismiss,
}: {
  toast: Toast;
  onDismiss: (id: string) => void;
}) {
  useEffect(() => {
    if (toast.type !== "success") return;

    const timerId = setTimeout(() => {
      onDismiss(toast.id);
    }, 5000);

    return () => clearTimeout(timerId);
  }, [toast.id, toast.type, onDismiss]);

  return (
    <div
      role={roleByType[toast.type]}
      className={`flex justify-between items-start p-4 bg-neutral-900 border shadow-lg rounded-lg text-sm text-white gap-3 ${styleByType[toast.type]}`}
    >
      <ul className="max-h-30 overflow-y-auto">
        {toast.messages.map((message, i) => (
          <li key={i}>{message}</li>
        ))}
      </ul>
      <button
        type="button"
        onClick={() => {
          onDismiss(toast.id);
        }}
        aria-label="Close"
        className="text-neutral-400 hover:text-white hover:bg-neutral-800 rounded p-1"
      >
        <svg
          className="size-4"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          aria-hidden="true"
        >
          <path d="M6 6l12 12M18 6 6 18" />
        </svg>
      </button>
    </div>
  );
}
