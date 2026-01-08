"use client";

import { downloadFile } from "./ChatInput";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

interface ChatMessageProps {
  message: Message;
  isStreaming?: boolean;
}

export default function ChatMessage({ message, isStreaming }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={`flex w-full py-6 px-4 md:px-12 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`flex gap-4 max-w-[85%] md:max-w-[60%] lg:max-w-[50%] ${
          isUser ? "flex-row-reverse" : "flex-row"
        }`}
      >
        <div
          className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
            isUser ? "bg-blue-600" : "bg-green-600"
          }`}
        >
          {isUser ? (
            <svg
              className="w-6 h-6 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          ) : (
            <svg
              className="w-6 h-6 text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
          )}
        </div>

        <div
          className={`flex-1 px-5 py-4 rounded-2xl shadow-sm relative ${
            isUser
              ? "bg-gray-700 text-white rounded-tr-none"
              : "bg-gray-800 text-gray-100 rounded-tl-none"
          }`}
        >
          <div className="text-xs font-bold mb-1 opacity-50 uppercase tracking-wide">
            {isUser ? "Вы" : "Ассистент"}
          </div>
          
          <div className="text-sm md:text-base leading-relaxed whitespace-pre-wrap">
            {message.content}
            {isStreaming && (
              <span className="inline-block w-2 h-5 bg-blue-400 ml-1 animate-pulse align-middle" />
            )}
            
            {message.content.match(/ID: ([a-f0-9-]+)/) && (
              <div className="mt-3 pt-3 border-t border-gray-600/50">
                <button
                  onClick={() => {
                     console.log("Download logic here");
                  }}
                  className="bg-gray-900/50 hover:bg-gray-900 px-3 py-2 rounded flex items-center gap-2 text-xs transition-colors"
                >
                  <svg
                    className="w-4 h-4 text-blue-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                  </svg>
                  <span className="text-blue-300">Скачать файл</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// export default function ChatMessage({ message, isStreaming }: ChatMessageProps) {
//   const isUser = message.role === "user";

//   return (
//     <div
//       className={`flex gap-4 p-4 ${
//         isUser ? "justify-start" : "justify-end"
//       }`}
//     >
//       <div
//         className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
//           isUser
//             ? "bg-blue-600"
//             : "bg-green-600"
//         }`}
//       >
//         {isUser ? (
//           <svg
//             className="w-5 h-5 text-white"
//             fill="none"
//             stroke="currentColor"
//             viewBox="0 0 24 24"
//           >
//             <path
//               strokeLinecap="round"
//               strokeLinejoin="round"
//               strokeWidth={2}
//               d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
//             />
//           </svg>
//         ) : (
//           <svg
//             className="w-5 h-5 text-white"
//             fill="none"
//             stroke="currentColor"
//             viewBox="0 0 24 24"
//           >
//             <path
//               strokeLinecap="round"
//               strokeLinejoin="round"
//               strokeWidth={2}
//               d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
//             />
//           </svg>
//         )}
//       </div>
//       <div className="flex-1">
//         <div className="text-sm font-semibold mb-1 text-gray-300">
//           {isUser ? "Вы" : "Ассистент"}
//         </div>
//         <div className="text-gray-100 whitespace-pre-wrap leading-relaxed">
//           {message.content}
//           {isStreaming && (
//             <span className="inline-block w-2 h-5 bg-gray-400 ml-1 animate-pulse" />
//           )}
//           {/* Парсим ссылки на файлы для скачивания */}
//           {message.content.match(/ID: ([a-f0-9-]+)/) && (
//             <div className="mt-2">
//               <button
//                 onClick={() => {
//                   const match = message.content.match(/ID: ([a-f0-9-]+)/);
//                   const filenameMatch = message.content.match(/Загружен файл: (.+?) \(/);
//                   if (match) {
//                     downloadFile(match[1], filenameMatch ? filenameMatch[1] : "file");
//                   }
//                 }}
//                 className="text-blue-400 hover:text-blue-300 text-sm flex items-center gap-1"
//               >
//                 <svg
//                   className="w-4 h-4"
//                   fill="none"
//                   stroke="currentColor"
//                   viewBox="0 0 24 24"
//                 >
//                   <path
//                     strokeLinecap="round"
//                     strokeLinejoin="round"
//                     strokeWidth={2}
//                     d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
//                   />
//                 </svg>
//                 Скачать файл
//               </button>
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }

