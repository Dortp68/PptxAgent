"use client";

import { useState, useEffect } from "react";

interface Thread {
  thread_id: string;
  created_at: string;
}

interface ChatSidebarProps {
  currentThreadId: string | null;
  onThreadSelect: (threadId: string | null) => void;
  onNewThread: () => void;
}

export default function ChatSidebar({
  currentThreadId,
  onThreadSelect,
  onNewThread
}: ChatSidebarProps) {
  const [threadIds, setThreadIds] = useState<Thread[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchThreads = async () => {
    try {
      // Получаем список thread_ids
      const threadIdsResponse = await fetch("http://localhost:8000/user/threads", {
        credentials: "include",
      });
      
      if (!threadIdsResponse.ok) {
        // Если ошибка, пытаемся получить детали из ответа
        const errorData = await threadIdsResponse.json().catch(() => ({}));
        console.error(`HTTP error! status: ${threadIdsResponse.status}`, errorData);
        setThreadIds([]);
        return;
      }
      
      const responseData: Thread[] = await threadIdsResponse.json();      
      setThreadIds(responseData);
      

    } catch (error) {
      console.error("Error fetching threads:", error);
      setThreadIds([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchThreads();
  }, [currentThreadId]);

  const deleteThread = async (threadId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    try {
      const threadDeleteResponse = await fetch(`http://localhost:8000/user/threads/${threadId}`, {
        method: "DELETE",
        credentials: "include",
      });
      if (!threadDeleteResponse.ok) {
        // Если ошибка, пытаемся получить детали из ответа
        const errorData = await threadDeleteResponse.json().catch(() => ({}));
        console.error(`HTTP error! status: ${threadDeleteResponse.status}`, errorData);
        return;
      }
      if (currentThreadId === threadId) {
        onThreadSelect(null);
      }
      fetchThreads();
    } catch (error) {
      console.error("Error deleting thread:", error);
    }
  };

  return (
    <div className="w-64 bg-gray-900 text-white flex flex-col h-screen">
      <div className="p-4 border-b border-gray-700">
        <button
          onClick={onNewThread}
          className="w-full bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          Новый чат
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-2">
        {loading ? (
          <div key="loading" className="text-gray-400 text-center py-4">Загрузка...</div>
        ) : threadIds.length === 0 ? (
          <div key="empty" className="text-gray-400 text-center py-4 text-sm">
            Нет чатов
          </div>
        ) : (
          threadIds.map((thread) => {
            if (!thread?.thread_id) {
              return null;
            }
            return (
              <div
                key={thread.thread_id}
                onClick={() => onThreadSelect(thread.thread_id)}
                className={`p-3 rounded-lg mb-2 cursor-pointer group hover:bg-gray-800 transition-colors ${
                  currentThreadId === thread.thread_id ? "bg-gray-800" : ""
                }`}
              >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium truncate">
                    {thread.thread_id}
                  </div>
                  <div className="text-xs text-gray-400 mt-1">
                    {new Date(thread.created_at).toLocaleDateString("ru-RU", {
                      day: "numeric",
                      month: "short",
                    })}
                  </div>
                </div>
                <button
                  onClick={(e) => deleteThread(thread.thread_id, e)}
                  className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-400 transition-opacity ml-2"
                >
                  <svg
                    className="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            </div>
            );
          })
        )}
      </div>
    </div>
  );
}

