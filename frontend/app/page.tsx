"use client";

import { useState, useEffect, useRef } from "react";
import ChatSidebar from "./components/ChatSidebar";
import ChatMessage from "./components/ChatMessage";
import ChatInput from "./components/ChatInput";
import { getUserId } from "./utils/cookies";

interface Message {
  role: "user" | "assistant";
  content: string;
  type?: "message" | "decision";
  timestamp?: string;
}

interface Thread {
  thread_id: string;
  created_at: string;
}

interface InterruptData {
  question?: string;
  details?: string;
  [key: string]: unknown;
}

export default function ChatPage() {
  const [currentThreadId, setCurrentThreadId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentStreamingMessage, setCurrentStreamingMessage] = useState("");
  const [isToolCalling, setIsToolCalling] = useState(false);
  const [isSubagentCalling, setIsSubagentCalling] = useState(false);
  const [toolMessage, setToolMessage] = useState<string>("");
  const [subagentMessage, setSubagentMessage] = useState<string>("");
  const [interruptData, setInterruptData] = useState<InterruptData | null>(null);
  const [reviseFeedback, setReviseFeedback] = useState("");
  const [editFeedback, setEditFeedback] = useState("");
  const wsRef = useRef<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, currentStreamingMessage]);

  // Убеждаемся, что user_id установлен в куки при первой загрузке
  useEffect(() => {
    // Вызываем getUserId() чтобы гарантировать, что user_id установлен в куки
    getUserId();
  }, []);

  const connectWebSocket = (threadId: string) => {
    // Закрываем предыдущее соединение если есть
    if (wsRef.current) {
      wsRef.current.close();
    }

    const ws = new WebSocket(`ws://localhost:8000/ws/${threadId}`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "tool") {
        setIsToolCalling(true);
        setToolMessage(data.data || "Вызывается инструмент...");
      }
      else if (data.type === "subagent") {
        setIsSubagentCalling(true);
        setSubagentMessage(data.data || "Вызывается субагент...");
      }
      else if (data.type === "interrupt"){
        setInterruptData(data.data);
      }
      else if (data.type === "stream") {
        // Стриминг ответа
        setIsStreaming(true);
        setCurrentStreamingMessage((prev) => prev + data.data.content);
      } else if (data.type === "message_complete") {
        // Сообщение завершено
        setIsStreaming(false);
        setMessages((prev) => [...prev, data.data]);
        setCurrentStreamingMessage("");
        setIsToolCalling(false);
        setIsSubagentCalling(false);
        setToolMessage("");
        setSubagentMessage("");
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };
  };

  const createNewThread = async () => {
    try {
      // Генерируем thread_id на frontend
      const threadId = crypto.randomUUID();
      const response = await fetch(`http://localhost:8000/user/threads/${threadId}`, {
        method: "POST",
        credentials: "include", // Важно для отправки куки
      });
      const thread: Thread = await response.json();
       setCurrentThreadId(thread.thread_id);
       setMessages([]);
       setCurrentStreamingMessage("");
       setIsToolCalling(false);
       setIsSubagentCalling(false);
       setToolMessage("");
       setSubagentMessage("");
       setInterruptData(null);
       setReviseFeedback("");
       setEditFeedback("");
      connectWebSocket(thread.thread_id);
    } catch (error) {
      console.error("Error creating thread:", error);
    }
  };

  const selectThread = async (threadId: string | null) => {
    if (threadId===null) {
      setCurrentThreadId(null);
      return;
    }
    setCurrentThreadId(threadId);
    setCurrentStreamingMessage("");
    setIsToolCalling(false);
    setIsSubagentCalling(false);
    setToolMessage("");
    setSubagentMessage("");
    setInterruptData(null);
    setReviseFeedback("");
    setEditFeedback("");

    // Загружаем сообщения треда
    try {
      const response = await fetch(
        `http://localhost:8000/user/threads/${threadId}`,
        {
          credentials: "include",
        }
      );
      
      if (!response.ok) {
        setMessages([]);
        return;
      }
      
      const threadMessages: Message[] = await response.json();
      setMessages(threadMessages);
      
    } catch (error) {
      console.error("Error loading messages:", error);
      setMessages([]);
    }

    connectWebSocket(threadId);
  };


  const sendMessage = (message: string) => {
    if (!currentThreadId || !wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      return;
    }
    const newMessage: Message = {
      role: "user",
      content: message
    };
    setMessages((prev) => [...prev, newMessage]);

    wsRef.current.send(
      JSON.stringify({
        type: "message",
        content: message,
      })
    );
  };

  const sendDecision = (action: string, feedback: string = "") => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      return;
    }
    wsRef.current.send(
      JSON.stringify({
        type: "decision",
        content: {
          action: action,
          feedback: feedback
        }
      })
    );
    setInterruptData(null);
    setReviseFeedback("");
    setEditFeedback("");
  };

  const handleFileUpload = async (file: File) => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/files/upload", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      const data = await response.json();
      
      // Отправляем сообщение о загруженном файле
      sendMessage(`Загружен файл: ${file.name} (ID: ${data.file_id})`);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Ошибка при загрузке файла");
  }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      <ChatSidebar
        currentThreadId={currentThreadId}
        onThreadSelect={selectThread}
        onNewThread={createNewThread}
      />

      <div className="flex-1 flex flex-col">
        {currentThreadId ? (
          <>
            <div className="flex-1 overflow-y-auto">
              {messages.length === 0 && !isStreaming ? (
                <div className="flex items-center justify-center h-full">
                  <div className="text-center">
                    <h2 className="text-2xl font-semibold mb-2">
                      Как я могу вам помочь?
                    </h2>
                    <p className="text-gray-400">
                      Начните новый разговор или выберите существующий чат
                    </p>
                  </div>
                </div>
              ) : (
                <div>
                  {Array.isArray(messages) && messages.map((message, index) => (
                    <ChatMessage key={index} message={message} />
                  ))}
                  {isStreaming && (
                    <ChatMessage
                      message={{
                        role: "assistant",
                        content: currentStreamingMessage,
                      }}
                      isStreaming={true}
                    />
                   )}
                   <div ref={messagesEndRef} />
                 </div>
               )}

                {(isToolCalling || isSubagentCalling) && (
                  <div className="px-4 md:px-12 py-2">
                    <div className="flex items-center gap-2 text-sm text-gray-400">
                      <div className="w-4 h-4 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
                      {isToolCalling && <span>{toolMessage}</span>}
                      {isSubagentCalling && <span>{subagentMessage}</span>}
                    </div>
                  </div>
                )}

               {interruptData && (
                 <div className="px-4 md:px-12 py-4 bg-gray-800 rounded-lg mx-4 md:mx-12 my-2">
                   <div className="text-sm text-gray-300 mb-3">
                     {interruptData.question || "Требуется подтверждение действия"}
                     {interruptData.details && (
                        <div className="mt-2 text-xs text-gray-400">
                          {interruptData.details}
                        </div>
                      )}
                   </div>
                   <div className="flex flex-col gap-3">
                     <button
                       onClick={() => sendDecision("approve")}
                       className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm transition-colors"
                     >
                       Согласиться
                     </button>
                     <div className="flex flex-col gap-2">
                       <input
                         type="text"
                         placeholder="Укажите причину несогласия"
                         value={reviseFeedback}
                         onChange={(e) => setReviseFeedback(e.target.value)}
                         className="bg-gray-700 text-white px-3 py-2 rounded text-sm"
                       />
                       <button
                         onClick={() => sendDecision("revise", reviseFeedback)}
                         disabled={!reviseFeedback.trim()}
                         className="bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 text-white px-4 py-2 rounded text-sm transition-colors"
                       >
                         Не согласен
                       </button>
                     </div>
                     <div className="flex flex-col gap-2">
                       <input
                         type="text"
                         placeholder="Предложите свой вариант"
                         value={editFeedback}
                         onChange={(e) => setEditFeedback(e.target.value)}
                         className="bg-gray-700 text-white px-3 py-2 rounded text-sm"
                       />
                       <button
                         onClick={() => sendDecision("edit", editFeedback)}
                         disabled={!editFeedback.trim()}
                         className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white px-4 py-2 rounded text-sm transition-colors"
                       >
                         Предложить вариант
                       </button>
                     </div>
                   </div>
                 </div>
               )}
             </div>

             <ChatInput
              onSendMessage={sendMessage}
              onFileUpload={handleFileUpload}
              disabled={isStreaming}
            />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <p className="text-gray-400">Выберите чат или создайте новый</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
