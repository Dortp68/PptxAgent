export function getUserId(): string {
  let user_id = document.cookie
    .split("; ")
    .find(row => row.startsWith("user_id="))
    ?.split("=")[1];

  if (!user_id) {
    user_id = crypto.randomUUID();
    document.cookie = `user_id=${user_id}; path=/; max-age=31536000`;
    console.log("Created new user_id:", user_id);
  } 

  return user_id;
}

export function ensureUserId(): void {
  if (typeof window !== "undefined") {
    getUserId();
  }
}

