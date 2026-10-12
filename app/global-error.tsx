"use client";
import "./globals.css";

export default function GlobalError({
  error,
  retry,
}: {
  error: Error & { digest?: string };
  retry: () => void;
}) {
  return (
    <html lang="en">
      <body className="min-h-full flex flex-col items-center justify-center gap-4 bg-neutral-950 text-white">
        <h2>Couldn&apos;t reach the budget server</h2>
        <p className="text-neutral-400">{error.message}</p>
        <button
          onClick={() => retry()}
          className="rounded border border-neutral-700 px-4 py-2"
        >
          Try again
        </button>
      </body>
    </html>
  );
}
