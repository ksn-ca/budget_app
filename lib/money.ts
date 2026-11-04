// Decimal string from the API, e.g. "3000.00". Never convert to number for math.
export type Money = `${number}`;

const currency = new Intl.NumberFormat("en-CA", { style: "currency", currency: "CAD" });

export function formatMoney(amount: Money): string {
  return currency.format(amount);
}
