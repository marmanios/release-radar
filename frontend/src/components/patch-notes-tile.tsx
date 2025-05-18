"use client";

import type { Tables } from "@/types/database";
import { getIconPathForSource } from "@/utils";
import Image from "next/image";
import { useRouter } from "next/navigation";

export function PatchNotesTile({ patch }: { patch: Tables<"patch_notes"> }) {
  const router = useRouter();
  return (
    <li
      key={patch.version}
      className="min-w-[295px] border-b border-gray-700 pb-2 text-xs sm:min-w-[378px] sm:text-lg cursor-pointer"
      onClick={() => {
        router.push(encodeURI(`/${patch.source}/${patch.version}`));
      }}
    >
      <div className="flex flex-row">
        <div className="w-[32px] h-[32px] sm:w-[48px] sm:h-[48px] relative">

        <Image src={getIconPathForSource(patch.source)} fill alt={`${patch.source} icon`}/>
        </div>
        <div className="w-full ml-4">
          <b>{patch.source.toLowerCase()}</b> - {patch.version.toLowerCase()} -{" "}
          <p className="text-gray-300">
            Released: {new Date(patch.released_at).toLocaleDateString()}
          </p>
        </div>
      </div>
    </li>
  );
}
