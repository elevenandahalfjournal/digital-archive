export const ALLOWED_GENRES = ["fiction", "nonfiction", "poetry", "art", "interview"] as const;
export type Genre = (typeof ALLOWED_GENRES)[number];

export const LABEL_MAP: Record<Genre, string> = {
  fiction: "Fiction",
  nonfiction: "Nonfiction",
  poetry: "Poetry",
  art: "Art",
  interview: "Interview",
};
