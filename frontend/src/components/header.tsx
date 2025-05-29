import Image from "next/image";
import Link from "next/link";
import { TrackedSources } from "./tracked-sources";

export default function Header({ source }: { source?: string }) {
  return (
    <header className="sticky top-0 flex h-16 items-center justify-center border-b-3 border-black px-4 backdrop-blur-sm">
      <div className="flex w-full max-w-5xl items-center justify-between">
        <Link className="text-xl" href={"/"}>
          Release<span className="text-[#FBC200]">Radar</span>
        </Link>

        <span className="flex items-center gap-4">
          <TrackedSources />

          {source !== undefined ? (
            <nav className="sticky top-0 flex h-16 items-center justify-between">
              <Link className="hover:underline" href={`/${source}`}>
                Previous Releases 📜
              </Link>
            </nav>
          ) : (
            <Link
              className="flex items-center gap-4 hover:underline"
              href={"https://github.com/marmanios/patch_notes"}
            >
              Contribute 👨‍💻
              {/* <Image
                src={`/github.svg`}
                height={32}
                width={32}
                alt={`GitHub`}
              /> */}
            </Link>
          )}
        </span>
      </div>
    </header>
  );
}
