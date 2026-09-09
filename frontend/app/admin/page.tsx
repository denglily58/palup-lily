"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

type EventRow = {
  id: string;
  user_email: string | null;
  action: string;
  target: string | null;
  metadata: Record<string, unknown> | null;
  timestamp: string;
};

type User = {
  id: string;
  email?: string;
  user_metadata?: { name?: string; role?: string };
};

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8080";

export default function AdminPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [events, setEvents] = useState<EventRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let channel: ReturnType<typeof supabase.channel> | null = null;

    (async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (!session) {
        router.push("/login");
        return;
      }
      setUser(session.user);

      // Authenticate realtime channel with user session (RLS respects this)
      supabase.realtime.setAuth(session.access_token);

      // Fetch recent events from backend
      const res = await fetch(`${BACKEND}/events?limit=30`);
      const data = await res.json();
      setEvents(data.events || []);
      setLoading(false);

      // Realtime subscribe: unique channel name to avoid React StrictMode double-subscribe
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      channel = (supabase.channel(`event_logs_${Date.now()}`) as any)
        .on(
          "postgres_changes",
          { event: "INSERT", schema: "public", table: "event_logs" },
          (payload: { new: EventRow }) => {
            setEvents((prev) => [payload.new, ...prev].slice(0, 50));
          }
        )
        .subscribe();
    })();

    return () => {
      if (channel) supabase.removeChannel(channel);
    };
  }, [router]);

  async function handleLogout() {
    if (user) {
      await fetch(`${BACKEND}/events`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          user_email: user.email,
          action: "logout",
        }),
      });
    }
    await supabase.auth.signOut();
    router.push("/login");
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-neutral-500">
        Loading...
      </div>
    );
  }

  const displayName = user?.user_metadata?.name || user?.email || "User";
  const role = user?.user_metadata?.role || "Member";

  return (
    <div className="min-h-screen bg-neutral-100">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-xl">🌙</span>
            <span className="font-semibold tracking-[0.15em]">LUNA</span>
            <span className="text-neutral-300">·</span>
            <span className="text-neutral-600 text-sm">Admin</span>
          </div>
          <div className="flex items-center gap-4">
            <button className="text-xs px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
              🟢 Lily is online
            </button>
            <div className="text-right">
              <div className="text-sm font-medium">{displayName}</div>
              <div className="text-xs text-neutral-500">{role}</div>
            </div>
            <div className="w-8 h-8 bg-gradient-to-br from-purple-200 to-pink-200 rounded-full" />
            <button
              onClick={handleLogout}
              className="text-xs text-neutral-500 hover:text-neutral-800"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8">
        <div>
          <h1 className="text-2xl font-light">Good morning, {displayName.split(" ")[0]} ☀️</h1>
          <p className="text-sm text-neutral-500">
            Welcome to LUNA Beauty Admin. Dashboard widgets & Lily-B coming Day 4-5.
          </p>
        </div>

        {/* Activity Log */}
        <section className="bg-white rounded-2xl border overflow-hidden">
          <div className="p-4 border-b flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-lg">📋</span>
              <span className="font-medium">Activity Log</span>
              <span className="text-xs text-neutral-500">(audit trail)</span>
            </div>
            <span className="text-xs text-neutral-400">{events.length} events</span>
          </div>

          {events.length === 0 ? (
            <div className="p-8 text-center text-sm text-neutral-500">
              No events yet — will populate as you use the app.
            </div>
          ) : (
            <div className="divide-y">
              {events.map((e) => (
                <div key={e.id} className="px-4 py-3 flex items-center gap-3 text-sm hover:bg-neutral-50">
                  <span
                    className={
                      "px-2 py-0.5 rounded text-xs " +
                      (e.action === "login"
                        ? "bg-emerald-100 text-emerald-700"
                        : e.action === "logout"
                        ? "bg-neutral-200 text-neutral-700"
                        : e.action === "chat_query"
                        ? "bg-purple-100 text-purple-700"
                        : "bg-blue-100 text-blue-700")
                    }
                  >
                    {e.action}
                  </span>
                  <span className="flex-1 text-neutral-600">
                    {e.user_email || <span className="text-neutral-400">anonymous</span>}
                    {e.target && <span className="text-neutral-400"> · {e.target}</span>}
                  </span>
                  <span className="text-xs text-neutral-400">
                    {new Date(e.timestamp).toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
