import { createFileRoute } from "@tanstack/react-router";

import ChapterPage from "@/pages/chapter";

export const Route = createFileRoute("/study/$courseId/$chapterId/")({
  component: () => {
    return <ChapterPage />;
  },
});
