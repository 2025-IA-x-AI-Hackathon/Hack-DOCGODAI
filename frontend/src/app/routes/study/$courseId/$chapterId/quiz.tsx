import { createFileRoute } from "@tanstack/react-router";

import QuizPage from "@/pages/quiz";

export const Route = createFileRoute("/study/$courseId/$chapterId/quiz")({
  component: QuizPage,
});

