"use client";

import { useState, useEffect } from "react";
import { Pencil, Sparkles } from "lucide-react";
import { motion } from "framer-motion";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import {
  useGenerateContentMutation,
  useUpdateNewsletterMutation,
} from "@/state/api";
import { modalVariants } from "@/lib/variants";
import { validateContent, validatePrompt } from "@/lib/validators";
import { LoadingButton } from "./loading-button";

export default function EditNewsletterModal({
  newsletter,
  open,
  onOpenChange,
}: EditNewsletterModalProps) {
  const [generateContent, { isLoading: isGenerating }] =
    useGenerateContentMutation();
  const [updateNewsletter, { isLoading: isUpdating }] =
    useUpdateNewsletterMutation();

  const [prompt, setPrompt] = useState("");
  const [generatedContent, setGeneratedContent] = useState("");
  const [editedContent, setEditedContent] = useState("");

  useEffect(() => {
    if (newsletter) {
      setPrompt(newsletter.prompt || "");
      setEditedContent(newsletter.edited_content || "");
    }
  }, [newsletter]);

  async function handleRegenerate() {
    if (!validatePrompt(prompt)) return;

    try {
      const result = await generateContent({ prompt }).unwrap();
      setGeneratedContent(result.generated_content);
      setEditedContent(result.generated_content);
    } catch (error) {
      console.error(error);
    }
  }

  async function handleUpdate() {
    if (!validateContent(editedContent)) return;

    try {
      await updateNewsletter({
        id: newsletter.id,
        prompt,
        generated_content: generatedContent,
        edited_content: editedContent,
      }).unwrap();

      onOpenChange(false);
    } catch (error) {
      console.error(error);
    }
  }

  const handleClose = () => {
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[800px] max-h-[90vh] overflow-y-auto p-0 gap-0">
        <motion.div
          initial="hidden"
          animate="visible"
          exit="exit"
          variants={modalVariants}
          className="p-6"
        >
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-xl">
              <motion.div
                initial={{ rotate: -10, scale: 0.8 }}
                animate={{ rotate: 0, scale: 1 }}
                transition={{
                  type: "spring",
                  stiffness: 200,
                  damping: 15,
                  delay: 0.3,
                }}
              >
                <Pencil className="h-5 w-5 text-purple-500" />
              </motion.div>
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 text-transparent bg-clip-text">
                Edit Newsletter
              </span>
            </DialogTitle>
            <DialogDescription>
              Edit your newsletter content or regenerate with AI
            </DialogDescription>
          </DialogHeader>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-6 py-4"
          >
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="prompt" className="text-sm font-medium">
                  Prompt
                </Label>
                <Textarea
                  id="prompt"
                  placeholder="Enter a prompt to generate newsletter content..."
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="min-h-[100px] resize-none transition-all duration-300 focus:ring-purple-500"
                />
              </div>

              <LoadingButton
                onClick={handleRegenerate}
                isLoading={isGenerating}
                loadingText="Regenerating..."
                disabled={!prompt}
                icon={<Sparkles className="h-4 w-4" />}
              >
                Regenerate Content
              </LoadingButton>
            </div>

            <div className="space-y-6">
              <div className="space-y-2">
                <Label htmlFor="content" className="text-sm font-medium">
                  Content
                </Label>
                <Card className="overflow-hidden border-slate-200 transition-all duration-300 hover:shadow-md">
                  <div className="p-4">
                    <Textarea
                      id="content"
                      placeholder="Newsletter content..."
                      value={editedContent}
                      onChange={(e) => setEditedContent(e.target.value)}
                      className="min-h-[300px] border-0 focus-visible:ring-0 p-0 resize-none"
                    />
                  </div>
                </Card>
              </div>

              <div className="flex justify-end gap-2">
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Button variant="outline" onClick={handleClose}>
                    Cancel
                  </Button>
                </motion.div>
                <LoadingButton
                  onClick={handleUpdate}
                  isLoading={isUpdating}
                  loadingText="Updating..."
                  disabled={!editedContent}
                >
                  Update Newsletter
                </LoadingButton>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </DialogContent>
    </Dialog>
  );
}
