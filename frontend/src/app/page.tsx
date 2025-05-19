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
  const limit = 5; // Default limit for pagination

  // Calculate the offset for pagination
  const offset = (page - 1) * limit;


  // Fetch the patches list from the database
  const { data: patches, error: fetchListError } = await supabase
    .from("patch_notes")
    .select("*")
    .range(offset, offset + limit - 1)
    .order("released_at", { ascending: false });
    
  if (fetchListError) {
    console.error("Database error in GET/patches: ", fetchListError);
  }

  // Also fetch count of patches for pagination
  const { count: totalPatches, error: countError } = await supabase
    .from("patch_notes")
    .select("*", { count: "exact" });

  if (countError || !totalPatches) {
    console.error("Database error in GET/patches count: ", countError);
  }


  return (
    <div className="min-h-screen bg-gradient-to-b from-[#440A5F] to-[#3A204F] text-[#E9EDF3]">
      <nav className="flex h-16 items-center justify-between px-4">
        <Link href={"www.google.com"}>Github</Link>
      </nav>
      <main className="flex flex-col items-center gap-12 px-4 py-8 sm:py-16 max-w-6xl mx-auto">
        <h1 className="text-5xl text-center font-extrabold tracking-tight sm:text-[5rem]">
          Your very own  <span className="text-[#FBC200]">Patch Notes</span> 📚
        </h1>
        <p className="text-sm text-gray-300 sm:text-xl text-center mx-auto">
          Changelogs summarized and explained with{" "}
          <span className="text-[#FBC200]">AI</span> ✨
        </p>
        <ul className="flex flex-col items-center overflow-y-auto max-w-md w-full">
          {patches?.map((patch) => (
            <PatchNotesTile
              key={patch.version}
              patch={patch}
            />
          ))}
          {patches && patches.length === 0 && (<li>
            No Changelogs Found 😢
          </li>)}
          {!patches && (<li>
            Error Getting Changelogs 💥
          </li>)}
        </ul>
        {totalPatches && (
          <div className="flex max-w-md w-full justify-between">
            <Link
              href={`?page=${page - 1}`}
              className={`px-3 py-1 rounded bg-[#FBC200] text-black font-semibold ${
                page <= 1 ? "opacity-50 pointer-events-none" : ""
              }`}
              aria-disabled={page <= 1}
            >
              Previous
            </Link>
            <span className="px-3 py-1">{page}</span>
            <Link
              href={`?page=${page + 1}`}
              className={`px-3 py-1 rounded bg-[#FBC200] text-black font-semibold ${
                offset + limit >= totalPatches ? "opacity-50 pointer-events-none" : ""
              }`}
              aria-disabled={offset + limit >= totalPatches}
            >
              Next
            </Link>
          </div>
        )}
      </main>
    </div>
  );
}
