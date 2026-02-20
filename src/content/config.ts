import { defineCollection, z } from "astro:content";

const issues = defineCollection({
  type: "content", // ✅ change from "data" to "content"
  schema: z.object({
    title: z.string(),
    year: z.number(),
    number: z.number(),
    pdf: z.string().optional(),
    digitized: z.boolean().optional(),
  }),
});

const entries = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    author: z.string().optional(),
    dedication: z.string().optional(),
    issueSlug: z.string(),
    issueNumber: z.number(),
    year: z.number(),
    genre: z.enum(["fiction", "nonfiction", "poetry", "art", "interview"]),
    order: z.number().optional(),
  }),
});

export const collections = { issues, entries };
