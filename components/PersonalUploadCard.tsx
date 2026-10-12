"use client";
import { useState } from "react";
import { accents, type Accent } from "@/lib/accents";
import ImportSummary from "./ImportSummary";

type PersonalUploadProps = {
  name: string;
  accent: Accent;
};

const banks = [
  { label: "Auto-detect", val: "auto" },
  { label: "Wealthsimple", val: "ws" },
  { label: "Rogers Bank", val: "rogers" },
  { label: "PC Financial", val: "pcf" },
  { label: "MNBA", val: "mnba" },
];

export default function PersonalUploadCard({
  name,
  accent,
}: PersonalUploadProps) {
  const [bank, setBank] = useState("auto");
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const bankLabel = banks.find((b) => b.val === bank)?.label;

  function handleFile(selected: File | undefined) {
    if (selected) setFile(selected);
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
            <option key={b.val} value={b.val}>
              {b.label}
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
        <p className="text-xs text-neutral-500">
          {bank === "auto" ? "Auto-detects columns" : `${bankLabel} format`}
        </p>
      </label>
      {file && (
        <ImportSummary
          accent={accent}
          filename={file?.name ? file.name : "None"}
          numNeedCategory={2}
          numTransactions={10}
        />
      )}
    </div>
  );
}
