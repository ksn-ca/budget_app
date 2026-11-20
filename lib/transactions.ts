export type Transaction = {
  imported_date: string;
  transaction_date: string;
  id: number;
  user: string;
  merchant: string;
  amount: string;
  category_id: number | null;
  bank_category: string | null;
  ignore: boolean;
  bank: string;
};
