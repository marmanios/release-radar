import { ReleaseTile } from "@/components/release-tile";
import { createAdminClient } from "@/utils/supabase/admin";
import Image from "next/image";
import Link from "next/link";

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  const supabase = await createAdminClient();
  const filters = await searchParams;
  const page = Array.isArray(filters.page)
    ? parseInt(filters.page[0] ?? "1")
    : parseInt(filters.page ?? "1");

  const resultsPerPage = 5; // Default resultsPerPage for pagination

  // Calculate the offset for pagination
  const offset = (page - 1) * resultsPerPage;

  // Fetch the releases list from the database
  const { data: releases, error: fetchListError } = await supabase
    .from("patch_notes")
    .select("*")
    .range(offset, offset + resultsPerPage - 1)
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
    .select("*", { count: "exact" });

  if (countError || !totalReleases) {
    console.error("Database error in GET/patches count: ", countError);
  }

  const totalPages = Math.ceil((totalReleases ?? 0) / resultsPerPage); 

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#440A5F] to-[#3A204F] text-[#E9EDF3]">
      <div className="hidden lg:block fixed top-1/2 right-0 -translate-y-1/2 mr-20 z-0">
        <Image
          src={`/clay-icon-tilted-left.png`}
          alt="Background"
          className="object-cover"
          width={360}
          height={360}
        />
      </div>
      <nav className="sticky top-0 flex h-16 items-center justify-between px-4 backdrop-blur-sm">
        <span> </span>
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
          Your very own <span className="text-[#FBC200]">Release Radar</span>
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
        {/* TODO: Pagination controls */}
        {totalReleases && (
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
                      className={`px-3 py-1 rounded ${
                        page === pageNumber
                          ? "bg-[#FBC200] text-black font-bold"
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
              className={`px-3 py-1 rounded bg-[#FBC200] text-black font-semibold ${
                totalPages <= page ? "opacity-50 pointer-events-none" : ""
              }`}
              aria-disabled={totalPages <= page}
            >
              Next
            </Link>
          </div>
        )}
      </main>
    </div>
  );
}
