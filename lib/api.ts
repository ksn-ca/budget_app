const apiUrl = process.env.API_URL;
if (!apiUrl) {
  throw new Error("API_URL is not set. Add it to .env.local");
}

export const API_URL: string = apiUrl;
