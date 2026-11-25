"use client";
import { useState } from "react";
import { accents, type Accent } from "@/lib/accents";
import ImportSummary from "./ImportSummary";
import type { Bank } from "@/lib/banks";
import type { ImportResult } from "@/lib/import_results";
import { useToast } from "./ToastProvider";

type PersonalUploadProps = {
  name: string;
  accent: Accent;
  banks: Bank[];
};

const NEXT_PUBLIC_API_URL = process.env.NEXT_PUBLIC_API_URL;
if (!NEXT_PUBLIC_API_URL) {
  throw new Error("NEXT_PUBLIC_API_URL is not set. Add it to .env.local");
}

export default function PersonalUploadCard({
  name,
  accent,
  banks,
}: PersonalUploadProps) {
  const [bank, setBank] = useState(banks[0]?.code ?? "");
  const [dragging, setDragging] = useState(false);
  const bankName = banks.find((b) => b.code === bank)?.name;
  const [fileResult, setFileResult] = useState<ImportResult | null>(null);
  const showToast = useToast();

  async function handleFile(selected: File | undefined) {
    if (selected) {
      setFileResult(null);
      const data = new FormData();
      data.append("file", selected);
      data.append("bank", bank);
      data.append("person", name);
      try {
        const res = await fetch(`${NEXT_PUBLIC_API_URL}/imports`, {
          method: "POST",
          body: data,
        });

        if (!res.ok) {
          const eRes = await res.json();
          if (!Array.isArray(eRes.detail)) {
            showToast([`Upload failed ${res.status}`], "error");

            return;
          }
          const details = eRes.detail.map((d: string | { msg: string }) =>
            typeof d === "string" ? d : d.msg,
          );
          showToast(details, "error");
        } else {
          const sRes: ImportResult = await res.json();
          setFileResult(sRes);
          showToast([`${sRes.num_transactions} imported`], "success");
        }
      } catch {
        showToast(["Something went wrong"], "error");
      }
    }
  }

  return (
    <div className="border border-neutral-800 bg-neutral-900 p-5 flex flex-col gap-4">
      <div className="flex items-center gap-2">
        <span className={`size-2 ${accents[accent].bg}`} />
        <span className="font-semibold text-white">{name}</span>
      </div>
      <div className="relative">
        <svg
          className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-neutral-500"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="M3 21h18M3 10h18M5 6l7-3 7 3M4 10v11M20 10v11M8 14v3M12 14v3M16 14v3" />
        </svg>
        <select
          value={bank}
          onChange={(e) => setBank(e.target.value)}
          className={`w-full appearance-none scheme-dark border border-neutral-800 bg-neutral-950 py-2.5 pl-10 pr-10 text-sm text-neutral-300 outline-none hover:border-neutral-700 ${accents[accent].focusBorder}`}
        >
          {banks.map((b) => (
            <option key={b.code} value={b.code}>
              {b.name}
            </option>
          ))}
        </select>
        <svg
          className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-neutral-500"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="m6 9 6 6 6-6" />
        </svg>
      </div>
      <label
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFile(e.dataTransfer.files[0]);
        }}
        className={`flex cursor-pointer flex-col items-center justify-center gap-1 border border-dashed bg-neutral-950/50 py-12 text-center hover:border-neutral-600 ${
          dragging ? accents[accent].border : "border-neutral-700"
        }`}
      >
        <input
          type="file"
          accept=".csv"
          className="hidden"
          onChange={(e) => {
            handleFile(e.target.files?.[0]);
            e.target.value = "";
          }}
        />
        <span
          className={`mb-3 flex size-8 items-center justify-center border ${accents[accent].tint}`}
        >
          <svg
            className="size-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <path d="M12 15V3m0 0-4 4m4-4 4 4M4 15v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4" />
          </svg>
        </span>
        <p className="text-sm font-semibold text-white">
          Drop CSV for <span className={accents[accent].text}>{name}</span>
        </p>
        <p className="text-xs text-neutral-500">{bankName} format</p>
      </label>
      {fileResult && (
        <ImportSummary
          accent={accent}
          filename={fileResult.filename}
          numNeedCategory={fileResult.num_need_category}
          numTransactions={fileResult.num_transactions}
          importId={fileResult.id}
        />
      )}
    </div>
  );
}
