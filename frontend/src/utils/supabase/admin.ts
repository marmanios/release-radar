import { env } from "@/env";
import { cookies } from "next/headers";
import type { Database } from "@/types/database";
import { createServerClient } from "@supabase/ssr";

export const createAdminClient = async () => {
  const cookieStore = await cookies();

  return createServerClient<Database>(
    env.NEXT_PUBLIC_SUPABASE_URL,
    env.SUPBASE_SERVICE_ROLE_KEY,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) => {
              cookieStore.set(name, value, options);
            });
          } catch (error) {
           console.log("Error setting cookies:", error);
          }
        },
      },
    },
  );
};
