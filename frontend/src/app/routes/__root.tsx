import { HeroUIProvider } from "@heroui/react";
import { Outlet, createRootRoute } from "@tanstack/react-router";
import { ThemeProvider } from "next-themes";

import Navigation from "@/widgets/navigation";

export const Route = createRootRoute({
  component: () => (
    <HeroUIProvider className="mx-auto w-full max-w-6xl px-6 md:px-8">
      <ThemeProvider attribute="class">
        <Navigation />
        <Outlet />
      </ThemeProvider>
    </HeroUIProvider>
  ),
});
