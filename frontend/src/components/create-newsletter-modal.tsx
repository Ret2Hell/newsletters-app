"use client";

import { useState } from "react";
import { Sparkles } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

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
  useCreateNewsletterMutation,
  useGenerateContentMutation,
} from "@/state/api";
import { validateContent, validatePrompt } from "@/lib/validators";
import { contentVariants, modalVariants } from "@/lib/variants";
import { LoadingButton } from "./loading-button";

export default function CreateNewsletterModal({
  open,
  onOpenChange,
}: CreateNewsletterModalProps) {
  const [generateContent, { isLoading: isGenerating }] =
    useGenerateContentMutation();
  const [createNewsletter, { isLoading: isCreating }] =
    useCreateNewsletterMutation();
  const [prompt, setPrompt] = useState("");
  const [generatedContent, setGeneratedContent] = useState("");
  const [editedContent, setEditedContent] = useState("");
  const [step, setStep] = useState(1);

  const handleGenerateContent = async () => {
    if (!validatePrompt(prompt)) return;

    try {
      const result = await generateContent({ prompt }).unwrap();
      setGeneratedContent(result.generated_content);
      setEditedContent(result.generated_content);
      setStep(2);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCreateNewsletter = async () => {
    if (!validateContent(editedContent)) return;

    try {
      await createNewsletter({
        prompt,
        generated_content: generatedContent,
        edited_content: editedContent,
      }).unwrap();

      resetForm();
      onOpenChange(false);
    } catch (error) {
      console.error(error);
    }
  };

  const resetForm = () => {
    setPrompt("");
    setEditedContent("");
    setStep(1);
  };

  const handleClose = () => {
    resetForm();
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
                <Sparkles className="h-5 w-5 text-purple-500" />
              </motion.div>
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 text-transparent bg-clip-text">
                Create Newsletter
              </span>
            </DialogTitle>
            <DialogDescription>
              Enter a prompt to generate newsletter content with AI
            </DialogDescription>
          </DialogHeader>

          <div className="relative overflow-hidden">
            <AnimatePresence mode="wait">
              {step === 1 ? (
                <motion.div
                  key="step1"
                  initial="hidden"
                  animate="visible"
                  exit="exit"
                  variants={contentVariants}
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
                        className="min-h-[100px] resize-none"
                      />
                    </div>

                    <LoadingButton
                      onClick={handleGenerateContent}
                      isLoading={isGenerating}
                      loadingText="Generating..."
                      icon={<Sparkles className="h-4 w-4" />}
                    >
                      Generate Content
                    </LoadingButton>
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key="step2"
                  initial="hidden"
                  animate="visible"
                  exit="exit"
                  variants={contentVariants}
                  className="space-y-6 py-4"
                >
                  <div className="space-y-6">
                    <div className="space-y-2">
                      <Label htmlFor="content" className="text-sm font-medium">
                        Content
                      </Label>
                      <Card className="overflow-hidden border-slate-200">
                        <div className="p-4">
                          <Textarea
                            id="content"
                            placeholder="Generated content will appear here..."
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
                        <Button variant="outline" onClick={() => setStep(1)}>
                          Back
                        </Button>
                      </motion.div>
                      <motion.div
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        <Button variant="outline" onClick={handleClose}>
                          Cancel
                        </Button>
                      </motion.div>
                      <LoadingButton
                        onClick={handleCreateNewsletter}
                        isLoading={isCreating}
                        loadingText="Saving..."
                      >
                        Save Newsletter
                      </LoadingButton>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </DialogContent>
    </Dialog>
  );
}
