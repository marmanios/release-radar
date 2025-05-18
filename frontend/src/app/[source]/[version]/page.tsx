import { PatchNotesTile } from "@/components/patch-notes-tile";
import type { TAiSummary } from "@/types";
import { createAdminClient } from "@/utils/supabase/admin";
import Link from "next/link";

export default async function PatchNotes({
  params,
}: {
  params: Promise<{ source: string; version: string }>;
}) {
  const supabase = await createAdminClient();
  const { source, version } = await params;

  console.log("Fetching patch notes for source:", source, "and version:", version);
  
  const { data, error } = await supabase
    .from("patch_notes")
    .select("*")
    .eq("source", decodeURI(source))
    .eq("version", decodeURI(version))
    .single();

  if (error || !data) {
    console.error("Database error in GET/patches: ", error);
    return (
    <div className="min-h-screen bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <nav className="flex h-16 items-center justify-between px-4">
        <Link href={"/"}>Home</Link>
        <Link href={"www.google.com"}>Github</Link>
      </nav>
    </div>
    )
  }
  
  const patchNotes: {
    ai_summary: TAiSummary;
    created_at: Date;
    released_at: Date;
    source: string;
    source_url: string;
    version: string;
  } = {
    ai_summary: JSON.parse(data.ai_summary),
    created_at:  new Date(data.created_at),
    released_at: new Date(data.released_at),
    source: data.source,
    source_url: data.source_url,
    version: data.version,
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <nav className="flex h-16 items-center justify-between px-4">
        <Link href={"/"}>Home</Link>
        <Link href={"www.google.com"}>Github</Link>
      </nav>
      <main className="flex flex-col items-center gap-12 px-4 py-8 sm:py-16">
        <h1 className="text-5xl font-extrabold tracking-tight sm:text-[5rem]">
           Changelog summary for <span className="text-[hsl(280,100%,70%)]">{version}</span>
        </h1>
        <p className="text-sm text-gray-300 sm:text-lg">
          Presented by <span className="text-[hsl(280,100%,70%)]">patchnotes.dev</span>. Find the full changelog <Link href={patchNotes.source_url} className="text-[hsl(280,100%,70%)] text-underline">here</Link>.
        </p>
        <section>
          {patchNotes.ai_summary.summary}
        </section>
      </main>
    </div>
  );
}
