"use client";

import { useGetNewslettersQuery } from "@/state/api";
import { Plus } from "lucide-react";
import React, { useState } from "react";
import { motion } from "framer-motion";
import AnimatedButton from "@/components/animated-button";
import NewsletterList from "../components/newsletter-list";
import NewsletterListSkeleton from "@/components/newsletter-list-skeleton";
import CreateNewsletterModal from "@/components/create-newsletter-modal";

const Home = () => {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const titleVariants = {
    hidden: { opacity: 0, y: -20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        type: "spring",
        stiffness: 100,
        damping: 15,
        delay: 0.2,
      },
    },
  };
  const { data: newsletters, isLoading } = useGetNewslettersQuery({});

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 relative overflow-hidden">
      <div className="py-10 mx-20 relative z-10">
        <div className="relative">
          <div className="absolute inset-0 bg-gradient-to-r from-purple-500/20 to-pink-500/20 rounded-2xl blur-3xl opacity-30 -z-10" />
          <div className="relative bg-white/80  backdrop-blur-sm rounded-2xl shadow-xl border border-slate-200/50  p-8">
            <div className="space-y-6">
              <motion.div
                className="flex items-center justify-between mb-8"
                initial="hidden"
                animate="visible"
                variants={containerVariants}
              >
                <motion.div variants={titleVariants}>
                  <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-purple-600 to-pink-600 text-transparent bg-clip-text pb-1">
                    Newsletter Manager
                  </h1>
                  <p className="text-muted-foreground mt-1">
                    Create and manage your newsletters with AI
                  </p>
                </motion.div>
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <AnimatedButton onClick={() => setIsCreateModalOpen(true)}>
                    <Plus className="mr-2 h-4 w-4" />
                    Create Newsletter
                  </AnimatedButton>
                </motion.div>
              </motion.div>

              {isLoading ? (
                <NewsletterListSkeleton />
              ) : (
                <NewsletterList newsletters={newsletters} />
              )}
            </div>
          </div>
        </div>
      </div>
      <CreateNewsletterModal
        open={isCreateModalOpen}
        onOpenChange={setIsCreateModalOpen}
      />
    </div>
  );
};

export default Home;
