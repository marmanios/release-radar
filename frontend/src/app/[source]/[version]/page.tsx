import type { TAiSummary } from "@/types";
import { createAdminClient } from "@/utils/supabase/admin";
import Link from "next/link";
import Image from "next/image";

export default async function ChangeLogs({
  params,
}: {
  params: Promise<{ source: string; version: string }>;
}) {
  const supabase = await createAdminClient();
  const { source, version } = await params;

  console.log("Fetching Changelogs for source:", source, "and version:", version);
  
  const { data, error } = await supabase
    .from("patch_notes")
    .select("*")
    .eq("source", decodeURI(source))
    .eq("version", decodeURI(version))
    .single();

  if (error || !data) {
    console.error(`Database error in GET/${source}/{version}: ${error.message}`);
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
    <div className="min-h-screen bg-gradient-to-b from-[#440A5F] to-[#3A204F] text-[#E9EDF3]">
      <nav className="flex h-16 items-center justify-between px-4 sticky top-0 backdrop-blur-sm ">
        <span className="flex items-center gap-4">
          <Link className="hover:underline" href={"/"}>Home</Link>
          <Link className="hover:underline" href={`/${source}`}>Previous Releases</Link>
        
        </span>
          
        <Link className="flex gap-4 items-center hover:underline" href={"https://github.com/marmanios/patch_notes"}>Contribute! <Image src={`/github.svg`} height={32} width={32} alt={`GitHub`}/></Link>
      </nav>
      <main className="flex flex-col items-center gap-12 px-4 py-8 sm:py-16 max-w-6xl mx-auto">
        <h1 className="text-5xl text-center font-extrabold tracking-tight sm:text-[5rem]">
           Changelog summary for <span className="text-[#FBC200]">{patchNotes.version}</span> 📕
        </h1>
        <p className="text-lg text-gray-300 sm:text-2xl">
          Presented by <span className="text-[#FBC200]">patchnotes.dev</span>. Find the full changelog <Link rel="noopener noreferrer" target="_blank" href={patchNotes.source_url} className="text-[#FBC200] underline">here</Link>.
        </p>
        <section id="summary" className="w-full max-w-6xl px-4 text-md rounded-lg sm:text-lg">
          {patchNotes.ai_summary.summary}
        </section>
        <section id="notes" className="w-full max-w-6xl px-4 text-md rounded-lg sm:text-lg">
          <h2 className="text-2xl font-bold mb-4">Notes</h2>
          <ul className="list-disc pl-5">
            {patchNotes.ai_summary.notes.map((note, index) => (
              <li key={`note-${index}`} className="mb-2">{note}</li>
            ))}
          </ul>
        </section>
        <section id="supplementary-definitions" className="w-full max-w-6xl px-4 text-md rounded-lg sm:text-lg">
          <h2 className="text-2xl font-bold mb-4">Supplementary Definitions</h2>
          <ul className="list-disc pl-5">
            {patchNotes.ai_summary.supplementary_definitions.map((definition, index) => (
              <li key={`definition-${index}`} className="mb-2"><b>{definition.term}: </b>{definition.definition}</li>
            ))}
          </ul>
        </section>
      </main>
    </div>
  );
}
