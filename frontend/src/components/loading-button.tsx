import { Loader2 } from "lucide-react";
import { ReactNode } from "react";
import AnimatedButton from "./animated-button";
import { ButtonProps } from "./ui/button";

interface LoadingButtonProps extends ButtonProps {
  isLoading: boolean;
  loadingText: string;
  icon?: ReactNode;
  children: ReactNode;
}

export function LoadingButton({
  isLoading,
  loadingText,
  icon,
  children,
  ...props
}: LoadingButtonProps) {
  return (
    <AnimatedButton disabled={isLoading} {...props}>
      {isLoading ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          {loadingText}
        </>
      ) : (
        <>
          {icon && <span className="mr-2">{icon}</span>}
          {children}
        </>
      )}
    </AnimatedButton>
  );
}
