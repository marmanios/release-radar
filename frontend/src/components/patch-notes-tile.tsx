"use client";

import type { Tables } from "@/types/database";
// import { getIconPathForSource } from "@/utils";
import Image from "next/image";
import { useRouter } from "next/navigation";

export function PatchNotesTile({ patch }: { patch: Tables<"patch_notes"> }) {
  const router = useRouter();
  return (
    <li
      key={patch.version}
      className="w-full cursor-pointer border-b rounded-sm border-gray-700 p-2 text-xs sm:text-lg hover:bg-gray-800"
      onClick={() => {
        router.push(encodeURI(`/${patch.source}/${patch.version}`));
      }}
    >
      <div className="flex flex-row items-center">
        <div className="relative h-[32px] w-[32px] sm:h-[48px] sm:w-[48px]">
          <Image
            src={`/source_icons/${patch.source}.svg`}
            fill
            alt={`${patch.source} icon`}
          />
        </div>
        <div className="ml-4 w-full">
          <b>{patch.source.toLowerCase()}</b> - {patch.version.toLowerCase()}
          <p className="text-gray-300">
            Released: {new Date(patch.released_at).toLocaleDateString()}
          </p>
        </div>
      </div>
    </li>
  );
}
