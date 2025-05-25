import type { TAiSummary } from "@/types";
import { createAdminClient } from "@/utils/supabase/admin";
import Link from "next/link";
import Image from "next/image";
import ReactMarkdown from "react-markdown";

export default async function ChangeLogs({
  params,
}: {
  params: Promise<{ source: string; version: string }>;
}) {
  const supabase = await createAdminClient();
  const { source, version } = await params;

  console.log(
    "Fetching Changelogs for source:",
    source,
    "and version:",
    version,
  );

  const { data, error } = await supabase
    .from("patch_notes")
    .select("*")
    .eq("source", decodeURI(source))
    .eq("version", decodeURI(version))
    .single();

  if (error || !data) {
    console.error(
      `Database error in GET/${source}/{version}: ${error?.message || "Data is null"}`,
    );
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
        <nav className="flex h-16 items-center justify-between px-4">
          <Link href={"/"}>Home</Link>
          <Link href={"www.google.com"}>Github</Link>
        </nav>
      </div>
    );
  }

  const patchNotes: {
    ai_summary: TAiSummary;
    created_at: Date;
    released_at: Date;
    source: string;
    source_url: string;
    version: string;
  } = {
    ai_summary: JSON.parse(data.ai_summary) as TAiSummary,
    created_at: new Date(data.created_at),
    released_at: new Date(data.released_at),
    source: data.source,
    source_url: data.source_url,
    version: data.version,
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#440A5F] to-[#3A204F] text-[#E9EDF3]">
      <nav className="sticky top-0 flex h-16 items-center justify-between px-4 backdrop-blur-sm">
        <span className="flex items-center gap-4">
          <Link className="hover:underline" href={"/"}>
            Home
          </Link>
          <Link className="hover:underline" href={`/${source}`}>
            Previous Releases
          </Link>
        </span>

        <Link
          className="flex items-center gap-4 hover:underline"
          href={"https://github.com/marmanios/patch_notes"}
        >
          Contribute!{" "}
          <Image src={`/github.svg`} height={32} width={32} alt={`GitHub`} />
        </Link>
      </nav>
      <main className="mx-auto flex max-w-6xl flex-col items-center gap-12 px-4 py-8 sm:py-16">
        <h1 className="text-center text-5xl font-extrabold tracking-tight sm:text-[5rem]">
          Changelog summary for{" "}
          <span className="text-[#FBC200]">{patchNotes.version}</span> 📕
        </h1>
        <p className="text-lg text-gray-300 sm:text-2xl">
          Presented by <span className="text-[#FBC200]">ReleaseRadar.dev</span>.
          Find the full changelog{" "}
          <Link
            rel="noopener noreferrer"
            target="_blank"
            href={patchNotes.source_url}
            className="text-[#FBC200] underline"
          >
            here
          </Link>
          .
        </p>
        <section
          id="summary"
          className="text-md w-full max-w-6xl rounded-lg px-4 sm:text-lg"
        >
          {patchNotes.ai_summary.summary && (
            <ReactMarkdown
              components={{
                code: ({ node, ...props }) => (
                  <code
                    style={{ color: "#FBC200", background: "#2e2d2b" }}
                    {...props}
                  />
                ),
              }}
            >
              {patchNotes.ai_summary.summary}
            </ReactMarkdown>
          )}
        </section>
        <section
          id="notes"
          className="text-md w-full max-w-6xl rounded-lg px-4 sm:text-lg"
        >
          <h2 className="mb-4 text-2xl font-bold">Notes</h2>
          <ul className="list-disc pl-5">
            {patchNotes.ai_summary.notes?.map((note, index) => (
              <li key={`note-${index}`} className="mb-2">
                <ReactMarkdown
                  components={{
                    code: ({ node, ...props }) => (
                      <code
                        style={{ color: "#FBC200", background: "#2e2d2b" }}
                        {...props}
                      />
                    ),
                  }}
                >
                  {note}
                </ReactMarkdown>
              </li>
            ))}
          </ul>
        </section>
        <section
          id="supplementary-definitions"
          className="text-md w-full max-w-6xl rounded-lg px-4 sm:text-lg"
        >
          <h2 className="mb-4 text-2xl font-bold">Supplementary Definitions</h2>
          <ul className="list-disc pl-5">
            {patchNotes.ai_summary.supplementary_definitions?.map(
              (definition, index) => (
                <li key={`definition-${index}`} className="mb-2">
                  <ReactMarkdown
                    components={{
                      code: ({ node, ...props }) => (
                        <code
                          style={{ color: "#FBC200", background: "#2e2d2b" }}
                          {...props}
                        />
                      ),
                    }}
                  >{`**${definition.term}**: ${definition.definition}`}</ReactMarkdown>
                </li>
              ),
            )}
          </ul>
        </section>
      </main>
    </div>
  );
}
