"use client";
import ChatBubble from "@/components/ChatBubble";
import { Input } from "@/components/ui/input";
import { ShinyButton } from "@/components/ui/shiny-button";
import { SparklesText } from "@/components/ui/sparkles-text";
import { Textarea } from "@/components/ui/textarea";
import { useEffect, useState } from "react";

const BASE_API = "http://localhost:5000";
//base api
export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [chat, setChat] = useState([]); 
  const [error, setError] = useState(null);

  const generateData = async () => {
    if (!query.trim()) return;

    // Add user query to chat
    setChat((prev) => [...prev, { type: "user", text: query }]);
    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch(`${BASE_API}/request`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!res.ok) throw new Error("Failed to fetch response");

      console.log("Response:", res);

      const data = await res.json();
      console.log("Response data:", data);
      console.log("Parsed function:", data.function);
      console.log("Parsed message:", data.message);
      console.log("Parsed output:", data.function.length == 0 ? data.message.content : data.function.output);
      const responses = data.function.map((f) => ({
        type: "bot",
        text: f.output === null ? data.message.content : f.output,
      }));
      console.log("Parsed responses:", responses);

      setChat((prev) => [...prev, ...responses]);
    } catch (err) {
      setError("Something went wrong. Please try again.");
      setChat((prev) => [...prev, { type: "bot", text: "Something went wrong. Please try again." }]);
    } finally {
      setIsLoading(false);
      setQuery(""); 
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      generateData();
    }
  };

  return (
    <div className="flex flex-col items-center min-h-screen px-4 md:px-72 pb-40">
      <SparklesText className="py-12" text="Store AI" />

      <div className="w-full flex flex-col gap-2">
        {chat.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"}`}
          >
            <ChatBubble
              message={msg.text}
              isLoading={false}
              customStyle={{
                backgroundColor: msg.type === "user" ? "#007AFF" : "#DCF8C6", // Blue for user, green for bot
                color: msg.type === "user" ? "#fff" : "#000",
                textAlign: msg.type === "user" ? "right" : "left",
              }}
            />
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <ChatBubble message="Generating response..." isLoading={true} />
          </div>
        )}
      </div>

      <div className="fixed w-full px-60 flex flex-col mt-auto pb-4 bottom-0 bg-white items-end justify-center gap-2">
        <Textarea
          placeholder="Enter your prompt"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown} 
          disabled={isLoading}
        />
        <ShinyButton onClick={generateData} disabled={isLoading}>
          {isLoading ? "Loading..." : "Generate"}
        </ShinyButton>
      </div>
    </div>
  );
}
