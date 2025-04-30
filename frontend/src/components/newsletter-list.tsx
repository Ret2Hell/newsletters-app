"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import ViewNewsletterModal from "./view-newsletter-modal";
import NewsletterCard from "./newsletter-card";
import { Sparkles } from "lucide-react";

const containerVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.2,
    },
  },
};

function EmptyState() {
  return (
    <motion.div
      className="text-center py-16 bg-slate-50/50 dark:bg-slate-800/30 rounded-xl border border-dashed backdrop-blur-sm"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{
          type: "spring",
          stiffness: 200,
          damping: 15,
          delay: 0.5,
        }}
      >
        <Sparkles className="h-16 w-16 mx-auto text-purple-500 mb-4" />
      </motion.div>
      <h3 className="text-xl font-medium mb-2">No newsletters found</h3>
      <p className="text-muted-foreground mb-6">
        Get started by creating your first newsletter
      </p>
    </motion.div>
  );
}

export default function NewsletterList({
  newsletters = [],
}: {
  newsletters: Newsletter[];
}) {
  const [selectedNewsletter, setSelectedNewsletter] =
    useState<Newsletter | null>(null);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);

  const handleOpenNewsletter = (newsletter: Newsletter) => {
    setSelectedNewsletter(newsletter);
    setIsViewModalOpen(true);
  };

  return (
    <div className="space-y-4">
      {newsletters.length === 0 ? (
        <EmptyState />
      ) : (
        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
          initial="hidden"
          animate="visible"
          variants={containerVariants}
        >
          {newsletters.map((newsletter) => (
            <NewsletterCard
              key={newsletter.id}
              newsletter={newsletter}
              onClick={() => handleOpenNewsletter(newsletter)}
            />
          ))}
        </motion.div>
      )}

      {selectedNewsletter && (
        <ViewNewsletterModal
          newsletter={selectedNewsletter}
          open={isViewModalOpen}
          onOpenChange={setIsViewModalOpen}
        />
      )}
    </div>
  );
}
