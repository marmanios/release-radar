import Footer from "@/components/footer";
import Header from "@/components/header";
import { ReleaseTile } from "@/components/release-tile";
import { createAdminClient } from "@/utils/supabase/admin";
import Link from "next/link";

export default async function SourcePage({
  params,
  searchParams,
}: {
  params: Promise<{ source: string }>;
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const { source } = await params;
  const resultsPerPage = 5;
  const supabase = await createAdminClient();
  const filters = await searchParams;
  const page = filters.page
    ? Array.isArray(filters.page)
      ? parseInt(filters.page[0]!)
      : 1
    : 1;
  const limit = 5; // Default limit for pagination

  // Calculate the offset for pagination
  const offset = (page - 1) * limit;

  // Fetch the releases list from the database
  const { data: releases, error: fetchListError } = await supabase
    .from("patch_notes")
    .select("*")
    .range(offset, offset + limit - 1)
    .eq("source", decodeURI(source))
    .order("released_at", { ascending: false });

  if (fetchListError) {
    console.error(
      "Database Error Fetching the releases list: ",
      fetchListError,
    );
  }

  // Also fetch count of releases for pagination
  const { count: totalReleases, error: countError } = await supabase
    .from("patch_notes")
    .select("*", { count: "exact" })
    .eq("source", decodeURI(source));

  if (countError || totalReleases === null) {
    console.error("Database error in GET/patches count: ", countError);
  }

  const totalPages = Math.ceil((totalReleases ?? 0) / resultsPerPage);

  return (
    <div className="flex min-h-screen flex-col bg-gradient-to-b from-[#440A5F] to-[#3A204F] text-[#E9EDF3]">
      <Header />
      <main className="mx-auto flex max-w-6xl flex-1 flex-col items-center gap-12 px-4 py-8 sm:py-16">
        <h1 className="text-center text-5xl font-extrabold tracking-tight sm:text-[5rem]">
          <span className="text-[#FBC200]">{source}</span> Release Radar
        </h1>
        <p className="mx-auto text-center text-sm text-gray-300 sm:text-xl">
          Changelogs summarized and explained with{" "}
          <span className="text-[#FBC200]">AI</span> ✨
        </p>
        <ul className="flex w-full max-w-md flex-col items-center overflow-y-auto">
          {releases?.map((release) => (
            <ReleaseTile key={release.version} patch={release} />
          ))}
          {releases && releases.length === 0 && <li>No Releases Found 😢</li>}
          {!releases && <li>Error Getting Releases 💥</li>}
        </ul>
        {/* Pagination controls */}
        {totalReleases && (
          <div className="flex w-full max-w-md justify-between">
            <Link
              href={`?page=${page - 1}`}
              className={`rounded bg-[#FBC200] px-3 py-1 font-semibold text-black ${
                page <= 1 ? "pointer-events-none opacity-50" : ""
              }`}
              aria-disabled={page <= 1}
            >
              Previous
            </Link>
            <div className="flex gap-1">
              {Array.from({ length: 5 }, (_, i) => {
                // Always show 5 entries, centered around current page when possible
                let startPage = Math.max(1, Math.min(page - 2, totalPages - 4));
                // If there are less than 5 pages, start at 1
                if (totalPages < 5) startPage = 1;
                const pageNumber = startPage + i;
                if (pageNumber > totalPages) return null;
                return (
                  <Link
                    key={pageNumber}
                    href={`?page=${pageNumber}`}
                    className={`rounded px-3 py-1 ${
                      page === pageNumber
                        ? "bg-[#FBC200] font-bold text-black"
                        : "bg-gray-700 text-white hover:bg-[#FBC200] hover:text-black"
                    }`}
                    aria-current={page === pageNumber ? "page" : undefined}
                  >
                    {pageNumber}
                  </Link>
                );
              })}
            </div>
            <Link
              href={`?page=${page + 1}`}
              className={`rounded bg-[#FBC200] px-3 py-1 font-semibold text-black ${
                totalPages <= page ? "pointer-events-none opacity-50" : ""
              }`}
              aria-disabled={totalPages <= page}
            >
              Next
            </Link>
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
