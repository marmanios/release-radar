import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { createAdminClient } from "@/utils/supabase/admin";

export async function TrackedSources() {
  const supabase = await createAdminClient();
  const dbResponse = await supabase.rpc("get_unique_sources");
  const uniqueSources =
    dbResponse.data?.map((item) => item.unique_source) ?? [];

  return (
    <Dialog>
      <DialogTrigger asChild>
        <p className="hover:cursor-pointer hover:underline">
          Tracked Releases 🔍
        </p>
      </DialogTrigger>
      <DialogContent className="bg-gradient-to-b from-[#440A5F] to-[#3A204F] text-[#E9EDF3] sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Tracked Releases</DialogTitle>
          <DialogDescription className="text-md text-gray-400">
            The following programming languages, frameworks & libraries are
            being tracked by ReleaseRadar.
          </DialogDescription>
        </DialogHeader>
        {dbResponse.error ? (
          <p>There was an error fetching this</p>
        ) : (
          <ul>
            {uniqueSources.map((source, index) => (
              <li key={index} className="mb-2">
                <a
                  href={`/${encodeURIComponent(source)}`}
                  className="text-[#FBC200] hover:underline"
                >
                  - {source.charAt(0).toUpperCase() + source.slice(1)}
                </a>
              </li>
            ))}
          </ul>
        )}
      </DialogContent>
    </Dialog>
  );
}
