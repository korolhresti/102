import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface NewsItem {
  id: number;
  title: string;
  content: string;
  created_at: string;
}

export default function NewsPage() {
  const [news, setNews] = useState<NewsItem[]>([]);

  useEffect(() => {
    fetch("/api/news")
      .then((res) => res.json())
      .then(setNews);
  }, []);

  const handleAnalyze = async (id: number, content: string) => {
    const res = await fetch("/api/analyze_news", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content })
    });
    const data = await res.json();
    alert(data.analysis);
  };

  return (
    <div className="grid grid-cols-1 gap-4 p-4">
      {news.map((item) => (
        <Card key={item.id} className="p-4">
          <h3 className="text-xl font-bold mb-2">{item.title}</h3>
          <p className="text-sm mb-4">{item.content}</p>
          <Button onClick={() => handleAnalyze(item.id, item.content)}>
            🔍 GPT Аналіз
          </Button>
        </Card>
      ))}
    </div>
  );
}