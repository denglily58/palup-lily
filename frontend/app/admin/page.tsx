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

type Stats = {
  today_conversations: { count: number; vs_yesterday_pct: number | null; yesterday_count: number };
  today_conversions: { converted: number; total: number; rate_pct: number; est_revenue_usd: number };
  demand_gaps: { question: string; category: string | null; count: number }[];
  red_alerts: { high_urgency: number; all_pending: number };
  sla_compliance: { on_time: number; total_resolved: number; pct: number | null };
};

type Metrics = {
  total_conversations: number;
  total_tokens: number;
  total_cost_usd: number;
  avg_latency_ms: number;
  by_model: Record<string, number>;
};

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8080";

type LilyBMsg = { role: "merchant" | "assistant"; content: string };

export default function AdminPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [events, setEvents] = useState<EventRow[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);

  // Lily-B chat state
  const [lbMessages, setLbMessages] = useState<LilyBMsg[]>([
    { role: "assistant", content: "Hi — I'm Lily-B, your business copilot. Ask me about buyer trends, demand gaps, sales, or the handoff queue." },
  ]);
  const [lbInput, setLbInput] = useState("");
  const [lbLoading, setLbLoading] = useState(false);
  const [lbSessionId] = useState(() =>
    typeof window !== "undefined" ? `admin-${Date.now()}` : "server"
  );

  async function sendToLilyB() {
    const text = lbInput.trim();
    if (!text || lbLoading) return;
    setLbInput("");
    setLbMessages((prev) => [...prev, { role: "merchant", content: text }]);
    setLbLoading(true);
    try {
      const res = await fetch(`${BACKEND}/analytics/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, session_id: lbSessionId }),
      });
      const data = await res.json();
      setLbMessages((prev) => [...prev, { role: "assistant", content: data.reply || "(no reply)" }]);
    } catch (err) {
      setLbMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Something went wrong: ${err}` },
      ]);
    } finally {
      setLbLoading(false);
    }
  }

  async function refreshStats() {
    try {
      const [statsRes, metricsRes] = await Promise.all([
        fetch(`${BACKEND}/admin/stats`),
        fetch(`${BACKEND}/metrics`),
      ]);
      setStats(await statsRes.json());
      setMetrics(await metricsRes.json());
    } catch {}
  }

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

      // Fetch recent events + stats
      const [eventsRes] = await Promise.all([
        fetch(`${BACKEND}/events?limit=30`),
        refreshStats(),
      ]);
      const data = await eventsRes.json();
      // Dedupe by id (StrictMode may fire twice)
      const unique = Array.from(
        new Map((data.events || []).map((e: EventRow) => [e.id, e])).values()
      ) as EventRow[];
      setEvents(unique);
      setLoading(false);

      // Realtime subscribe: unique channel name to avoid React StrictMode double-subscribe
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      channel = (supabase.channel(`event_logs_${Date.now()}`) as any)
        .on(
          "postgres_changes",
          { event: "INSERT", schema: "public", table: "event_logs" },
          (payload: { new: EventRow }) => {
            setEvents((prev) => {
              if (prev.some((e) => e.id === payload.new.id)) return prev;
              return [payload.new, ...prev].slice(0, 50);
            });
            refreshStats();
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
      <header className="bg-white shadow-sm sticky top-0 z-10">
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
            {stats?.today_conversations.count ?? 0} conversations today · Lily-B chat coming Day 4
          </p>
        </div>

        {/* Starter Widgets */}
        {stats && (
          <section>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-medium tracking-wide text-neutral-500">📌 Dashboard</h2>
              <span className="text-xs text-neutral-400">auto-refreshes with new events</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Today's Conversations */}
              <div className="bg-white rounded-xl shadow-sm hover:shadow-md p-5 transition">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-xs text-neutral-500">Today's Conversations</div>
                  {stats.today_conversations.vs_yesterday_pct !== null && (
                    <span
                      className={
                        "text-xs px-2 py-0.5 rounded-full " +
                        (stats.today_conversations.vs_yesterday_pct >= 0
                          ? "bg-emerald-50 text-emerald-700"
                          : "bg-red-50 text-red-700")
                      }
                    >
                      {stats.today_conversations.vs_yesterday_pct >= 0 ? "↑" : "↓"}{" "}
                      {Math.abs(stats.today_conversations.vs_yesterday_pct)}%
                    </span>
                  )}
                </div>
                <div className="text-3xl font-light">{stats.today_conversations.count}</div>
                <div className="text-xs text-neutral-500 mt-2">
                  vs yesterday {stats.today_conversations.yesterday_count}
                </div>
              </div>

              {/* Today's Conversions */}
              <div className="bg-white rounded-xl shadow-sm hover:shadow-md p-5 transition">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-xs text-neutral-500">Today's Conversions</div>
                  <span className="text-xs px-2 py-0.5 bg-purple-50 text-purple-700 rounded-full">
                    {stats.today_conversions.rate_pct}%
                  </span>
                </div>
                <div className="text-3xl font-light">
                  {stats.today_conversions.converted}
                  <span className="text-lg text-neutral-400">/{stats.today_conversions.total}</span>
                </div>
                <div className="text-xs text-neutral-500 mt-2">
                  Est. revenue ${stats.today_conversions.est_revenue_usd.toLocaleString()}
                </div>
              </div>

              {/* Demand Gaps */}
              <div className="bg-white rounded-xl shadow-sm hover:shadow-md p-5 transition">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-xs text-neutral-500">Demand Gaps Top 3</div>
                  <span className="text-xs px-2 py-0.5 bg-amber-50 text-amber-700 rounded-full">
                    this week
                  </span>
                </div>
                {stats.demand_gaps.length === 0 ? (
                  <div className="text-sm text-neutral-400 mt-2">No gaps logged yet.</div>
                ) : (
                  <ul className="text-xs space-y-1 mt-1">
                    {stats.demand_gaps.map((g, i) => (
                      <li key={i} className="flex justify-between gap-2">
                        <span className="truncate">{g.category || g.question}</span>
                        <span className="text-neutral-400 shrink-0">{g.count}×</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>

              {/* Human Handoffs */}
              <div className="bg-white rounded-xl shadow-sm hover:shadow-md p-5 transition">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-xs text-neutral-500">Human Handoffs</div>
                  <span
                    className={
                      "text-xs px-2 py-0.5 rounded-full " +
                      (stats.red_alerts.high_urgency > 0
                        ? "bg-red-50 text-red-700"
                        : "bg-neutral-100 text-neutral-600")
                    }
                  >
                    {stats.red_alerts.high_urgency > 0 ? "urgent" : "normal"}
                  </span>
                </div>
                <div className="text-3xl font-light">{stats.red_alerts.all_pending}</div>
                <div className="text-xs text-neutral-500 mt-2">
                  {stats.red_alerts.high_urgency} high-urgency · returns auto
                </div>
              </div>

              {/* SLA Compliance */}
              <div className="bg-white rounded-xl shadow-sm hover:shadow-md p-5 transition">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-xs text-neutral-500">SLA Compliance</div>
                  <span
                    className={
                      "text-xs px-2 py-0.5 rounded-full " +
                      ((stats.sla_compliance.pct ?? 100) >= 90
                        ? "bg-emerald-50 text-emerald-700"
                        : (stats.sla_compliance.pct ?? 100) >= 75
                        ? "bg-amber-50 text-amber-700"
                        : "bg-red-50 text-red-700")
                    }
                  >
                    {stats.sla_compliance.pct !== null ? `${stats.sla_compliance.pct}%` : "—"}
                  </span>
                </div>
                <div className="text-3xl font-light">
                  {stats.sla_compliance.on_time}
                  <span className="text-lg text-neutral-400">/{stats.sla_compliance.total_resolved}</span>
                </div>
                <div className="text-xs text-neutral-500 mt-2">
                  on-time · high=1h, normal=4h, low=24h
                </div>
              </div>

              {/* AI Usage */}
              {metrics && (
                <div className="bg-white rounded-xl shadow-sm hover:shadow-md p-5 transition">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-xs text-neutral-500">🤖 AI Usage</div>
                    <span className="text-xs px-2 py-0.5 bg-purple-50 text-purple-700 rounded-full">
                      this month
                    </span>
                  </div>
                  <div className="text-3xl font-light">
                    ${metrics.total_cost_usd.toFixed(3)}
                  </div>
                  <div className="text-xs text-neutral-500 mt-2">
                    {metrics.total_conversations} chats · {(metrics.total_tokens / 1000).toFixed(1)}k tokens
                  </div>
                </div>
              )}
            </div>
          </section>
        )}

        {/* Lily-B analyst chat */}
        <section className="bg-white rounded-2xl shadow-sm overflow-hidden">
          <div className="p-4 border-b border-neutral-100 flex items-center gap-2">
            <span className="text-lg">💬</span>
            <span className="font-medium">Ask Lily-B</span>
            <span className="text-xs text-neutral-500">— your business copilot</span>
          </div>
          <div className="p-6 space-y-4 max-h-[400px] overflow-y-auto">
            {lbMessages.map((m, i) => (
              <div
                key={i}
                className={m.role === "merchant" ? "flex justify-end" : "flex gap-3 items-start"}
              >
                {m.role === "assistant" && (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-300 to-pink-300 flex items-center justify-center text-sm flex-shrink-0">
                    🌙
                  </div>
                )}
                <div
                  className={
                    m.role === "merchant"
                      ? "bg-purple-500 text-white rounded-2xl rounded-tr-sm px-4 py-2 max-w-[600px] text-sm whitespace-pre-wrap"
                      : "bg-neutral-50 rounded-2xl rounded-tl-sm px-4 py-3 max-w-[700px] text-sm whitespace-pre-wrap"
                  }
                >
                  {m.content}
                </div>
              </div>
            ))}
            {lbLoading && (
              <div className="flex gap-3 items-start">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-300 to-pink-300 flex-shrink-0" />
                <div className="bg-neutral-50 rounded-2xl px-4 py-3 text-sm text-neutral-500">
                  Lily-B is analyzing...
                </div>
              </div>
            )}
          </div>
          <div className="p-4 border-t border-neutral-100 flex items-center gap-2">
            <input
              value={lbInput}
              onChange={(e) => setLbInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendToLilyB()}
              placeholder="Ask about buyer trends, demand gaps, sales, handoff queue..."
              disabled={lbLoading}
              className="flex-1 px-4 py-3 rounded-xl bg-neutral-50 text-sm outline-none focus:ring-2 focus:ring-purple-300"
            />
            <button
              onClick={sendToLilyB}
              disabled={lbLoading || !lbInput.trim()}
              className="px-5 py-3 bg-purple-500 text-white rounded-xl text-sm hover:bg-purple-600 disabled:opacity-40"
            >
              Send
            </button>
          </div>
          <div className="px-4 pb-3 flex flex-wrap gap-2">
            <button
              onClick={() => setLbInput("What did buyers ask about in the last 24 hours?")}
              className="text-xs px-3 py-1 rounded-full bg-neutral-100 hover:bg-neutral-200"
            >
              What did buyers ask today?
            </button>
            <button
              onClick={() => setLbInput("What product should we consider adding based on demand gaps?")}
              className="text-xs px-3 py-1 rounded-full bg-neutral-100 hover:bg-neutral-200"
            >
              Product ideas from demand gaps
            </button>
            <button
              onClick={() => setLbInput("What is our AoV and top products?")}
              className="text-xs px-3 py-1 rounded-full bg-neutral-100 hover:bg-neutral-200"
            >
              AoV & top products
            </button>
            <button
              onClick={() => setLbInput("Are there any urgent handoffs pending?")}
              className="text-xs px-3 py-1 rounded-full bg-neutral-100 hover:bg-neutral-200"
            >
              Urgent handoffs
            </button>
          </div>
        </section>

        {/* Activity Log */}
        <section className="bg-white rounded-2xl shadow-sm overflow-hidden">
          <div className="p-4 border-b border-neutral-100 flex items-center justify-between">
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
            <div className="divide-y divide-neutral-100">
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
