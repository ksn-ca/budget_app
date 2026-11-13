import { accents, type Accent } from "@/lib/accents";
import Link from "next/link";

type ImportSummaryProps = {
  accent: Accent;
  filename: string;
  numTransactions: number;
  numNeedCategory: number;
  importId: number;
};

export default function ImportSummary({
  accent,
  filename,
  numTransactions,
  numNeedCategory,
  importId,
}: ImportSummaryProps) {
  return (
    <div
      className={`border ${accents[accent].tint} px-4 py-2 flex items-center justify-between gap-4`}
    >
      <div className="flex-1 min-w-0">
        <div className="font-bold">
          <p className="truncate">{filename}</p>
          <p>Transactions imported: {numTransactions}</p>
        </div>
        <p className="text-neutral-400 text-xs">
          Unidentified Categories: {numNeedCategory}
        </p>
      </div>

      <Link
        href={`/imports/${importId}`}
        className={`${accents[accent].bg} text-neutral-950 uppercase tracking-wider font-semibold text-sm px-5 py-2 hover:opacity-90 shrink-0`}
      >
        Review Import
      </Link>
    </div>
  );
}
