import { toast } from "sonner";

export function validatePrompt(prompt: string): boolean {
  if (!prompt.trim()) {
    toast.error("Please enter a prompt first");
    return false;
  }
  return true;
}

export function validateContent(content: string): boolean {
  if (!content.trim()) {
    toast.error("Content is required");
    return false;
  }
  return true;
}
