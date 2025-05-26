
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="sticky bottom-0 flex w-full items-center justify-center border-t-3 border-black p-4 bg-gradient-to-b from-[#440A5F] to-[#3A204F]">
    <p className="text-sm text-gray-300">
      Made by{" "}
      <Link href={"https://marmanios.com"} className="text-[#FBC200]">Maged</Link>
    </p>
  </footer>
  );
}
