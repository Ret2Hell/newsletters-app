"use client";

import { useState } from "react";
import { Edit, Trash2 } from "lucide-react";
import { motion } from "framer-motion";

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import AnimatedButton from "./animated-button";
import DeleteNewsletterModal from "./delete-newsletter-modal";
import EditNewsletterModal from "./edit-newsletter-modal";
import { contentVariants, modalVariants } from "@/lib/variants";

export default function ViewNewsletterModal({
  newsletter,
  open,
  onOpenChange,
}: ViewNewsletterModalProps) {
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);

  const handleEdit = () => {
    onOpenChange(false);
    setIsEditModalOpen(true);
  };

  const handleDeleteResult = (isOpen: boolean, wasDeleted: boolean) => {
    setIsDeleteModalOpen(isOpen);

    if (!isOpen && wasDeleted) {
      onOpenChange(false);
    }
  };

  return (
    <>
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
              <DialogTitle className="text-xl font-semibold mb-2">
                Newsletter Details
              </DialogTitle>
              <div className="text-sm text-muted-foreground">
                Created on{" "}
                {new Date(newsletter.created_at).toLocaleDateString()} at{" "}
                {new Date(newsletter.created_at).toLocaleTimeString()}
              </div>
              <div className="text-sm text-muted-foreground">
                Last updated on{" "}
                {new Date(newsletter.updated_at).toLocaleDateString()} at{" "}
                {new Date(newsletter.updated_at).toLocaleTimeString()}
              </div>
            </DialogHeader>

            <motion.div variants={contentVariants} className="space-y-6 py-4">
              <motion.div
                className="bg-slate-50 p-4 rounded-md border"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <h4 className="text-sm font-medium text-muted-foreground mb-2">
                  Prompt:
                </h4>
                <p className="text-sm">{newsletter.prompt}</p>
              </motion.div>

              <motion.div
                className="border rounded-lg p-6 bg-white shadow-sm"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.4 }}
              >
                <h4 className="text-sm font-medium text-muted-foreground mb-2">
                  Content:
                </h4>
                <div
                  className="prose max-w-none"
                  dangerouslySetInnerHTML={{
                    __html: newsletter.edited_content,
                  }}
                />
              </motion.div>

              <motion.div
                className="flex justify-end gap-2"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Button variant="outline" onClick={() => onOpenChange(false)}>
                    Close
                  </Button>
                </motion.div>
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <a
                    href={
                      `mailto:?subject=${encodeURIComponent(
                        newsletter.prompt
                      )}` +
                      `&body=${encodeURIComponent(newsletter.edited_content)}`
                    }
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <Button variant="outline">Open in Email</Button>
                  </a>
                </motion.div>
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <Button
                    variant="outline"
                    className="text-red-500 hover:text-red-700 hover:bg-red-50"
                    onClick={() => setIsDeleteModalOpen(true)}
                  >
                    <Trash2 className="mr-2 h-4 w-4" />
                    Delete
                  </Button>
                </motion.div>
                <motion.div
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <AnimatedButton onClick={handleEdit}>
                    <Edit className="mr-2 h-4 w-4" />
                    Edit
                  </AnimatedButton>
                </motion.div>
              </motion.div>
            </motion.div>
          </motion.div>
        </DialogContent>
      </Dialog>

      <DeleteNewsletterModal
        id={newsletter.id}
        open={isDeleteModalOpen}
        onOpenChange={(open, wasDeleted = false) =>
          handleDeleteResult(open, wasDeleted)
        }
      />

      <EditNewsletterModal
        newsletter={newsletter}
        open={isEditModalOpen}
        onOpenChange={setIsEditModalOpen}
      />
    </>
  );
}
