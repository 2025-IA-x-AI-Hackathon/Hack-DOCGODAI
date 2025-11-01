import { createFileRoute } from "@tanstack/react-router";

import ConceptPage from "@/pages/concept";

export const Route = createFileRoute("/study/$courseId/$chapterId/concept")({
  component: ConceptPage,
});
