declare global {
  interface Newsletter {
    id: string;
    prompt: string;
    generated_content: string;
    edited_content: string;
    created_at: string;
    updated_at: string;
  }

  interface CreateNewsletterModalProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
  }

  interface ViewNewsletterModalProps {
    newsletter: Newsletter;
    open: boolean;
    onOpenChange: (open: boolean) => void;
  }

  interface EditNewsletterModalProps {
    newsletter: Newsletter;
    open: boolean;
    onOpenChange: (open: boolean) => void;
  }
}

export {};
