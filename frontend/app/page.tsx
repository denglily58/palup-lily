"use client";

import { useEffect, useRef, useState } from "react";

type Message = { role: "user" | "assistant"; content: string };

const BACKEND = "http://localhost:8080";

export default function Home() {
  const [lang, setLang] = useState<"en" | "zh">("en");
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi, I'm Lily ✨ Looking for something? I can help with shade matching, reviews, shipping, and returns.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, loading]);

  function toggleLang() {
    const next = lang === "en" ? "zh" : "en";
    setLang(next);
    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content:
          next === "en"
            ? "Switched to English ✨ How can I help?"
            : "已切換為中文 ✨ 有什麼我可以幫你的嗎？",
      },
    ]);
  }

  async function send() {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setLoading(true);

    try {
      const res = await fetch(`${BACKEND}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, lang }),
      });
      if (!res.ok) throw new Error(`Backend ${res.status}`);
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "assistant", content: data.reply }]);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "unknown";
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            lang === "en"
              ? `Something went wrong (${msg}) — the backend may be offline.`
              : `抱歉出錯了 (${msg}) — backend 可能沒開。`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-neutral-50 flex items-center justify-center p-4">
      <div
        className="w-full max-w-md bg-white rounded-2xl shadow-xl border overflow-hidden flex flex-col"
        style={{ height: "620px" }}
      >
        {/* Header */}
        <div className="p-4 border-b flex items-center gap-3 bg-gradient-to-r from-purple-50 via-pink-50 to-rose-50">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-300 to-pink-300 flex items-center justify-center text-lg">
            🌙
          </div>
          <div className="flex-1">
            <div className="font-medium text-sm">Lily</div>
            <div className="text-xs text-neutral-500 flex items-center gap-1">
              <span className="w-2 h-2 bg-emerald-400 rounded-full" />
              LUNA Beauty · v0.2
            </div>
          </div>
          <button
            onClick={toggleLang}
            className="text-xs px-2 py-1 rounded-full bg-white border border-neutral-200 text-neutral-600 hover:bg-neutral-50"
            title="Switch language"
          >
            {lang === "en" ? "EN" : "中"}
          </button>
        </div>

        {/* Messages */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((m, i) => (
            <div key={i} className={m.role === "user" ? "flex justify-end" : "flex gap-2 items-start"}>
              {m.role === "assistant" && (
                <div className="w-6 h-6 rounded-full bg-gradient-to-br from-purple-300 to-pink-300 flex-shrink-0 flex items-center justify-center text-xs">
                  🌙
                </div>
              )}
              <div
                className={
                  m.role === "user"
                    ? "bg-purple-500 text-white rounded-2xl rounded-tr-sm px-3 py-2 max-w-[280px] text-sm whitespace-pre-wrap"
                    : "bg-neutral-100 rounded-2xl rounded-tl-sm px-3 py-2 max-w-[280px] text-sm whitespace-pre-wrap"
                }
              >
                {m.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex gap-2 items-start">
              <div className="w-6 h-6 rounded-full bg-gradient-to-br from-purple-300 to-pink-300 flex-shrink-0" />
              <div className="bg-neutral-100 rounded-2xl px-3 py-2 text-sm text-neutral-500">
                {lang === "en" ? "Lily is typing..." : "Lily 正在打字..."}
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="p-3 border-t flex items-center gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder={lang === "en" ? "Type a message..." : "輸入訊息..."}
            className="flex-1 px-4 py-2 rounded-full bg-neutral-100 text-sm outline-none focus:ring-2 focus:ring-purple-300"
            disabled={loading}
          />
          <button
            onClick={send}
            disabled={loading || !input.trim()}
            className="w-9 h-9 bg-purple-500 text-white rounded-full flex items-center justify-center disabled:opacity-40 hover:bg-purple-600"
          >
            →
          </button>
        </div>
      </div>
    </div>
  );
}
