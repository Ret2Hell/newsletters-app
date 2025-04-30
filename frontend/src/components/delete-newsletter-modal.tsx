"use client";
import { Loader2, Trash2 } from "lucide-react";
import { motion } from "framer-motion";

import { Button } from "@/components/ui/button";
import {
  AlertDialog,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { useDeleteNewsletterMutation } from "@/state/api";
import { modalVariants } from "@/lib/variants";

export default function DeleteNewsletterModal({
  id,
  open,
  onOpenChange,
}: {
  id: string;
  open: boolean;
  onOpenChange: (open: boolean, wasDeleted?: boolean) => void;
}) {
  const [deleteNewsletter, { isLoading: isDeleting }] =
    useDeleteNewsletterMutation();

  const handleDelete = async () => {
    try {
      await deleteNewsletter(id).unwrap();
      onOpenChange(false, true);
    } catch (error) {
      console.error(error);
      onOpenChange(false, false);
    }
  };

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent className="sm:max-w-[425px] p-0 gap-0">
        <motion.div
          initial="hidden"
          animate="visible"
          exit="exit"
          variants={modalVariants}
          className="p-6"
        >
          <AlertDialogHeader>
            <AlertDialogTitle className="flex items-center gap-2">
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
                <Trash2 className="h-5 w-5 text-red-500" />
              </motion.div>
              <span className="text-red-500">Delete Newsletter</span>
            </AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure you want to delete this Newsletter? This action
              cannot be undone.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter className="mt-4">
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
            </motion.div>
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Button
                variant="destructive"
                disabled={isDeleting}
                onClick={handleDelete}
              >
                {isDeleting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Deleting...
                  </>
                ) : (
                  "Delete"
                )}
              </Button>
            </motion.div>
          </AlertDialogFooter>
        </motion.div>
      </AlertDialogContent>
    </AlertDialog>
  );
}
