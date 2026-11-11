export type Toast = {
  id: string;
  messages: string[];
  type: "error" | "success";
};

export type ShowToast = (messages: string[], type: Toast["type"]) => void;
