import { PatchNotesTile } from "@/components/patch-notes-tile";
import { createAdminClient } from "@/utils/supabase/admin";
import Link from "next/link";

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const supabase = await createAdminClient();
  const filters = await searchParams;
  const page = filters.page
    ? Array.isArray(filters.page!)
      ? parseInt(filters.page[0]!)
      : 1
    : 1;
  const limit = 10; // Default limit for pagination

  // Calculate the offset for pagination
  const offset = (page - 1) * limit;

  const { data: patches, error } = await supabase
    .from("patch_notes")
    .select("*")
    .range(offset, offset + limit - 1)
    .order("released_at", { ascending: false });

  if (error) {
    console.error("Database error in GET/patches: ", error);
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <nav className="flex h-16 items-center justify-between px-4">
        <Link href={"www.google.com"}>Github</Link>
      </nav>
      <main className="flex flex-col items-center gap-12 px-4 py-8 sm:py-16">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-[5rem]">
          Your very own  <span className="text-[hsl(280,100%,70%)]">Patch Notes</span> 📚
        </h1>
        <p className="text-sm text-gray-300 sm:text-xl">
          Changelogs summarized and explained with{" "}
          <span className="text-[hsl(280,100%,70%)]">AI</span> ✨
        </p>
        <ul className="flex flex-col items-center gap-4 overflow-y-auto">
          {patches?.map((patch) => (
            <PatchNotesTile
              key={patch.version}
              patch={patch}
            />
          ))}
        </ul>
      </main>
    </div>
  );
}
