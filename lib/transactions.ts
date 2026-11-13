export type Transaction = {
  imported_date: string;
  transaction_date: string;
  user: string;
  merchant: string;
  amount: string;
  category_id: number | null;
  bank_category: string | null;
  import_id: number;
  ignore: boolean;
  bank: string;
};
