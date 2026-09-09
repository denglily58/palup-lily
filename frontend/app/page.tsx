"use client";

import { useEffect, useRef, useState } from "react";

type Message = { role: "user" | "assistant"; content: string };

type Product = {
  id: string;
  sku: string;
  name_en: string;
  name_zh: string;
  category: string;
  subcategory: string;
  price: number;
  shade_count: number;
  avg_rating: number;
  review_count: number;
  emoji: string;
  image_url: string;
  tags: string[];
};

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8080";

export default function Home() {
  const [lang, setLang] = useState<"en" | "zh">("en");
  const [sessionId, setSessionId] = useState("");
  const [products, setProducts] = useState<Product[]>([]);

  // Chat widget state
  const [chatOpen, setChatOpen] = useState(true);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi, I'm Lily — your shopping sidekick ✨ Ask me anything: shade matching, reviews, shipping, returns, or just what's new.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let id = localStorage.getItem("luna_lily_session");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("luna_lily_session", id);
    }
    setSessionId(id);

    fetch(`${BACKEND}/products`)
      .then((r) => r.json())
      .then((d) => setProducts(d.products || []))
      .catch(() => {});
  }, []);

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
            ? "Switched to English ✨ How can your shopping sidekick help?"
            : "已切換為中文 ✨ 你的逛街小幫手能幫上什麼？",
      },
    ]);
  }

  async function resetConversation() {
    if (!sessionId) return;
    await fetch(`${BACKEND}/reset?session_id=${sessionId}`, { method: "POST" });
    setMessages([
      {
        role: "assistant",
        content:
          lang === "en"
            ? "Fresh start ✨ What are you looking for?"
            : "從頭開始 ✨ 想找什麼？",
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
        body: JSON.stringify({ message: text, lang, session_id: sessionId }),
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
              ? `Something went wrong (${msg}) — try again in a moment.`
              : `抱歉出錯了 (${msg}) — 請稍後再試。`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-neutral-50 text-neutral-900">
      {/* Top banner */}
      <div className="bg-neutral-900 text-white text-xs text-center py-2 tracking-wider">
        {lang === "en"
          ? "FREE SHIPPING OVER $60 · VEGAN · CRUELTY-FREE"
          : "滿 $60 免運 · 純素 · 無動物實驗"}
      </div>

      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">🌙</span>
            <span className="text-xl font-semibold tracking-[0.15em]">LUNA</span>
            <span className="text-xs uppercase tracking-widest text-neutral-400 ml-1">
              Beauty
            </span>
          </div>
          <nav className="hidden md:flex gap-8 text-sm">
            <a href="#" className="hover:text-purple-600">Shop</a>
            <a href="#" className="hover:text-purple-600">About</a>
            <a href="#" className="hover:text-purple-600">Journal</a>
            <a href="#" className="hover:text-purple-600">Loyalty</a>
          </nav>
          <div className="flex items-center gap-4 text-sm">
            <span>🔍</span>
            <span>👤</span>
            <span>🛍 0</span>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 py-16 text-center">
        <h1 className="text-5xl font-light mb-4 tracking-tight">
          {lang === "en" ? "Colour, quietly considered." : "細膩色彩，靜謐雕琢。"}
        </h1>
        <p className="text-neutral-500 mb-6">
          {lang === "en"
            ? "Vegan · Cruelty-free · Made for every undertone"
            : "純素 · 無動物實驗 · 適合所有膚色底調"}
        </p>
        <button className="bg-neutral-900 text-white px-8 py-3 text-sm tracking-widest">
          {lang === "en" ? "SHOP BESTSELLERS" : "選購熱銷"}
        </button>
      </section>

      {/* Product Grid */}
      <section className="max-w-6xl mx-auto px-6 pb-24">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-lg font-medium tracking-wide">
            {lang === "en" ? "BESTSELLERS" : "熱銷商品"}
          </h2>
          <span className="text-sm text-neutral-500">{products.length} products</span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
          {products.map((p) => (
            <div key={p.id} className="group cursor-pointer">
              <div className="aspect-square rounded-lg mb-3 overflow-hidden shadow-sm hover:shadow-md transition bg-gradient-to-br from-purple-50 via-pink-50 to-rose-50">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={p.image_url}
                  alt={p.name_en}
                  loading="lazy"
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = "none";
                    const parent = target.parentElement;
                    if (parent && !parent.querySelector(".emoji-fallback")) {
                      const span = document.createElement("span");
                      span.className = "emoji-fallback w-full h-full flex items-center justify-center text-6xl";
                      span.textContent = p.emoji;
                      parent.appendChild(span);
                    }
                  }}
                />
              </div>
              <div className="text-xs text-neutral-500 mb-1 uppercase tracking-wider">
                {p.subcategory}
              </div>
              <div className="font-medium mb-1 text-sm">
                {lang === "en" ? p.name_en : p.name_zh}
              </div>
              <div className="text-sm">
                ${p.price}
                {p.shade_count > 1 && (
                  <span className="text-neutral-500"> · {p.shade_count} shades</span>
                )}
              </div>
              <div className="text-xs text-neutral-500 mt-1">
                ★★★★★ {p.avg_rating || "—"} ({p.review_count})
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Chat Widget (fixed bottom-right) */}
      {chatOpen ? (
        <div
          className="fixed bottom-6 right-6 w-[400px] bg-white rounded-2xl shadow-2xl overflow-hidden flex flex-col"
          style={{ height: "620px", maxHeight: "calc(100vh - 48px)" }}
        >
          <div className="p-4 border-b border-neutral-100 flex items-center gap-3 bg-gradient-to-r from-purple-50 via-pink-50 to-rose-50">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-300 to-pink-300 flex items-center justify-center text-lg">
              🌙
            </div>
            <div className="flex-1">
              <div className="font-medium text-sm">Lily</div>
              <div className="text-xs text-neutral-500 flex items-center gap-1">
                <span className="w-2 h-2 bg-emerald-400 rounded-full" />
                Your Shopping Sidekick · LUNA Beauty
              </div>
            </div>
            <button
              onClick={resetConversation}
              className="text-xs px-2 py-1 rounded-full bg-white/70 text-neutral-600 hover:bg-white"
              title="Reset"
            >
              ⟳
            </button>
            <button
              onClick={toggleLang}
              className="text-xs px-2 py-1 rounded-full bg-white/70 text-neutral-600 hover:bg-white"
              title="Switch language"
            >
              {lang === "en" ? "EN" : "中"}
            </button>
            <button
              onClick={() => setChatOpen(false)}
              className="text-neutral-400 hover:text-neutral-700 px-1"
              title="Minimize"
            >
              ─
            </button>
          </div>

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

          <div className="p-3 border-t border-neutral-100 flex items-center gap-2">
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
      ) : (
        <button
          onClick={() => setChatOpen(true)}
          className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 text-white shadow-2xl hover:scale-105 transition flex items-center justify-center text-2xl"
          title="Chat with Lily"
        >
          🌙
        </button>
      )}
    </div>
  );
}
