import React from "react";
import { motion } from "framer-motion";
import { Calendar, ChevronRight } from "lucide-react";

const cardVariants = {
  hidden: { opacity: 0, y: 5 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      type: "spring",
      stiffness: 80,
      damping: 20,
    },
  },
};

const NewsletterCard = ({
  newsletter,
  onClick,
}: {
  newsletter: Newsletter;
  onClick: () => void;
}) => {
  return (
    <motion.div
      variants={cardVariants}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden cursor-pointer transition-all hover:shadow-md"
      onClick={onClick}
    >
      <div className="p-6">
        <div
          className="text-sm text-slate-600 line-clamp-3 mb-4"
          dangerouslySetInnerHTML={{
            __html: newsletter.edited_content.substring(0, 150) + "...",
          }}
        />
        <div className="flex justify-between items-center text-xs text-muted-foreground">
          <div className="flex items-center">
            <Calendar className="h-3.5 w-3.5 mr-1" />
            {new Date(newsletter.created_at).toLocaleDateString()}
          </div>
          <ChevronRight className="h-4 w-4" />
        </div>
      </div>
    </motion.div>
  );
};

export default NewsletterCard;
